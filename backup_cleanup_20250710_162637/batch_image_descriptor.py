#!/usr/bin/env python3
"""
Batch image descriptor for all papers with empty image alt text
Processes papers in batches with API key rotation and rate limiting
"""
import os
import re
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Load environment variables
env_path = Path('.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"\'')

# Get API keys
API_KEYS = os.environ.get('GEMINI_API_KEYS', '').split(',')
API_KEYS = [key.strip() for key in API_KEYS if key.strip()]

class BatchImageDescriptor:
    def __init__(self):
        self.api_key_index = 0
        self.processed_count = 0
        self.checkpoint_file = Path('image_description_checkpoint.json')
        self.log_file = Path(f'image_description_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        self.checkpoint = self.load_checkpoint()
        
        # Install required packages if needed
        try:
            import google.generativeai as genai
            from PIL import Image
        except ImportError:
            print("Installing required packages...")
            os.system(f"{sys.executable} -m pip install google-generativeai pillow")
        
    def load_checkpoint(self):
        """Load checkpoint from previous run"""
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return {'processed': [], 'failed': {}}
    
    def save_checkpoint(self):
        """Save checkpoint"""
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.checkpoint, f, indent=2)
    
    def get_next_api_key(self):
        """Get next API key in rotation"""
        if not API_KEYS:
            raise ValueError("No API keys found in .env file")
        key = API_KEYS[self.api_key_index]
        self.api_key_index = (self.api_key_index + 1) % len(API_KEYS)
        return key
    
    def log(self, message):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
    
    def describe_images_in_paper(self, paper_path, paper_name):
        """Describe images in a single paper"""
        import google.generativeai as genai
        from PIL import Image
        
        # Skip if already processed
        if paper_name in self.checkpoint['processed']:
            return True, 0, "Already processed"
        
        # Check if previously failed
        if paper_name in self.checkpoint['failed']:
            retry_count = self.checkpoint['failed'][paper_name].get('retry_count', 0)
            if retry_count >= 3:
                return False, 0, "Max retries exceeded"
        
        try:
            # Configure API with current key
            api_key = self.get_next_api_key()
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Read the markdown content
            with open(paper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all images with empty alt text
            image_pattern = r'!\[\]\(([^)]+)\)'
            empty_images = re.findall(image_pattern, content)
            
            if not empty_images:
                self.checkpoint['processed'].append(paper_name)
                self.save_checkpoint()
                return True, 0, "No empty images"
            
            # Process each image
            updated_content = content
            images_described = 0
            
            for i, image_file in enumerate(empty_images):
                image_path = paper_path.parent / image_file
                if not image_path.exists():
                    continue
                
                try:
                    # Load and describe the image
                    img = Image.open(image_path)
                    
                    prompt = """Analyze this image from an academic paper and provide a concise description 
                    focusing on the technical content. Describe any diagrams, charts, graphs, equations, 
                    or technical illustrations. Be specific about what the image shows. 
                    Keep the description under 80 words."""
                    
                    response = model.generate_content([prompt, img])
                    
                    if response.text:
                        description = response.text.strip().replace('\n', ' ')
                        # Update the image reference
                        old_ref = f'![]({image_file})'
                        new_ref = f'![{description}]({image_file})'
                        updated_content = updated_content.replace(old_ref, new_ref, 1)
                        images_described += 1
                        
                        # Rate limiting
                        time.sleep(0.5)  # Half second between images
                        
                except Exception as e:
                    self.log(f"  Error processing image {image_file}: {str(e)}")
            
            # Save if any images were described
            if images_described > 0:
                # Backup original
                backup_path = paper_path.parent / f"{paper_path.stem}_backup{paper_path.suffix}"
                if not backup_path.exists():
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                
                # Write updated content
                with open(paper_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            # Mark as processed
            self.checkpoint['processed'].append(paper_name)
            self.save_checkpoint()
            
            return True, images_described, f"Described {images_described}/{len(empty_images)} images"
            
        except Exception as e:
            # Track failures
            if paper_name not in self.checkpoint['failed']:
                self.checkpoint['failed'][paper_name] = {'retry_count': 0, 'errors': []}
            self.checkpoint['failed'][paper_name]['retry_count'] += 1
            self.checkpoint['failed'][paper_name]['errors'].append(str(e))
            self.save_checkpoint()
            
            return False, 0, str(e)
    
    def process_batch(self, papers_list, batch_size=5):
        """Process papers in batches"""
        total = len(papers_list)
        
        self.log(f"Starting batch processing of {total} papers")
        self.log(f"Using {len(API_KEYS)} API keys in rotation")
        self.log(f"Batch size: {batch_size}")
        
        stats = {
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'total_images': 0
        }
        
        for i in range(0, total, batch_size):
            batch = papers_list[i:i+batch_size]
            batch_num = i // batch_size + 1
            total_batches = (total + batch_size - 1) // batch_size
            
            self.log(f"\nProcessing batch {batch_num}/{total_batches}")
            
            for paper in batch:
                paper_path = Path('markdown_papers') / paper / 'paper.md'
                if not paper_path.exists():
                    self.log(f"  {paper}: File not found")
                    stats['skipped'] += 1
                    continue
                
                self.log(f"  Processing {paper}...")
                success, images_count, message = self.describe_images_in_paper(paper_path, paper)
                
                if success:
                    stats['successful'] += 1
                    stats['total_images'] += images_count
                    self.log(f"    ✓ {message}")
                else:
                    stats['failed'] += 1
                    self.log(f"    ✗ {message}")
            
            # Batch delay to avoid rate limits
            if i + batch_size < total:
                self.log(f"  Batch complete. Waiting 5 seconds before next batch...")
                time.sleep(5)
        
        # Final summary
        self.log("\n" + "="*60)
        self.log("PROCESSING COMPLETE")
        self.log("="*60)
        self.log(f"Papers processed successfully: {stats['successful']}")
        self.log(f"Papers failed: {stats['failed']}")
        self.log(f"Papers skipped: {stats['skipped']}")
        self.log(f"Total images described: {stats['total_images']}")
        self.log(f"Log saved to: {self.log_file}")

def main():
    """Main entry point"""
    if not API_KEYS:
        print("Error: No API keys found in .env file")
        print("Please ensure GEMINI_API_KEYS is set in .env")
        return
    
    # Load list of papers needing descriptions
    papers_file = Path('papers_needing_image_descriptions.txt')
    if not papers_file.exists():
        print("Running paper scanner first...")
        os.system('python find_papers_needing_image_descriptions.py')
    
    # Read the list
    papers_to_process = []
    with open(papers_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('=') and not line.startswith('Papers'):
                papers_to_process.append(line)
    
    if not papers_to_process:
        print("No papers to process")
        return
    
    # Create descriptor and process
    descriptor = BatchImageDescriptor()
    
    # Filter out already processed papers
    remaining = [p for p in papers_to_process if p not in descriptor.checkpoint['processed']]
    
    print(f"Total papers: {len(papers_to_process)}")
    print(f"Already processed: {len(descriptor.checkpoint['processed'])}")
    print(f"Remaining to process: {len(remaining)}")
    
    if remaining:
        descriptor.process_batch(remaining, batch_size=3)  # Small batches to avoid rate limits
    else:
        print("All papers already processed!")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Image descriptor that adds descriptions as HTML comments below images
Format: 
![](_page_X_Figure_Y.jpeg)
<!-- Image Description: [description] -->
"""
import os
import re
import time
import json
from pathlib import Path
from datetime import datetime

# Import required packages
try:
    import google.generativeai as genai
    from PIL import Image
except ImportError:
    print("Error: Required packages not installed")
    print("Please run: pip install google-generativeai pillow")
    exit(1)

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

if not API_KEYS:
    print("Error: No API keys found in .env file")
    exit(1)

def has_image_description(content, image_file):
    """Check if an image already has a description comment"""
    # Pattern to find image followed by description comment
    pattern = rf'!\[\]\({re.escape(image_file)}\)\s*\n\s*<!-- Image Description:.*?-->'
    return bool(re.search(pattern, content, re.DOTALL))

def describe_images_in_paper(paper_path, api_key):
    """Describe images in a single paper using HTML comments"""
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Read the markdown content
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all images with empty alt text
        image_pattern = r'!\[\]\(([^)]+)\)'
        empty_images = re.findall(image_pattern, content)
        
        if not empty_images:
            return 0, "No images with empty alt text found"
        
        # Filter out images that already have descriptions
        images_to_process = []
        for image_file in empty_images:
            if not has_image_description(content, image_file):
                images_to_process.append(image_file)
        
        if not images_to_process:
            return 0, "All images already have descriptions"
        
        # Process each image
        updated_content = content
        images_described = 0
        
        for image_file in images_to_process:
            image_path = paper_path.parent / image_file
            if not image_path.exists():
                continue
            
            try:
                # Load and describe the image
                img = Image.open(image_path)
                
                prompt = """Analyze this image from an academic paper and provide a concise description 
                focusing on the technical content. Describe any diagrams, charts, graphs, equations, 
                or technical illustrations. Be specific about what the image shows and its purpose 
                in the context of the paper. Keep the description under 100 words."""
                
                response = model.generate_content([prompt, img])
                
                if response.text:
                    description = response.text.strip().replace('\n', ' ')
                    
                    # Find the image reference and add description comment after it
                    old_pattern = rf'(!\[\]\({re.escape(image_file)}\))'
                    new_text = f'![]({image_file})\n<!-- Image Description: {description} -->'
                    
                    # Replace only if not already has description
                    if not has_image_description(updated_content, image_file):
                        updated_content = re.sub(old_pattern, new_text, updated_content, count=1)
                        images_described += 1
                    
                    # Rate limiting
                    time.sleep(1)  # 1 second between images
                    
            except Exception as e:
                print(f"    Error with image {image_file}: {str(e)}")
        
        # Save if any images were described
        if images_described > 0:
            # Backup original if not already exists
            backup_path = paper_path.parent / f"{paper_path.stem}_backup{paper_path.suffix}"
            if not backup_path.exists():
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Write updated content
            with open(paper_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
        
        return images_described, f"Described {images_described}/{len(images_to_process)} images"
        
    except Exception as e:
        return 0, f"Error: {str(e)}"

def main():
    """Main function"""
    # Get list of papers to process
    papers_to_process = []
    
    # Check if we have specific papers or all papers
    import sys
    if len(sys.argv) > 1:
        # Specific papers provided
        papers_to_process = sys.argv[1:]
    else:
        # Get all papers needing descriptions
        papers_file = Path('papers_needing_image_descriptions.txt')
        if papers_file.exists():
            with open(papers_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('=') and not line.startswith('Papers'):
                        papers_to_process.append(line)
        
        # Exclude already processed papers
        processed = ['li_2022', 'xie_2024a']  # Already done
        papers_to_process = [p for p in papers_to_process if p not in processed]
    
    if not papers_to_process:
        print("No papers to process")
        print("Usage: python image_descriptor_with_comments.py [paper_folder1] [paper_folder2] ...")
        return
    
    print(f"Processing {len(papers_to_process)} papers...")
    print("Using format: ![](image.jpeg)")
    print("             <!-- Image Description: ... -->")
    print("=" * 60)
    
    # Track progress
    api_key_index = 0
    total_images = 0
    processed_papers = 0
    start_time = time.time()
    
    # Process each paper
    for i, paper in enumerate(papers_to_process):
        paper_path = Path('markdown_papers') / paper / 'paper.md'
        
        if not paper_path.exists():
            print(f"{i+1}/{len(papers_to_process)}: {paper} - File not found")
            continue
        
        # Use API key in rotation
        api_key = API_KEYS[api_key_index % len(API_KEYS)]
        api_key_index += 1
        
        # Estimate time remaining
        if i > 0:
            elapsed = time.time() - start_time
            avg_time_per_paper = elapsed / i
            remaining_papers = len(papers_to_process) - i
            eta_seconds = avg_time_per_paper * remaining_papers
            eta_str = f" (ETA: {int(eta_seconds//60)}m {int(eta_seconds%60)}s)"
        else:
            eta_str = ""
        
        print(f"{i+1}/{len(papers_to_process)}: Processing {paper}{eta_str}...")
        
        images_count, message = describe_images_in_paper(paper_path, api_key)
        
        print(f"  {message}")
        
        total_images += images_count
        if images_count > 0:
            processed_papers += 1
        
        # Rate limiting between papers
        if i < len(papers_to_process) - 1:
            time.sleep(2)
    
    # Summary
    elapsed_total = time.time() - start_time
    print("=" * 60)
    print(f"Complete! Processed {processed_papers} papers in {int(elapsed_total//60)}m {int(elapsed_total%60)}s")
    print(f"Total images described: {total_images}")
    
    # Save progress report
    report_file = Path(f'image_description_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
    with open(report_file, 'w') as f:
        f.write(f"Image Description Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"="*60 + "\n")
        f.write(f"Total papers processed: {processed_papers}\n")
        f.write(f"Total images described: {total_images}\n")
        f.write(f"Total time: {int(elapsed_total//60)}m {int(elapsed_total%60)}s\n")
    
    print(f"\nReport saved to: {report_file}")

if __name__ == '__main__':
    main()
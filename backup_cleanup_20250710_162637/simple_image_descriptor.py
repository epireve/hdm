#!/usr/bin/env python3
"""
Simple image descriptor for papers - processes papers one by one
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

def describe_images_in_paper(paper_path, api_key):
    """Describe images in a single paper"""
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
            return 0, "No images need descriptions"
        
        # Process each image
        updated_content = content
        images_described = 0
        
        for image_file in empty_images:
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
                    time.sleep(1)  # 1 second between images
                    
            except Exception as e:
                print(f"    Error with image {image_file}: {str(e)}")
        
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
        
        return images_described, f"Described {images_described}/{len(empty_images)} images"
        
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
    
    if not papers_to_process:
        print("No papers to process")
        print("Usage: python simple_image_descriptor.py [paper_folder1] [paper_folder2] ...")
        return
    
    print(f"Processing {len(papers_to_process)} papers...")
    print("=" * 60)
    
    # Track progress
    api_key_index = 0
    total_images = 0
    processed_papers = 0
    
    # Process each paper
    for i, paper in enumerate(papers_to_process):
        paper_path = Path('markdown_papers') / paper / 'paper.md'
        
        if not paper_path.exists():
            print(f"{i+1}/{len(papers_to_process)}: {paper} - File not found")
            continue
        
        # Use API key in rotation
        api_key = API_KEYS[api_key_index % len(API_KEYS)]
        api_key_index += 1
        
        print(f"{i+1}/{len(papers_to_process)}: Processing {paper}...")
        
        images_count, message = describe_images_in_paper(paper_path, api_key)
        
        print(f"  {message}")
        
        total_images += images_count
        if images_count > 0:
            processed_papers += 1
        
        # Rate limiting between papers
        if i < len(papers_to_process) - 1:
            time.sleep(2)
    
    # Summary
    print("=" * 60)
    print(f"Complete! Processed {processed_papers} papers")
    print(f"Total images described: {total_images}")

if __name__ == '__main__':
    main()
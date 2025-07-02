#!/usr/bin/env python3
"""
Describe images for the newly renamed folders: li_2022 and xie_2024a
"""
import os
import re
import sys
from pathlib import Path

# Load environment variables
env_path = Path('.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"\'')

def describe_images_in_paper(paper_path):
    """Describe images in a single paper using Gemini API"""
    
    # Get API key
    api_keys = os.environ.get('GEMINI_API_KEYS', '')
    if not api_keys:
        print("Error: GEMINI_API_KEYS not found in .env")
        return False
    
    api_key = api_keys.split(',')[0].strip()
    
    try:
        import google.generativeai as genai
        from PIL import Image
    except ImportError:
        print("Installing required packages...")
        os.system(f"{sys.executable} -m pip install google-generativeai pillow")
        import google.generativeai as genai
        from PIL import Image
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Read the markdown content
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all images
    image_pattern = r'!\[(.*?)\]\(([^)]+)\)'
    images = re.findall(image_pattern, content)
    
    if not images:
        print(f"No images found in {paper_path}")
        return True
    
    print(f"Found {len(images)} images in {paper_path.parent.name}")
    
    # Process each image
    updated_content = content
    images_described = 0
    
    for i, (alt_text, image_file) in enumerate(images):
        # Skip if already has description
        if alt_text and alt_text.strip():
            print(f"  Image {i+1}/{len(images)}: Already has description, skipping")
            continue
        
        image_path = paper_path.parent / image_file
        if not image_path.exists():
            print(f"  Image {i+1}/{len(images)}: File not found: {image_file}")
            continue
        
        try:
            # Load and describe the image
            img = Image.open(image_path)
            
            prompt = """Analyze this image from an academic paper and provide a concise description 
            focusing on the technical content. Describe any diagrams, charts, graphs, equations, 
            or technical illustrations. Be specific about what the image shows and its purpose. 
            Keep the description under 80 words."""
            
            response = model.generate_content([prompt, img])
            
            if response.text:
                description = response.text.strip().replace('\n', ' ')
                # Update the image reference with description
                old_ref = f'![]({image_file})'
                new_ref = f'![{description}]({image_file})'
                updated_content = updated_content.replace(old_ref, new_ref)
                images_described += 1
                print(f"  Image {i+1}/{len(images)}: Described successfully")
            else:
                print(f"  Image {i+1}/{len(images)}: No description generated")
                
        except Exception as e:
            print(f"  Image {i+1}/{len(images)}: Error - {str(e)}")
    
    # Save the updated content
    if images_described > 0:
        # Backup original
        backup_path = paper_path.parent / f"{paper_path.stem}_backup{paper_path.suffix}"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write updated content
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✓ Updated {images_described} image descriptions in {paper_path.parent.name}")
        print(f"  Backup saved to {backup_path.name}")
    else:
        print(f"No images needed description in {paper_path.parent.name}")
    
    return True

def main():
    """Process the two newly renamed folders"""
    folders = ['li_2022', 'xie_2024a']
    
    print("Image Description for Renamed Folders")
    print("=" * 40)
    
    for folder in folders:
        paper_path = Path('markdown_papers') / folder / 'paper.md'
        if paper_path.exists():
            print(f"\nProcessing {folder}...")
            describe_images_in_paper(paper_path)
        else:
            print(f"\nWarning: {paper_path} not found")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Basic image descriptor using simple descriptions
Works without special dependencies
"""
import re
from pathlib import Path
from datetime import datetime

def has_image_description(content, image_file):
    """Check if an image already has a description comment"""
    pattern = rf'!\[\]\({re.escape(image_file)}\)\s*\n\s*<!-- Image Description:.*?-->'
    return bool(re.search(pattern, content, re.DOTALL))

def get_basic_description(image_file, paper_name):
    """Generate a basic description based on image filename"""
    # Extract page and figure number if available
    page_match = re.search(r'_page_(\d+)', image_file)
    figure_match = re.search(r'Figure_(\d+)', image_file)
    
    if page_match and figure_match:
        return f"Figure {figure_match.group(1)} from page {page_match.group(1)} of the paper, showing content related to the research topic."
    elif figure_match:
        return f"Figure {figure_match.group(1)} illustrating concepts discussed in the paper."
    elif 'table' in image_file.lower():
        return "A table presenting data or comparisons relevant to the research."
    elif 'graph' in image_file.lower():
        return "A graph showing relationships or trends discussed in the research."
    elif 'diagram' in image_file.lower():
        return "A diagram illustrating the conceptual framework or system architecture."
    else:
        return "An illustration supporting the research content presented in this paper."

def process_paper(paper_path):
    """Process a single paper and add image descriptions"""
    paper_name = paper_path.parent.name
    print(f"\nProcessing: {paper_name}")
    
    try:
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all images with empty alt text
        image_pattern = r'!\[\]\(([^)]+)\)'
        empty_images = re.findall(image_pattern, content)
        
        if not empty_images:
            print("  No images found")
            return 0
        
        # Filter out images that already have descriptions
        images_to_process = []
        for image_file in empty_images:
            if not has_image_description(content, image_file):
                images_to_process.append(image_file)
        
        if not images_to_process:
            print("  All images already have descriptions")
            return 0
        
        print(f"  Found {len(images_to_process)} images to describe")
        
        # Process each image
        updated_content = content
        images_described = 0
        
        for image_file in images_to_process:
            description = get_basic_description(image_file, paper_name)
            
            # Find the image reference and add description comment after it
            old_pattern = rf'(!\[\]\({re.escape(image_file)}\))'
            new_text = f'![]({image_file})\n<!-- Image Description: {description} -->'
            
            # Replace only if not already has description
            if not has_image_description(updated_content, image_file):
                updated_content = re.sub(old_pattern, new_text, updated_content, count=1)
                images_described += 1
                print(f"    - Described: {image_file}")
        
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
            
            print(f"  ✓ Updated {images_described} images")
        
        return images_described
        
    except Exception as e:
        print(f"  Error: {str(e)}")
        return 0

def main():
    """Main function"""
    print("Basic Image Descriptor")
    print("=" * 60)
    
    # Papers that need descriptions
    papers_to_process = ['xu_2023a', 'liu_2024b', 'vassiliou_2023', 'xu_2023b']
    
    print(f"Papers to process: {len(papers_to_process)}")
    print("Using basic descriptions based on filenames")
    print("=" * 60)
    
    total_images = 0
    processed_papers = 0
    
    for paper_name in papers_to_process:
        paper_path = Path('markdown_papers') / paper_name / 'paper.md'
        
        if not paper_path.exists():
            print(f"\n{paper_name}: File not found")
            continue
        
        images_count = process_paper(paper_path)
        if images_count > 0:
            processed_papers += 1
            total_images += images_count
    
    # Final summary
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Papers processed: {processed_papers}")
    print(f"Total images described: {total_images}")

if __name__ == '__main__':
    main()
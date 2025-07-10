#!/usr/bin/env python3
"""
Update the list of papers needing image descriptions
Checks actual folders and excludes non-existent ones
"""
import re
from pathlib import Path
from datetime import datetime

def has_image_description(content, image_file):
    """Check if an image already has a description comment"""
    pattern = rf'!\[\]\({re.escape(image_file)}\)\s*\n\s*<!-- Image Description:.*?-->'
    return bool(re.search(pattern, content, re.DOTALL))

def check_paper_needs_descriptions(paper_path):
    """Check if a paper needs image descriptions"""
    try:
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all images with empty alt text
        image_pattern = r'!\[\]\(([^)]+)\)'
        empty_images = re.findall(image_pattern, content)
        
        if not empty_images:
            return False, 0
        
        # Check which images need descriptions
        images_needing_descriptions = 0
        for image_file in empty_images:
            if not has_image_description(content, image_file):
                images_needing_descriptions += 1
        
        return images_needing_descriptions > 0, images_needing_descriptions
        
    except Exception as e:
        print(f"Error checking {paper_path}: {e}")
        return False, 0

def main():
    """Main function"""
    markdown_papers = Path('markdown_papers')
    papers_needing_descriptions = []
    total_images_to_describe = 0
    
    print("Checking papers for image descriptions...")
    print("=" * 60)
    
    # Check all papers
    for folder in sorted(markdown_papers.iterdir()):
        if folder.is_dir():
            paper_path = folder / 'paper.md'
            if paper_path.exists():
                needs_descriptions, image_count = check_paper_needs_descriptions(paper_path)
                if needs_descriptions:
                    papers_needing_descriptions.append((folder.name, image_count))
                    total_images_to_describe += image_count
    
    # Write to file
    output_file = Path('papers_needing_image_descriptions_updated.txt')
    with open(output_file, 'w') as f:
        f.write("Papers needing image descriptions\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 60 + "\n")
        f.write(f"Total papers: {len(papers_needing_descriptions)}\n")
        f.write(f"Total images to describe: {total_images_to_describe}\n")
        f.write("=" * 60 + "\n\n")
        
        for paper_name, image_count in papers_needing_descriptions:
            f.write(f"{paper_name} ({image_count} images)\n")
    
    print(f"Found {len(papers_needing_descriptions)} papers needing descriptions")
    print(f"Total images to describe: {total_images_to_describe}")
    print(f"\nList saved to: {output_file}")
    
    # Also create a simple list for the concurrent processor
    simple_list_file = Path('papers_for_concurrent_processing.txt')
    with open(simple_list_file, 'w') as f:
        for paper_name, _ in papers_needing_descriptions:
            f.write(f"{paper_name}\n")
    
    print(f"Simple list saved to: {simple_list_file}")

if __name__ == '__main__':
    main()
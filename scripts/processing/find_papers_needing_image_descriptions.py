#!/usr/bin/env python3
"""
Find all papers that have images with empty alt text and need descriptions
"""
import re
from pathlib import Path

def check_paper_for_empty_alt_text(paper_path):
    """Check if a paper has images with empty alt text"""
    try:
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find images with empty alt text
        empty_alt_pattern = r'!\[\]\([^)]+\)'
        empty_alt_images = re.findall(empty_alt_pattern, content)
        
        # Find all images
        all_images_pattern = r'!\[.*?\]\([^)]+\)'
        all_images = re.findall(all_images_pattern, content)
        
        return len(empty_alt_images), len(all_images)
    except Exception as e:
        return 0, 0

def main():
    """Find all papers needing image descriptions"""
    markdown_papers = Path('markdown_papers')
    papers_needing_descriptions = []
    
    print("Scanning for papers with images needing descriptions...")
    print("=" * 60)
    
    # Scan all paper folders
    for folder in sorted(markdown_papers.iterdir()):
        if folder.is_dir():
            paper_path = folder / 'paper.md'
            if paper_path.exists():
                empty_count, total_count = check_paper_for_empty_alt_text(paper_path)
                if empty_count > 0:
                    papers_needing_descriptions.append({
                        'folder': folder.name,
                        'path': paper_path,
                        'empty_alt': empty_count,
                        'total_images': total_count
                    })
    
    # Display results
    print(f"\nFound {len(papers_needing_descriptions)} papers with images needing descriptions:")
    print("-" * 60)
    
    for paper in papers_needing_descriptions:
        print(f"{paper['folder']:50} | {paper['empty_alt']:3}/{paper['total_images']:3} images need descriptions")
    
    print("-" * 60)
    print(f"Total papers: {len(papers_needing_descriptions)}")
    
    # Save list to file
    output_file = Path('papers_needing_image_descriptions.txt')
    with open(output_file, 'w') as f:
        f.write("Papers needing image descriptions\n")
        f.write("=" * 60 + "\n\n")
        for paper in papers_needing_descriptions:
            f.write(f"{paper['folder']}\n")
    
    print(f"\nList saved to: {output_file}")
    
    # Calculate total images to process
    total_images = sum(p['empty_alt'] for p in papers_needing_descriptions)
    print(f"\nTotal images to describe: {total_images}")
    
    return papers_needing_descriptions

if __name__ == '__main__':
    papers = main()
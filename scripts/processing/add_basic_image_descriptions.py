#!/usr/bin/env python3
"""
Add basic image descriptions based on filenames for papers without image descriptions
"""

import re
from pathlib import Path

def add_basic_descriptions(markdown_file):
    """Add basic alt text to images based on their filenames"""
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all image references with empty alt text
    pattern = r'!\[\]\(([^)]+)\)'
    
    def replace_image(match):
        filename = match.group(1)
        # Extract meaningful parts from filename
        # Example: _page_0_Picture_1.jpeg -> "Picture 1 from page 0"
        # Example: _page_3_Figure_2.jpeg -> "Figure 2 from page 3"
        
        parts = filename.replace('_', ' ').replace('.jpeg', '').replace('.png', '').strip()
        
        # Clean up the description
        if 'Figure' in parts:
            desc = re.sub(r'page (\d+) Figure (\d+)', r'Figure \2 from page \1', parts)
        elif 'Picture' in parts:
            desc = re.sub(r'page (\d+) Picture (\d+)', r'Picture \2 from page \1', parts)
        elif 'Table' in parts:
            desc = re.sub(r'page (\d+) Table (\d+)', r'Table \2 from page \1', parts)
        else:
            desc = parts.strip()
        
        return f'![{desc}]({filename})'
    
    # Replace all empty alt texts
    updated_content = re.sub(pattern, replace_image, content)
    
    # Count changes
    original_count = len(re.findall(pattern, content))
    
    if original_count > 0:
        # Backup original file
        backup_path = markdown_file.parent / f"{markdown_file.stem}_backup{markdown_file.suffix}"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write updated content
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Updated {original_count} image descriptions in {markdown_file}")
        print(f"Backup saved to {backup_path}")
        return True
    else:
        print(f"No empty image descriptions found in {markdown_file}")
        return False

def main():
    # Process the two newly renamed folders
    folders = ['li_2022', 'xie_2024a']
    
    for folder in folders:
        paper_path = Path('markdown_papers') / folder / 'paper.md'
        if paper_path.exists():
            print(f"\nProcessing {folder}...")
            add_basic_descriptions(paper_path)
        else:
            print(f"\nWarning: {paper_path} not found")

if __name__ == '__main__':
    main()
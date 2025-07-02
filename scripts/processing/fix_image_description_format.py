#!/usr/bin/env python3
"""
Fix image description format to use HTML comments instead of alt text
"""
import re
from pathlib import Path

def fix_format_in_paper(paper_path):
    """Convert from ![description](image) to ![](image)<!-- Image Description: description -->"""
    
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find images with descriptions in alt text
    pattern = r'!\[([^]]+)\]\(([^)]+)\)'
    
    def replace_format(match):
        description = match.group(1).strip()
        image_file = match.group(2)
        
        # Skip if it's already empty alt text
        if not description:
            return match.group(0)
        
        # Convert to new format
        return f'![]({image_file})\n<!-- Image Description: {description} -->'
    
    # Replace all occurrences
    updated_content = re.sub(pattern, replace_format, content)
    
    if updated_content != content:
        # Write updated content
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        return True
    return False

def main():
    """Fix format in the two recently processed folders"""
    folders = ['li_2022', 'xie_2024a']
    
    print("Fixing image description format...")
    print("=" * 40)
    
    for folder in folders:
        paper_path = Path('markdown_papers') / folder / 'paper.md'
        if paper_path.exists():
            print(f"Processing {folder}...")
            if fix_format_in_paper(paper_path):
                print(f"  ✓ Fixed format in {folder}")
            else:
                print(f"  - No changes needed in {folder}")
        else:
            print(f"  ✗ {paper_path} not found")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
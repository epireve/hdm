#!/usr/bin/env python3
"""
Fix title and authors formatting in all markdown files:
- Remove quotes and brackets from title and authors
- Ensure they are on single lines (no line breaks)
"""

import os
import re

def fix_title_authors(content):
    """Fix title and authors formatting"""
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('title:'):
            # Handle title - collect all continuation lines
            title_parts = [line[6:].strip()]
            j = i + 1
            
            # Look for continuation lines (indented or empty lines followed by content)
            while j < len(lines):
                next_line = lines[j]
                if next_line.strip() == '':
                    j += 1
                    continue
                elif next_line.startswith('  ') and not next_line.startswith('  -'):
                    # This is a continuation of the title
                    title_parts.append(next_line.strip())
                    j += 1
                else:
                    # This is a new field
                    break
            
            # Join all title parts and clean
            full_title = ' '.join(title_parts).strip()
            
            # Remove various quote patterns
            full_title = re.sub(r'^["\'\[\(]+|["\'\]\)]+$', '', full_title)
            full_title = full_title.replace('""', '"').replace("''", "'")
            full_title = full_title.strip()
            
            fixed_lines.append(f'title: {full_title}')
            i = j - 1
            
        elif line.startswith('authors:'):
            # Handle authors - collect all continuation lines
            authors_parts = [line[8:].strip()]
            j = i + 1
            
            # Look for continuation lines
            while j < len(lines):
                next_line = lines[j]
                if next_line.strip() == '':
                    j += 1
                    continue
                elif next_line.startswith('  ') and not next_line.startswith('  -'):
                    # This is a continuation of the authors
                    authors_parts.append(next_line.strip())
                    j += 1
                else:
                    # This is a new field
                    break
            
            # Join all authors parts and clean
            full_authors = ' '.join(authors_parts).strip()
            
            # Remove various quote patterns
            full_authors = re.sub(r'^["\'\[\(]+|["\'\]\)]+$', '', full_authors)
            full_authors = full_authors.replace('""', '"').replace("''", "'")
            full_authors = full_authors.strip()
            
            fixed_lines.append(f'authors: {full_authors}')
            i = j - 1
            
        else:
            fixed_lines.append(line)
        
        i += 1
    
    return '\n'.join(fixed_lines)

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_title_authors(content)
        
        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all markdown files"""
    base_dir = "/Users/invoture/dev.local/hdm/markdown_papers"
    
    if not os.path.exists(base_dir):
        print(f"Directory not found: {base_dir}")
        return
    
    print("=== TITLE AND AUTHORS FORMAT FIX ===")
    print("Removing quotes/brackets and ensuring single lines...")
    print()
    
    files_processed = 0
    files_updated = 0
    
    # Find all markdown files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                files_processed += 1
                
                if process_file(file_path):
                    files_updated += 1
                    print(f"✓ Updated: {os.path.basename(file_path)}")
                
                if files_processed % 50 == 0:
                    print(f"Processed {files_processed} files...")
    
    print(f"\n=== SUMMARY ===")
    print(f"Total files processed: {files_processed}")
    print(f"Files updated: {files_updated}")
    print(f"Files unchanged: {files_processed - files_updated}")

if __name__ == "__main__":
    main()
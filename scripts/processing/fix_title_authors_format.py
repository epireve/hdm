#!/usr/bin/env python3
"""
Fix title and authors formatting in all markdown files:
- Remove quotes and brackets from title and authors
- Ensure they are on single lines (no line breaks)
"""

import os
import re
import yaml
from pathlib import Path

def fix_yaml_frontmatter(content):
    """Fix YAML frontmatter to remove quotes from title and authors and ensure single lines"""
    
    # Split content into frontmatter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Parse and fix YAML
    try:
        # Manual parsing to preserve structure and handle line breaks
        lines = frontmatter.strip().split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('title:'):
                # Extract title value, handling multi-line and quotes
                title_value = line[6:].strip()
                
                # Remove quotes and brackets
                title_value = re.sub(r'^["\'\[\(]|["\'\]\)]$', '', title_value).strip()
                
                # Check for continuation lines
                j = i + 1
                while j < len(lines) and (lines[j].startswith('  ') or not lines[j].strip()):
                    if lines[j].strip():
                        # Add continuation to title
                        continuation = lines[j].strip()
                        continuation = re.sub(r'^["\'\[\(]|["\'\]\)]$', '', continuation).strip()
                        if continuation:
                            title_value += ' ' + continuation
                    j += 1
                
                # Clean up any remaining quotes
                title_value = re.sub(r'^["\'\[\(]+|["\'\]\)]+$', '', title_value).strip()
                title_value = title_value.replace('""', '"').replace("''", "'")
                
                fixed_lines.append(f'title: {title_value}')
                i = j - 1
                
            elif line.startswith('authors:'):
                # Extract authors value, handling multi-line and quotes
                authors_value = line[8:].strip()
                
                # Remove quotes and brackets
                authors_value = re.sub(r'^["\'\[\(]|["\'\]\)]$', '', authors_value).strip()
                
                # Check for continuation lines
                j = i + 1
                while j < len(lines) and (lines[j].startswith('  ') or not lines[j].strip()):
                    if lines[j].strip():
                        # Add continuation to authors
                        continuation = lines[j].strip()
                        continuation = re.sub(r'^["\'\[\(]|["\'\]\)]$', '', continuation).strip()
                        if continuation:
                            authors_value += ' ' + continuation
                    j += 1
                
                # Clean up any remaining quotes
                authors_value = re.sub(r'^["\'\[\(]+|["\'\]\)]+$', '', authors_value).strip()
                authors_value = authors_value.replace('""', '"').replace("''", "'")
                
                fixed_lines.append(f'authors: {authors_value}')
                i = j - 1
                
            else:
                fixed_lines.append(line)
            
            i += 1
        
        # Reconstruct content
        fixed_frontmatter = '\n'.join(fixed_lines)
        return f'---\n{fixed_frontmatter}\n---{body}'
        
    except Exception as e:
        print(f"Error processing YAML: {e}")
        return content

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_yaml_frontmatter(content)
        
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
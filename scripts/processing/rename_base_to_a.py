#!/usr/bin/env python3
"""
Rename base folders to have 'a' suffix when there's also a 'b' version
"""
import os
from pathlib import Path

def update_metadata_in_file(file_path, old_cite_key, new_cite_key):
    """Update cite_key in markdown file metadata"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('---\n'):
            end_idx = content.find('\n---\n', 4)
            if end_idx != -1:
                yaml_content = content[4:end_idx]
                rest_content = content[end_idx:]
                
                lines = yaml_content.split('\n')
                new_lines = []
                for line in lines:
                    if line.startswith('cite_key:'):
                        new_lines.append(f'cite_key: {new_cite_key}')
                    else:
                        new_lines.append(line)
                
                new_content = '---\n' + '\n'.join(new_lines) + rest_content
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True
    except Exception as e:
        print(f"Error updating metadata in {file_path}: {e}")
    return False

def rename_base_folders():
    """Rename base folders to 'a' when 'b' exists"""
    markdown_papers_dir = Path('markdown_papers')
    
    base_folders = [
        'schmitt_2020', 'zhang_2021', 'lin_2024', 'xie_2024',
        'ghani_2020', 'wang_2022', 'ilkou_2022', 'li_2022',
        'li_2023', 'xie_2022', 'wang_2024', 'chen_2023',
        'chen_2024', 'yang_2024'
    ]
    
    renamed_count = 0
    failed_count = 0
    
    print("Renaming base folders to 'a' suffix...\n")
    
    for base_folder in base_folders:
        old_path = markdown_papers_dir / base_folder
        new_name = f"{base_folder}a"
        new_path = markdown_papers_dir / new_name
        
        if not old_path.exists():
            print(f"✗ Not found: {base_folder}")
            failed_count += 1
            continue
            
        if new_path.exists():
            print(f"✗ Target exists: {new_name}")
            failed_count += 1
            continue
        
        try:
            # Update metadata
            md_files = list(old_path.glob('*.md'))
            for md_file in md_files:
                update_metadata_in_file(md_file, base_folder, new_name)
            
            # Rename folder
            old_path.rename(new_path)
            print(f"✓ Renamed: {base_folder} → {new_name}")
            renamed_count += 1
            
        except Exception as e:
            print(f"✗ Error renaming {base_folder}: {e}")
            failed_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Successfully renamed: {renamed_count}")
    print(f"Failed: {failed_count}")

if __name__ == "__main__":
    rename_base_folders()
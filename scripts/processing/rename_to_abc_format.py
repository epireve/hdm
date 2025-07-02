#!/usr/bin/env python3
"""
Rename folders from _2, _arxiv format to a, b, c format
"""
import os
import json
from pathlib import Path
from collections import defaultdict

def extract_metadata_from_markdown(md_file):
    """Extract metadata from markdown file"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if content.startswith('---\n'):
            end_idx = content.find('\n---\n', 4)
            if end_idx != -1:
                yaml_content = content[4:end_idx]
                metadata = {}
                
                for line in yaml_content.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if ':' in line and not line.startswith('- '):
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        elif value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        
                        if value:
                            metadata[key] = value
                            
                return metadata
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
    return None

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

def rename_to_abc_format():
    """Rename folders to use a, b, c suffixes"""
    markdown_papers_dir = Path('markdown_papers')
    
    # Folders to rename based on previous renaming
    folders_to_rename = {
        'schmitt_2020_2': 'schmitt_2020b',
        'zhang_2021_2': 'zhang_2021b', 
        'lin_2024_2': 'lin_2024b',
        'xie_2024_2': 'xie_2024b',
        'ghani_2020_arxiv2004': 'ghani_2020b',
        'wang_2022_arxiv2022': 'wang_2022b',
        'ilkou_2022_arxiv2203': 'ilkou_2022b',
        'li_2022_arxiv2203': 'li_2022b',
        'li_2023_arxiv2304': 'li_2023b',
        'xie_2022_arxiv2412': 'xie_2022b',
        'wang_2024_arxiv2409': 'wang_2024b',
        'chen_2023_2': 'chen_2023b',
        'chen_2024_2': 'chen_2024b',
        'yang_2024_2': 'yang_2024b'
    }
    
    # Check which base folders need to be renamed to 'a'
    base_folders_to_check = set()
    for old_name in folders_to_rename:
        if '_2' in old_name:
            base_key = old_name.replace('_2', '')
        elif '_arxiv' in old_name:
            base_key = old_name.split('_arxiv')[0]
        else:
            continue
        base_folders_to_check.add(base_key)
    
    # First pass: rename base folders to 'a' if they exist
    for base_key in base_folders_to_check:
        base_path = markdown_papers_dir / base_key
        if base_path.exists():
            new_name = f"{base_key}a"
            new_path = markdown_papers_dir / new_name
            
            if not new_path.exists():
                # Update metadata
                md_files = list(base_path.glob('*.md'))
                for md_file in md_files:
                    update_metadata_in_file(md_file, base_key, new_name)
                
                # Rename folder
                base_path.rename(new_path)
                print(f"✓ Renamed: {base_key} → {new_name}")
                folders_to_rename[base_key] = new_name  # Track this rename
    
    # Second pass: rename the conflicting folders
    rename_plan = []
    for old_name, new_name in folders_to_rename.items():
        if old_name in ['schmitt_2020_2', 'zhang_2021_2', 'lin_2024_2', 'xie_2024_2', 
                       'ghani_2020_arxiv2004', 'wang_2022_arxiv2022', 'ilkou_2022_arxiv2203',
                       'li_2022_arxiv2203', 'li_2023_arxiv2304', 'xie_2022_arxiv2412',
                       'wang_2024_arxiv2409', 'chen_2023_2', 'chen_2024_2', 'yang_2024_2']:
            rename_plan.append({
                'old': old_name,
                'new': new_name
            })
    
    # Execute renaming
    results = {
        'renamed': [],
        'failed': []
    }
    
    print(f"Renaming {len(rename_plan)} folders to a/b/c format...\n")
    
    for plan in rename_plan:
        old_path = markdown_papers_dir / plan['old']
        new_path = markdown_papers_dir / plan['new']
        
        if not old_path.exists():
            print(f"✗ Not found: {plan['old']}")
            results['failed'].append({
                'old': plan['old'],
                'reason': 'Not found'
            })
            continue
            
        if new_path.exists() and old_path != new_path:
            print(f"✗ Target exists: {plan['new']}")
            results['failed'].append({
                'old': plan['old'],
                'reason': f"Target {plan['new']} already exists"
            })
            continue
        
        try:
            # Update metadata first
            md_files = list(old_path.glob('*.md'))
            for md_file in md_files:
                update_metadata_in_file(md_file, plan['old'], plan['new'])
            
            # Rename folder
            if old_path != new_path:
                old_path.rename(new_path)
                print(f"✓ Renamed: {plan['old']} → {plan['new']}")
                results['renamed'].append({
                    'old': plan['old'],
                    'new': plan['new']
                })
            
        except Exception as e:
            print(f"✗ Error: {e}")
            results['failed'].append({
                'old': plan['old'],
                'reason': str(e)
            })
    
    # Save results
    with open('abc_format_rename_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Summary ===")
    print(f"Successfully renamed: {len(results['renamed'])}")
    print(f"Failed: {len(results['failed'])}")
    print("Report saved: abc_format_rename_report.json")
    
    return results

if __name__ == "__main__":
    rename_to_abc_format()
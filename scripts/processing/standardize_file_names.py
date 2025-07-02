#!/usr/bin/env python3
"""
Standardize file names in all markdown_papers folders
- Rename all .md files to paper.md
- Rename all .json files to metadata.json
"""
import os
from pathlib import Path
import json
from datetime import datetime

def standardize_folder_files(folder_path):
    """Standardize file names in a single folder"""
    results = {
        'folder': folder_path.name,
        'md_renamed': False,
        'json_renamed': False,
        'errors': []
    }
    
    # Find and rename markdown file
    md_files = list(folder_path.glob('*.md'))
    if len(md_files) == 0:
        results['errors'].append('No markdown file found')
    elif len(md_files) > 1:
        results['errors'].append(f'Multiple markdown files found: {[f.name for f in md_files]}')
    else:
        old_md = md_files[0]
        new_md = folder_path / 'paper.md'
        if old_md.name != 'paper.md':
            try:
                old_md.rename(new_md)
                results['md_renamed'] = True
                results['old_md_name'] = old_md.name
            except Exception as e:
                results['errors'].append(f'Error renaming markdown: {str(e)}')
        else:
            results['md_already_standard'] = True
    
    # Find and rename JSON file
    json_files = list(folder_path.glob('*.json'))
    if len(json_files) == 0:
        results['errors'].append('No JSON file found')
    elif len(json_files) > 1:
        results['errors'].append(f'Multiple JSON files found: {[f.name for f in json_files]}')
    else:
        old_json = json_files[0]
        new_json = folder_path / 'metadata.json'
        if old_json.name != 'metadata.json':
            try:
                old_json.rename(new_json)
                results['json_renamed'] = True
                results['old_json_name'] = old_json.name
            except Exception as e:
                results['errors'].append(f'Error renaming JSON: {str(e)}')
        else:
            results['json_already_standard'] = True
    
    return results

def main():
    """Process all folders in markdown_papers"""
    markdown_papers_dir = Path('markdown_papers')
    
    if not markdown_papers_dir.exists():
        print("Error: markdown_papers directory not found")
        return
    
    # Get all folders
    folders = [f for f in markdown_papers_dir.iterdir() if f.is_dir()]
    folders.sort()
    
    print(f"Processing {len(folders)} folders...\n")
    
    # Process each folder
    all_results = []
    stats = {
        'total_folders': len(folders),
        'md_renamed': 0,
        'json_renamed': 0,
        'already_standard': 0,
        'errors': 0
    }
    
    for folder in folders:
        result = standardize_folder_files(folder)
        all_results.append(result)
        
        if result['md_renamed']:
            stats['md_renamed'] += 1
            print(f"✓ {folder.name}: Renamed {result['old_md_name']} → paper.md")
        
        if result['json_renamed']:
            stats['json_renamed'] += 1
            print(f"✓ {folder.name}: Renamed {result['old_json_name']} → metadata.json")
        
        if result.get('md_already_standard') and result.get('json_already_standard'):
            stats['already_standard'] += 1
        
        if result['errors']:
            stats['errors'] += 1
            print(f"✗ {folder.name}: Errors: {', '.join(result['errors'])}")
    
    # Save detailed report
    report = {
        'timestamp': datetime.now().isoformat(),
        'statistics': stats,
        'details': all_results
    }
    
    with open('file_standardization_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print(f"\n{'='*50}")
    print("STANDARDIZATION COMPLETE")
    print(f"{'='*50}")
    print(f"Total folders processed: {stats['total_folders']}")
    print(f"Markdown files renamed: {stats['md_renamed']}")
    print(f"JSON files renamed: {stats['json_renamed']}")
    print(f"Already standardized: {stats['already_standard']}")
    print(f"Folders with errors: {stats['errors']}")
    print(f"\nDetailed report saved to: file_standardization_report.json")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Check the results of the folder renaming process.
"""

import csv
import os

def main():
    # Load CSV cite_keys
    csv_path = '/Users/invoture/dev.local/hdm/research_papers_clean.csv'
    csv_cite_keys = set()
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cite_key = row.get('cite_key', '').strip()
            if cite_key:
                csv_cite_keys.add(cite_key)
    
    # Check folders
    markdown_papers_dir = '/Users/invoture/dev.local/hdm/markdown_papers'
    folders = [f for f in os.listdir(markdown_papers_dir) 
               if os.path.isdir(os.path.join(markdown_papers_dir, f))]
    
    # Categorize folders
    cite_key_pattern_folders = [f for f in folders if f and f[0].islower() and '_' in f]
    other_folders = [f for f in folders if f not in cite_key_pattern_folders]
    
    # Check which CSV cite_keys have folders
    matched_folders = [f for f in cite_key_pattern_folders if f in csv_cite_keys]
    
    print("=== Folder Rename Results Summary ===")
    print(f"Total folders: {len(folders)}")
    print(f"Folders with cite_key pattern: {len(cite_key_pattern_folders)}")
    print(f"Folders matching CSV cite_keys: {len(matched_folders)}")
    print(f"Other folders (not renamed): {len(other_folders)}")
    print(f"CSV cite_keys: {len(csv_cite_keys)}")
    
    # Check for missing CSV cite_keys
    missing_cite_keys = csv_cite_keys - set(matched_folders)
    print(f"CSV cite_keys without folders: {len(missing_cite_keys)}")
    
    if missing_cite_keys:
        print(f"\nSample missing cite_keys:")
        for cite_key in sorted(missing_cite_keys)[:10]:
            print(f"  {cite_key}")
    
    if other_folders:
        print(f"\nSample unprocessed folders:")
        for folder in sorted(other_folders)[:10]:
            print(f"  {folder}")

if __name__ == '__main__':
    main()
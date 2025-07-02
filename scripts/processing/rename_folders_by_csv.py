#!/usr/bin/env python3
"""
Rename folders in markdown_papers to match cite_keys from research_papers_clean.csv.
Only rename folders whose papers have cite_keys that exist in the CSV file.
"""

import csv
import os
import re
from typing import Set, Dict, List, Tuple

def load_csv_cite_keys(csv_path: str) -> Set[str]:
    """Load all cite_keys from the CSV file."""
    cite_keys = set()
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cite_key = row.get('cite_key', '').strip()
            if cite_key:
                cite_keys.add(cite_key)
    return cite_keys

def extract_cite_key_from_markdown(md_file_path: str) -> str:
    """Extract cite_key from markdown file's YAML frontmatter."""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for YAML frontmatter
        if content.startswith('---'):
            # Find the end of YAML frontmatter
            parts = content.split('---', 2)
            if len(parts) >= 2:
                yaml_content = parts[1]
                # Use regex to find cite_key line
                cite_key_match = re.search(r'^cite_key:\s*(.+)$', yaml_content, re.MULTILINE)
                if cite_key_match:
                    return cite_key_match.group(1).strip()
    except Exception as e:
        print(f"Error reading {md_file_path}: {e}")
    
    return ""

def find_markdown_file_in_folder(folder_path: str) -> str:
    """Find the main markdown file in a folder."""
    try:
        for file in os.listdir(folder_path):
            if file.endswith('.md') and not file.endswith('_meta.json'):
                return os.path.join(folder_path, file)
    except Exception as e:
        print(f"Error listing folder {folder_path}: {e}")
    return ""

def scan_folders_for_cite_keys(markdown_papers_dir: str, csv_cite_keys: Set[str]) -> Dict[str, Tuple[str, str]]:
    """
    Scan all folders and find those with cite_keys that exist in the CSV.
    Returns: {current_folder_name: (cite_key, full_folder_path)}
    """
    matching_folders = {}
    
    try:
        folders = [f for f in os.listdir(markdown_papers_dir) 
                  if os.path.isdir(os.path.join(markdown_papers_dir, f))]
        
        print(f"Scanning {len(folders)} folders for cite_keys in CSV...")
        
        for folder_name in folders:
            folder_path = os.path.join(markdown_papers_dir, folder_name)
            
            # Find markdown file in folder
            md_file = find_markdown_file_in_folder(folder_path)
            if not md_file:
                continue
            
            # Extract cite_key from markdown file
            cite_key = extract_cite_key_from_markdown(md_file)
            if not cite_key:
                continue
            
            # Check if cite_key exists in CSV
            if cite_key in csv_cite_keys:
                matching_folders[folder_name] = (cite_key, folder_path)
                print(f"  Found: {folder_name} -> {cite_key}")
    
    except Exception as e:
        print(f"Error scanning folders: {e}")
    
    return matching_folders

def safe_rename_folder(old_path: str, new_name: str, base_dir: str) -> bool:
    """Safely rename a folder, handling conflicts."""
    new_path = os.path.join(base_dir, new_name)
    
    # Check if target already exists
    if os.path.exists(new_path):
        if os.path.samefile(old_path, new_path):
            print(f"  Skipping: {old_path} already has correct name")
            return True
        else:
            print(f"  Conflict: {new_path} already exists (different folder)")
            return False
    
    try:
        os.rename(old_path, new_path)
        print(f"  Renamed: {os.path.basename(old_path)} -> {new_name}")
        return True
    except Exception as e:
        print(f"  Error renaming {old_path} to {new_path}: {e}")
        return False

def main():
    """Main function to rename folders based on CSV cite_keys."""
    
    # Paths
    csv_path = '/Users/invoture/dev.local/hdm/research_papers_clean.csv'
    markdown_papers_dir = '/Users/invoture/dev.local/hdm/markdown_papers'
    
    print("=== Folder Renaming Based on CSV Cite Keys ===")
    
    # Load cite_keys from CSV
    print(f"Loading cite_keys from {csv_path}...")
    csv_cite_keys = load_csv_cite_keys(csv_path)
    print(f"Found {len(csv_cite_keys)} cite_keys in CSV")
    
    # Scan folders for matching cite_keys
    matching_folders = scan_folders_for_cite_keys(markdown_papers_dir, csv_cite_keys)
    print(f"\nFound {len(matching_folders)} folders with cite_keys in CSV")
    
    if not matching_folders:
        print("No folders to rename!")
        return
    
    # Show what will be renamed
    print(f"\n=== Folders to Rename ===")
    for old_name, (cite_key, folder_path) in matching_folders.items():
        if old_name != cite_key:
            print(f"  {old_name} -> {cite_key}")
        else:
            print(f"  {old_name} (already correct)")
    
    # Auto-proceed for automation
    print(f"\nProceeding with renaming {len(matching_folders)} folders...")
    
    # Perform renames
    print(f"\n=== Performing Renames ===")
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for old_name, (cite_key, folder_path) in matching_folders.items():
        if old_name == cite_key:
            print(f"  Skipping: {old_name} already has correct name")
            skip_count += 1
            continue
        
        if safe_rename_folder(folder_path, cite_key, markdown_papers_dir):
            success_count += 1
        else:
            error_count += 1
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Successfully renamed: {success_count} folders")
    print(f"Skipped (already correct): {skip_count} folders")
    print(f"Errors: {error_count} folders")
    print(f"Total processed: {len(matching_folders)} folders")
    
    # Show remaining folders that weren't processed
    total_folders = len([f for f in os.listdir(markdown_papers_dir) 
                        if os.path.isdir(os.path.join(markdown_papers_dir, f))])
    unprocessed = total_folders - len(matching_folders)
    print(f"Unprocessed folders (not in CSV): {unprocessed}")
    
    if error_count > 0:
        print(f"\nWARNING: {error_count} folders could not be renamed. Check for conflicts or permissions.")

if __name__ == '__main__':
    main()
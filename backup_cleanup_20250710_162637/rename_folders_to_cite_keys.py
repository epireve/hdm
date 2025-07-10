#!/usr/bin/env python3
"""
Rename markdown paper folders to match their cite_keys
"""

import os
import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional

MARKDOWN_PAPERS = Path("markdown_papers")
RENAME_LOG = Path("folder_rename_log.json")

def extract_cite_key_from_yaml(md_path: Path) -> Optional[str]:
    """Extract cite_key from YAML frontmatter"""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for cite_key in YAML frontmatter
        yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            cite_key_match = re.search(r'^cite_key:\s*"([^"]+)"', yaml_content, re.MULTILINE)
            if cite_key_match:
                return cite_key_match.group(1)
    except Exception as e:
        print(f"Error reading {md_path}: {e}")
    
    return None

def sanitize_folder_name(name: str) -> str:
    """Sanitize folder name for filesystem"""
    # Remove or replace problematic characters
    name = re.sub(r'[<>:"|?*]', '_', name)
    name = re.sub(r'[\\/]', '_', name)
    name = name.strip()
    
    # Limit length to reasonable size
    if len(name) > 200:
        name = name[:200]
    
    return name

def rename_folders():
    """Rename all paper folders to match their cite_keys"""
    rename_log = []
    errors = []
    skipped = []
    
    # Get all folders in markdown_papers
    folders = [f for f in MARKDOWN_PAPERS.iterdir() if f.is_dir()]
    print(f"Found {len(folders)} folders to process")
    
    for folder in sorted(folders):
        md_path = folder / "paper.md"
        
        if not md_path.exists():
            skipped.append({
                "folder": folder.name,
                "reason": "No paper.md found"
            })
            continue
        
        # Extract cite_key
        cite_key = extract_cite_key_from_yaml(md_path)
        
        if not cite_key:
            skipped.append({
                "folder": folder.name,
                "reason": "No cite_key found in YAML"
            })
            continue
        
        # Sanitize cite_key for folder name
        new_folder_name = sanitize_folder_name(cite_key)
        
        # Skip if already correctly named
        if folder.name == new_folder_name:
            skipped.append({
                "folder": folder.name,
                "reason": "Already correctly named"
            })
            continue
        
        # Check if target exists
        new_folder_path = MARKDOWN_PAPERS / new_folder_name
        if new_folder_path.exists():
            # Add suffix to make unique
            suffix = 1
            while True:
                test_name = f"{new_folder_name}_{suffix}"
                test_path = MARKDOWN_PAPERS / test_name
                if not test_path.exists():
                    new_folder_name = test_name
                    new_folder_path = test_path
                    break
                suffix += 1
        
        # Perform rename
        try:
            shutil.move(str(folder), str(new_folder_path))
            rename_log.append({
                "old_name": folder.name,
                "new_name": new_folder_name,
                "cite_key": cite_key,
                "status": "success"
            })
            print(f"✓ Renamed: {folder.name} -> {new_folder_name}")
        except Exception as e:
            errors.append({
                "folder": folder.name,
                "cite_key": cite_key,
                "error": str(e)
            })
            print(f"✗ Error renaming {folder.name}: {e}")
    
    # Save log
    from datetime import datetime
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "folders_processed": len(folders),
        "renamed": len(rename_log),
        "skipped": len(skipped),
        "errors": len(errors),
        "rename_log": rename_log,
        "skipped_folders": skipped,
        "error_log": errors
    }
    
    with open(RENAME_LOG, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("Folder Renaming Summary:")
    print(f"Total folders: {len(folders)}")
    print(f"Successfully renamed: {len(rename_log)}")
    print(f"Skipped: {len(skipped)}")
    print(f"Errors: {len(errors)}")
    print(f"\nLog saved to: {RENAME_LOG}")
    
    # Show a few examples if any were renamed
    if rename_log:
        print("\nExample renames:")
        for item in rename_log[:5]:
            print(f"  {item['old_name']} -> {item['new_name']}")

if __name__ == "__main__":
    rename_folders()
#!/usr/bin/env python3
"""
Process untouched folders: delete duplicates and rename to cite_keys
"""
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

def create_backup_directory():
    """Create a backup directory for deleted folders"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"deleted_duplicates_backup_{timestamp}")
    backup_dir.mkdir(exist_ok=True)
    return backup_dir

def delete_duplicate_folders(duplicates_list, backup_dir, dry_run=False):
    """Delete duplicate folders with backup"""
    deleted = []
    failed = []
    
    markdown_papers_dir = Path('markdown_papers')
    
    for folder_name in duplicates_list:
        folder_path = markdown_papers_dir / folder_name
        
        if not folder_path.exists():
            print(f"Warning: Folder {folder_name} not found")
            failed.append((folder_name, "Not found"))
            continue
        
        try:
            if dry_run:
                print(f"[DRY RUN] Would delete: {folder_name}")
            else:
                # Move to backup directory
                backup_path = backup_dir / folder_name
                shutil.move(str(folder_path), str(backup_path))
                print(f"Deleted (backed up): {folder_name}")
                deleted.append(folder_name)
        except Exception as e:
            print(f"Error deleting {folder_name}: {e}")
            failed.append((folder_name, str(e)))
    
    return deleted, failed

def rename_folders(rename_mapping, dry_run=False):
    """Rename folders to their cite_keys"""
    renamed = []
    failed = []
    
    markdown_papers_dir = Path('markdown_papers')
    
    for old_name, new_name in rename_mapping.items():
        old_path = markdown_papers_dir / old_name
        new_path = markdown_papers_dir / new_name
        
        if not old_path.exists():
            print(f"Warning: Folder {old_name} not found")
            failed.append((old_name, new_name, "Not found"))
            continue
        
        if new_path.exists():
            print(f"Warning: Target folder {new_name} already exists")
            failed.append((old_name, new_name, "Target exists"))
            continue
        
        try:
            if dry_run:
                print(f"[DRY RUN] Would rename: {old_name} → {new_name}")
            else:
                old_path.rename(new_path)
                print(f"Renamed: {old_name} → {new_name}")
                renamed.append((old_name, new_name))
        except Exception as e:
            print(f"Error renaming {old_name}: {e}")
            failed.append((old_name, new_name, str(e)))
    
    return renamed, failed

def main(dry_run=False):
    """Main processing function"""
    # Load action plan
    with open('untouched_folders_action_plan.json', 'r', encoding='utf-8') as f:
        action_plan = json.load(f)
    
    print(f"Processing untouched folders (dry_run={dry_run})")
    print(f"- Folders to delete: {len(action_plan['duplicates_to_delete'])}")
    print(f"- Folders to rename: {len(action_plan['folders_to_rename'])}")
    print()
    
    # Create backup directory for deletions
    backup_dir = None
    if not dry_run and action_plan['duplicates_to_delete']:
        backup_dir = create_backup_directory()
        print(f"Backup directory created: {backup_dir}")
    
    # Delete duplicates
    if action_plan['duplicates_to_delete']:
        print("\n=== Deleting Duplicate Folders ===")
        deleted, delete_failed = delete_duplicate_folders(
            action_plan['duplicates_to_delete'], 
            backup_dir, 
            dry_run
        )
        print(f"Deleted: {len(deleted)}, Failed: {len(delete_failed)}")
    
    # Rename folders
    if action_plan['folders_to_rename']:
        print("\n=== Renaming Folders to Cite Keys ===")
        renamed, rename_failed = rename_folders(
            action_plan['folders_to_rename'], 
            dry_run
        )
        print(f"Renamed: {len(renamed)}, Failed: {len(rename_failed)}")
    
    # Create processing report
    if not dry_run:
        report = {
            'timestamp': datetime.now().isoformat(),
            'backup_directory': str(backup_dir) if backup_dir else None,
            'deleted': deleted if 'deleted' in locals() else [],
            'delete_failed': delete_failed if 'delete_failed' in locals() else [],
            'renamed': renamed if 'renamed' in locals() else [],
            'rename_failed': rename_failed if 'rename_failed' in locals() else [],
            'folders_missing_metadata': action_plan['folders_missing_metadata']
        }
        
        with open('untouched_folders_processing_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nProcessing report saved to: untouched_folders_processing_report.json")

if __name__ == "__main__":
    import sys
    
    # Run in dry-run mode first
    print("=== DRY RUN MODE ===")
    main(dry_run=True)
    
    response = input("\nProceed with actual processing? (yes/no): ")
    if response.lower() == 'yes':
        print("\n=== ACTUAL PROCESSING ===")
        main(dry_run=False)
    else:
        print("Processing cancelled.")
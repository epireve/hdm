#!/usr/bin/env python3
"""
Safely delete only confirmed duplicates (matching cite_key AND title)
"""
import json
import shutil
from pathlib import Path
from datetime import datetime

def create_backup_and_delete():
    """Delete only confirmed duplicates"""
    # Load verification results
    with open('duplicate_verification_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    confirmed_duplicates = results['verification_results']['confirmed_duplicates']
    
    if not confirmed_duplicates:
        print("No confirmed duplicates to delete.")
        return
    
    # Create backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"deleted_duplicates_backup_verified_{timestamp}")
    backup_dir.mkdir(exist_ok=True)
    
    print(f"Backup directory: {backup_dir}")
    print(f"Deleting {len(confirmed_duplicates)} confirmed duplicates...\n")
    
    markdown_papers_dir = Path('markdown_papers')
    deleted = []
    failed = []
    
    for dup in confirmed_duplicates:
        folder_to_delete = dup['old_folder']
        folder_path = markdown_papers_dir / folder_to_delete
        
        if not folder_path.exists():
            print(f"Already deleted: {folder_to_delete}")
            continue
        
        try:
            # Move to backup
            backup_path = backup_dir / folder_to_delete
            shutil.move(str(folder_path), str(backup_path))
            print(f"✓ Deleted: {folder_to_delete}")
            print(f"  - Cite key: {dup['cite_key']}")
            print(f"  - Title: {dup['title'][:80]}...")
            deleted.append(folder_to_delete)
        except Exception as e:
            print(f"✗ Failed to delete {folder_to_delete}: {e}")
            failed.append((folder_to_delete, str(e)))
    
    # Save deletion report
    report = {
        'timestamp': datetime.now().isoformat(),
        'backup_directory': str(backup_dir),
        'deleted_count': len(deleted),
        'failed_count': len(failed),
        'deleted_folders': deleted,
        'failed_deletions': failed
    }
    
    with open(f'deletion_report_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n=== Summary ===")
    print(f"Deleted: {len(deleted)} folders")
    print(f"Failed: {len(failed)} folders")
    print(f"Backup location: {backup_dir}")
    print(f"Report saved: deletion_report_{timestamp}.json")

if __name__ == "__main__":
    response = input("This will delete 36 confirmed duplicate folders. Continue? (yes/no): ")
    if response.lower() == 'yes':
        create_backup_and_delete()
    else:
        print("Deletion cancelled.")
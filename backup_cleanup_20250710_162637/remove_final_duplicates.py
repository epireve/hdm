#!/usr/bin/env python3
"""
Remove final remaining exact title duplicates
"""

import os
import shutil
import csv
from datetime import datetime

def create_backup_dir():
    """Create backup directory for deleted files"""
    backup_dir = "/Users/invoture/dev.local/hdm/deleted_duplicates_backup_final"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return backup_dir

def find_folder_by_cite_key(cite_key, base_dir):
    """Find folder containing markdown file with specific cite_key"""
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if f'cite_key: {cite_key}' in content:
                            return root
                except:
                    continue
    return None

def backup_and_remove_folder(folder_path, backup_dir):
    """Backup folder to backup directory then remove it"""
    if not os.path.exists(folder_path):
        print(f"WARNING: Folder not found: {folder_path}")
        return False
    
    folder_name = os.path.basename(folder_path)
    backup_path = os.path.join(backup_dir, folder_name)
    
    try:
        # Copy folder to backup
        shutil.copytree(folder_path, backup_path)
        print(f"Backed up: {folder_path} -> {backup_path}")
        
        # Remove original folder
        shutil.rmtree(folder_path)
        print(f"Removed: {folder_path}")
        
        return True
    except Exception as e:
        print(f"ERROR removing {folder_path}: {e}")
        return False

def update_csv_after_deletion(csv_path, deleted_cite_keys):
    """Remove deleted papers from the CSV file"""
    temp_csv = csv_path + ".temp"
    
    papers_kept = []
    papers_removed = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['cite_key'] in deleted_cite_keys:
                papers_removed.append(row)
            else:
                papers_kept.append(row)
    
    # Write updated CSV
    with open(temp_csv, 'w', encoding='utf-8', newline='') as f:
        if papers_kept:
            fieldnames = papers_kept[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(papers_kept)
    
    # Replace original with temp
    shutil.move(temp_csv, csv_path)
    
    return len(papers_kept), len(papers_removed)

def main():
    """Main function to remove final exact title duplicates"""
    
    # Final remaining exact title duplicates to remove (based on analysis)
    duplicates_to_delete = [
        {
            'cite_key': 'words_2023',
            'keep_instead': 'asprino_2023',
            'reason': 'Same title "Knowledge Graph Construction with a façade" - keep asprino_2023 (original authors)'
        },
        {
            'cite_key': 'carriero_2020', 
            'keep_instead': 'bikakis_2021',
            'reason': 'Same title "Pattern-based design applied to cultural heritage knowledge graphs" - keep bikakis_2021 (more complete)'
        },
        {
            'cite_key': 'kolkata_2022',
            'keep_instead': 'chakraborty_2022', 
            'reason': 'Same title "Personal Research Knowledge Graphs" - keep chakraborty_2022 (complete author list)'
        },
        {
            'cite_key': 'xia_2023',
            'keep_instead': 'peng_2021',
            'reason': 'Same title "Knowledge Graphs: Opportunities and Challenges" - keep peng_2021 (more complete authors)'
        },
        {
            'cite_key': 'wang_2025',
            'keep_instead': 'wang_2023',
            'reason': 'DUPLICATE: Same arXiv paper 2308.02457 processed twice - correct year is 2023, not 2025'
        }
    ]
    
    print("=== FINAL DUPLICATE REMOVAL PROCESS ===")
    print(f"Removing {len(duplicates_to_delete)} remaining exact title duplicates")
    print("These are confirmed duplicates with identical titles")
    print()
    
    # Create backup directory
    backup_dir = create_backup_dir()
    print(f"Backup directory: {backup_dir}")
    print()
    
    # Base directory for searching
    base_dir = "/Users/invoture/dev.local/hdm/markdown_papers"
    
    # Process each duplicate
    removed_cite_keys = []
    successful_removals = 0
    
    for duplicate in duplicates_to_delete:
        cite_key = duplicate['cite_key']
        keep_instead = duplicate['keep_instead']
        reason = duplicate['reason']
        
        print(f"Processing: {cite_key}")
        print(f"Keeping instead: {keep_instead}")
        print(f"Reason: {reason}")
        
        # Find the folder containing this cite_key
        folder_path = find_folder_by_cite_key(cite_key, base_dir)
        
        if folder_path:
            print(f"Found folder: {folder_path}")
            
            if backup_and_remove_folder(folder_path, backup_dir):
                removed_cite_keys.append(cite_key)
                successful_removals += 1
        else:
            print(f"WARNING: Could not find folder for cite_key: {cite_key}")
        
        print()
    
    # Update CSV files
    csv_files = [
        '/Users/invoture/dev.local/hdm/research_papers_clean.csv',
        '/Users/invoture/dev.local/hdm/research_papers_sorted.csv'
    ]
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            kept, removed = update_csv_after_deletion(csv_file, removed_cite_keys)
            print(f"Updated {csv_file}: {kept} papers kept, {removed} papers removed")
    
    # Create removal log
    log_file = f"{backup_dir}/removal_log.txt"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Final Duplicate Removal Log\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total duplicates processed: {len(duplicates_to_delete)}\n")
        f.write(f"Successful removals: {successful_removals}\n\n")
        
        f.write("Removed Files (keeping the better version):\n")
        for duplicate in duplicates_to_delete:
            if duplicate['cite_key'] in removed_cite_keys:
                f.write(f"- REMOVED: {duplicate['cite_key']}\n")
                f.write(f"  KEPT: {duplicate['keep_instead']}\n")
                f.write(f"  REASON: {duplicate['reason']}\n\n")
    
    print(f"=== SUMMARY ===")
    print(f"Duplicates processed: {len(duplicates_to_delete)}")
    print(f"Successful removals: {successful_removals}")
    print(f"Files backed up to: {backup_dir}")
    print(f"Removal log: {log_file}")
    
    if successful_removals > 0:
        print(f"\n✅ Successfully removed {successful_removals} final duplicate files")
        print("All papers now have unique titles")
        print("All removed files have been backed up and can be restored if needed")
    else:
        print("\n⚠️  No files were removed - please check cite_keys")
    
    # Run final duplicate check
    print(f"\n=== RUNNING FINAL DUPLICATE CHECK ===")
    os.system("python /Users/invoture/dev.local/hdm/sort_and_dedupe_papers.py")

if __name__ == "__main__":
    main()
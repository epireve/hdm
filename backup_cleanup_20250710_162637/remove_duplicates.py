#!/usr/bin/env python3
"""
Remove confirmed duplicate markdown files after backing them up
"""

import os
import shutil
import csv
from datetime import datetime

def create_backup_dir():
    """Create backup directory for deleted files"""
    backup_dir = "/Users/invoture/dev.local/hdm/deleted_duplicates_backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return backup_dir

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
    """Main function to remove confirmed duplicates"""
    
    # List of confirmed duplicates to delete (based on detailed analysis and verified paths)
    duplicates_to_delete = [
        {
            'cite_key': 'galu_2024',
            'folder': '/Users/invoture/dev.local/hdm/markdown_papers/arxiv_2402.07540_PKG_API_A_Tool_for_Personal_Knowledge_Graph_Manag',
            'reason': 'Incomplete author list, keep Bernard version with complete metadata'
        },
        {
            'cite_key': 'yue_2023',  
            'folder': '/Users/invoture/dev.local/hdm/markdown_papers/arxiv_arxiv_2311.16502_MMMU_A_Massive_Multi-discipline_Multimodal_Understanding_and_Reasoning_Benchmark_for_Expert_AGI',
            'reason': 'Redundant arxiv_arxiv prefix, keep clean version'
        },
        {
            'cite_key': 'neupane_2024',
            'folder': '/Users/invoture/dev.local/hdm/markdown_papers/patient_centric_kg_survey_2024',
            'reason': 'Incomplete author list, keep frontiers version with complete metadata'
        },
        {
            'cite_key': 'arazzi_2019',
            'folder': '/Users/invoture/dev.local/hdm/markdown_papers/arxiv_arxiv_2401.03552_Privacy-preserving_in_Blockchain-based_Federated_Learning_Systems',
            'reason': 'Incorrect year and authorship, redundant prefix'
        }
    ]
    
    print("=== DUPLICATE REMOVAL PROCESS ===")
    print(f"Starting removal of {len(duplicates_to_delete)} confirmed duplicate files")
    print()
    
    # Create backup directory
    backup_dir = create_backup_dir()
    print(f"Backup directory: {backup_dir}")
    print()
    
    # Process each duplicate
    removed_cite_keys = []
    successful_removals = 0
    
    for duplicate in duplicates_to_delete:
        cite_key = duplicate['cite_key']
        folder_path = duplicate['folder']
        reason = duplicate['reason']
        
        print(f"Processing: {cite_key}")
        print(f"Folder: {folder_path}")
        print(f"Reason: {reason}")
        
        if backup_and_remove_folder(folder_path, backup_dir):
            removed_cite_keys.append(cite_key)
            successful_removals += 1
        
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
        f.write(f"Duplicate Removal Log\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total duplicates processed: {len(duplicates_to_delete)}\n")
        f.write(f"Successful removals: {successful_removals}\n\n")
        
        f.write("Removed Files:\n")
        for duplicate in duplicates_to_delete:
            if duplicate['cite_key'] in removed_cite_keys:
                f.write(f"- {duplicate['cite_key']}: {duplicate['folder']}\n")
                f.write(f"  Reason: {duplicate['reason']}\n\n")
    
    print(f"=== SUMMARY ===")
    print(f"Duplicates processed: {len(duplicates_to_delete)}")
    print(f"Successful removals: {successful_removals}")
    print(f"Files backed up to: {backup_dir}")
    print(f"Removal log: {log_file}")
    
    if successful_removals > 0:
        print(f"\n✅ Successfully removed {successful_removals} duplicate files")
        print("All removed files have been backed up and can be restored if needed")
    else:
        print("\n⚠️  No files were removed - please check folder paths")

if __name__ == "__main__":
    main()
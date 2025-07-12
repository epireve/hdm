#!/usr/bin/env python3
"""
Delete empty folders that have no content
"""
import json
import shutil
from pathlib import Path
from datetime import datetime

def delete_empty_folders():
    """Delete folders that are empty"""
    empty_folders = [
        "arxiv_arxiv_2112.08025_TLogic_Temporal_Logical_Rules_for_Explainable_Link_Forecasting_on_Temporal_Knowledge_Graphs",
        "arxiv_arxiv_2502.13412_Explore-Construct-Filter_An_Automated_Framework_for_Rich_and_Reliable_API_Knowle",
        "constructing_pkg_conversation_rl_2024",
        "jmir_2023_digital_health_coaching_hpv",
        "Local-Global_History-Aware_Contrastive_Learning_for_Temporal_Knowledge_Graph_Reasoning",
        "openreview_141b7821_Share_Your_Representation_Only_Guaranteed_Improvement_of_the_Privacy-Utility_Tradeoff_in_Federated_L",
        "precision_nutrition_pkg_2024",
        "Question_Answering_Over_Temporal_KG_ACL2021"
    ]
    
    markdown_papers_dir = Path('markdown_papers')
    
    # Create backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"deleted_empty_folders_backup_{timestamp}")
    backup_dir.mkdir(exist_ok=True)
    
    results = {
        'deleted': [],
        'failed': [],
        'timestamp': timestamp
    }
    
    print(f"Deleting {len(empty_folders)} empty folders...")
    print(f"Backup directory: {backup_dir}\n")
    
    for folder in empty_folders:
        folder_path = markdown_papers_dir / folder
        
        if not folder_path.exists():
            print(f"✗ Already gone: {folder}")
            continue
        
        try:
            # Move to backup
            backup_path = backup_dir / folder
            shutil.move(str(folder_path), str(backup_path))
            print(f"✓ Deleted: {folder}")
            results['deleted'].append(folder)
        except Exception as e:
            print(f"✗ Failed to delete {folder}: {e}")
            results['failed'].append({
                'folder': folder,
                'error': str(e)
            })
    
    # Save report
    report = {
        'timestamp': datetime.now().isoformat(),
        'backup_directory': str(backup_dir),
        'total_deleted': len(results['deleted']),
        'total_failed': len(results['failed']),
        'deleted_folders': results['deleted'],
        'failed_deletions': results['failed']
    }
    
    with open(f'empty_folders_deletion_report_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n=== Summary ===")
    print(f"Deleted: {len(results['deleted'])} empty folders")
    print(f"Failed: {len(results['failed'])}")
    print(f"Backup: {backup_dir}")
    print(f"Report: empty_folders_deletion_report_{timestamp}.json")

if __name__ == "__main__":
    response = input("Delete 8 empty folders? (yes/no): ")
    if response.lower() == 'yes':
        delete_empty_folders()
    else:
        print("Deletion cancelled.")
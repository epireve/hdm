#!/usr/bin/env python3
"""
Fix specific folder names to match their cite_keys
"""

import shutil
from pathlib import Path

MARKDOWN_PAPERS = Path("markdown_papers")

def rename_specific_folders():
    """Rename specific folders to match their cite_keys"""
    
    # Define the folders to rename
    folders_to_rename = [
        {
            "old_name": "1_s2_0_s0950584922001240_main",
            "new_name": "li_2022",
            "cite_key": "li_2022"
        },
        {
            "old_name": "log_anomaly_detection_by_adversarial_autoencoders_with_graph_feature_fusion",
            "new_name": "xie_2024a",
            "cite_key": "xie_2024a"
        }
    ]
    
    success_count = 0
    
    for folder_info in folders_to_rename:
        old_path = MARKDOWN_PAPERS / folder_info["old_name"]
        new_path = MARKDOWN_PAPERS / folder_info["new_name"]
        
        if old_path.exists():
            if new_path.exists() and new_path != old_path:
                print(f"✗ Target folder already exists: {folder_info['new_name']}")
                continue
            
            try:
                print(f"Renaming: {folder_info['old_name']} -> {folder_info['new_name']}")
                shutil.move(str(old_path), str(new_path))
                success_count += 1
                print(f"✓ Successfully renamed folder to match cite_key: {folder_info['cite_key']}")
            except Exception as e:
                print(f"✗ Error renaming {folder_info['old_name']}: {e}")
        else:
            print(f"✗ Folder not found: {folder_info['old_name']}")
            # Check if it's already renamed
            if new_path.exists():
                print(f"  → Already renamed to: {folder_info['new_name']}")
    
    print(f"\nSummary: Successfully renamed {success_count} folders")

if __name__ == "__main__":
    rename_specific_folders()
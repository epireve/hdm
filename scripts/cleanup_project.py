#!/usr/bin/env python3
"""
Clean up redundant files in the HDM project, keeping only final versions
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Define files to keep and remove
KEEP_CSV_FILES = {
    "research_papers_complete_FINAL_normalized_tags.csv",
    "research_papers_merged_final_normalized_tags.csv", 
    "personalized_pkg_paperguide_clean.csv",
    "research_papers_final.csv",  # Original base file
}

REMOVE_CSV_FILES = {
    "research_papers_complete.csv",
    "research_papers_complete_cleaned.csv",
    "research_papers_complete_extracted.csv",
    "research_papers_complete_filled.csv",
    "research_papers_complete_FINAL_clean_tags.csv",
    "research_papers_complete_FINAL.csv",
    "research_papers_complete_final.csv",
    "research_papers_complete_regenerated.csv",
    "research_papers_complete_updated.csv",
    "research_papers_complete_with_relevancy.csv",
    "research_papers_merged_efficient.csv",
    "research_papers_merged_final_clean_tags.csv",
    "research_papers_merged_final.csv",
    "research_papers_merged.csv",
    "research_papers_test_output.csv",
    "unmatched_papers_efficient.csv",
    "unmatched_papers_final.csv",
    "unmatched_papers.csv",
    "papers_clean.csv",
    "personalized_pkg_paperguide_manual.csv",
    "personalized_pkg_paperguide.csv",
    "pkg_papers_clean.csv",
}

KEEP_SCRIPTS = {
    # Core processing scripts
    "process_new_papers_batch.py",
    "smart_converter.py",
    "validate_and_fix_yaml.py",
    "markdown_header_standardizer.py",
    "normalize_tags.py",
    "standardize_tags.py",
    
    # Final consolidated merge script
    "merge_datasets_final.py",
    
    # Utility scripts to keep
    "extract_pkg_papers.py",
    "verify_merge.py",
}

# Script patterns to remove
REMOVE_SCRIPT_PATTERNS = [
    "*duplicate*.py",
    "merge_*.py",
    "fix_*.py",
    "*converter*.py",
    "*convert*.py",
    "*image_descriptor*.py",
    "complete_*.py",
    "fill_*.py",
    "update_*.py",
    "extract_full_authors.py",
    "update_missing_authors.py",
    "rename_folders_to_cite_keys.py",
]

# Temporary files to remove
TEMP_FILES = [
    "comprehensive_checkpoint.json",
    "relevancy_checkpoint.json", 
    "processing.out",
    "complete_data_batch1.log",
    "complete_missing_data.log",
    "relevancy_analysis.log",
    "relevancy_regeneration.log",
    "papers_to_download.csv",
    "new_papers_checkpoint.json",
]

def create_backup_directory():
    """Create a backup directory with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"backup_cleanup_{timestamp}")
    backup_dir.mkdir(exist_ok=True)
    return backup_dir

def backup_file(file_path, backup_dir):
    """Backup a file before deletion"""
    if file_path.exists():
        relative_path = file_path.relative_to(Path.cwd())
        backup_path = backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return True
    return False

def clean_csv_files(backup_dir, dry_run=True):
    """Clean up redundant CSV files"""
    print("\n=== Cleaning CSV Files ===")
    
    removed_count = 0
    for csv_file in REMOVE_CSV_FILES:
        file_path = Path(csv_file)
        if file_path.exists():
            if dry_run:
                print(f"Would remove: {csv_file}")
            else:
                backup_file(file_path, backup_dir)
                file_path.unlink()
                print(f"Removed: {csv_file}")
            removed_count += 1
    
    print(f"\nCSV files to remove: {removed_count}")
    
    # List files we're keeping
    print("\nKeeping these CSV files:")
    for csv_file in KEEP_CSV_FILES:
        if Path(csv_file).exists():
            print(f"  ✓ {csv_file}")

def clean_scripts(backup_dir, dry_run=True):
    """Clean up redundant Python scripts"""
    print("\n=== Cleaning Python Scripts ===")
    
    scripts_dir = Path("scripts/processing")
    if not scripts_dir.exists():
        print("Scripts directory not found")
        return
    
    # Get all Python files
    all_scripts = set(f.name for f in scripts_dir.glob("*.py"))
    
    # Determine which to remove
    scripts_to_remove = set()
    
    # Add scripts matching remove patterns
    for pattern in REMOVE_SCRIPT_PATTERNS:
        for script in scripts_dir.glob(pattern):
            if script.name not in KEEP_SCRIPTS:
                scripts_to_remove.add(script.name)
    
    # Remove scripts
    removed_count = 0
    for script_name in sorted(scripts_to_remove):
        script_path = scripts_dir / script_name
        if script_path.exists():
            if dry_run:
                print(f"Would remove: {script_name}")
            else:
                backup_file(script_path, backup_dir)
                script_path.unlink()
                print(f"Removed: {script_name}")
            removed_count += 1
    
    print(f"\nScripts to remove: {removed_count}")
    
    # List scripts we're keeping
    print("\nKeeping these scripts:")
    remaining_scripts = all_scripts - scripts_to_remove
    for script in sorted(remaining_scripts):
        print(f"  ✓ {script}")

def clean_temp_files(backup_dir, dry_run=True):
    """Clean up temporary and log files"""
    print("\n=== Cleaning Temporary Files ===")
    
    removed_count = 0
    
    # Clean files in root and scripts/processing
    for temp_file in TEMP_FILES:
        # Check in root
        file_path = Path(temp_file)
        if file_path.exists():
            if dry_run:
                print(f"Would remove: {temp_file}")
            else:
                backup_file(file_path, backup_dir)
                file_path.unlink()
                print(f"Removed: {temp_file}")
            removed_count += 1
        
        # Check in scripts/processing
        script_path = Path("scripts/processing") / temp_file
        if script_path.exists():
            if dry_run:
                print(f"Would remove: scripts/processing/{temp_file}")
            else:
                backup_file(script_path, backup_dir)
                script_path.unlink()
                print(f"Removed: scripts/processing/{temp_file}")
            removed_count += 1
    
    print(f"\nTemporary files to remove: {removed_count}")

def clean_backup_files(backup_dir, dry_run=True):
    """Clean up paper_backup.md files"""
    print("\n=== Cleaning Backup Files ===")
    
    markdown_dir = Path("markdown_papers")
    if not markdown_dir.exists():
        print("Markdown papers directory not found")
        return
    
    removed_count = 0
    backup_files = list(markdown_dir.glob("*/paper_backup.md"))
    
    for backup_file in backup_files:
        if dry_run:
            # Use absolute path if relative path fails
            try:
                rel_path = backup_file.relative_to(Path.cwd())
            except ValueError:
                rel_path = backup_file
            print(f"Would remove: {rel_path}")
        else:
            if backup_dir:
                backup_file_path = backup_file
                try:
                    backup_file(backup_file_path, backup_dir)
                except:
                    pass
            backup_file.unlink()
            try:
                rel_path = backup_file.relative_to(Path.cwd())
            except ValueError:
                rel_path = backup_file
            print(f"Removed: {rel_path}")
        removed_count += 1
    
    print(f"\nBackup files to remove: {removed_count}")

def main():
    """Main cleanup function"""
    print("HDM Project Cleanup Tool")
    print("=" * 50)
    
    # First, do a dry run
    print("\n🔍 DRY RUN - Showing what would be removed...")
    print("=" * 50)
    
    backup_dir = None
    
    # Dry run
    clean_csv_files(backup_dir, dry_run=True)
    clean_scripts(backup_dir, dry_run=True)
    clean_temp_files(backup_dir, dry_run=True)
    clean_backup_files(backup_dir, dry_run=True)
    
    # Ask for confirmation
    print("\n" + "=" * 50)
    response = input("\nDo you want to proceed with cleanup? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        # Create backup directory
        backup_dir = create_backup_directory()
        print(f"\n✅ Creating backup in: {backup_dir}")
        
        # Perform actual cleanup
        print("\n🧹 Performing cleanup...")
        print("=" * 50)
        
        clean_csv_files(backup_dir, dry_run=False)
        clean_scripts(backup_dir, dry_run=False)
        clean_temp_files(backup_dir, dry_run=False)
        clean_backup_files(backup_dir, dry_run=False)
        
        print("\n✅ Cleanup completed!")
        print(f"📁 Backup created in: {backup_dir}")
        print("\n⚠️  If you need to restore any files, check the backup directory.")
    else:
        print("\n❌ Cleanup cancelled.")

if __name__ == "__main__":
    main()
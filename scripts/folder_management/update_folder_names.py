#!/usr/bin/env python3
"""
Update folder names to match corrected cite_keys.
This ensures folder structure matches the database cite_keys.
"""

import sqlite3
import os
import json
from pathlib import Path
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FolderUpdater:
    def __init__(self, db_path='hdm_papers.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        self.base_paths = [
            'markdown_papers',
            'production_final_reformatted_1752365947'
        ]
        
        self.rename_log = []
        self.errors = []
        
    def analyze_folder_updates_needed(self):
        """Analyze which folders need to be renamed."""
        
        # Get papers where cite_key != corrected_cite_key
        self.cursor.execute("""
            SELECT cite_key, corrected_cite_key, title, year
            FROM papers
            WHERE corrected_cite_key IS NOT NULL 
            AND corrected_cite_key != ''
            AND corrected_cite_key != cite_key
            ORDER BY cite_key
        """)
        
        papers_needing_update = self.cursor.fetchall()
        
        print(f"\n📊 FOLDER RENAMING ANALYSIS")
        print(f"=" * 70)
        print(f"Papers with cite_key corrections: {len(papers_needing_update)}")
        
        updates_needed = []
        
        for paper in papers_needing_update:
            old_cite_key = paper['cite_key']
            new_cite_key = paper['corrected_cite_key']
            
            # Find existing folder
            current_folder = None
            for base_path in self.base_paths:
                # Try exact match first
                test_path = Path(base_path) / old_cite_key
                if test_path.exists():
                    current_folder = test_path
                    break
                    
                # Try with new cite_key (might already be renamed)
                test_path = Path(base_path) / new_cite_key
                if test_path.exists():
                    current_folder = test_path
                    break
            
            if current_folder:
                updates_needed.append({
                    'old_cite_key': old_cite_key,
                    'new_cite_key': new_cite_key,
                    'current_folder': str(current_folder),
                    'title': paper['title'],
                    'year': paper['year']
                })
                
        print(f"Folders found that need renaming: {len(updates_needed)}")
        
        return updates_needed
    
    def create_cite_key_from_year_correction(self):
        """Create corrected cite_keys for papers where year was corrected."""
        
        # Find papers where the year in cite_key doesn't match actual year
        self.cursor.execute("""
            SELECT cite_key, year, title, authors, corrected_cite_key
            FROM papers
            WHERE cite_key LIKE '%_20%'
            ORDER BY cite_key
        """)
        
        papers = self.cursor.fetchall()
        corrections_needed = []
        
        for paper in papers:
            cite_key = paper['cite_key']
            actual_year = paper['year']
            
            # Extract year from cite_key
            import re
            match = re.search(r'(.+?)_(\d{4})([a-z]?)$', cite_key)
            if match:
                base_name = match.group(1)
                cite_key_year = int(match.group(2))
                suffix = match.group(3)
                
                if cite_key_year != actual_year:
                    # Need to create new cite_key
                    new_cite_key = f"{base_name}_{actual_year}{suffix}"
                    
                    # Check if this would create a duplicate
                    self.cursor.execute(
                        "SELECT COUNT(*) FROM papers WHERE cite_key = ? OR corrected_cite_key = ?",
                        (new_cite_key, new_cite_key)
                    )
                    
                    if self.cursor.fetchone()[0] > 0:
                        # Would create duplicate, add suffix
                        for letter in 'abcdefghijklmnopqrstuvwxyz':
                            test_key = f"{base_name}_{actual_year}{letter}"
                            self.cursor.execute(
                                "SELECT COUNT(*) FROM papers WHERE cite_key = ? OR corrected_cite_key = ?",
                                (test_key, test_key)
                            )
                            if self.cursor.fetchone()[0] == 0:
                                new_cite_key = test_key
                                break
                    
                    corrections_needed.append({
                        'cite_key': cite_key,
                        'new_cite_key': new_cite_key,
                        'year': actual_year,
                        'title': paper['title'][:60] + '...'
                    })
        
        if corrections_needed:
            print(f"\n🔧 CITE_KEY CORRECTIONS NEEDED DUE TO YEAR CHANGES:")
            print(f"Found {len(corrections_needed)} papers needing cite_key updates")
            
            for correction in corrections_needed[:10]:
                print(f"  {correction['cite_key']} → {correction['new_cite_key']} (year: {correction['year']})")
            
            if len(corrections_needed) > 10:
                print(f"  ... and {len(corrections_needed) - 10} more")
                
        return corrections_needed
    
    def update_corrected_cite_keys(self, corrections):
        """Update corrected_cite_key column in database."""
        
        updated_count = 0
        
        for correction in corrections:
            self.cursor.execute("""
                UPDATE papers 
                SET corrected_cite_key = ? 
                WHERE cite_key = ?
            """, (correction['new_cite_key'], correction['cite_key']))
            
            if self.cursor.rowcount > 0:
                updated_count += 1
                
        self.conn.commit()
        
        print(f"\n✅ Updated {updated_count} corrected_cite_keys in database")
        return updated_count
    
    def rename_folders(self, updates_needed, dry_run=True):
        """Rename folders to match corrected cite_keys."""
        
        if dry_run:
            print(f"\n🔍 DRY RUN - No changes will be made")
        else:
            print(f"\n🔧 RENAMING FOLDERS")
            
        print(f"=" * 70)
        
        success_count = 0
        
        for update in updates_needed:
            current_folder = Path(update['current_folder'])
            new_folder = current_folder.parent / update['new_cite_key']
            
            if current_folder.name == update['new_cite_key']:
                # Already renamed
                print(f"✓ Already correct: {update['new_cite_key']}")
                success_count += 1
                continue
                
            if new_folder.exists():
                # Target already exists
                error_msg = f"Target already exists: {new_folder}"
                print(f"❌ {error_msg}")
                self.errors.append({
                    'old': str(current_folder),
                    'new': str(new_folder),
                    'error': error_msg
                })
                continue
                
            if dry_run:
                print(f"Would rename: {current_folder.name} → {new_folder.name}")
                self.rename_log.append({
                    'old': str(current_folder),
                    'new': str(new_folder),
                    'status': 'dry_run'
                })
            else:
                try:
                    shutil.move(str(current_folder), str(new_folder))
                    print(f"✅ Renamed: {current_folder.name} → {new_folder.name}")
                    success_count += 1
                    
                    self.rename_log.append({
                        'old': str(current_folder),
                        'new': str(new_folder),
                        'status': 'success'
                    })
                    
                    # Update folder_path in database
                    self.cursor.execute("""
                        UPDATE papers 
                        SET folder_path = ? 
                        WHERE cite_key = ? OR corrected_cite_key = ?
                    """, (str(new_folder), update['old_cite_key'], update['new_cite_key']))
                    
                except Exception as e:
                    error_msg = str(e)
                    print(f"❌ Error renaming {current_folder.name}: {error_msg}")
                    self.errors.append({
                        'old': str(current_folder),
                        'new': str(new_folder),
                        'error': error_msg
                    })
        
        if not dry_run:
            self.conn.commit()
            
        return success_count
    
    def save_logs(self):
        """Save rename logs and errors."""
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'rename_log': self.rename_log,
            'errors': self.errors,
            'summary': {
                'total_renames': len(self.rename_log),
                'successful': len([l for l in self.rename_log if l.get('status') == 'success']),
                'errors': len(self.errors)
            }
        }
        
        with open('folder_rename_log.json', 'w') as f:
            json.dump(log_data, f, indent=2)
            
        print(f"\n📝 Logs saved to folder_rename_log.json")
    
    def close(self):
        """Close database connection."""
        self.conn.close()


def main():
    """Main execution function."""
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description='Update folder names to match corrected cite_keys')
    parser.add_argument('--execute', action='store_true', 
                       help='Execute the rename operations (default is dry run)')
    parser.add_argument('--update-cite-keys', action='store_true',
                       help='Update corrected_cite_keys based on year corrections')
    
    args = parser.parse_args()
    
    updater = FolderUpdater()
    
    try:
        # Step 1: Check for cite_key corrections needed due to year changes
        if args.update_cite_keys:
            corrections = updater.create_cite_key_from_year_correction()
            if corrections:
                response = input(f"\nUpdate {len(corrections)} corrected_cite_keys? (y/n): ")
                if response.lower() == 'y':
                    updater.update_corrected_cite_keys(corrections)
        
        # Step 2: Analyze what needs to be renamed
        updates_needed = updater.analyze_folder_updates_needed()
        
        if not updates_needed:
            print("\n✅ No folder updates needed!")
            return
            
        # Step 3: Perform renames
        if args.execute:
            response = input(f"\nRename {len(updates_needed)} folders? (y/n): ")
            if response.lower() == 'y':
                success_count = updater.rename_folders(updates_needed, dry_run=False)
                print(f"\n✅ Successfully renamed {success_count} folders")
        else:
            updater.rename_folders(updates_needed, dry_run=True)
            print(f"\n💡 To execute renames, run with --execute flag")
            
        # Step 4: Save logs
        updater.save_logs()
        
    finally:
        updater.close()


if __name__ == "__main__":
    main()
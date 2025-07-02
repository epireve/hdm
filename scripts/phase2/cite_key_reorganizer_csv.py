"""
Reorganizes markdown paper folders using cite keys from CSV as folder names
CSV version of cite_key_reorganizer.py
"""
import sys
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    MARKDOWN_DIR, CITE_KEY_MAPPING_FILE, TEST_MODE, TEST_PAPERS, BACKUP_DIR
)
from utils import (
    setup_logging, load_json, save_json, ProgressTracker
)

# Check for environment override
EFFECTIVE_TEST_MODE = TEST_MODE
if os.environ.get('PHASE2_TEST_MODE', '').lower() == 'false':
    EFFECTIVE_TEST_MODE = False


class CiteKeyReorganizer:
    """Handles folder reorganization based on cite keys"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "folders_renamed": 0,
            "files_updated": 0,
            "references_updated": 0,
            "errors": 0,
            "skipped": 0
        }
        self.rename_mapping = {}
    
    def reorganize_folders(self, papers: Dict) -> bool:
        """Reorganize all paper folders to use cite keys"""
        try:
            # Create backup of entire markdown_papers directory
            if not EFFECTIVE_TEST_MODE:
                self.logger.info("Creating backup of markdown_papers directory...")
                backup_path = BACKUP_DIR / f"markdown_papers_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copytree(MARKDOWN_DIR, backup_path)
                self.logger.info(f"Backup created at: {backup_path}")
            
            # Process papers
            papers_to_process = list(papers.items())
            process_limit = TEST_PAPERS if EFFECTIVE_TEST_MODE else len(papers_to_process)
            
            if EFFECTIVE_TEST_MODE:
                self.logger.info(f"Test mode: Processing only {TEST_PAPERS} papers")
            
            progress = ProgressTracker(min(process_limit, len(papers_to_process)), self.logger)
            
            # First pass: check for conflicts and prepare renames
            rename_plan = []
            processed = 0
            
            for folder_name, paper_info in papers_to_process:
                if processed >= process_limit:
                    break
                
                cite_key = paper_info.get("cite_key")
                if not cite_key:
                    self.logger.warning(f"No cite_key found for {folder_name}")
                    self.stats["skipped"] += 1
                    processed += 1
                    continue
                
                old_path = MARKDOWN_DIR / folder_name
                new_path = MARKDOWN_DIR / cite_key
                
                if not old_path.exists():
                    self.logger.warning(f"Folder not found: {old_path}")
                    self.stats["skipped"] += 1
                    processed += 1
                    continue
                
                if old_path == new_path:
                    self.logger.debug(f"Folder already has correct name: {cite_key}")
                    processed += 1
                    continue
                
                if new_path.exists():
                    # Try adding suffix
                    suffix = 2
                    while (MARKDOWN_DIR / f"{cite_key}_{suffix}").exists():
                        suffix += 1
                    new_path = MARKDOWN_DIR / f"{cite_key}_{suffix}"
                    self.logger.warning(f"Target exists, using: {new_path.name}")
                
                rename_plan.append((old_path, new_path, folder_name, cite_key))
                processed += 1
            
            # Execute renames
            self.logger.info(f"Executing {len(rename_plan)} folder renames...")
            
            for old_path, new_path, old_folder, new_folder in rename_plan:
                progress.update(f"Renaming {old_folder} -> {new_folder}")
                
                try:
                    # Rename folder
                    old_path.rename(new_path)
                    self.rename_mapping[old_folder] = new_path.name
                    self.stats["folders_renamed"] += 1
                    self.logger.info(f"Renamed: {old_folder} -> {new_path.name}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to rename {old_folder}: {e}")
                    self.stats["errors"] += 1
            
            # Second pass: update internal references
            if self.rename_mapping:
                self.logger.info("Updating internal references...")
                self._update_internal_references()
            
            # Save rename mapping for reference
            mapping_file = BACKUP_DIR / f"rename_mapping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_json({"rename_mapping": self.rename_mapping, "stats": self.stats}, mapping_file)
            self.logger.info(f"Rename mapping saved to: {mapping_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during reorganization: {e}")
            self.stats["errors"] += 1
            return False
    
    def _update_internal_references(self):
        """Update image references in markdown files after folder rename"""
        for old_folder, new_folder in self.rename_mapping.items():
            new_path = MARKDOWN_DIR / new_folder
            
            # Process all markdown files in the folder
            for md_file in new_path.glob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Update image references if they include folder paths
                    content = self._update_image_paths(content, old_folder, new_folder)
                    
                    # Update cite_key comment if present
                    content = re.sub(
                        rf'<!-- cite_key: \w+ -->', 
                        f'<!-- cite_key: {new_folder} -->', 
                        content
                    )
                    
                    if content != original_content:
                        with open(md_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        self.stats["files_updated"] += 1
                        self.logger.debug(f"Updated references in: {md_file.name}")
                        
                except Exception as e:
                    self.logger.error(f"Error updating {md_file}: {e}")
                    self.stats["errors"] += 1
    
    def _update_image_paths(self, content: str, old_folder: str, new_folder: str) -> str:
        """Update image paths in markdown content"""
        # Pattern to match image references that might include folder names
        patterns = [
            # Full path references
            (rf'!\[([^\]]*)\]\({re.escape(old_folder)}/([^\)]+)\)', 
             rf'![\1]({new_folder}/\2)'),
            # Relative path references
            (rf'!\[([^\]]*)\]\(\.\/{re.escape(old_folder)}/([^\)]+)\)', 
             rf'![\1](./{new_folder}/\2)'),
        ]
        
        refs_updated = 0
        for pattern, replacement in patterns:
            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                refs_updated += count
        
        if refs_updated > 0:
            self.stats["references_updated"] += refs_updated
            
        return content


def main():
    """Main function to reorganize folders with cite keys"""
    logger = setup_logging("cite_key_reorganizer_csv")
    logger.info("Starting folder reorganization with CSV cite keys")
    
    # Check if cite key mapping exists
    if not CITE_KEY_MAPPING_FILE.exists():
        logger.error(f"Cite key mapping not found at: {CITE_KEY_MAPPING_FILE}")
        logger.info("Please run paper_analyzer_csv.py first")
        return 1
    
    # Load cite key mapping
    logger.info("Loading cite key mappings...")
    mapping_data = load_json(CITE_KEY_MAPPING_FILE)
    papers = mapping_data.get('papers', {})
    
    if not papers:
        logger.error("No papers found in cite key mapping")
        return 1
    
    logger.info(f"Found {len(papers)} papers to process")
    
    # Initialize reorganizer
    reorganizer = CiteKeyReorganizer(logger)
    
    # Reorganize folders
    if reorganizer.reorganize_folders(papers):
        # Print summary
        stats = reorganizer.stats
        logger.info("\n" + "="*50)
        logger.info("REORGANIZATION SUMMARY")
        logger.info("="*50)
        logger.info(f"Folders renamed: {stats['folders_renamed']}")
        logger.info(f"Files updated: {stats['files_updated']}")
        logger.info(f"References updated: {stats['references_updated']}")
        logger.info(f"Folders skipped: {stats['skipped']}")
        logger.info(f"Errors: {stats['errors']}")
        logger.info("="*50)
        
        if stats['errors'] > 0:
            logger.warning("Some errors occurred during reorganization")
            return 1
    else:
        logger.error("Reorganization failed")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
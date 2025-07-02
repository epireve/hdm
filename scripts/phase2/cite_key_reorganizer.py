"""
Reorganizes markdown paper folders using cite keys as folder names
"""
import sys
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    MARKDOWN_PAPERS, OUTPUT_DIR, TEST_MODE, TEST_PAPERS, BACKUP_DIR
)
from utils import (
    setup_logging, read_json, write_json, ProgressTracker
)


class CiteKeyReorganizer:
    """Handles folder reorganization based on cite keys"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "folders_renamed": 0,
            "files_updated": 0,
            "references_updated": 0,
            "errors": 0
        }
        self.rename_mapping = {}
    
    def reorganize_folders(self, papers: Dict) -> bool:
        """Reorganize all paper folders to use cite keys"""
        try:
            # Create backup of entire markdown_papers directory
            if not TEST_MODE:
                self.logger.info("Creating backup of markdown_papers directory...")
                backup_path = BACKUP_DIR / f"markdown_papers_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copytree(MARKDOWN_PAPERS, backup_path)
                self.logger.info(f"Backup created at: {backup_path}")
            
            # Process papers
            papers_to_process = list(papers.items())
            if TEST_MODE:
                papers_to_process = papers_to_process[:TEST_PAPERS]
                self.logger.info(f"Test mode: Processing only {TEST_PAPERS} papers")
            
            # First pass: rename folders
            for folder_name, paper_info in papers_to_process:
                cite_key = paper_info["cite_key"]
                old_path = MARKDOWN_PAPERS / folder_name
                new_path = MARKDOWN_PAPERS / cite_key
                
                if not old_path.exists():
                    self.logger.warning(f"Folder not found: {old_path}")
                    continue
                
                if old_path != new_path:
                    if new_path.exists():
                        self.logger.warning(f"Target folder already exists: {new_path}")
                        continue
                    
                    # Rename folder
                    old_path.rename(new_path)
                    self.rename_mapping[folder_name] = cite_key
                    self.stats["folders_renamed"] += 1
                    self.logger.info(f"Renamed folder: {folder_name} -> {cite_key}")
            
            # Second pass: update internal references
            self._update_internal_references()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during reorganization: {e}")
            self.stats["errors"] += 1
            return False
    
    def _update_internal_references(self):
        """Update image references in markdown files after folder rename"""
        for old_folder, new_folder in self.rename_mapping.items():
            new_path = MARKDOWN_PAPERS / new_folder
            
            # Process all markdown files in the folder
            for md_file in new_path.glob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Update image references if they include folder paths
                    # This handles cases where images might have relative paths
                    content = self._update_image_paths(content, old_folder, new_folder)
                    
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
        # Pattern to match image references
        img_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        
        def replace_path(match):
            alt_text = match.group(1)
            img_path = match.group(2)
            
            # Check if the path contains the old folder name
            if old_folder in img_path:
                new_path = img_path.replace(old_folder, new_folder)
                self.stats["references_updated"] += 1
                return f'![{alt_text}]({new_path})'
            
            return match.group(0)
        
        return re.sub(img_pattern, replace_path, content)
    
    def create_reorganization_report(self) -> Dict:
        """Create a detailed report of the reorganization"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "rename_mapping": self.rename_mapping,
            "test_mode": TEST_MODE
        }
        
        return report


def main():
    """Main function to reorganize folders"""
    logger = setup_logging("cite_key_reorganizer")
    logger.info("Starting cite key reorganization")
    
    # Load paper analysis
    mapping_file = Path("cite_key_mapping.json")
    if not mapping_file.exists():
        logger.error("cite_key_mapping.json not found. Run paper_analyzer.py first.")
        return
    
    paper_mapping = read_json(mapping_file)
    papers = paper_mapping.get("papers", {})
    
    # Initialize reorganizer
    reorganizer = CiteKeyReorganizer(logger)
    
    # Perform reorganization
    logger.info(f"Reorganizing {len(papers)} paper folders...")
    if reorganizer.reorganize_folders(papers):
        logger.info("Reorganization completed successfully")
    else:
        logger.error("Reorganization failed")
    
    # Generate report
    report = reorganizer.create_reorganization_report()
    
    # Log summary
    logger.info("\nReorganization Summary:")
    logger.info(f"Folders renamed: {reorganizer.stats['folders_renamed']}")
    logger.info(f"Files updated: {reorganizer.stats['files_updated']}")
    logger.info(f"References updated: {reorganizer.stats['references_updated']}")
    logger.info(f"Errors: {reorganizer.stats['errors']}")
    
    # Save report
    report_file = OUTPUT_DIR / "reorganization_report.json"
    write_json(report, report_file)
    logger.info(f"Report saved to: {report_file}")
    
    # Update cite_key_mapping.json with new folder names
    if reorganizer.rename_mapping:
        for old_folder, new_folder in reorganizer.rename_mapping.items():
            if old_folder in paper_mapping["papers"]:
                paper_mapping["papers"][new_folder] = paper_mapping["papers"].pop(old_folder)
                paper_mapping["papers"][new_folder]["original_folder"] = old_folder
                paper_mapping["folder_mapping"][old_folder] = new_folder
        
        # Save updated mapping
        write_json(paper_mapping, mapping_file)
        logger.info(f"Updated cite_key_mapping.json")


if __name__ == "__main__":
    main()
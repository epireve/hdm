"""
Integrates metadata from CSV research table into markdown files as YAML front matter
CSV version of metadata_integrator.py
"""
import sys
import re
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
import shutil
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    MARKDOWN_DIR, RESEARCH_TABLE_CSV, CITE_KEY_MAPPING_FILE,
    TEST_MODE, TEST_PAPERS, BACKUP_DIR
)
from csv_utils import read_csv_to_dict
from utils import (
    setup_logging, load_json, ProgressTracker
)
from improved_author_extractor import extract_clean_authors, extract_title_from_markdown

# Check for environment override
EFFECTIVE_TEST_MODE = TEST_MODE
if os.environ.get('PHASE2_TEST_MODE', '').lower() == 'false':
    EFFECTIVE_TEST_MODE = False


class MetadataIntegrator:
    """Handles metadata integration into markdown files"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "papers_processed": 0,
            "metadata_added": 0,
            "metadata_updated": 0,
            "skipped": 0,
            "failed": 0
        }
    
    def integrate_metadata(self, markdown_path: Path, cite_key: str, 
                          research_data: Dict, paper_info: Dict) -> bool:
        """Add or update YAML front matter in markdown file"""
        try:
            # Read current content
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if cite_key comment already exists (from standardizer)
            # Remove it as we'll add proper YAML frontmatter
            content = re.sub(r'^<!-- cite_key: \w+ -->\n\n', '', content)
            
            # Check if YAML front matter exists
            yaml_pattern = r'^---\n(.*?)\n---\n'
            yaml_match = re.match(yaml_pattern, content, re.DOTALL)
            
            # Build YAML front matter
            yaml_content = self._build_yaml_frontmatter(cite_key, research_data, paper_info, markdown_path)
            
            if yaml_match:
                # Replace existing front matter
                new_content = re.sub(yaml_pattern, f'---\n{yaml_content}\n---\n', 
                                   content, count=1, flags=re.DOTALL)
                self.stats["metadata_updated"] += 1
                action = "Updated"
            else:
                # Add new front matter
                new_content = f'---\n{yaml_content}\n---\n\n{content}'
                self.stats["metadata_added"] += 1
                action = "Added"
            
            # Create backup
            backup_path = BACKUP_DIR / "metadata_integrator" / markdown_path.parent.name
            backup_path.mkdir(parents=True, exist_ok=True)
            backup_file = backup_path / f"{markdown_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            shutil.copy2(markdown_path, backup_file)
            
            # Write updated content
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"{action} metadata for: {cite_key}")
            self.stats["papers_processed"] += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Error integrating metadata for {cite_key}: {e}")
            self.stats["failed"] += 1
            return False
    
    def _build_yaml_frontmatter(self, cite_key: str, research_data: Dict, 
                               paper_info: Dict, markdown_path: Path) -> str:
        """Build YAML front matter content"""
        yaml_lines = []
        
        # Core metadata
        yaml_lines.append(f'cite_key: "{cite_key}"')
        
        # Extract clean title and authors from the markdown file
        extracted_title = extract_title_from_markdown(markdown_path)
        extracted_authors = extract_clean_authors(markdown_path)
        
        # Title - prefer extracted clean title, then research table
        if extracted_title:
            yaml_lines.append(f'title: "{self._escape_yaml(extracted_title)}"')
        elif research_data and research_data.get("Paper Title"):
            yaml_lines.append(f'title: "{self._escape_yaml(research_data["Paper Title"])}"')
        elif paper_info.get("metadata", {}).get("title"):
            yaml_lines.append(f'title: "{self._escape_yaml(paper_info["metadata"]["title"])}"')
        
        # Authors - prefer extracted clean authors
        if extracted_authors:
            yaml_lines.append(f'authors: "{self._escape_yaml(extracted_authors)}"')
        elif research_data and research_data.get("Authors"):
            # Try to clean research table authors too
            authors = research_data["Authors"]
            # Remove "et al." if present
            authors = re.sub(r'\s+et\s+al\.?', '', authors, flags=re.IGNORECASE)
            yaml_lines.append(f'authors: "{self._escape_yaml(authors)}"')
        elif paper_info.get("metadata", {}).get("authors"):
            yaml_lines.append(f'authors: "{self._escape_yaml(paper_info["metadata"]["authors"])}"')
        
        # Year
        if research_data and research_data.get("Year"):
            yaml_lines.append(f'year: {research_data["Year"]}')
        elif paper_info.get("metadata", {}).get("year"):
            yaml_lines.append(f'year: {paper_info["metadata"]["year"]}')
        
        # Journal/Venue
        if paper_info.get("metadata", {}).get("journal"):
            yaml_lines.append(f'journal: "{self._escape_yaml(paper_info["metadata"]["journal"])}"')
        
        # DOI
        if research_data and research_data.get("DOI"):
            yaml_lines.append(f'doi: "{research_data["DOI"]}"')
        elif paper_info.get("metadata", {}).get("doi"):
            yaml_lines.append(f'doi: "{paper_info["metadata"]["doi"]}"')
        
        # URL
        if research_data and research_data.get("url"):
            yaml_lines.append(f'url: "{research_data["url"]}"')
        
        # Additional research table metadata
        if research_data:
            # Relevancy
            if research_data.get("Relevancy"):
                yaml_lines.append(f'relevancy: "{research_data["Relevancy"]}"')
            
            # Downloaded status
            if research_data.get("Downloaded"):
                yaml_lines.append(f'downloaded: "{research_data["Downloaded"]}"')
            
            # Tags
            if research_data.get("Tags"):
                tags = [tag.strip() for tag in research_data["Tags"].split(",") if tag.strip()]
                if tags:
                    yaml_lines.append("tags:")
                    for tag in tags:
                        yaml_lines.append(f'  - "{self._escape_yaml(tag)}"')
            
            # TL;DR
            if research_data.get("TL;DR"):
                yaml_lines.append(f'tldr: "{self._escape_yaml(research_data["TL;DR"])}"')
        
        # Processing metadata
        yaml_lines.append(f'date_processed: "{datetime.now().strftime("%Y-%m-%d")}"')
        yaml_lines.append('phase2_processed: true')
        
        # Paper info metadata
        if paper_info:
            if paper_info.get("original_folder"):
                yaml_lines.append(f'original_folder: "{paper_info["original_folder"]}"')
            
            # Image statistics
            images = paper_info.get("images", {})
            if images:
                yaml_lines.append(f'images_total: {len(images.get("keep", [])) + len(images.get("remove", []))}')
                yaml_lines.append(f'images_kept: {len(images.get("keep", []))}')
                yaml_lines.append(f'images_removed: {len(images.get("remove", []))}')
        
        return '\n'.join(yaml_lines)
    
    def _escape_yaml(self, value: str) -> str:
        """Escape special characters for YAML"""
        if not value:
            return ""
        # Escape quotes and backslashes
        value = value.replace('\\', '\\\\')
        value = value.replace('"', '\\"')
        # Remove newlines
        value = value.replace('\n', ' ').replace('\r', ' ')
        return value


def main():
    """Main function to integrate metadata into markdown files"""
    logger = setup_logging("metadata_integrator_csv")
    logger.info("Starting metadata integration with CSV data")
    
    # Check if required files exist
    if not CITE_KEY_MAPPING_FILE.exists():
        logger.error(f"Cite key mapping not found at: {CITE_KEY_MAPPING_FILE}")
        logger.info("Please run paper_analyzer_csv.py first")
        return 1
    
    if not RESEARCH_TABLE_CSV.exists():
        logger.error(f"Research table CSV not found at: {RESEARCH_TABLE_CSV}")
        return 1
    
    # Load cite key mapping
    logger.info("Loading cite key mappings...")
    mapping_data = load_json(CITE_KEY_MAPPING_FILE)
    papers_info = mapping_data.get('papers', {})
    
    if not papers_info:
        logger.error("No papers found in cite key mapping")
        return 1
    
    # Load research table
    logger.info("Loading research table from CSV...")
    headers, rows = read_csv_to_dict(RESEARCH_TABLE_CSV)
    
    # Create lookup by cite_key
    research_by_cite_key = {}
    for row in rows:
        cite_key = row.get("cite_key")
        if cite_key:
            research_by_cite_key[cite_key] = row
    
    logger.info(f"Found {len(papers_info)} papers to process")
    logger.info(f"Found {len(research_by_cite_key)} papers in research table")
    
    # Initialize integrator
    integrator = MetadataIntegrator(logger)
    
    # Process limit based on mode
    process_limit = TEST_PAPERS if EFFECTIVE_TEST_MODE else len(papers_info)
    
    # Create progress tracker
    progress = ProgressTracker(min(process_limit, len(papers_info)), logger)
    
    # Process each paper
    processed = 0
    for folder_name, paper_info in papers_info.items():
        if processed >= process_limit:
            logger.info(f"{'Test' if EFFECTIVE_TEST_MODE else 'Full'} mode: Processed {processed} papers")
            break
        
        cite_key = paper_info.get("cite_key")
        if not cite_key:
            logger.warning(f"No cite_key for {folder_name}")
            integrator.stats["skipped"] += 1
            processed += 1
            continue
        
        # Get research data if available
        research_data = research_by_cite_key.get(cite_key, {})
        
        # Find markdown file
        # Try multiple possible folder names
        possible_dirs = [
            MARKDOWN_DIR / cite_key,  # Renamed folder
            MARKDOWN_DIR / folder_name,  # Original folder
        ]
        
        paper_dir = None
        for possible_dir in possible_dirs:
            if possible_dir.exists():
                paper_dir = possible_dir
                break
        
        if not paper_dir:
            logger.warning(f"Paper directory not found: {folder_name} or {cite_key}")
            integrator.stats["skipped"] += 1
            processed += 1
            continue
        
        # Find markdown file
        markdown_file = None
        if paper_info.get("markdown_file"):
            markdown_file = paper_dir / paper_info["markdown_file"]
        
        if not markdown_file or not markdown_file.exists():
            # Try to find any markdown file
            md_files = list(paper_dir.glob("*.md"))
            if md_files:
                markdown_file = md_files[0]
            else:
                logger.warning(f"No markdown file found in: {paper_dir}")
                integrator.stats["skipped"] += 1
                processed += 1
                continue
        
        # Integrate metadata
        progress.update(f"Processing {cite_key}")
        integrator.integrate_metadata(markdown_file, cite_key, research_data, paper_info)
        
        processed += 1
    
    # Print summary
    stats = integrator.stats
    logger.info("\n" + "="*50)
    logger.info("METADATA INTEGRATION SUMMARY")
    logger.info("="*50)
    logger.info(f"Papers processed: {stats['papers_processed']}")
    logger.info(f"Metadata added: {stats['metadata_added']}")
    logger.info(f"Metadata updated: {stats['metadata_updated']}")
    logger.info(f"Papers skipped: {stats['skipped']}")
    logger.info(f"Failed: {stats['failed']}")
    logger.info("="*50)
    
    return 0 if stats['failed'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
"""
Integrates metadata from research table into markdown files as YAML front matter
"""
import sys
import re
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    MARKDOWN_PAPERS, RESEARCH_TABLE, OUTPUT_DIR, 
    TEST_MODE, TEST_PAPERS, BACKUP_DIR
)
from utils import (
    setup_logging, read_json, write_json,
    parse_markdown_table, extract_metadata_from_markdown
)


class MetadataIntegrator:
    """Handles metadata integration into markdown files"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "papers_processed": 0,
            "metadata_added": 0,
            "metadata_updated": 0,
            "failed": 0
        }
    
    def integrate_metadata(self, markdown_path: Path, cite_key: str, 
                          research_data: Dict, paper_info: Dict) -> bool:
        """Add or update YAML front matter in markdown file"""
        try:
            # Read current content
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if YAML front matter exists
            yaml_pattern = r'^---\n(.*?)\n---\n'
            yaml_match = re.match(yaml_pattern, content, re.DOTALL)
            
            # Build YAML front matter
            yaml_content = self._build_yaml_frontmatter(cite_key, research_data, paper_info)
            
            if yaml_match:
                # Replace existing front matter
                new_content = re.sub(yaml_pattern, f'---\n{yaml_content}\n---\n', 
                                   content, count=1, flags=re.DOTALL)
                self.stats["metadata_updated"] += 1
            else:
                # Add new front matter
                new_content = f'---\n{yaml_content}\n---\n\n{content}'
                self.stats["metadata_added"] += 1
            
            # Create backup
            backup_path = BACKUP_DIR / "metadata_integrator" / markdown_path.parent.name
            backup_path.mkdir(parents=True, exist_ok=True)
            shutil.copy2(markdown_path, backup_path / markdown_path.name)
            
            # Write updated content
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"Integrated metadata for: {cite_key}")
            self.stats["papers_processed"] += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Error integrating metadata for {cite_key}: {e}")
            self.stats["failed"] += 1
            return False
    
    def _build_yaml_frontmatter(self, cite_key: str, research_data: Dict, 
                               paper_info: Dict) -> str:
        """Build YAML front matter content"""
        yaml_lines = []
        
        # Core metadata
        yaml_lines.append(f'cite_key: "{cite_key}"')
        
        if research_data.get("Paper Title"):
            yaml_lines.append(f'title: "{self._escape_yaml(research_data["Paper Title"])}"')
        elif paper_info.get("metadata", {}).get("title"):
            yaml_lines.append(f'title: "{self._escape_yaml(paper_info["metadata"]["title"])}"')
        
        if research_data.get("Authors"):
            yaml_lines.append(f'authors: "{self._escape_yaml(research_data["Authors"])}"')
        elif paper_info.get("metadata", {}).get("authors"):
            yaml_lines.append(f'authors: "{self._escape_yaml(paper_info["metadata"]["authors"])}"')
        
        if research_data.get("Year"):
            yaml_lines.append(f'year: {research_data["Year"]}')
        elif paper_info.get("metadata", {}).get("year"):
            yaml_lines.append(f'year: {paper_info["metadata"]["year"]}')
        
        # Additional research table data
        if research_data.get("DOI"):
            yaml_lines.append(f'doi: "{research_data["DOI"]}"')
        elif paper_info.get("metadata", {}).get("doi"):
            yaml_lines.append(f'doi: "{paper_info["metadata"]["doi"]}"')
        
        if research_data.get("url"):
            yaml_lines.append(f'url: "{research_data["url"]}"')
        
        if research_data.get("Relevancy"):
            yaml_lines.append(f'relevancy: "{research_data["Relevancy"]}"')
        
        if research_data.get("Tags"):
            tags = [tag.strip() for tag in research_data["Tags"].split(",") if tag.strip()]
            if tags:
                yaml_lines.append("tags:")
                for tag in tags:
                    yaml_lines.append(f'  - "{self._escape_yaml(tag)}"')
        
        # Processing metadata
        yaml_lines.append(f'processed_date: "{datetime.now().isoformat()}"')
        yaml_lines.append(f'phase2_version: "1.0"')
        
        # Statistics
        if paper_info.get("images"):
            yaml_lines.append("image_stats:")
            yaml_lines.append(f'  total: {len(paper_info["images"].get("keep", [])) + len(paper_info["images"].get("remove", []))}')
            yaml_lines.append(f'  kept: {len(paper_info["images"].get("keep", []))}')
            yaml_lines.append(f'  removed: {len(paper_info["images"].get("remove", []))}')
        
        return "\n".join(yaml_lines)
    
    def _escape_yaml(self, text: str) -> str:
        """Escape special characters for YAML"""
        if not text:
            return ""
        # Escape double quotes and backslashes
        text = text.replace('\\', '\\\\').replace('"', '\\"')
        return text


def main():
    """Main function to integrate metadata"""
    logger = setup_logging("metadata_integrator")
    logger.info("Starting metadata integration")
    
    # Load research table
    logger.info("Loading research table...")
    headers, rows = parse_markdown_table(RESEARCH_TABLE)
    
    # Create lookup by title
    research_lookup = {}
    for row in rows:
        if row.get("Paper Title"):
            research_lookup[row["Paper Title"]] = row
    
    # Load paper analysis
    mapping_file = Path("cite_key_mapping.json")
    if not mapping_file.exists():
        logger.error("cite_key_mapping.json not found. Run paper_analyzer.py first.")
        return
    
    paper_mapping = read_json(mapping_file)
    papers = paper_mapping.get("papers", {})
    
    # Initialize integrator
    integrator = MetadataIntegrator(logger)
    
    # Process papers
    papers_to_process = list(papers.items())
    if TEST_MODE:
        papers_to_process = papers_to_process[:TEST_PAPERS]
        logger.info(f"Test mode: Processing only {TEST_PAPERS} papers")
    
    logger.info(f"Processing {len(papers_to_process)} papers...")
    
    for folder_name, paper_info in papers_to_process:
        markdown_path = MARKDOWN_PAPERS / folder_name / paper_info["markdown_file"]
        cite_key = paper_info["cite_key"]
        
        if not markdown_path.exists():
            logger.warning(f"Markdown file not found: {markdown_path}")
            continue
        
        # Find matching research table entry
        research_data = {}
        paper_title = paper_info.get("metadata", {}).get("title")
        if paper_title and paper_title in research_lookup:
            research_data = research_lookup[paper_title]
            logger.debug(f"Found research table match for: {cite_key}")
        
        # Integrate metadata
        integrator.integrate_metadata(markdown_path, cite_key, research_data, paper_info)
    
    # Log summary
    logger.info("\nMetadata Integration Summary:")
    logger.info(f"Papers processed: {integrator.stats['papers_processed']}")
    logger.info(f"New metadata added: {integrator.stats['metadata_added']}")
    logger.info(f"Metadata updated: {integrator.stats['metadata_updated']}")
    logger.info(f"Failed: {integrator.stats['failed']}")
    
    # Save stats
    stats_file = OUTPUT_DIR / "metadata_integration_stats.json"
    write_json(integrator.stats, stats_file)
    logger.info(f"Stats saved to: {stats_file}")


if __name__ == "__main__":
    main()
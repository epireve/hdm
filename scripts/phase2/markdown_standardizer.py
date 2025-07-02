"""
Standardizes markdown files by fixing headers, removing unwanted images, and cleaning formatting
"""
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    MARKDOWN_PAPERS, OUTPUT_DIR, TEST_MODE, TEST_PAPERS,
    REMOVE_IMAGE_PATTERNS, BACKUP_DIR
)
from utils import (
    setup_logging, read_json, write_json,
    parse_markdown_content, should_remove_image
)


class MarkdownStandardizer:
    """Handles markdown standardization tasks"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "papers_processed": 0,
            "headers_fixed": 0,
            "images_removed": 0,
            "formatting_cleaned": 0
        }
    
    def standardize_paper(self, markdown_path: Path, paper_info: Dict) -> bool:
        """Standardize a single markdown paper"""
        try:
            # Read markdown content
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix headers
            content = self._fix_headers(content)
            
            # Remove unwanted images
            content, images_removed = self._remove_unwanted_images(content, paper_info)
            self.stats["images_removed"] += images_removed
            
            # Clean formatting
            content = self._clean_formatting(content)
            
            # Write back if changed
            if content != original_content:
                # Create backup
                backup_path = BACKUP_DIR / "standardizer" / markdown_path.parent.name
                backup_path.mkdir(parents=True, exist_ok=True)
                shutil.copy2(markdown_path, backup_path / markdown_path.name)
                
                # Write standardized content
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.logger.info(f"Standardized: {markdown_path.name}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error standardizing {markdown_path}: {e}")
            return False
    
    def _fix_headers(self, content: str) -> str:
        """Fix header hierarchy and consistency"""
        lines = content.split('\n')
        fixed_lines = []
        header_stack = []
        headers_fixed = 0
        
        for line in lines:
            # Check if it's a header
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                
                # Clean up title
                title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
                title = re.sub(r'^[0-9]+\.\s*', '', title)  # Remove numbering
                
                # Fix header level based on hierarchy
                if not header_stack:
                    # First header should be H1
                    level = 1
                else:
                    # Ensure proper hierarchy
                    last_level = header_stack[-1][0]
                    if level > last_level + 1:
                        level = last_level + 1
                        headers_fixed += 1
                
                # Update header stack
                while header_stack and header_stack[-1][0] >= level:
                    header_stack.pop()
                header_stack.append((level, title))
                
                # Create fixed header
                fixed_line = f"{'#' * level} {title}"
                fixed_lines.append(fixed_line)
                
                if fixed_line != line:
                    headers_fixed += 1
            else:
                fixed_lines.append(line)
        
        self.stats["headers_fixed"] += headers_fixed
        return '\n'.join(fixed_lines)
    
    def _remove_unwanted_images(self, content: str, paper_info: Dict) -> Tuple[str, int]:
        """Remove images marked for removal"""
        images_to_remove = paper_info.get("images", {}).get("remove", [])
        if not images_to_remove:
            return content, 0
        
        removed_count = 0
        lines = content.split('\n')
        filtered_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            # Check if line contains an image to remove
            should_skip = False
            for img in images_to_remove:
                if img in line and re.search(r'!\[.*?\]\(.*?' + re.escape(img) + r'.*?\)', line):
                    should_skip = True
                    removed_count += 1
                    self.logger.debug(f"Removing image: {img}")
                    
                    # Also skip the next line if it's just a caption or empty
                    if i + 1 < len(lines) and (not lines[i + 1].strip() or 
                                               lines[i + 1].strip().startswith('*') or
                                               lines[i + 1].strip().startswith('_')):
                        skip_next = True
                    break
            
            if skip_next:
                skip_next = False
                continue
                
            if not should_skip:
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines), removed_count
    
    def _clean_formatting(self, content: str) -> str:
        """Clean up general formatting issues"""
        # Remove multiple consecutive blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Fix spacing around headers
        content = re.sub(r'(\n#{1,6}\s+[^\n]+)\n([^\n])', r'\1\n\n\2', content)
        content = re.sub(r'([^\n])\n(#{1,6}\s+)', r'\1\n\n\2', content)
        
        # Remove trailing whitespace
        lines = content.split('\n')
        lines = [line.rstrip() for line in lines]
        content = '\n'.join(lines)
        
        # Ensure file ends with single newline
        content = content.rstrip() + '\n'
        
        self.stats["formatting_cleaned"] += 1
        
        return content


def main():
    """Main function to standardize markdown papers"""
    logger = setup_logging("markdown_standardizer")
    logger.info("Starting markdown standardization")
    
    # Load paper analysis
    mapping_file = Path("cite_key_mapping.json")
    if not mapping_file.exists():
        logger.error("cite_key_mapping.json not found. Run paper_analyzer.py first.")
        return
    
    paper_mapping = read_json(mapping_file)
    papers = paper_mapping.get("papers", {})
    
    # Initialize standardizer
    standardizer = MarkdownStandardizer(logger)
    
    # Process papers
    papers_to_process = list(papers.items())
    if TEST_MODE:
        papers_to_process = papers_to_process[:TEST_PAPERS]
        logger.info(f"Test mode: Processing only {TEST_PAPERS} papers")
    
    logger.info(f"Processing {len(papers_to_process)} papers...")
    
    for folder_name, paper_info in papers_to_process:
        markdown_path = MARKDOWN_PAPERS / folder_name / paper_info["markdown_file"]
        
        if not markdown_path.exists():
            logger.warning(f"Markdown file not found: {markdown_path}")
            continue
        
        if standardizer.standardize_paper(markdown_path, paper_info):
            standardizer.stats["papers_processed"] += 1
    
    # Log summary
    logger.info("\nStandardization Summary:")
    logger.info(f"Papers processed: {standardizer.stats['papers_processed']}")
    logger.info(f"Headers fixed: {standardizer.stats['headers_fixed']}")
    logger.info(f"Images removed: {standardizer.stats['images_removed']}")
    logger.info(f"Formatting cleaned: {standardizer.stats['formatting_cleaned']}")
    
    # Save stats
    stats_file = OUTPUT_DIR / "standardization_stats.json"
    write_json(standardizer.stats, stats_file)
    logger.info(f"Stats saved to: {stats_file}")


if __name__ == "__main__":
    main()
"""
Standardizes markdown files using cite key mappings from CSV
CSV version of markdown_standardizer.py
"""
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import shutil
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    MARKDOWN_DIR, CITE_KEY_MAPPING_FILE, TEST_MODE, TEST_PAPERS,
    REMOVE_IMAGE_PATTERNS, BACKUP_DIR
)
from utils import (
    setup_logging, load_json,
    should_remove_image, ProgressTracker
)

# Check for environment override
EFFECTIVE_TEST_MODE = TEST_MODE
if os.environ.get('PHASE2_TEST_MODE', '').lower() == 'false':
    EFFECTIVE_TEST_MODE = False


class MarkdownStandardizer:
    """Handles markdown standardization tasks"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "papers_processed": 0,
            "headers_fixed": 0,
            "images_removed": 0,
            "formatting_cleaned": 0,
            "papers_modified": 0
        }
    
    def standardize_paper(self, markdown_path: Path, paper_info: Dict) -> bool:
        """Standardize a single markdown paper"""
        try:
            # Read markdown content
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix headers
            content, headers_fixed = self._fix_headers(content)
            self.stats["headers_fixed"] += headers_fixed
            
            # Remove unwanted images
            content, images_removed = self._remove_unwanted_images(content, paper_info)
            self.stats["images_removed"] += images_removed
            
            # Clean formatting
            content = self._clean_formatting(content)
            
            # Add cite key comment at the top if not present
            cite_key = paper_info.get('cite_key', '')
            if cite_key and f"<!-- cite_key: {cite_key} -->" not in content:
                content = f"<!-- cite_key: {cite_key} -->\n\n{content}"
            
            # Write back if changed
            if content != original_content:
                # Create backup
                backup_path = BACKUP_DIR / "standardizer" / markdown_path.parent.name
                backup_path.mkdir(parents=True, exist_ok=True)
                backup_file = backup_path / f"{markdown_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                shutil.copy2(markdown_path, backup_file)
                
                # Write standardized content
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.logger.info(f"Standardized: {markdown_path.parent.name}/{markdown_path.name}")
                self.stats["papers_modified"] += 1
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error standardizing {markdown_path}: {e}")
            return False
    
    def _fix_headers(self, content: str) -> Tuple[str, int]:
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
                title = re.sub(r'\*{2,}', '', title)  # Remove excessive asterisks
                
                # Fix header level based on hierarchy
                if not header_stack:
                    # First header should be H1
                    if level != 1:
                        level = 1
                        headers_fixed += 1
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
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines), headers_fixed
    
    def _remove_unwanted_images(self, content: str, paper_info: Dict) -> Tuple[str, int]:
        """Remove unwanted images based on patterns"""
        images_to_remove = paper_info.get('images', {}).get('remove', [])
        images_removed = 0
        
        for image_path in images_to_remove:
            # Escape special regex characters in image path
            escaped_path = re.escape(image_path)
            # Match image markdown syntax
            pattern = rf'!\[[^\]]*\]\({escaped_path}\)'
            
            # Remove the image
            new_content = re.sub(pattern, '', content)
            if new_content != content:
                images_removed += 1
                content = new_content
        
        # Also remove images matching remove patterns
        image_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            if should_remove_image(image_path, REMOVE_IMAGE_PATTERNS):
                nonlocal images_removed
                images_removed += 1
                return ''  # Remove the image
            else:
                return match.group(0)  # Keep the image
        
        content = re.sub(image_pattern, replace_image, content)
        
        return content, images_removed
    
    def _clean_formatting(self, content: str) -> str:
        """Clean up formatting issues"""
        # Remove multiple consecutive blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Remove trailing whitespace
        lines = content.split('\n')
        lines = [line.rstrip() for line in lines]
        content = '\n'.join(lines)
        
        # Ensure file ends with single newline
        content = content.rstrip() + '\n'
        
        # Fix common markdown issues
        # Fix bold text
        content = re.sub(r'\*\*\s+([^\*]+)\s+\*\*', r'**\1**', content)
        
        # Fix italic text
        content = re.sub(r'\*\s+([^\*]+)\s+\*', r'*\1*', content)
        
        # Fix code blocks with missing language
        content = re.sub(r'```\n', '```text\n', content)
        
        # Remove page numbers and footers
        content = re.sub(r'^Page \d+ of \d+$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\d+$', '', content, flags=re.MULTILINE)
        
        self.stats["formatting_cleaned"] += 1
        
        return content


def main():
    """Main function to standardize markdown files"""
    logger = setup_logging("markdown_standardizer_csv")
    logger.info("Starting markdown standardization with CSV data")
    
    # Check if cite key mapping exists
    if not CITE_KEY_MAPPING_FILE.exists():
        logger.error(f"Cite key mapping not found at: {CITE_KEY_MAPPING_FILE}")
        logger.info("Please run paper_analyzer_csv.py first")
        return 1
    
    # Load cite key mapping
    logger.info("Loading cite key mappings...")
    mapping_data = load_json(CITE_KEY_MAPPING_FILE)
    papers_info = mapping_data.get('papers', {})
    
    if not papers_info:
        logger.error("No papers found in cite key mapping")
        return 1
    
    logger.info(f"Found {len(papers_info)} papers to process")
    
    # Initialize standardizer
    standardizer = MarkdownStandardizer(logger)
    
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
        
        # Get markdown file path
        paper_dir = MARKDOWN_DIR / folder_name
        if not paper_dir.exists():
            logger.warning(f"Paper directory not found: {paper_dir}")
            continue
        
        markdown_file = paper_dir / paper_info.get('markdown_file', '')
        if not markdown_file.exists():
            # Try to find any markdown file
            md_files = list(paper_dir.glob('*.md'))
            if md_files:
                markdown_file = md_files[0]
            else:
                logger.warning(f"No markdown file found in: {paper_dir}")
                continue
        
        # Standardize the paper
        progress.update(f"Standardizing {folder_name}")
        if standardizer.standardize_paper(markdown_file, paper_info):
            standardizer.stats["papers_processed"] += 1
        
        processed += 1
    
    # Print summary
    stats = standardizer.stats
    logger.info("\n" + "="*50)
    logger.info("STANDARDIZATION SUMMARY")
    logger.info("="*50)
    logger.info(f"Papers processed: {stats['papers_processed']}")
    logger.info(f"Papers modified: {stats['papers_modified']}")
    logger.info(f"Headers fixed: {stats['headers_fixed']}")
    logger.info(f"Images removed: {stats['images_removed']}")
    logger.info(f"Formatting cleaned: {stats['formatting_cleaned']}")
    logger.info("="*50)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
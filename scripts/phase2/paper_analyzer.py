"""
Analyzes papers and generates cite key mappings
"""
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    MARKDOWN_DIR, RESEARCH_TABLE, CITE_KEY_MAPPING_FILE,
    REMOVE_IMAGE_PATTERNS, KEEP_IMAGE_PATTERNS,
    TEST_MODE, TEST_PAPERS
)
from utils import (
    setup_logging, save_json, parse_markdown_table,
    extract_metadata_from_markdown, extract_author_year,
    generate_cite_key, ProgressTracker
)


def analyze_images(markdown_file: Path) -> Tuple[List[str], List[str]]:
    """Analyze images in a markdown file and categorize them"""
    images_to_remove = []
    images_to_keep = []
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all image references
    image_pattern = r'!\[.*?\]\((.+?)\)'
    images = re.findall(image_pattern, content)
    
    for image in images:
        image_path = Path(image)
        should_remove = False
        should_keep = False
        
        # Check against remove patterns
        for pattern in REMOVE_IMAGE_PATTERNS:
            if image_path.match(pattern):
                should_remove = True
                break
        
        # Check against keep patterns
        if not should_remove:
            for pattern in KEEP_IMAGE_PATTERNS:
                if image_path.match(pattern):
                    should_keep = True
                    break
        
        if should_remove:
            images_to_remove.append(image)
        elif should_keep or not should_remove:
            images_to_keep.append(image)
    
    return images_to_keep, images_to_remove


def main():
    """Main function to analyze papers"""
    logger = setup_logging("paper_analyzer")
    logger.info("Starting paper analysis")
    
    # Parse research table if it exists
    research_table_data = {}
    if RESEARCH_TABLE.exists():
        logger.info("Loading research table...")
        headers, rows = parse_markdown_table(RESEARCH_TABLE)
        
        # Create lookup by title
        for row in rows:
            title = row.get("Paper Title", "").strip()
            if title:
                research_table_data[title.lower()] = row
    
    # Get all markdown papers
    paper_dirs = sorted([d for d in MARKDOWN_DIR.iterdir() if d.is_dir()])
    logger.info(f"Found {len(paper_dirs)} paper directories")
    
    # Analysis results
    analysis_results = {
        "papers": {},
        "cite_key_mapping": {},
        "folder_mapping": {},  # old_folder -> new_folder
        "statistics": {
            "total_papers": 0,
            "papers_with_metadata": 0,
            "papers_matched_to_research_table": 0,
            "total_images": 0,
            "images_to_remove": 0,
            "images_to_keep": 0
        }
    }
    
    existing_keys: Set[str] = set()
    progress = ProgressTracker(len(paper_dirs), logger)
    
    # Analyze each paper
    for i, paper_dir in enumerate(paper_dirs):
        if TEST_MODE and i >= TEST_PAPERS:
            logger.info(f"Test mode: Stopping after {TEST_PAPERS} papers")
            break
        
        # Find markdown file
        md_files = list(paper_dir.glob("*.md"))
        if not md_files:
            logger.warning(f"No markdown file found in {paper_dir}")
            continue
        
        md_file = md_files[0]
        progress.update(f"Analyzing {paper_dir.name}")
        
        # Extract metadata from markdown
        metadata = extract_metadata_from_markdown(md_file)
        
        # Try to match with research table
        matched_row = None
        if metadata['title']:
            title_lower = metadata['title'].lower()
            # Try exact match first
            if title_lower in research_table_data:
                matched_row = research_table_data[title_lower]
            else:
                # Try partial match
                for rt_title, rt_row in research_table_data.items():
                    if title_lower in rt_title or rt_title in title_lower:
                        matched_row = rt_row
                        break
        
        # Get cite key
        cite_key = None
        if matched_row and "cite_key" in matched_row:
            # Use cite key from research table
            cite_key = matched_row["cite_key"]
            analysis_results["statistics"]["papers_matched_to_research_table"] += 1
        else:
            # Generate cite key from metadata
            if metadata['authors'] and metadata['year']:
                last_name, year = extract_author_year(metadata['authors'], metadata['year'])
                cite_key = generate_cite_key(last_name, year, existing_keys)
                existing_keys.add(cite_key)
            else:
                # Use folder name as fallback
                folder_name = paper_dir.name.replace("-", "_").replace(" ", "_")
                cite_key = re.sub(r'[^a-zA-Z0-9_]', '', folder_name).lower()[:30]
                if cite_key in existing_keys:
                    cite_key = f"{cite_key}_{i}"
                existing_keys.add(cite_key)
        
        # Analyze images
        images_to_keep, images_to_remove = analyze_images(md_file)
        
        # Store results
        paper_info = {
            "original_folder": paper_dir.name,
            "markdown_file": md_file.name,
            "cite_key": cite_key,
            "metadata": metadata,
            "matched_research_table": matched_row is not None,
            "images": {
                "keep": images_to_keep,
                "remove": images_to_remove
            }
        }
        
        analysis_results["papers"][paper_dir.name] = paper_info
        analysis_results["cite_key_mapping"][metadata.get('title', paper_dir.name)] = cite_key
        analysis_results["folder_mapping"][paper_dir.name] = cite_key
        
        # Update statistics
        analysis_results["statistics"]["total_papers"] += 1
        if metadata['title'] and metadata['authors'] and metadata['year']:
            analysis_results["statistics"]["papers_with_metadata"] += 1
        analysis_results["statistics"]["total_images"] += len(images_to_keep) + len(images_to_remove)
        analysis_results["statistics"]["images_to_remove"] += len(images_to_remove)
        analysis_results["statistics"]["images_to_keep"] += len(images_to_keep)
    
    # Save results
    logger.info(f"Saving analysis results to {CITE_KEY_MAPPING_FILE}")
    save_json(analysis_results, CITE_KEY_MAPPING_FILE)
    
    # Print summary
    stats = analysis_results["statistics"]
    logger.info("\n" + "="*50)
    logger.info("ANALYSIS SUMMARY")
    logger.info("="*50)
    logger.info(f"Total papers analyzed: {stats['total_papers']}")
    logger.info(f"Papers with complete metadata: {stats['papers_with_metadata']}")
    logger.info(f"Papers matched to research table: {stats['papers_matched_to_research_table']}")
    logger.info(f"Total images found: {stats['total_images']}")
    logger.info(f"Images to remove: {stats['images_to_remove']}")
    logger.info(f"Images to keep: {stats['images_to_keep']}")
    logger.info("="*50)
    
    # Show some examples
    logger.info("\nExample cite key mappings:")
    for i, (title, cite_key) in enumerate(list(analysis_results["cite_key_mapping"].items())[:5]):
        logger.info(f"  {cite_key}: {title[:60]}...")


if __name__ == "__main__":
    main()
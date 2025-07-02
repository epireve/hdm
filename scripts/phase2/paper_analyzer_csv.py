"""
Analyzes papers and generates cite key mappings using CSV data
CSV version of paper_analyzer.py
"""
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    MARKDOWN_DIR, RESEARCH_TABLE_CSV, CITE_KEY_MAPPING_FILE,
    REMOVE_IMAGE_PATTERNS, KEEP_IMAGE_PATTERNS,
    TEST_MODE, TEST_PAPERS
)
from csv_utils import read_csv_to_dict
from utils import (
    setup_logging, save_json,
    extract_metadata_from_markdown, extract_author_year,
    generate_cite_key, ProgressTracker, should_remove_image
)

# Check for environment override
EFFECTIVE_TEST_MODE = TEST_MODE
if os.environ.get('PHASE2_TEST_MODE', '').lower() == 'false':
    EFFECTIVE_TEST_MODE = False


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
        if should_remove_image(image, REMOVE_IMAGE_PATTERNS):
            images_to_remove.append(image)
        else:
            images_to_keep.append(image)
    
    return images_to_keep, images_to_remove


def normalize_title(title: str) -> str:
    """Normalize title for matching"""
    # Remove special characters and extra spaces
    title = re.sub(r'[^\w\s]', ' ', title.lower())
    title = ' '.join(title.split())
    return title


def main():
    """Main function to analyze papers"""
    logger = setup_logging("paper_analyzer_csv")
    logger.info("Starting paper analysis with CSV data")
    
    # Check if CSV exists
    if not RESEARCH_TABLE_CSV.exists():
        logger.error(f"Research table CSV not found at: {RESEARCH_TABLE_CSV}")
        logger.info("Please run convert_to_csv.py first")
        return 1
    
    # Load research table from CSV
    logger.info("Loading research table from CSV...")
    headers, rows = read_csv_to_dict(RESEARCH_TABLE_CSV)
    
    # Create lookup by title and cite_key
    research_table_by_title = {}
    research_table_by_cite_key = {}
    cite_keys_from_table = set()
    
    for row in rows:
        title = row.get("Paper Title", "").strip()
        cite_key = row.get("cite_key", "").strip()
        
        if title:
            # Store both original and normalized title
            research_table_by_title[title] = row
            research_table_by_title[normalize_title(title)] = row
        
        if cite_key:
            research_table_by_cite_key[cite_key] = row
            cite_keys_from_table.add(cite_key)
    
    logger.info(f"Loaded {len(rows)} papers from research table")
    logger.info(f"Found {len(cite_keys_from_table)} cite keys in research table")
    
    # Get all markdown papers
    paper_dirs = sorted([d for d in MARKDOWN_DIR.iterdir() if d.is_dir()])
    logger.info(f"Found {len(paper_dirs)} paper directories")
    
    # Analysis results
    analysis_results = {
        "papers": {},
        "cite_key_mapping": {},
        "folder_mapping": {},  # old_folder -> new_folder (cite_key)
        "statistics": {
            "total_papers": 0,
            "papers_with_metadata": 0,
            "papers_matched_to_research_table": 0,
            "papers_using_table_cite_key": 0,
            "total_images": 0,
            "images_to_remove": 0,
            "images_to_keep": 0
        }
    }
    
    existing_keys: Set[str] = cite_keys_from_table.copy()
    progress = ProgressTracker(len(paper_dirs), logger)
    
    # Process limit based on mode
    process_limit = TEST_PAPERS if EFFECTIVE_TEST_MODE else len(paper_dirs)
    
    # Analyze each paper
    for i, paper_dir in enumerate(paper_dirs):
        if i >= process_limit:
            logger.info(f"{'Test' if EFFECTIVE_TEST_MODE else 'Full'} mode: Processed {i} papers")
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
        cite_key = None
        
        # First try to match by title
        if metadata['title']:
            # Try exact match
            if metadata['title'] in research_table_by_title:
                matched_row = research_table_by_title[metadata['title']]
            # Try normalized match
            elif normalize_title(metadata['title']) in research_table_by_title:
                matched_row = research_table_by_title[normalize_title(metadata['title'])]
            # Try partial match on original titles
            else:
                for rt_title, rt_row in research_table_by_title.items():
                    if not isinstance(rt_title, str):
                        continue
                    if (metadata['title'].lower() in rt_title.lower() or 
                        rt_title.lower() in metadata['title'].lower()):
                        matched_row = rt_row
                        break
        
        # If matched, use cite key from table
        if matched_row and matched_row.get("cite_key"):
            cite_key = matched_row["cite_key"]
            analysis_results["statistics"]["papers_matched_to_research_table"] += 1
            analysis_results["statistics"]["papers_using_table_cite_key"] += 1
            logger.debug(f"Matched '{metadata.get('title', 'Unknown')[:50]}...' to cite_key: {cite_key}")
        else:
            # Generate new cite key
            if metadata['authors'] and metadata['year']:
                last_name, year = extract_author_year(metadata['authors'], metadata['year'])
                cite_key = generate_cite_key(last_name, year, existing_keys)
            else:
                # Use folder name as fallback
                folder_name = paper_dir.name.replace("-", "_").replace(" ", "_")
                cite_key = re.sub(r'[^a-zA-Z0-9_]', '', folder_name).lower()[:30]
                if cite_key in existing_keys:
                    cite_key = f"{cite_key}_{i}"
            
            existing_keys.add(cite_key)
            if metadata and metadata.get('title'):
                title_for_log = metadata['title']
            else:
                title_for_log = paper_dir.name
            logger.debug(f"Generated new cite_key '{cite_key}' for '{title_for_log[:50]}...'")
        
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
        
        # Use title from metadata or folder name for mapping
        mapping_key = metadata.get('title', paper_dir.name) if metadata and metadata.get('title') else paper_dir.name
        analysis_results["cite_key_mapping"][mapping_key] = cite_key
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
    logger.info(f"Papers using cite keys from table: {stats['papers_using_table_cite_key']}")
    logger.info(f"Total images found: {stats['total_images']}")
    logger.info(f"Images to remove: {stats['images_to_remove']}")
    logger.info(f"Images to keep: {stats['images_to_keep']}")
    logger.info("="*50)
    
    # Show some examples
    logger.info("\nExample cite key mappings:")
    example_count = min(10, len(analysis_results["cite_key_mapping"]))
    for i, (title, cite_key) in enumerate(list(analysis_results["cite_key_mapping"].items())[:example_count]):
        logger.info(f"  {cite_key}: {title[:60]}...")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
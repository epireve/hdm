"""
Updates research_table.md with cite_key column
"""
import sys
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import RESEARCH_TABLE, UPDATED_RESEARCH_TABLE, TEST_MODE, TEST_PAPERS, BACKUP_DIR
from utils import (
    setup_logging, parse_markdown_table, 
    write_markdown_table, extract_author_year, generate_cite_key
)


def main():
    """Main function to update research table with cite keys"""
    logger = setup_logging("research_table_updater")
    logger.info("Starting research table update with cite_key column")
    
    # Create backup
    if RESEARCH_TABLE.exists():
        # Just backup the research table file, not the entire directory
        backup_dir = BACKUP_DIR / "research_table_backup"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / f"research_table_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        import shutil
        shutil.copy2(RESEARCH_TABLE, backup_file)
        logger.info(f"Created backup at: {backup_file}")
    else:
        logger.error(f"Research table not found at: {RESEARCH_TABLE}")
        return
    
    # Parse existing table
    logger.info("Parsing research table...")
    headers, rows = parse_markdown_table(RESEARCH_TABLE)
    logger.info(f"Found {len(rows)} papers in research table")
    
    # Check if cite_key column already exists
    if "cite_key" in headers:
        logger.info("cite_key column already exists in research table")
        return
    
    # Insert cite_key as second column
    headers.insert(1, "cite_key")
    
    # Generate cite keys
    logger.info("Generating cite keys...")
    existing_keys: Set[str] = set()
    
    # Process rows
    for i, row in enumerate(rows):
        if TEST_MODE and i >= TEST_PAPERS:
            logger.info(f"Test mode: Stopping after {TEST_PAPERS} papers")
            break
        
        # Extract author and year
        authors = row.get("Authors", "")
        year = row.get("Year", "")
        
        if not authors:
            logger.warning(f"No authors for paper: {row.get('Paper Title', 'Unknown')}")
            last_name = "unknown"
        else:
            last_name, year = extract_author_year(authors, year)
        
        # Generate unique cite key
        cite_key = generate_cite_key(last_name, year, existing_keys)
        existing_keys.add(cite_key)
        
        # Add cite key to row
        row["cite_key"] = cite_key
        
        logger.debug(f"Generated cite_key '{cite_key}' for '{row.get('Paper Title', 'Unknown')[:50]}...'")
    
    # Write updated table
    output_file = UPDATED_RESEARCH_TABLE if TEST_MODE else RESEARCH_TABLE
    logger.info(f"Writing updated table to: {output_file}")
    write_markdown_table(headers, rows, output_file)
    
    logger.info(f"Successfully updated research table with {len(rows)} cite keys")
    
    # Print summary
    logger.info("\nSummary of cite keys generated:")
    logger.info(f"Total papers: {len(rows)}")
    logger.info(f"Unique cite keys: {len(existing_keys)}")
    
    # Show some examples
    num_examples = min(10, len([r for r in rows if 'cite_key' in r]))
    logger.info(f"\nFirst {num_examples} cite keys:")
    for i, row in enumerate(rows[:num_examples]):
        if 'cite_key' in row:
            logger.info(f"  {row['cite_key']}: {row.get('Paper Title', 'Unknown')[:60]}...")


if __name__ == "__main__":
    main()
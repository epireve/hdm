"""
Updates research_table.csv with cite_key column
CSV version of research_table_updater.py
"""
import sys
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

import os
from config import (
    RESEARCH_TABLE_CSV, UPDATED_RESEARCH_TABLE_CSV, 
    TEST_MODE, TEST_PAPERS, BACKUP_DIR
)

# Check for environment override
EFFECTIVE_TEST_MODE = TEST_MODE
if os.environ.get('PHASE2_TEST_MODE', '').lower() == 'false':
    EFFECTIVE_TEST_MODE = False
from csv_utils import read_csv_to_dict, write_dict_to_csv, validate_csv_integrity
from utils import (
    setup_logging, extract_author_year, generate_cite_key
)


def main():
    """Main function to update research table CSV with cite keys"""
    logger = setup_logging("research_table_updater_csv")
    logger.info("Starting research table CSV update with cite_key column")
    
    # Check if CSV exists
    if not RESEARCH_TABLE_CSV.exists():
        logger.error(f"Research table CSV not found at: {RESEARCH_TABLE_CSV}")
        logger.info("Please run convert_to_csv.py first to convert markdown table to CSV")
        return 1
    
    # Create backup
    backup_dir = BACKUP_DIR / "csv_backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_file = backup_dir / f"research_table_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    shutil.copy2(RESEARCH_TABLE_CSV, backup_file)
    logger.info(f"Created backup at: {backup_file}")
    
    # Read CSV
    logger.info("Reading research table CSV...")
    headers, rows = read_csv_to_dict(RESEARCH_TABLE_CSV)
    logger.info(f"Found {len(rows)} papers in research table")
    
    # Check if cite_key column already exists
    if "cite_key" in headers:
        logger.info("cite_key column already exists in research table")
        # Check if any rows are missing cite keys
        missing_keys = [i for i, row in enumerate(rows) if not row.get("cite_key")]
        if not missing_keys:
            logger.info("All papers already have cite keys")
            return 0
        else:
            logger.info(f"Found {len(missing_keys)} papers without cite keys")
    else:
        # Insert cite_key as second column
        headers.insert(1, "cite_key")
        logger.info("Added cite_key column to headers")
    
    # Generate cite keys
    logger.info("Generating cite keys...")
    existing_keys: Set[str] = set()
    
    # First pass: collect existing cite keys
    for row in rows:
        if row.get("cite_key"):
            existing_keys.add(row["cite_key"])
    
    # Second pass: generate missing cite keys
    processed_count = 0
    for i, row in enumerate(rows):
        if EFFECTIVE_TEST_MODE and processed_count >= TEST_PAPERS:
            logger.info(f"Test mode: Stopping after {TEST_PAPERS} papers")
            break
        
        # Skip if already has cite key
        if row.get("cite_key"):
            continue
        
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
        processed_count += 1
        
        logger.debug(f"Generated cite_key '{cite_key}' for '{row.get('Paper Title', 'Unknown')[:50]}...'")
    
    # Write updated CSV
    output_file = UPDATED_RESEARCH_TABLE_CSV if EFFECTIVE_TEST_MODE else RESEARCH_TABLE_CSV
    logger.info(f"Writing updated CSV to: {output_file}")
    write_dict_to_csv(headers, rows, output_file)
    
    # Validate the output
    if validate_csv_integrity(output_file):
        logger.info("CSV validation passed")
    else:
        logger.error("CSV validation failed")
        return 1
    
    logger.info(f"Successfully updated research table with cite keys")
    
    # Print summary
    logger.info("\nSummary:")
    logger.info(f"Total papers: {len(rows)}")
    logger.info(f"Papers with cite keys: {len([r for r in rows if r.get('cite_key')])}")
    logger.info(f"Unique cite keys: {len(existing_keys)}")
    
    # Show some examples
    examples = [r for r in rows if r.get('cite_key')][:10]
    if examples:
        logger.info(f"\nFirst {len(examples)} cite keys:")
        for row in examples:
            logger.info(f"  {row['cite_key']}: {row.get('Paper Title', 'Unknown')[:60]}...")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
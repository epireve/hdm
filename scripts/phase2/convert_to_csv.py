#!/usr/bin/env python3
"""
Convert research_table.md to CSV format
This is a one-time conversion script
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import RESEARCH_TABLE, RESEARCH_TABLE_CSV, BACKUP_DIR
from csv_utils import markdown_table_to_csv, validate_csv_integrity
from utils import setup_logging


def main():
    """Convert markdown table to CSV"""
    logger = setup_logging("convert_to_csv")
    
    logger.info("Starting conversion of research_table.md to CSV format")
    
    # Check if markdown file exists
    if not RESEARCH_TABLE.exists():
        logger.error(f"Research table not found at: {RESEARCH_TABLE}")
        return 1
    
    # Create backup
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"research_table_backup_{timestamp}.md"
    
    import shutil
    shutil.copy2(RESEARCH_TABLE, backup_file)
    logger.info(f"Created backup at: {backup_file}")
    
    # Check if CSV already exists
    if RESEARCH_TABLE_CSV.exists():
        logger.warning(f"CSV file already exists at: {RESEARCH_TABLE_CSV}")
        response = input("Overwrite existing CSV? (y/n): ")
        if response.lower() != 'y':
            logger.info("Conversion cancelled by user")
            return 0
    
    # Convert to CSV
    try:
        row_count = markdown_table_to_csv(RESEARCH_TABLE, RESEARCH_TABLE_CSV)
        logger.info(f"Successfully converted {row_count} rows to CSV")
        
        # Validate the CSV
        if validate_csv_integrity(RESEARCH_TABLE_CSV):
            logger.info("CSV validation passed")
            
            # Show file sizes
            md_size = RESEARCH_TABLE.stat().st_size / 1024
            csv_size = RESEARCH_TABLE_CSV.stat().st_size / 1024
            logger.info(f"File sizes: MD={md_size:.1f}KB, CSV={csv_size:.1f}KB")
            
            return 0
        else:
            logger.error("CSV validation failed")
            return 1
            
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
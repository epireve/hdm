"""
CSV utilities for Phase 2 processing
Handles conversion between markdown tables and CSV format
"""
import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import logging

sys.path.append(str(Path(__file__).parent))
from utils import parse_markdown_table


def markdown_table_to_csv(markdown_file: Path, csv_file: Path) -> int:
    """Convert markdown table to CSV format"""
    logger = logging.getLogger(__name__)
    
    # Parse markdown table
    headers, rows = parse_markdown_table(markdown_file)
    
    if not headers or not rows:
        logger.error(f"No data found in {markdown_file}")
        return 0
    
    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        
        for row in rows:
            # Clean up row data - remove extra whitespace, handle multiline
            cleaned_row = {}
            for key, value in row.items():
                if value:
                    # Replace multiple spaces with single space
                    value = ' '.join(value.split())
                cleaned_row[key] = value
            writer.writerow(cleaned_row)
    
    logger.info(f"Converted {len(rows)} rows from {markdown_file} to {csv_file}")
    return len(rows)


def read_csv_to_dict(csv_file: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    """Read CSV file and return headers and rows as dictionaries"""
    headers = []
    rows = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)
    
    return headers, rows


def write_dict_to_csv(headers: List[str], rows: List[Dict[str, str]], csv_file: Path) -> None:
    """Write dictionary data to CSV file"""
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def append_to_csv(row: Dict[str, str], csv_file: Path) -> None:
    """Append a single row to CSV file"""
    # Check if file exists and get headers
    file_exists = csv_file.exists()
    
    if file_exists:
        # Read headers from existing file
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
    else:
        # Use keys from row as headers
        headers = list(row.keys())
    
    # Append the row
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(row)


def validate_csv_integrity(csv_file: Path) -> bool:
    """Validate CSV file integrity"""
    logger = logging.getLogger(__name__)
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            if not headers:
                logger.error(f"No headers found in {csv_file}")
                return False
            
            row_count = 0
            for i, row in enumerate(reader):
                row_count += 1
                # Check if all headers have values (even if empty)
                for header in headers:
                    if header not in row:
                        logger.error(f"Row {i+1} missing column '{header}'")
                        return False
            
            logger.info(f"CSV validation passed: {row_count} rows, {len(headers)} columns")
            return True
            
    except Exception as e:
        logger.error(f"CSV validation failed: {e}")
        return False


def merge_csv_files(file1: Path, file2: Path, output_file: Path, key_column: str) -> None:
    """Merge two CSV files based on a key column"""
    logger = logging.getLogger(__name__)
    
    # Read both files
    headers1, rows1 = read_csv_to_dict(file1)
    headers2, rows2 = read_csv_to_dict(file2)
    
    # Create lookup dictionary from second file
    lookup = {row[key_column]: row for row in rows2 if key_column in row}
    
    # Merge headers (avoiding duplicates)
    merged_headers = headers1.copy()
    for header in headers2:
        if header not in merged_headers and header != key_column:
            merged_headers.append(header)
    
    # Merge rows
    merged_rows = []
    for row1 in rows1:
        if key_column in row1 and row1[key_column] in lookup:
            # Merge with data from file2
            row2 = lookup[row1[key_column]]
            merged_row = row1.copy()
            for key, value in row2.items():
                if key != key_column:
                    merged_row[key] = value
            merged_rows.append(merged_row)
        else:
            # Keep row from file1 as is
            merged_rows.append(row1)
    
    # Write merged data
    write_dict_to_csv(merged_headers, merged_rows, output_file)
    logger.info(f"Merged {len(merged_rows)} rows into {output_file}")
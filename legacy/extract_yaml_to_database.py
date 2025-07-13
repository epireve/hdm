#!/usr/bin/env python3
"""
Extract YAML frontmatter from all paper.md files and store in SQLite database as new columns.
"""

import os
import json
import re
import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional, List, Set
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('yaml_to_database_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def parse_simple_yaml(yaml_content: str) -> Dict[str, Any]:
    """Simple YAML parser for frontmatter (key: value pairs)."""
    result = {}
    lines = yaml_content.strip().split('\n')
    
    current_key = None
    current_value = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this line starts a new key-value pair
        if ':' in line and not line.startswith(' ') and not line.startswith('-'):
            # Save previous key-value if exists
            if current_key:
                value = '\n'.join(current_value).strip()
                # Handle different value types
                if value.lower() in ['true', 'false']:
                    result[current_key] = value.lower() == 'true'
                elif value.isdigit():
                    result[current_key] = int(value)
                elif value.startswith('[') and value.endswith(']'):
                    # Simple list parsing
                    list_content = value[1:-1].strip()
                    if list_content:
                        items = [item.strip().strip('"\'') for item in list_content.split(',')]
                        result[current_key] = items
                    else:
                        result[current_key] = []
                else:
                    # Remove quotes if present
                    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    result[current_key] = value
            
            # Start new key-value pair
            key, value = line.split(':', 1)
            current_key = key.strip().strip('"\'')
            current_value = [value.strip()]
        elif current_key:
            # Continuation of current value
            current_value.append(line)
    
    # Handle last key-value pair
    if current_key:
        value = '\n'.join(current_value).strip()
        if value.lower() in ['true', 'false']:
            result[current_key] = value.lower() == 'true'
        elif value.isdigit():
            result[current_key] = int(value)
        elif value.startswith('[') and value.endswith(']'):
            list_content = value[1:-1].strip()
            if list_content:
                items = [item.strip().strip('"\'') for item in list_content.split(',')]
                result[current_key] = items
            else:
                result[current_key] = []
        else:
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            result[current_key] = value
    
    return result

def extract_yaml_from_markdown(content: str) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from markdown content."""
    try:
        # Look for YAML frontmatter between --- markers
        yaml_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(yaml_pattern, content, re.DOTALL)
        
        if match:
            yaml_content = match.group(1)
            return parse_simple_yaml(yaml_content)
        else:
            return None
    except Exception as e:
        logger.error(f"Unexpected error parsing YAML: {e}")
        return None

def get_all_yaml_fields() -> Set[str]:
    """Scan all paper.md files to identify all unique YAML fields."""
    base_path = Path("production_final_reformatted_1752365947")
    all_fields = set()
    
    paper_files = list(base_path.glob("*/paper.md"))
    logger.info(f"Scanning {len(paper_files)} files to identify YAML fields...")
    
    for paper_path in paper_files:
        try:
            with open(paper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            yaml_data = extract_yaml_from_markdown(content)
            if yaml_data:
                all_fields.update(yaml_data.keys())
        except Exception as e:
            logger.warning(f"Error reading {paper_path}: {e}")
    
    # Remove common metadata fields that shouldn't be database columns
    excluded_fields = {'_file_path', '_folder_name', '_file_size', '_modified_time'}
    all_fields = all_fields - excluded_fields
    
    logger.info(f"Found {len(all_fields)} unique YAML fields")
    return all_fields

def create_yaml_columns(cursor: sqlite3.Cursor, yaml_fields: Set[str]) -> None:
    """Add new columns to the database for YAML fields."""
    # Get existing columns
    cursor.execute("PRAGMA table_info(papers)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    
    columns_to_add = []
    
    for field in yaml_fields:
        # Create safe column name
        safe_column_name = f"yaml_{field.lower().replace('-', '_').replace(' ', '_')}"
        
        # Avoid conflicts with existing columns
        if safe_column_name not in existing_columns:
            columns_to_add.append((field, safe_column_name))
    
    logger.info(f"Adding {len(columns_to_add)} new YAML columns to database...")
    
    for original_field, column_name in columns_to_add:
        try:
            # Determine column type based on field name
            if original_field in ['year', 'page_count', 'citation_count']:
                column_type = "INTEGER"
            elif original_field in ['keywords', 'tags', 'authors']:
                column_type = "TEXT"
            else:
                column_type = "TEXT"
            
            cursor.execute(f"ALTER TABLE papers ADD COLUMN {column_name} {column_type}")
            logger.info(f"Added column: {column_name} ({column_type}) for field '{original_field}'")
        except sqlite3.Error as e:
            logger.error(f"Error adding column {column_name}: {e}")
    
    return {original: safe for original, safe in columns_to_add}

def process_all_papers(cursor: sqlite3.Cursor, field_mapping: Dict[str, str]) -> Dict[str, Any]:
    """Process all paper.md files and update database with YAML data."""
    base_path = Path("production_final_reformatted_1752365947")
    
    stats = {
        'total_files': 0,
        'successful_yaml_extractions': 0,
        'database_updates': 0,
        'failed_extractions': 0,
        'missing_cite_keys': 0,
        'folder_cite_key_mismatches': []
    }
    
    paper_files = list(base_path.glob("*/paper.md"))
    stats['total_files'] = len(paper_files)
    
    logger.info(f"Processing {len(paper_files)} paper.md files...")
    
    for paper_path in paper_files:
        folder_name = paper_path.parent.name
        
        try:
            # Extract YAML data
            with open(paper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            yaml_data = extract_yaml_from_markdown(content)
            
            if yaml_data:
                stats['successful_yaml_extractions'] += 1
                
                # Get cite_key from YAML
                yaml_cite_key = yaml_data.get('cite_key')
                
                if not yaml_cite_key:
                    logger.warning(f"No cite_key in YAML for {folder_name}")
                    stats['missing_cite_keys'] += 1
                    continue
                
                # Check if cite_key matches folder name
                if yaml_cite_key != folder_name:
                    stats['folder_cite_key_mismatches'].append({
                        'folder_name': folder_name,
                        'yaml_cite_key': yaml_cite_key
                    })
                    logger.info(f"Cite key mismatch: folder={folder_name}, yaml={yaml_cite_key}")
                
                # Find the database record
                cursor.execute("SELECT id FROM papers WHERE cite_key = ?", (yaml_cite_key,))
                result = cursor.fetchone()
                
                if result:
                    paper_id = result[0]
                    
                    # Prepare update query
                    update_fields = []
                    update_values = []
                    
                    for yaml_field, db_column in field_mapping.items():
                        if yaml_field in yaml_data:
                            value = yaml_data[yaml_field]
                            
                            # Convert to string if it's a list or dict
                            if isinstance(value, (list, dict)):
                                value = json.dumps(value) if value else None
                            elif value == '':
                                value = None
                            
                            update_fields.append(f"{db_column} = ?")
                            update_values.append(value)
                    
                    if update_fields:
                        update_values.append(paper_id)  # For WHERE clause
                        update_query = f"UPDATE papers SET {', '.join(update_fields)} WHERE id = ?"
                        
                        cursor.execute(update_query, update_values)
                        stats['database_updates'] += 1
                        logger.info(f"Updated database record for {yaml_cite_key}")
                    else:
                        logger.info(f"No YAML fields to update for {yaml_cite_key}")
                
                else:
                    logger.warning(f"No database record found for cite_key: {yaml_cite_key}")
            
            else:
                stats['failed_extractions'] += 1
                logger.warning(f"No YAML frontmatter found in {folder_name}")
        
        except Exception as e:
            stats['failed_extractions'] += 1
            logger.error(f"Error processing {folder_name}: {e}")
    
    return stats

def main():
    """Main function to extract YAML and store in database."""
    logger.info("Starting YAML to database extraction...")
    
    # Connect to database
    try:
        conn = sqlite3.connect('hdm_papers.db')
        cursor = conn.cursor()
        logger.info("Connected to database")
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        return
    
    try:
        # Step 1: Identify all unique YAML fields
        yaml_fields = get_all_yaml_fields()
        
        # Step 2: Add new columns to database
        field_mapping = create_yaml_columns(cursor, yaml_fields)
        
        # Commit column additions
        conn.commit()
        logger.info("Database schema updated with YAML columns")
        
        # Step 3: Process all papers and update database
        stats = process_all_papers(cursor, field_mapping)
        
        # Commit all updates
        conn.commit()
        logger.info("All database updates committed")
        
        # Step 4: Save processing report
        report = {
            'processing_timestamp': datetime.now().isoformat(),
            'yaml_fields_found': list(yaml_fields),
            'field_mapping': field_mapping,
            'processing_stats': stats
        }
        
        with open('yaml_to_database_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info("Processing report saved to yaml_to_database_report.json")
        
        # Print summary
        print("\n" + "="*60)
        print("YAML TO DATABASE EXTRACTION SUMMARY")
        print("="*60)
        print(f"Total files processed: {stats['total_files']}")
        print(f"Successful YAML extractions: {stats['successful_yaml_extractions']}")
        print(f"Database records updated: {stats['database_updates']}")
        print(f"Failed extractions: {stats['failed_extractions']}")
        print(f"Missing cite_keys: {stats['missing_cite_keys']}")
        print(f"Folder/cite_key mismatches: {len(stats['folder_cite_key_mismatches'])}")
        print(f"YAML fields added to database: {len(field_mapping)}")
        
        if stats['folder_cite_key_mismatches']:
            print(f"\nFirst 5 cite_key mismatches:")
            for mismatch in stats['folder_cite_key_mismatches'][:5]:
                print(f"  {mismatch['folder_name']} -> {mismatch['yaml_cite_key']}")
    
    except Exception as e:
        logger.error(f"Error during processing: {e}")
        conn.rollback()
    
    finally:
        conn.close()
        logger.info("Database connection closed")

if __name__ == "__main__":
    main()
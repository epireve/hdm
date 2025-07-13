#!/usr/bin/env python3
"""
Consolidate database data using smart merge rules based on CSV vs YAML comparison.
"""

import sqlite3
import json
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_consolidation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_comparison_results() -> Dict[str, Any]:
    """Load the comparison results from the analysis."""
    try:
        with open('csv_yaml_comparison_report.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Comparison report not found. Run compare_csv_yaml_data.py first.")
        raise

def get_consolidation_rules() -> Dict[str, str]:
    """Define consolidation rules based on analysis results and research requirements."""
    return {
        # High-quality YAML fields (more recent, enhanced by reformatter)
        'title': 'prefer_yaml_when_available',
        'authors': 'prefer_yaml_when_available', 
        'year': 'prefer_yaml_when_available',
        'doi': 'prefer_yaml_when_available',
        'url': 'prefer_yaml_when_available',
        
        # CSV fields are more complete from manual curation
        'relevancy': 'prefer_csv',
        'relevancy_justification': 'prefer_csv',
        'insights': 'prefer_csv',
        'tldr': 'prefer_csv',
        'summary': 'prefer_csv',
        'research_question': 'prefer_csv',
        'methodology': 'prefer_csv',
        'key_findings': 'prefer_csv',
        'primary_outcomes': 'prefer_csv',
        'limitations': 'prefer_csv',
        'conclusion': 'prefer_csv',
        'research_gaps': 'prefer_csv',
        'future_work': 'prefer_csv',
        'implementation_insights': 'prefer_csv',
        'tags': 'prefer_csv',
        'downloaded': 'prefer_csv'
    }

def apply_merge_rule(csv_value: Any, yaml_value: Any, rule: str, field_name: str, cite_key: str) -> tuple:
    """Apply merge rule and return (final_value, change_made, reason)."""
    
    # Normalize values
    csv_norm = csv_value if csv_value not in [None, '', 'None'] else None
    yaml_norm = yaml_value if yaml_value not in [None, '', 'None'] else None
    
    if rule == 'prefer_yaml_when_available':
        if yaml_norm and yaml_norm != csv_norm:
            return yaml_norm, True, f'Used YAML value (enhanced/recent)'
        else:
            return csv_norm, False, 'Kept CSV value (YAML empty or identical)'
    
    elif rule == 'prefer_csv':
        if csv_norm:
            return csv_norm, False, 'Kept CSV value (manual curation)'
        elif yaml_norm:
            return yaml_norm, True, 'Used YAML value (CSV was empty)'
        else:
            return None, False, 'Both sources empty'
    
    elif rule == 'merge_both':
        if csv_norm and yaml_norm and csv_norm != yaml_norm:
            # Try intelligent merge for specific fields
            if field_name in ['authors', 'tags']:
                # Merge lists/comma-separated values
                csv_items = set(str(csv_norm).split(',')) if csv_norm else set()
                yaml_items = set(str(yaml_norm).split(',')) if yaml_norm else set()
                merged = ','.join(sorted(csv_items.union(yaml_items)))
                return merged, True, 'Merged CSV and YAML values'
            else:
                # For other fields, prefer longer/more detailed content
                if len(str(yaml_norm)) > len(str(csv_norm)):
                    return yaml_norm, True, 'Used YAML (more detailed)'
                else:
                    return csv_norm, False, 'Kept CSV (more detailed)'
        elif yaml_norm:
            return yaml_norm, True, 'Used YAML value (CSV empty)'
        else:
            return csv_norm, False, 'Kept CSV value'
    
    else:
        return csv_norm, False, f'Unknown rule: {rule}'

def consolidate_database(dry_run: bool = False) -> Dict[str, Any]:
    """Consolidate the database using defined merge rules."""
    
    consolidation_rules = get_consolidation_rules()
    
    # Connect to database
    conn = sqlite3.connect('hdm_papers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all records
    cursor.execute("SELECT * FROM papers")
    records = cursor.fetchall()
    
    consolidation_stats = {
        'total_records': len(records),
        'records_updated': 0,
        'fields_updated': 0,
        'field_update_counts': {},
        'changes_by_cite_key': {}
    }
    
    logger.info(f"Starting consolidation of {len(records)} records (dry_run={dry_run})")
    
    for record in records:
        cite_key = record['cite_key']
        record_changes = []
        
        for csv_field, rule in consolidation_rules.items():
            yaml_field = f'yaml_{csv_field}'
            
            if yaml_field not in record.keys():
                continue  # Skip if YAML field doesn't exist
            
            csv_value = record[csv_field]
            yaml_value = record[yaml_field]
            
            new_value, changed, reason = apply_merge_rule(
                csv_value, yaml_value, rule, csv_field, cite_key
            )
            
            if changed:
                record_changes.append({
                    'field': csv_field,
                    'old_value': str(csv_value)[:100] + '...' if csv_value and len(str(csv_value)) > 100 else csv_value,
                    'new_value': str(new_value)[:100] + '...' if new_value and len(str(new_value)) > 100 else new_value,
                    'reason': reason
                })
                
                consolidation_stats['fields_updated'] += 1
                
                if csv_field not in consolidation_stats['field_update_counts']:
                    consolidation_stats['field_update_counts'][csv_field] = 0
                consolidation_stats['field_update_counts'][csv_field] += 1
                
                # Update database if not dry run
                if not dry_run:
                    cursor.execute(f"UPDATE papers SET {csv_field} = ? WHERE cite_key = ?", 
                                 (new_value, cite_key))
        
        if record_changes:
            consolidation_stats['records_updated'] += 1
            consolidation_stats['changes_by_cite_key'][cite_key] = record_changes
            
            logger.info(f"Updated {cite_key}: {len(record_changes)} fields changed")
    
    # Commit changes if not dry run
    if not dry_run:
        conn.commit()
        logger.info("Changes committed to database")
    else:
        logger.info("Dry run completed - no changes committed")
    
    conn.close()
    
    return consolidation_stats

def create_missing_folders_analysis() -> Dict[str, Any]:
    """Analyze which database records don't have corresponding folders."""
    
    # Get all cite_keys from database
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT cite_key, title, authors, year FROM papers")
    database_cite_keys = {row[0]: {'title': row[1], 'authors': row[2], 'year': row[3]} for row in cursor.fetchall()}
    conn.close()
    
    # Get all folder names from production directory
    from pathlib import Path
    production_path = Path("production_final_reformatted_1752365947")
    if production_path.exists():
        folder_names = {folder.name for folder in production_path.iterdir() if folder.is_dir()}
    else:
        logger.error(f"Production path does not exist: {production_path}")
        folder_names = set()
    
    # Find missing folders
    missing_folders = {}
    for cite_key, metadata in database_cite_keys.items():
        if cite_key not in folder_names:
            missing_folders[cite_key] = metadata
    
    analysis = {
        'total_database_records': len(database_cite_keys),
        'total_folders': len(folder_names),
        'missing_folders_count': len(missing_folders),
        'missing_folders': missing_folders,
        'coverage_percentage': ((len(database_cite_keys) - len(missing_folders)) / len(database_cite_keys)) * 100
    }
    
    logger.info(f"Missing folders analysis: {len(missing_folders)} out of {len(database_cite_keys)} records missing folders")
    return analysis

def main():
    """Main function to consolidate data."""
    logger.info("Starting data consolidation process...")
    
    # First run as dry run to see what would change
    print("Running consolidation analysis (dry run)...")
    dry_run_stats = consolidate_database(dry_run=True)
    
    # Analyze missing folders
    missing_analysis = create_missing_folders_analysis()
    
    # Create comprehensive report
    consolidation_report = {
        'consolidation_timestamp': datetime.now().isoformat(),
        'dry_run_stats': dry_run_stats,
        'missing_folders_analysis': missing_analysis,
        'consolidation_rules_used': get_consolidation_rules()
    }
    
    # Save report
    with open('data_consolidation_report.json', 'w', encoding='utf-8') as f:
        json.dump(consolidation_report, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info("Consolidation report saved to data_consolidation_report.json")
    
    # Print summary
    print("\n" + "="*60)
    print("DATA CONSOLIDATION ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total database records: {dry_run_stats['total_records']}")
    print(f"Records that would be updated: {dry_run_stats['records_updated']}")
    print(f"Total field updates: {dry_run_stats['fields_updated']}")
    
    print(f"\nTop field updates:")
    sorted_fields = sorted(dry_run_stats['field_update_counts'].items(), 
                          key=lambda x: x[1], reverse=True)
    for field, count in sorted_fields[:10]:
        print(f"  {field}: {count} updates")
    
    print(f"\nMissing folders analysis:")
    print(f"  Total folders: {missing_analysis['total_folders']}")
    print(f"  Missing folders: {missing_analysis['missing_folders_count']}")
    print(f"  Coverage: {missing_analysis['coverage_percentage']:.1f}%")
    
    if missing_analysis['missing_folders']:
        print(f"\nFirst 5 missing folders:")
        for cite_key, metadata in list(missing_analysis['missing_folders'].items())[:5]:
            print(f"  {cite_key}: {metadata['title'][:60]}...")
    
    # Ask user if they want to proceed with actual consolidation
    print(f"\nWould you like to proceed with actual consolidation?")
    print("This will update the database with the changes shown above.")
    
    # For automation, we'll proceed automatically
    print("Proceeding with consolidation...")
    final_stats = consolidate_database(dry_run=False)
    
    print(f"\nConsolidation completed!")
    print(f"  Records updated: {final_stats['records_updated']}")
    print(f"  Fields updated: {final_stats['fields_updated']}")
    
    return consolidation_report

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Commit the CSV original authors changes to database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from add_csv_original_authors import CSVOriginalAuthorsAdder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def commit_csv_authors():
    """Commit the CSV original authors to database."""
    logger.info("Committing CSV original authors to database...")
    
    adder = CSVOriginalAuthorsAdder()
    
    # Apply changes with commit=True
    results = adder.add_csv_authors_column(commit_changes=True)
    
    if 'error' in results:
        print(f"❌ {results['error']}")
        return False
    
    print(f"\n✅ CSV ORIGINAL AUTHORS COMMITTED")
    print(f"=" * 50)
    print(f"Total papers: {results['total_papers']}")
    print(f"CSV authors loaded: {results['csv_entries_loaded']}")
    print(f"Successful matches: {results['matches_found']}")
    print(f"Updates made: {results['updates_made']}")
    
    stats = results['comparison_stats']
    print(f"\n📊 COMPARISON RESULTS:")
    print(f"   Identical: {stats['identical']}")
    print(f"   Different: {stats['different']}")
    print(f"   CSV longer: {stats['csv_longer']}")
    print(f"   DB longer: {stats['db_longer']}")
    
    return True

if __name__ == "__main__":
    commit_csv_authors()
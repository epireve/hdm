#!/usr/bin/env python3
"""
Add original CSV authors data as a separate column to the database.
"""

import sqlite3
import csv
import logging
from typing import Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVOriginalAuthorsAdder:
    """Add original CSV authors data to the database."""
    
    def __init__(self, csv_file_path: str = 'research_papers_merged_final.csv'):
        self.csv_file_path = csv_file_path
        self.csv_authors_map = {}
    
    def load_csv_authors(self) -> Dict[str, str]:
        """Load authors data from the original CSV file."""
        logger.info(f"Loading authors data from {self.csv_file_path}...")
        
        authors_map = {}
        rows_processed = 0
        
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    cite_key = row.get('cite_key', '').strip()
                    authors = row.get('authors', '').strip()
                    
                    if cite_key and authors:
                        authors_map[cite_key] = authors
                        rows_processed += 1
                    
                    if rows_processed % 50 == 0:
                        logger.info(f"Processed {rows_processed} CSV rows...")
        
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_file_path}")
            return {}
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return {}
        
        logger.info(f"✅ Loaded {len(authors_map)} author entries from CSV")
        self.csv_authors_map = authors_map
        return authors_map
    
    def add_csv_authors_column(self, commit_changes: bool = False) -> Dict[str, any]:
        """Add csv_original_authors column to database."""
        logger.info(f"Adding csv_original_authors column (commit={commit_changes})...")
        
        # Load CSV data first
        if not self.csv_authors_map:
            self.load_csv_authors()
        
        if not self.csv_authors_map:
            logger.error("No CSV authors data loaded - aborting")
            return {'error': 'No CSV data loaded'}
        
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(papers)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'csv_original_authors' not in columns:
            logger.info("Adding csv_original_authors column...")
            cursor.execute("ALTER TABLE papers ADD COLUMN csv_original_authors TEXT")
        else:
            logger.info("csv_original_authors column already exists")
        
        # Get all papers from database
        cursor.execute("SELECT id, cite_key, authors FROM papers ORDER BY cite_key")
        papers = cursor.fetchall()
        
        # Track statistics
        matches_found = 0
        no_matches = 0
        updates_made = 0
        comparison_stats = {
            'identical': 0,
            'different': 0,
            'csv_longer': 0,
            'db_longer': 0,
            'missing_from_csv': 0
        }
        
        logger.info(f"Processing {len(papers)} papers from database...")
        
        # Process each paper
        for paper in papers:
            paper_id = paper['id']
            cite_key = paper['cite_key']
            current_authors = paper['authors'] or ''
            
            # Find matching CSV authors
            csv_authors = self.csv_authors_map.get(cite_key, '')
            
            if csv_authors:
                matches_found += 1
                
                # Update database with CSV authors
                cursor.execute(
                    "UPDATE papers SET csv_original_authors = ? WHERE id = ?",
                    (csv_authors, paper_id)
                )
                updates_made += 1
                
                # Compare current vs CSV authors
                if current_authors == csv_authors:
                    comparison_stats['identical'] += 1
                else:
                    comparison_stats['different'] += 1
                    if len(csv_authors) > len(current_authors):
                        comparison_stats['csv_longer'] += 1
                    elif len(current_authors) > len(csv_authors):
                        comparison_stats['db_longer'] += 1
            else:
                no_matches += 1
                comparison_stats['missing_from_csv'] += 1
        
        if commit_changes:
            conn.commit()
            logger.info("✅ Changes committed to database")
        else:
            logger.info("📝 Changes prepared but NOT committed")
        
        conn.close()
        
        return {
            'total_papers': len(papers),
            'csv_entries_loaded': len(self.csv_authors_map),
            'matches_found': matches_found,
            'no_matches': no_matches,
            'updates_made': updates_made,
            'comparison_stats': comparison_stats
        }
    
    def analyze_differences(self, limit: int = 20) -> None:
        """Analyze differences between current authors and CSV authors."""
        logger.info("Analyzing differences between current and CSV authors...")
        
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get papers where authors differ
        cursor.execute("""
            SELECT cite_key, authors, csv_original_authors 
            FROM papers 
            WHERE csv_original_authors IS NOT NULL 
            AND authors != csv_original_authors 
            ORDER BY cite_key 
            LIMIT ?
        """, (limit,))
        
        differences = cursor.fetchall()
        
        print(f"\n📊 AUTHOR DIFFERENCES ANALYSIS (showing first {limit}):")
        print("=" * 80)
        
        for diff in differences:
            cite_key = diff['cite_key']
            current = diff['authors'] or 'NULL'
            csv_original = diff['csv_original_authors'] or 'NULL'
            
            print(f"\n🔑 {cite_key}")
            print(f"   Current:  {current}")
            print(f"   CSV Orig: {csv_original}")
            
            # Highlight potential issues
            if 'et al' in current.lower() and 'et al' not in csv_original.lower():
                print(f"   ⚠️  Current has 'et al', CSV has full author list")
            elif len(csv_original) > len(current) * 1.5:
                print(f"   ⚠️  CSV authors much longer ({len(csv_original)} vs {len(current)} chars)")
        
        conn.close()

def main():
    """Execute CSV original authors addition."""
    logger.info("Adding CSV Original Authors to Database...")
    
    adder = CSVOriginalAuthorsAdder()
    
    # Add the column with data
    results = adder.add_csv_authors_column(commit_changes=False)
    
    if 'error' in results:
        print(f"❌ {results['error']}")
        return
    
    print(f"\n📊 CSV ORIGINAL AUTHORS ADDITION SUMMARY:")
    print(f"=" * 60)
    print(f"Total papers in database: {results['total_papers']}")
    print(f"CSV entries loaded: {results['csv_entries_loaded']}")
    print(f"Matches found: {results['matches_found']}")
    print(f"No matches: {results['no_matches']}")
    print(f"Updates made: {results['updates_made']}")
    
    print(f"\n📈 AUTHOR COMPARISON STATISTICS:")
    stats = results['comparison_stats']
    print(f"   Identical authors: {stats['identical']}")
    print(f"   Different authors: {stats['different']}")
    print(f"   CSV longer: {stats['csv_longer']}")
    print(f"   DB longer: {stats['db_longer']}")
    print(f"   Missing from CSV: {stats['missing_from_csv']}")
    
    # Show some differences
    adder.analyze_differences(limit=15)
    
    print(f"\n💾 csv_original_authors column populated")
    print(f"   Run with commit_changes=True to save changes")
    
    return results

if __name__ == "__main__":
    main()
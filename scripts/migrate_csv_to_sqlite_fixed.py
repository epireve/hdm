#!/usr/bin/env python3
"""
Fixed migration script using proper CSV parsing
"""

import csv
import json
import sqlite3
from pathlib import Path
from datetime import datetime

class PaperMigratorFixed:
    def __init__(self, csv_file, corrections_file, output_dir, db_path="hdm_papers.db"):
        self.csv_file = Path(csv_file)
        self.corrections_file = Path(corrections_file)
        self.output_dir = Path(output_dir)
        self.db_path = db_path
        self.cite_key_corrections = {}
        
    def load_cite_key_corrections(self):
        """Load cite key corrections from JSON file"""
        if self.corrections_file.exists():
            with open(self.corrections_file, 'r') as f:
                self.cite_key_corrections = json.load(f)
            print(f"✅ Loaded {len(self.cite_key_corrections)} cite key corrections")
        else:
            print("⚠️  No cite key corrections file found")
    
    def load_csv_data(self):
        """Load papers from CSV file using proper CSV parser"""
        papers = []
        skipped_count = 0
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for line_num, row in enumerate(reader, 2):
                try:
                    # Map CSV columns to database columns
                    paper = {
                        'cite_key': row.get('cite_key', '').strip(),
                        'title': row.get('Paper Title', row.get('title', '')).strip(),
                        'authors': row.get('Authors', row.get('authors', '')).strip(),
                        'year': row.get('Year', row.get('year', '')).strip(),
                        'downloaded': row.get('Downloaded', '').strip(),
                        'relevancy': row.get('Relevancy', '').strip(),
                        'relevancy_justification': row.get('Relevancy Justification', '').strip(),
                        'insights': row.get('Insights', '').strip(),
                        'tldr': row.get('TL;DR', '').strip(),
                        'summary': row.get('Summary', '').strip(),
                        'research_question': row.get('Research Question', '').strip(),
                        'methodology': row.get('Methodology', '').strip(),
                        'key_findings': row.get('Key Findings', '').strip(),
                        'primary_outcomes': row.get('Primary Outcomes', '').strip(),
                        'limitations': row.get('Limitations', '').strip(),
                        'conclusion': row.get('Conclusion', '').strip(),
                        'research_gaps': row.get('Research Gaps', '').strip(),
                        'future_work': row.get('Future Work', '').strip(),
                        'implementation_insights': row.get('Implementation Insights', '').strip(),
                        'url': row.get('url', '').strip(),
                        'doi': row.get('DOI', '').strip(),
                        'tags': row.get('Tags', '').strip()
                    }
                    
                    # Clean empty strings to None
                    for key, value in paper.items():
                        if value == '':
                            paper[key] = None
                    
                    # Skip papers without cite_key
                    if not paper.get('cite_key'):
                        print(f"⚠️  Line {line_num}: Skipping paper without cite_key - Title: {paper.get('title', 'NO TITLE')[:50]}")
                        skipped_count += 1
                        continue
                    
                    papers.append(paper)
                    
                except Exception as e:
                    print(f"❌ Error parsing line {line_num}: {e}")
                    skipped_count += 1
                    continue
        
        print(f"✅ Loaded {len(papers)} papers from CSV")
        print(f"⚠️  Skipped {skipped_count} papers")
        return papers
    
    def apply_corrections(self, papers):
        """Apply cite key corrections and update folder paths"""
        corrected_count = 0
        
        for paper in papers:
            old_cite_key = paper['cite_key']
            
            # Apply cite key correction if exists
            if old_cite_key in self.cite_key_corrections:
                new_cite_key = self.cite_key_corrections[old_cite_key]
                paper['old_cite_key'] = old_cite_key
                paper['cite_key'] = new_cite_key
                corrected_count += 1
            else:
                paper['old_cite_key'] = None
                # Check if paper exists in output directory
                if not (self.output_dir / old_cite_key).exists():
                    # It might have been processed but not in corrections file
                    # Check for similar folders
                    possible_folders = list(self.output_dir.glob(f"{old_cite_key}*"))
                    if possible_folders:
                        paper['cite_key'] = possible_folders[0].name
                        paper['old_cite_key'] = old_cite_key
                        corrected_count += 1
            
            # Set folder path
            paper['folder_path'] = f"production_final_reformatted_1752365947/{paper['cite_key']}"
            
            # Add date_processed
            paper['date_processed'] = datetime.now().strftime('%Y-%m-%d')
            
            # Convert year to integer
            if paper.get('year'):
                try:
                    paper['year'] = int(paper['year'])
                except:
                    paper['year'] = None
        
        print(f"✅ Applied corrections to {corrected_count} papers")
        return papers
    
    def clear_existing_data(self):
        """Clear existing data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM papers")
            conn.commit()
            print("✅ Cleared existing data from database")
        except Exception as e:
            print(f"❌ Error clearing data: {e}")
        finally:
            conn.close()
    
    def insert_to_database(self, papers):
        """Insert papers into SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Prepare insert statement
        columns = [
            'cite_key', 'old_cite_key', 'title', 'authors', 'year', 
            'downloaded', 'relevancy', 'relevancy_justification', 
            'insights', 'tldr', 'summary', 'research_question', 
            'methodology', 'key_findings', 'primary_outcomes', 
            'limitations', 'conclusion', 'research_gaps', 
            'future_work', 'implementation_insights', 'url', 'doi', 
            'tags', 'date_processed', 'folder_path'
        ]
        
        placeholders = ', '.join(['?' for _ in columns])
        insert_sql = f"INSERT INTO papers ({', '.join(columns)}) VALUES ({placeholders})"
        
        # Insert papers
        success_count = 0
        error_count = 0
        duplicate_keys = []
        
        for paper in papers:
            try:
                values = [paper.get(col) for col in columns]
                cursor.execute(insert_sql, values)
                success_count += 1
            except sqlite3.IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    duplicate_keys.append(paper['cite_key'])
                else:
                    print(f"⚠️  Integrity error for '{paper['cite_key']}': {e}")
                error_count += 1
            except Exception as e:
                print(f"❌ Error inserting paper '{paper.get('title', 'Unknown')[:50]}': {e}")
                error_count += 1
        
        conn.commit()
        
        print(f"\n✅ Successfully inserted {success_count} papers")
        if error_count > 0:
            print(f"⚠️  Failed to insert {error_count} papers")
        if duplicate_keys:
            print(f"⚠️  Found {len(duplicate_keys)} duplicate cite_keys: {duplicate_keys[:5]}...")
        
        # Show statistics
        cursor.execute("SELECT * FROM papers_statistics")
        stats = cursor.fetchone()
        if stats:
            columns = [desc[0] for desc in cursor.description]
            
            print("\n📊 Database Statistics:")
            for i, col in enumerate(columns):
                print(f"   {col}: {stats[i]}")
        
        conn.close()
    
    def migrate(self):
        """Run the complete migration process"""
        print("🚀 Starting fixed CSV to SQLite migration...")
        
        # Create database first if needed
        if not Path(self.db_path).exists():
            from create_papers_database import create_database
            create_database(self.db_path)
        else:
            # Clear existing data
            self.clear_existing_data()
        
        # Load cite key corrections
        self.load_cite_key_corrections()
        
        # Load CSV data
        papers = self.load_csv_data()
        
        # Apply corrections
        papers = self.apply_corrections(papers)
        
        # Insert to database
        self.insert_to_database(papers)
        
        print("\n✅ Migration completed successfully!")
        print(f"📁 Database: {self.db_path}")

def main():
    """Main entry point"""
    base_dir = Path("/Users/invoture/dev.local/hdm")
    
    # Configuration
    csv_file = base_dir / "research_papers_merged_final.csv"
    corrections_file = base_dir / "production_final_reformatted_1752365947" / "cite_key_corrections.json"
    output_dir = base_dir / "production_final_reformatted_1752365947"
    db_path = base_dir / "hdm_papers.db"
    
    # Check if files exist
    if not csv_file.exists():
        print(f"❌ CSV file not found: {csv_file}")
        return
    
    # Run migration
    migrator = PaperMigratorFixed(csv_file, corrections_file, output_dir, db_path)
    migrator.migrate()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Migrate papers from CSV to SQLite database with cite key corrections
"""

import csv
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import re

class PaperMigrator:
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
    
    def parse_csv_line(self, line):
        """Parse a single CSV line handling quoted values and escaped quotes"""
        result = []
        current = ''
        in_quotes = False
        
        for i in range(len(line)):
            char = line[i]
            next_char = line[i + 1] if i + 1 < len(line) else None
            
            if char == '"':
                if in_quotes and next_char == '"':
                    # Escaped quote inside quoted field
                    current += '"'
                    i += 1  # Skip next quote
                else:
                    # Toggle quote state
                    in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                result.append(current.strip())
                current = ''
            else:
                current += char
        
        result.append(current.strip())
        return result
    
    def load_csv_data(self):
        """Load papers from CSV file"""
        papers = []
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            # Read header
            header_line = f.readline().strip()
            headers = [h.strip().strip('"') for h in header_line.split(',')]
            
            # Normalize header names to match database columns
            header_map = {
                'Paper Title': 'title',
                'Authors': 'authors',
                'Year': 'year',
                'Downloaded': 'downloaded',
                'Relevancy': 'relevancy',
                'Relevancy Justification': 'relevancy_justification',
                'Insights': 'insights',
                'TL;DR': 'tldr',
                'Summary': 'summary',
                'Research Question': 'research_question',
                'Methodology': 'methodology',
                'Key Findings': 'key_findings',
                'Primary Outcomes': 'primary_outcomes',
                'Limitations': 'limitations',
                'Conclusion': 'conclusion',
                'Research Gaps': 'research_gaps',
                'Future Work': 'future_work',
                'Implementation Insights': 'implementation_insights',
                'url': 'url',
                'DOI': 'doi',
                'Tags': 'tags',
                'cite_key': 'cite_key'
            }
            
            # Read data lines
            line_num = 1
            for line in f:
                line_num += 1
                line = line.strip()
                if not line:
                    continue
                
                try:
                    values = self.parse_csv_line(line)
                    if len(values) < len(headers):
                        print(f"⚠️  Line {line_num}: Skipping incomplete row")
                        continue
                    
                    paper = {}
                    for i, header in enumerate(headers):
                        db_column = header_map.get(header, header.lower().replace(' ', '_'))
                        value = values[i] if i < len(values) else ''
                        # Clean up value
                        value = value.strip().strip('"')
                        paper[db_column] = value if value else None
                    
                    # Skip papers without cite_key
                    if not paper.get('cite_key'):
                        print(f"⚠️  Line {line_num}: Skipping paper without cite_key")
                        continue
                    
                    papers.append(paper)
                    
                except Exception as e:
                    print(f"❌ Error parsing line {line_num}: {e}")
                    continue
        
        print(f"✅ Loaded {len(papers)} papers from CSV")
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
        
        for paper in papers:
            try:
                values = [paper.get(col) for col in columns]
                cursor.execute(insert_sql, values)
                success_count += 1
            except sqlite3.IntegrityError as e:
                print(f"⚠️  Duplicate cite_key '{paper['cite_key']}': {e}")
                error_count += 1
            except Exception as e:
                print(f"❌ Error inserting paper '{paper.get('title', 'Unknown')}': {e}")
                error_count += 1
        
        conn.commit()
        
        print(f"\n✅ Successfully inserted {success_count} papers")
        if error_count > 0:
            print(f"⚠️  Failed to insert {error_count} papers")
        
        # Show statistics
        cursor.execute("SELECT * FROM papers_statistics")
        stats = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        
        print("\n📊 Database Statistics:")
        for i, col in enumerate(columns):
            print(f"   {col}: {stats[i]}")
        
        conn.close()
    
    def migrate(self):
        """Run the complete migration process"""
        print("🚀 Starting CSV to SQLite migration...")
        
        # Create database first
        from create_papers_database import create_database
        create_database(self.db_path)
        
        # Load cite key corrections
        self.load_cite_key_corrections()
        
        # Load CSV data
        papers = self.load_csv_data()
        
        # Apply corrections
        papers = self.apply_corrections(papers)
        
        # Insert to database
        self.insert_to_database(papers)
        
        print("\n✅ Migration completed successfully!")
        print(f"📁 Database created: {self.db_path}")

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
    migrator = PaperMigrator(csv_file, corrections_file, output_dir, db_path)
    migrator.migrate()

if __name__ == "__main__":
    main()
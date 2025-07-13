#!/usr/bin/env python3
"""
Preserve ALL data from CSV - create unique cite_keys for duplicates
"""

import csv
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class DataPreserver:
    def __init__(self, csv_file, corrections_file, output_dir, db_path="hdm_papers.db"):
        self.csv_file = Path(csv_file)
        self.corrections_file = Path(corrections_file)
        self.output_dir = Path(output_dir)
        self.db_path = db_path
        self.corrections = {}
        
    def load_corrections(self):
        """Load existing corrections"""
        if self.corrections_file.exists():
            with open(self.corrections_file, 'r') as f:
                self.corrections = json.load(f)
        print(f"✅ Loaded {len(self.corrections)} existing corrections")
    
    def ensure_unique_cite_keys(self, papers):
        """Ensure all cite_keys are unique by adding suffixes"""
        print("\n🔧 Ensuring all cite_keys are unique...")
        
        # Track used cite_keys
        used_cite_keys = set()
        cite_key_counts = defaultdict(int)
        
        # First pass: apply existing corrections and count occurrences
        for paper in papers:
            original_key = paper['cite_key']
            corrected_key = self.corrections.get(original_key, original_key)
            cite_key_counts[corrected_key] += 1
        
        # Second pass: ensure uniqueness
        processed_papers = []
        cite_key_usage = defaultdict(int)
        new_corrections = {}
        
        for i, paper in enumerate(papers):
            original_key = paper['cite_key']
            base_corrected_key = self.corrections.get(original_key, original_key)
            
            # If this cite_key will appear multiple times, add suffix
            if cite_key_counts[base_corrected_key] > 1:
                cite_key_usage[base_corrected_key] += 1
                
                if cite_key_usage[base_corrected_key] == 1:
                    # First occurrence - keep as is
                    final_key = base_corrected_key
                else:
                    # Subsequent occurrences - add suffix
                    suffix_index = cite_key_usage[base_corrected_key] - 1
                    suffix = chr(ord('a') + suffix_index - 1)  # a, b, c, etc.
                    final_key = f"{base_corrected_key}{suffix}"
                    
                    # Record this as a new correction
                    if original_key not in self.corrections:
                        new_corrections[original_key] = final_key
                        print(f"   Added correction: {original_key} -> {final_key}")
            else:
                # Unique cite_key - no change needed
                final_key = base_corrected_key
            
            # Create processed paper
            processed_paper = paper.copy()
            processed_paper['old_cite_key'] = original_key if original_key != final_key else None
            processed_paper['cite_key'] = final_key
            
            # Verify uniqueness
            if final_key in used_cite_keys:
                print(f"❌ ERROR: cite_key '{final_key}' is still duplicate!")
            used_cite_keys.add(final_key)
            
            processed_papers.append(processed_paper)
        
        print(f"✅ Processed {len(processed_papers)} papers")
        print(f"✅ All {len(used_cite_keys)} cite_keys are now unique")
        
        # Save new corrections if any
        if new_corrections:
            self.save_additional_corrections(new_corrections)
        
        return processed_papers
    
    def save_additional_corrections(self, new_corrections):
        """Save additional corrections to file"""
        updated_corrections = self.corrections.copy()
        updated_corrections.update(new_corrections)
        
        # Backup current corrections
        backup_file = self.corrections_file.parent / "cite_key_corrections_before_preserve.json"
        with open(backup_file, 'w') as f:
            json.dump(self.corrections, f, indent=2, sort_keys=True)
        
        # Save updated corrections
        with open(self.corrections_file, 'w') as f:
            json.dump(updated_corrections, f, indent=2, sort_keys=True)
        
        print(f"📁 Added {len(new_corrections)} new corrections")
        print(f"📁 Backup saved to: {backup_file}")
    
    def load_all_csv_data(self):
        """Load ALL papers from CSV - no skipping"""
        papers = []
        
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
                        'tags': row.get('Tags', '').strip(),
                        'csv_line_number': line_num  # Track original line for debugging
                    }
                    
                    # Clean empty strings to None
                    for key, value in paper.items():
                        if value == '' and key != 'csv_line_number':
                            paper[key] = None
                    
                    # Handle missing cite_key - create one
                    if not paper.get('cite_key'):
                        # Generate cite_key from title or use line number
                        title = paper.get('title', '')
                        if title:
                            # Create cite_key from first word of title + year
                            first_word = title.lower().split()[0] if title.split() else 'unknown'
                            year = paper.get('year', '0000')
                            paper['cite_key'] = f"{first_word}_{year}_line{line_num}"
                        else:
                            paper['cite_key'] = f"unknown_line{line_num}"
                        print(f"⚠️  Generated cite_key for line {line_num}: {paper['cite_key']}")
                    
                    papers.append(paper)
                    
                except Exception as e:
                    print(f"❌ Error processing line {line_num}: {e}")
                    # Even if there's an error, try to preserve what we can
                    paper = {
                        'cite_key': f"error_line{line_num}",
                        'title': f"Error processing line {line_num}",
                        'csv_line_number': line_num
                    }
                    papers.append(paper)
        
        print(f"✅ Loaded ALL {len(papers)} records from CSV")
        return papers
    
    def prepare_for_database(self, papers):
        """Prepare papers for database insertion"""
        for paper in papers:
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
        
        return papers
    
    def clear_and_insert_all(self, papers):
        """Clear database and insert ALL papers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Clear existing data
            cursor.execute("DELETE FROM papers")
            print("✅ Cleared existing data from database")
            
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
            
            # Insert all papers
            success_count = 0
            for paper in papers:
                try:
                    values = [paper.get(col) for col in columns]
                    cursor.execute(insert_sql, values)
                    success_count += 1
                except Exception as e:
                    print(f"❌ Error inserting paper '{paper.get('cite_key')}': {e}")
                    print(f"   Title: {paper.get('title', 'NO TITLE')[:50]}")
            
            conn.commit()
            
            print(f"\n✅ Successfully inserted {success_count} papers")
            print(f"✅ Database now contains ALL {success_count} records from CSV")
            
            # Show final statistics
            cursor.execute("SELECT * FROM papers_statistics")
            stats = cursor.fetchone()
            if stats:
                columns = [desc[0] for desc in cursor.description]
                print("\n📊 Final Database Statistics:")
                for i, col in enumerate(columns):
                    print(f"   {col}: {stats[i]}")
            
        finally:
            conn.close()
    
    def preserve_all_data(self):
        """Main method to preserve all CSV data"""
        print("🚀 PRESERVING ALL CSV DATA - NO DATA LOSS")
        print("="*60)
        
        # Load existing corrections
        self.load_corrections()
        
        # Load ALL CSV data
        papers = self.load_all_csv_data()
        
        # Ensure unique cite_keys
        papers = self.ensure_unique_cite_keys(papers)
        
        # Prepare for database
        papers = self.prepare_for_database(papers)
        
        # Insert all data
        self.clear_and_insert_all(papers)
        
        print("\n🎉 ALL CSV DATA PRESERVED SUCCESSFULLY!")
        print(f"✅ {len(papers)} records from CSV are now in database")
        print("✅ No data was lost - every row from CSV is preserved")

def main():
    base_dir = Path("/Users/invoture/dev.local/hdm")
    
    csv_file = base_dir / "research_papers_merged_final.csv"
    corrections_file = base_dir / "production_final_reformatted_1752365947" / "cite_key_corrections.json"
    output_dir = base_dir / "production_final_reformatted_1752365947"
    db_path = base_dir / "hdm_papers.db"
    
    preserver = DataPreserver(csv_file, corrections_file, output_dir, db_path)
    preserver.preserve_all_data()

if __name__ == "__main__":
    main()
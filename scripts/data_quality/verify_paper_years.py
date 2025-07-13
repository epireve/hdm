#!/usr/bin/env python3
"""
Comprehensive year verification and correction for all papers.
Uses Task agents to scan paper.md files and extract accurate publication years.
"""

import sqlite3
import json
import os
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YearVerifier:
    def __init__(self):
        self.conn = sqlite3.connect('hdm_papers.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.issues = []
        self.corrections = {}
        
    def analyze_year_issues(self):
        """Identify all papers with potential year issues."""
        
        # 1. Papers outside expected range (2019-2025)
        self.cursor.execute('''
            SELECT cite_key, year, title, corrected_cite_key
            FROM papers
            WHERE year < 2019 OR year > 2025
            ORDER BY year
        ''')
        out_of_range = self.cursor.fetchall()
        
        # 2. Year-cite_key mismatches
        self.cursor.execute('''
            SELECT cite_key, year, title, corrected_cite_key
            FROM papers
            WHERE cite_key LIKE '%_20%'
        ''')
        all_papers = self.cursor.fetchall()
        
        mismatches = []
        for paper in all_papers:
            # Extract year from cite_key
            match = re.search(r'_(\d{4})[a-z]?$', paper['cite_key'])
            if match:
                cite_key_year = int(match.group(1))
                if cite_key_year != paper['year']:
                    mismatches.append(paper)
        
        print(f"\n📊 YEAR VERIFICATION ANALYSIS")
        print(f"=" * 70)
        print(f"Total papers: {self.cursor.execute('SELECT COUNT(*) FROM papers').fetchone()[0]}")
        print(f"Papers outside 2019-2025: {len(out_of_range)}")
        print(f"Year-cite_key mismatches: {len(mismatches)}")
        
        # Combine issues
        all_issues = {}
        
        for paper in out_of_range:
            all_issues[paper['cite_key']] = {
                'year': paper['year'],
                'title': paper['title'],
                'issue': 'out_of_range',
                'corrected_cite_key': paper['corrected_cite_key']
            }
            
        for paper in mismatches:
            if paper['cite_key'] not in all_issues:
                all_issues[paper['cite_key']] = {
                    'year': paper['year'],
                    'title': paper['title'],
                    'issue': 'mismatch',
                    'corrected_cite_key': paper['corrected_cite_key']
                }
            else:
                all_issues[paper['cite_key']]['issue'] = 'both'
        
        self.issues = all_issues
        return all_issues
    
    def get_folder_for_paper(self, cite_key, corrected_cite_key=None):
        """Find the folder path for a paper."""
        # Check multiple possible locations
        base_paths = [
            'markdown_papers',
            'production_final_reformatted_1752365947'
        ]
        
        # Try original cite_key first
        for base in base_paths:
            folder = Path(base) / cite_key
            if folder.exists():
                return folder
                
        # Try corrected cite_key if available
        if corrected_cite_key:
            for base in base_paths:
                folder = Path(base) / corrected_cite_key
                if folder.exists():
                    return folder
        
        # Try fuzzy match (remove suffix)
        base_key = re.sub(r'[a-z]$', '', cite_key)
        for base in base_paths:
            base_path = Path(base)
            if base_path.exists():
                for folder in base_path.iterdir():
                    if folder.is_dir() and folder.name.startswith(base_key):
                        return folder
        
        return None
    
    def extract_year_from_paper_md(self, folder_path):
        """Extract year from paper.md file."""
        paper_md_path = folder_path / 'paper.md'
        
        if not paper_md_path.exists():
            return None
            
        try:
            with open(paper_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for year in YAML frontmatter
            yaml_match = re.search(r'^---\s*\n.*?year:\s*(\d{4}).*?\n---', content, re.DOTALL | re.MULTILINE)
            if yaml_match:
                return int(yaml_match.group(1))
                
            # Look for year patterns in content
            # Common patterns: "Published in 2023", "2023 IEEE", "(2023)", etc.
            year_patterns = [
                r'Published\s+in\s+(\d{4})',
                r'©\s*(\d{4})',
                r'\((\d{4})\)\s*\d+[-–]\d+',  # (2023) 123-456
                r'(\d{4})\s+IEEE',
                r'(\d{4})\s+ACM',
                r'Accepted.*?(\d{4})',
                r'Received.*?(\d{4})',
            ]
            
            for pattern in year_patterns:
                match = re.search(pattern, content)
                if match:
                    year = int(match.group(1))
                    if 2000 <= year <= 2025:  # Reasonable range
                        return year
                        
        except Exception as e:
            logger.error(f"Error reading {paper_md_path}: {e}")
            
        return None
    
    def create_batch_verification_tasks(self):
        """Create tasks for batch verification using Task agents."""
        
        # Group papers by issue type for efficient processing
        out_of_range = []
        mismatches = []
        
        for cite_key, info in self.issues.items():
            folder = self.get_folder_for_paper(cite_key, info['corrected_cite_key'])
            if folder:
                info['folder'] = str(folder)
                if info['issue'] == 'out_of_range' or info['issue'] == 'both':
                    out_of_range.append((cite_key, info))
                else:
                    mismatches.append((cite_key, info))
        
        print(f"\n📁 FOLDER MAPPING:")
        print(f"   Papers with folders found: {len([i for i in self.issues.values() if 'folder' in i])}")
        print(f"   Papers without folders: {len([i for i in self.issues.values() if 'folder' not in i])}")
        
        # Save issues for Task agent processing
        with open('year_verification_tasks.json', 'w') as f:
            json.dump({
                'out_of_range': out_of_range,
                'mismatches': mismatches,
                'total_issues': len(self.issues)
            }, f, indent=2)
            
        print(f"\n✅ Created year_verification_tasks.json")
        print(f"   Out of range papers: {len(out_of_range)}")
        print(f"   Mismatch papers: {len(mismatches)}")
        
        return out_of_range, mismatches
    
    def apply_corrections(self, corrections_file='year_corrections.json'):
        """Apply year corrections from Task agent results."""
        
        if not os.path.exists(corrections_file):
            print(f"❌ Corrections file not found: {corrections_file}")
            return
            
        with open(corrections_file, 'r') as f:
            corrections = json.load(f)
            
        updated_count = 0
        
        print(f"\n🔧 APPLYING YEAR CORRECTIONS")
        print(f"=" * 70)
        
        for cite_key, new_year in corrections.items():
            self.cursor.execute("SELECT year, title FROM papers WHERE cite_key = ?", (cite_key,))
            result = self.cursor.fetchone()
            
            if result:
                old_year = result['year']
                if old_year != new_year:
                    self.cursor.execute("UPDATE papers SET year = ? WHERE cite_key = ?", 
                                      (new_year, cite_key))
                    updated_count += 1
                    print(f"✅ {cite_key}: {old_year} → {new_year}")
                    print(f"   {result['title'][:60]}...")
        
        self.conn.commit()
        
        print(f"\n📊 YEAR CORRECTIONS SUMMARY:")
        print(f"   Papers updated: {updated_count}")
        
        return updated_count
    
    def final_validation(self):
        """Perform final validation of year data."""
        
        # Check remaining issues
        self.cursor.execute('''
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN year < 2019 OR year > 2025 THEN 1 END) as out_of_range,
                COUNT(CASE WHEN year BETWEEN 2019 AND 2025 THEN 1 END) as valid_range
            FROM papers
        ''')
        stats = self.cursor.fetchone()
        
        print(f"\n📊 FINAL YEAR DATA VALIDATION:")
        print(f"   Total papers: {stats['total']}")
        print(f"   Valid range (2019-2025): {stats['valid_range']} ({stats['valid_range']/stats['total']*100:.1f}%)")
        print(f"   Still out of range: {stats['out_of_range']}")
        
        if stats['out_of_range'] > 0:
            self.cursor.execute('''
                SELECT cite_key, year, title
                FROM papers
                WHERE year < 2019 OR year > 2025
                ORDER BY year
                LIMIT 10
            ''')
            print(f"\n⚠️  REMAINING PAPERS OUTSIDE RANGE:")
            for row in self.cursor.fetchall():
                print(f"   {row['cite_key']} (year={row['year']}): {row['title'][:50]}...")
    
    def close(self):
        """Close database connection."""
        self.conn.close()


def main():
    """Main execution function."""
    verifier = YearVerifier()
    
    try:
        # Step 1: Analyze issues
        issues = verifier.analyze_year_issues()
        
        # Step 2: Create verification tasks
        out_of_range, mismatches = verifier.create_batch_verification_tasks()
        
        # Step 3: Try local extraction first
        print(f"\n🔍 ATTEMPTING LOCAL YEAR EXTRACTION...")
        local_corrections = {}
        
        for cite_key, info in issues.items():
            if 'folder' in info:
                folder_path = Path(info['folder'])
                extracted_year = verifier.extract_year_from_paper_md(folder_path)
                if extracted_year and extracted_year != info['year']:
                    local_corrections[cite_key] = extracted_year
                    print(f"   Found: {cite_key} should be {extracted_year} (was {info['year']})")
        
        if local_corrections:
            with open('year_corrections_local.json', 'w') as f:
                json.dump(local_corrections, f, indent=2)
            print(f"\n✅ Found {len(local_corrections)} corrections locally")
            print(f"   Saved to year_corrections_local.json")
        
        print(f"\n📝 NEXT STEPS:")
        print(f"1. Review year_verification_tasks.json")
        print(f"2. Use Task agents to verify years from paper.md files")
        print(f"3. Save corrections to year_corrections.json")
        print(f"4. Run: python verify_paper_years.py --apply-corrections")
        
    finally:
        verifier.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--apply-corrections':
        verifier = YearVerifier()
        
        # Apply local corrections first if available
        if os.path.exists('year_corrections_local.json'):
            print("Applying local corrections...")
            verifier.apply_corrections('year_corrections_local.json')
            
        # Apply Task agent corrections if available
        if os.path.exists('year_corrections.json'):
            print("\nApplying Task agent corrections...")
            verifier.apply_corrections('year_corrections.json')
            
        verifier.final_validation()
        verifier.close()
    else:
        main()
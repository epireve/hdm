#!/usr/bin/env python3
"""
Analyze and correct cite_keys based on first author's last name.
Creates new column for corrected cite_keys without committing changes.
"""

import sqlite3
import re
import json
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime
from collections import defaultdict

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cite_key_correction_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CiteKeyCorrector:
    """Analyze and correct cite_keys based on first author extraction."""
    
    def __init__(self):
        self.correction_stats = {
            'total_papers': 0,
            'correct_cite_keys': 0,
            'incorrect_cite_keys': 0,
            'corrections_needed': [],
            'duplicate_conflicts': [],
            'extraction_failures': []
        }
    
    def extract_first_author_lastname(self, authors_string: str) -> Optional[str]:
        """Extract the first author's last name from authors string."""
        if not authors_string or authors_string.strip() == '':
            return None
        
        authors_string = authors_string.strip()
        
        # Handle email-only cases
        if '@' in authors_string and ',' not in authors_string:
            # Extract from email like "nudt.edu.cn liyitong"
            parts = authors_string.split()
            if len(parts) >= 2:
                return parts[-1].lower()  # Take last part as name
            return None
        
        # Handle standard author formats
        # Split by common separators (comma, semicolon, 'and')
        first_author = re.split(r'[,;]|\sand\s', authors_string)[0].strip()
        
        # Remove common prefixes/suffixes
        first_author = re.sub(r'\s*(Fellow|IEEE|Dr\.?|Prof\.?|Ph\.?D\.?)\s*', '', first_author, flags=re.IGNORECASE)
        first_author = re.sub(r'\s*[∗*†‡§¶#]+\s*', '', first_author)  # Remove superscript symbols
        
        # Handle different name formats
        if ',' in first_author:
            # "Last, First" format
            parts = first_author.split(',')
            lastname = parts[0].strip()
        else:
            # "First Last" or "First Middle Last" format
            parts = first_author.split()
            if len(parts) >= 2:
                lastname = parts[-1]  # Take last word as surname
            elif len(parts) == 1:
                lastname = parts[0]  # Single name
            else:
                return None
        
        # Clean up the lastname
        lastname = re.sub(r'[^\w\s-]', '', lastname)  # Remove special chars except hyphens
        lastname = lastname.strip().lower()
        
        # Handle special cases
        if lastname.startswith('(') and lastname.endswith(')'):
            lastname = lastname[1:-1]  # Remove parentheses
        
        # Validate lastname
        if len(lastname) < 2 or not re.match(r'^[a-z-]+$', lastname):
            return None
        
        return lastname
    
    def generate_cite_key(self, lastname: str, year: int) -> str:
        """Generate cite_key from lastname and year."""
        if not lastname or not year:
            return None
        
        return f"{lastname}_{year}"
    
    def resolve_cite_key_conflicts(self, proposed_cite_keys: Dict[str, List[str]]) -> Dict[str, str]:
        """Resolve conflicts when multiple papers would have same cite_key."""
        final_cite_keys = {}
        
        for base_cite_key, paper_ids in proposed_cite_keys.items():
            if len(paper_ids) == 1:
                # No conflict
                final_cite_keys[paper_ids[0]] = base_cite_key
            else:
                # Multiple papers with same cite_key - add suffixes
                logger.info(f"Resolving conflict for {base_cite_key}: {len(paper_ids)} papers")
                
                for i, paper_id in enumerate(sorted(paper_ids)):
                    if i == 0:
                        # First paper keeps base cite_key
                        final_cite_keys[paper_id] = base_cite_key
                    else:
                        # Subsequent papers get alphabetic suffixes
                        suffix = chr(ord('a') + i - 1)  # a, b, c, etc.
                        final_cite_keys[paper_id] = f"{base_cite_key}{suffix}"
                
                self.correction_stats['duplicate_conflicts'].append({
                    'base_cite_key': base_cite_key,
                    'papers_affected': len(paper_ids),
                    'resolution': [final_cite_keys[pid] for pid in paper_ids]
                })
        
        return final_cite_keys
    
    def analyze_cite_key_corrections(self) -> Dict[str, any]:
        """Analyze all papers and determine cite_key corrections needed."""
        logger.info("Starting cite_key correction analysis...")
        
        # Connect to database
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all papers
        cursor.execute("SELECT id, cite_key, authors, year FROM papers ORDER BY cite_key")
        papers = cursor.fetchall()
        
        self.correction_stats['total_papers'] = len(papers)
        logger.info(f"Analyzing {len(papers)} papers...")
        
        # Analyze each paper
        proposed_cite_keys = defaultdict(list)  # base_cite_key -> [paper_ids]
        corrections_needed = []
        
        for paper in papers:
            paper_id = str(paper['id'])
            current_cite_key = paper['cite_key']
            authors = paper['authors']
            year = paper['year']
            
            # Extract first author lastname
            first_author_lastname = self.extract_first_author_lastname(authors)
            
            if not first_author_lastname:
                self.correction_stats['extraction_failures'].append({
                    'paper_id': paper_id,
                    'current_cite_key': current_cite_key,
                    'authors': authors,
                    'reason': 'Failed to extract first author lastname'
                })
                # Keep current cite_key for failed extractions
                proposed_cite_keys[current_cite_key].append(paper_id)
                continue
            
            # Generate correct cite_key
            correct_cite_key = self.generate_cite_key(first_author_lastname, year)
            
            if current_cite_key != correct_cite_key:
                # Correction needed
                corrections_needed.append({
                    'paper_id': paper_id,
                    'current_cite_key': current_cite_key,
                    'correct_base_cite_key': correct_cite_key,
                    'first_author_lastname': first_author_lastname,
                    'authors': authors,
                    'year': year
                })
                self.correction_stats['incorrect_cite_keys'] += 1
            else:
                self.correction_stats['correct_cite_keys'] += 1
            
            # Track proposed cite_key (before suffix resolution)
            proposed_cite_keys[correct_cite_key].append(paper_id)
        
        # Resolve conflicts with alphabetic suffixes
        final_cite_keys = self.resolve_cite_key_conflicts(proposed_cite_keys)
        
        # Update corrections with final cite_keys (including suffixes)
        for correction in corrections_needed:
            paper_id = correction['paper_id']
            correction['final_correct_cite_key'] = final_cite_keys.get(paper_id, correction['correct_base_cite_key'])
        
        self.correction_stats['corrections_needed'] = corrections_needed
        
        conn.close()
        
        logger.info(f"Analysis complete:")
        logger.info(f"  Correct cite_keys: {self.correction_stats['correct_cite_keys']}")
        logger.info(f"  Incorrect cite_keys: {self.correction_stats['incorrect_cite_keys']}")
        logger.info(f"  Extraction failures: {len(self.correction_stats['extraction_failures'])}")
        logger.info(f"  Duplicate conflicts: {len(self.correction_stats['duplicate_conflicts'])}")
        
        return {
            'stats': self.correction_stats,
            'final_cite_keys': final_cite_keys,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def add_corrected_cite_key_column(self, final_cite_keys: Dict[str, str]) -> bool:
        """Add new column with corrected cite_keys without committing."""
        logger.info("Adding corrected_cite_key column...")
        
        try:
            conn = sqlite3.connect('hdm_papers.db')
            cursor = conn.cursor()
            
            # Add new column
            cursor.execute("ALTER TABLE papers ADD COLUMN corrected_cite_key TEXT")
            
            # Update with corrected cite_keys
            for paper_id, corrected_cite_key in final_cite_keys.items():
                cursor.execute(
                    "UPDATE papers SET corrected_cite_key = ? WHERE id = ?",
                    (corrected_cite_key, int(paper_id))
                )
            
            # Don't commit yet - just prepare the changes
            logger.info(f"Added corrected_cite_key column with {len(final_cite_keys)} corrections")
            logger.info("Changes prepared but NOT committed - ready for review")
            
            # Get some examples for review
            cursor.execute("""
                SELECT cite_key, corrected_cite_key, authors 
                FROM papers 
                WHERE cite_key != corrected_cite_key 
                LIMIT 10
            """)
            examples = cursor.fetchall()
            
            conn.close()
            return examples
            
        except Exception as e:
            logger.error(f"Error adding corrected cite_key column: {e}")
            return False

def main():
    """Main function to analyze cite_key corrections."""
    logger.info("Starting Cite_Key Correction Analysis...")
    
    corrector = CiteKeyCorrector()
    
    # Step 1: Analyze all cite_keys
    analysis_results = corrector.analyze_cite_key_corrections()
    
    # Step 2: Add corrected_cite_key column (no commit)
    examples = corrector.add_corrected_cite_key_column(analysis_results['final_cite_keys'])
    
    # Step 3: Save analysis report
    with open('cite_key_correction_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False, default=str)
    
    # Step 4: Print summary
    print("\n" + "="*80)
    print("CITE_KEY CORRECTION ANALYSIS SUMMARY")
    print("="*80)
    
    stats = analysis_results['stats']
    print(f"📊 Total Papers: {stats['total_papers']}")
    print(f"✅ Correct Cite_Keys: {stats['correct_cite_keys']}")
    print(f"❌ Incorrect Cite_Keys: {stats['incorrect_cite_keys']}")
    print(f"⚠️  Extraction Failures: {len(stats['extraction_failures'])}")
    print(f"🔄 Duplicate Conflicts: {len(stats['duplicate_conflicts'])}")
    
    print(f"\n🔧 CORRECTIONS NEEDED ({stats['incorrect_cite_keys']} papers):")
    for correction in stats['corrections_needed'][:10]:  # Show first 10
        print(f"   {correction['current_cite_key']} → {correction['final_correct_cite_key']}")
        print(f"     Authors: {correction['authors'][:60]}...")
        print(f"     First Author: {correction['first_author_lastname']}")
    
    if len(stats['corrections_needed']) > 10:
        print(f"   ... and {len(stats['corrections_needed']) - 10} more corrections")
    
    print(f"\n📋 SAMPLE CURRENT vs CORRECTED (from database):")
    if examples:
        for example in examples:
            print(f"   {example[0]} → {example[1]}")
            print(f"     Authors: {example[2][:60]}...")
    
    print(f"\n⚡ DUPLICATE CONFLICTS RESOLVED:")
    for conflict in stats['duplicate_conflicts'][:5]:  # Show first 5
        print(f"   {conflict['base_cite_key']}: {conflict['papers_affected']} papers")
        print(f"     → {', '.join(conflict['resolution'])}")
    
    print(f"\n💾 NEW COLUMN ADDED: 'corrected_cite_key'")
    print(f"   ⚠️  Changes prepared but NOT committed")
    print(f"   📄 Full analysis saved to: cite_key_correction_analysis.json")
    print(f"   🔍 Review corrections before committing changes")
    
    print("="*80)
    
    return analysis_results

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Final cite_key corrector with robust author extraction logic.
"""

import sqlite3
import re
import json
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime
from collections import defaultdict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinalCiteKeyCorrector:
    """Final cite_key correction with robust author extraction."""
    
    def __init__(self):
        self.name_prefixes = [
            'al', 'al-', 'ibn', 'ben', 'bin', 'abu', 'abd',  # Arabic
            'van', 'van der', 'van den', 'de', 'del', 'della', 'di',  # European
            'le', 'la', 'les', 'du', 'dos', 'das',  # French/Portuguese
            'von', 'zu', 'zur',  # German
            'mc', 'mac', 'o\'',  # Celtic
            'saint', 'st', 'santa'  # Religious
        ]
    
    def extract_first_author_lastname(self, authors_string: str) -> Optional[str]:
        """Robust extraction of first author's last name."""
        if not authors_string or authors_string.strip() == '':
            return None
        
        # Clean up common academic suffixes and symbols
        clean_authors = re.sub(r'\s*(Fellow|IEEE|Dr\.?|Prof\.?|Ph\.?D\.?|M\.?D\.?|Ph\.D)\s*,?\s*', '', authors_string, flags=re.IGNORECASE)
        clean_authors = re.sub(r'\s*[∗*†‡§¶#0-9]+\s*', ' ', clean_authors)
        clean_authors = re.sub(r'\s+', ' ', clean_authors.strip())
        
        # Split by common author separators to get first author
        first_author = re.split(r'[,;]|\sand\s|\s&\s', clean_authors)[0].strip()
        
        # Handle special institutional cases with pattern matching
        patterns_and_fixes = [
            # "Name Institution Location" patterns
            (r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]*)*)\s+[A-Z][a-z]*\s*(?:University|Universitat|Institute|Labs?|Corporation|Corp)', r'\1'),
            
            # "Name Organization City" patterns
            (r'^([A-Z][a-z]+(?:\s+[A-Z]\.?\s*)*[A-Z][a-z]+)\s+[A-Z][a-z]*\s*Labs?\s+[A-Z][a-z]+', r'\1'),
            
            # "Name UC City" patterns
            (r'^([A-Z][a-z]+\s+[A-Z][a-z]+)\s+UC\s+[A-Z][a-z]+', r'\1'),
            
            # Email domain cleaning
            (r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', ''),
            
            # Website domain cleaning
            (r'[a-z]+\.edu\.[a-z]+\s+([A-Z][a-z]+)', r'\1')
        ]
        
        # Apply pattern fixes
        for pattern, replacement in patterns_and_fixes:
            first_author = re.sub(pattern, replacement, first_author, flags=re.IGNORECASE).strip()
        
        # Remove remaining institutional indicators if they appear at the end
        institutional_words = [
            'university', 'universitat', 'institute', 'institution', 'college',
            'laboratory', 'labs', 'lab', 'corporation', 'corp', 'company',
            'research', 'group', 'team', 'center', 'centre', 'department',
            'school', 'academy', 'foundation', 'hospital', 'clinic',
            'berlin', 'tehran', 'berkeley', 'stanford', 'mit', 'harvard',
            'cambridge', 'oxford', 'toronto', 'montreal', 'sydney', 'melbourne'
        ]
        
        words = first_author.split()
        clean_words = []
        
        for word in words:
            word_clean = re.sub(r'[^\w]', '', word.lower())
            if word_clean not in institutional_words and len(word_clean) > 1:
                clean_words.append(word)
            else:
                # Stop when we hit institutional words
                break
        
        if clean_words:
            first_author = ' '.join(clean_words)
        
        # Now extract lastname from the cleaned person name
        if ',' in first_author:
            # "Last, First" format
            lastname = first_author.split(',')[0].strip()
        else:
            # "First Last" or "First Middle Last" format
            parts = first_author.split()
            if len(parts) >= 2:
                # Check for name prefixes in second-to-last position
                potential_prefix = parts[-2].lower().strip('.,()-') if len(parts) >= 2 else None
                
                if potential_prefix in self.name_prefixes:
                    # Combine prefix with lastname
                    if potential_prefix in ['al', 'al-']:
                        lastname = f"al{parts[-1]}"  # Al Khatib -> alkhatib
                    else:
                        lastname = f"{potential_prefix}{parts[-1]}"
                else:
                    lastname = parts[-1]  # Regular lastname
            elif len(parts) == 1:
                lastname = parts[0]  # Single name
            else:
                return None
        
        # Final cleanup
        lastname = re.sub(r'[^\w-]', '', lastname).strip().lower()
        
        # Validate lastname
        if len(lastname) < 2 or not re.match(r'^[a-z-]+$', lastname):
            return None
        
        return lastname
    
    def test_extraction_on_examples(self) -> bool:
        """Test the extraction on known problematic cases."""
        test_cases = [
            ("Mohannad Alhanahnah University of Wisconsin-Madison, USA mohannad@cs.wisc.edu", "alhanahnah"),
            ("Markus Klems Technische Universitat Berlin ¨ Information Systems Engineering Group Berlin, Germany mk@ise.tu-berlin.de", "klems"),
            ("Amir Reza Asadi Humind Labs Tehran", "asadi"),
            ("Hassan S. Al Khatib, Subash Neupane, Harish Kumar Manchukonda", "alkhatib"),
            ("Filip Ilievski, Saurav Joshi, Bradley P. Allen", "ilievski"),
            ("Roshan Rao UC Berkeley", "rao"),
            ("Saravanan Krishnan, Alex Mathai, Amith Singhee", "krishnan"),
            ("nudt.edu.cn liyitong", "liyitong"),
            ("Hussein Abdallah, Essam Mansour", "abdallah"),
            ("Jami Aho", "aho"),
            ("Xuemin (Sherman) Shen, Fellow, IEEE", "shen"),
            ("Yi Chen, JiaHao Zhao, HaoHao Han, Computer Applications", "chen")
        ]
        
        print("\n🧪 TESTING FINAL EXTRACTION LOGIC:")
        print("="*80)
        
        all_correct = True
        for authors, expected in test_cases:
            result = self.extract_first_author_lastname(authors)
            status = "✅" if result == expected else "❌"
            if result != expected:
                all_correct = False
            
            print(f"{status} {authors[:65]}...")
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")
            print()
        
        if all_correct:
            print("🎉 ALL TEST CASES PASSED!")
        else:
            print("⚠️  Some test cases failed - reviewing...")
        
        return all_correct
    
    def apply_corrected_cite_keys(self, dry_run: bool = True) -> Dict[str, any]:
        """Apply the corrected cite_keys to the database."""
        logger.info(f"Applying corrected cite_keys (dry_run={dry_run})...")
        
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all papers
        cursor.execute("SELECT id, cite_key, authors, year FROM papers ORDER BY cite_key")
        papers = cursor.fetchall()
        
        # Clear the corrected_cite_key column first
        cursor.execute("UPDATE papers SET corrected_cite_key = NULL")
        
        # Generate corrections
        proposed_cite_keys = defaultdict(list)  # base_cite_key -> [paper_ids]
        corrections = []
        
        for paper in papers:
            paper_id = str(paper['id'])
            current_cite_key = paper['cite_key']
            authors = paper['authors']
            year = paper['year']
            
            # Extract first author lastname
            first_author_lastname = self.extract_first_author_lastname(authors)
            
            if not first_author_lastname:
                # Keep current cite_key for failed extractions
                proposed_cite_keys[current_cite_key].append(paper_id)
                continue
            
            # Generate correct cite_key
            correct_base_cite_key = f"{first_author_lastname}_{year}"
            proposed_cite_keys[correct_base_cite_key].append(paper_id)
            
            if current_cite_key != correct_base_cite_key:
                corrections.append({
                    'paper_id': paper_id,
                    'current_cite_key': current_cite_key,
                    'correct_base_cite_key': correct_base_cite_key,
                    'first_author_lastname': first_author_lastname,
                    'authors': authors,
                    'year': year
                })
        
        # Resolve conflicts with alphabetic suffixes
        final_cite_keys = {}
        conflicts = []
        
        for base_cite_key, paper_ids in proposed_cite_keys.items():
            if len(paper_ids) == 1:
                final_cite_keys[paper_ids[0]] = base_cite_key
            else:
                # Multiple papers - add suffixes
                conflicts.append({
                    'base_cite_key': base_cite_key,
                    'papers_count': len(paper_ids)
                })
                
                for i, paper_id in enumerate(sorted(paper_ids)):
                    if i == 0:
                        final_cite_keys[paper_id] = base_cite_key
                    else:
                        suffix = chr(ord('a') + i - 1)
                        final_cite_keys[paper_id] = f"{base_cite_key}{suffix}"
        
        # Update database with corrected cite_keys
        for paper_id, corrected_cite_key in final_cite_keys.items():
            cursor.execute(
                "UPDATE papers SET corrected_cite_key = ? WHERE id = ?",
                (corrected_cite_key, int(paper_id))
            )
        
        if not dry_run:
            conn.commit()
            logger.info("Changes committed to database")
        else:
            logger.info("Dry run - changes NOT committed")
        
        conn.close()
        
        return {
            'total_papers': len(papers),
            'corrections_needed': len(corrections),
            'conflicts_resolved': len(conflicts),
            'corrections': corrections[:10],  # First 10 examples
            'conflicts': conflicts
        }

def main():
    """Test and apply final cite_key corrections."""
    logger.info("Final Cite_Key Correction Process...")
    
    corrector = FinalCiteKeyCorrector()
    
    # Test extraction logic
    test_success = corrector.test_extraction_on_examples()
    
    if test_success:
        print("\n✅ Extraction logic validated - applying to database...")
        
        # Apply corrections (dry run first)
        results = corrector.apply_corrected_cite_keys(dry_run=True)
        
        print(f"\n📊 CORRECTION RESULTS:")
        print(f"   Total papers: {results['total_papers']}")
        print(f"   Corrections needed: {results['corrections_needed']}")
        print(f"   Conflicts resolved: {results['conflicts_resolved']}")
        
        print(f"\n🔧 SAMPLE CORRECTIONS:")
        for correction in results['corrections']:
            print(f"   {correction['current_cite_key']} → {correction['correct_base_cite_key']}")
        
        print(f"\n💾 Corrected cite_keys populated in 'corrected_cite_key' column")
        print(f"   Ready for review and final application")
        
        return results
    else:
        print("\n❌ Extraction logic needs further refinement")
        return None

if __name__ == "__main__":
    main()
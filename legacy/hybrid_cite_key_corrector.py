#!/usr/bin/env python3
"""
Hybrid cite_key corrector with manual overrides for edge cases.
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

class HybridCiteKeyCorrector:
    """Hybrid approach: improved logic + manual overrides for edge cases."""
    
    def __init__(self):
        # Manual overrides for problematic cases (cite_key -> correct_cite_key)
        self.manual_overrides = {
            # Institution contamination cases
            'kuhlenkamp_2014': 'klems_2014',  # Markus Klems Technische Universitat Berlin
            'asadi_2021': 'asadi_2020',  # Amir Reza Asadi Humind Labs Tehran (also fix year)
            'rao_2019': 'rao_2017',  # Roshan Rao UC Berkeley (also fix year)
            
            # Wrong author cases
            'allen_2018': 'ilievski_2018',  # Filip Ilievski is first author
            'saariluoma_2024': 'aho_2023',  # Jami Aho is author, year is 2023
            'ammar_2023': 'olusanya_2023',  # Olufunto A Olusanya is first author
            
            # Wrong year cases (where author extraction would be correct)
            'abdallah_2023': 'abdallah_2021',  # Hussein Abdallah, year 2021
            'azevedo_2024': 'azevedo_2023',  # Leonardo Guerreiro Azevedo, year 2023
            'bianchini_2023': 'bianchini_2022',  # Devis Bianchini, year 2022
            
            # Special complex cases found from analysis
            'banking_2022': 'krishnan_2022',  # Saravanan Krishnan is first author
            'alatrash_2024': 'alatrash_2023',  # Wrong year
            'bogachov_2018': 'bogachov_2021',  # Wrong year
            'budhdeo_2021': 'budhdeo_2020',  # Wrong year
            'cai_2022': 'cai_2023',  # Wrong year
        }
        
        # Name prefixes to preserve
        self.name_prefixes = ['al', 'al-', 'ibn', 'ben', 'bin', 'abu', 'abd', 
                             'van', 'van der', 'van den', 'de', 'del', 'della', 'di',
                             'le', 'la', 'les', 'du', 'dos', 'das',
                             'von', 'zu', 'zur', 'mc', 'mac', 'o\'']
    
    def extract_first_author_lastname(self, authors_string: str) -> Optional[str]:
        """Extract first author lastname with improved logic."""
        if not authors_string or authors_string.strip() == '':
            return None
        
        # Clean up
        clean_authors = re.sub(r'\s*(Fellow|IEEE|Dr\.?|Prof\.?|Ph\.?D\.?|M\.?D\.?)\s*,?\s*', '', authors_string, flags=re.IGNORECASE)
        clean_authors = re.sub(r'\s*[∗*†‡§¶#0-9]+\s*', ' ', clean_authors)
        clean_authors = re.sub(r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', clean_authors)
        clean_authors = re.sub(r'\s+', ' ', clean_authors.strip())
        
        # Get first author
        first_author = re.split(r'[,;]|\sand\s|\s&\s', clean_authors)[0].strip()
        
        # Handle specific patterns
        if re.match(r'^Mohannad\s+Alhanahnah\s+University', first_author, re.IGNORECASE):
            return 'alhanahnah'
        
        if re.match(r'^Hassan\s+S\.\s+Al\s+Khatib', first_author, re.IGNORECASE):
            return 'alkhatib'
        
        # Remove institutional contamination
        institutional_words = [
            'university', 'universitat', 'institute', 'laboratory', 'labs', 'lab',
            'corporation', 'corp', 'company', 'research', 'group', 'team',
            'center', 'centre', 'department', 'school', 'academy', 'foundation',
            'technische', 'information', 'systems', 'engineering', 'humind'
        ]
        
        words = first_author.split()
        name_words = []
        
        for word in words:
            word_clean = re.sub(r'[^\w-]', '', word).lower()
            if word_clean in institutional_words:
                break
            if len(word_clean) >= 2 and word_clean.isalpha():
                name_words.append(word)
        
        if not name_words:
            return None
        
        clean_name = ' '.join(name_words)
        
        # Extract lastname
        if ',' in clean_name:
            lastname = clean_name.split(',')[0].strip()
        else:
            parts = clean_name.split()
            if len(parts) >= 2:
                # Handle name prefixes
                potential_prefix = parts[-2].lower() if len(parts) >= 2 else None
                if potential_prefix in self.name_prefixes:
                    if potential_prefix in ['al', 'al-']:
                        lastname = f"al{parts[-1]}"
                    else:
                        lastname = f"{potential_prefix}{parts[-1]}"
                else:
                    lastname = parts[-1]
            else:
                lastname = parts[0]
        
        # Clean and validate
        lastname = re.sub(r'[^\w-]', '', lastname).strip().lower()
        return lastname if len(lastname) >= 2 else None
    
    def apply_hybrid_corrections(self, commit_changes: bool = False) -> Dict[str, any]:
        """Apply hybrid corrections: improved logic + manual overrides."""
        logger.info(f"Applying hybrid corrections (commit={commit_changes})...")
        
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all papers
        cursor.execute("SELECT id, cite_key, authors, year FROM papers ORDER BY cite_key")
        papers = cursor.fetchall()
        
        # Clear corrected_cite_key column
        cursor.execute("UPDATE papers SET corrected_cite_key = NULL")
        
        # Generate corrections
        proposed_cite_keys = defaultdict(list)
        manual_corrections = []
        algorithmic_corrections = []
        no_change_needed = []
        
        for paper in papers:
            paper_id = str(paper['id'])
            current_cite_key = paper['cite_key']
            authors = paper['authors']
            year = paper['year']
            
            # Check manual overrides first
            if current_cite_key in self.manual_overrides:
                correct_cite_key = self.manual_overrides[current_cite_key]
                proposed_cite_keys[correct_cite_key].append(paper_id)
                manual_corrections.append({
                    'paper_id': paper_id,
                    'current': current_cite_key,
                    'corrected': correct_cite_key,
                    'method': 'manual_override',
                    'authors': authors[:80]
                })
                continue
            
            # Use improved algorithm
            first_author_lastname = self.extract_first_author_lastname(authors)
            
            if first_author_lastname:
                correct_cite_key = f"{first_author_lastname}_{year}"
                proposed_cite_keys[correct_cite_key].append(paper_id)
                
                if current_cite_key != correct_cite_key:
                    algorithmic_corrections.append({
                        'paper_id': paper_id,
                        'current': current_cite_key,
                        'corrected': correct_cite_key,
                        'method': 'algorithm',
                        'author_extracted': first_author_lastname,
                        'authors': authors[:80]
                    })
                else:
                    no_change_needed.append(paper_id)
            else:
                # Keep current cite_key if extraction fails
                proposed_cite_keys[current_cite_key].append(paper_id)
                no_change_needed.append(paper_id)
        
        # Resolve conflicts with suffixes
        final_cite_keys = {}
        conflicts = []
        
        for base_cite_key, paper_ids in proposed_cite_keys.items():
            if len(paper_ids) == 1:
                final_cite_keys[paper_ids[0]] = base_cite_key
            else:
                conflicts.append({
                    'base': base_cite_key,
                    'count': len(paper_ids),
                    'paper_ids': paper_ids
                })
                
                for i, paper_id in enumerate(sorted(paper_ids)):
                    if i == 0:
                        final_cite_keys[paper_id] = base_cite_key
                    else:
                        suffix = chr(ord('a') + i - 1)
                        final_cite_keys[paper_id] = f"{base_cite_key}{suffix}"
        
        # Update database
        for paper_id, corrected_cite_key in final_cite_keys.items():
            cursor.execute(
                "UPDATE papers SET corrected_cite_key = ? WHERE id = ?",
                (corrected_cite_key, int(paper_id))
            )
        
        if commit_changes:
            conn.commit()
            logger.info("✅ Changes committed to database")
        else:
            logger.info("📝 Changes prepared but NOT committed")
        
        conn.close()
        
        return {
            'total_papers': len(papers),
            'manual_corrections': len(manual_corrections),
            'algorithmic_corrections': len(algorithmic_corrections),
            'no_change_needed': len(no_change_needed),
            'conflicts_resolved': len(conflicts),
            'sample_manual': manual_corrections[:10],
            'sample_algorithmic': algorithmic_corrections[:10],
            'conflicts': conflicts
        }

def main():
    """Execute hybrid cite_key correction."""
    logger.info("Hybrid Cite_Key Correction Process...")
    
    corrector = HybridCiteKeyCorrector()
    
    # Apply corrections
    results = corrector.apply_hybrid_corrections(commit_changes=False)
    
    print(f"\n📊 HYBRID CORRECTION SUMMARY:")
    print(f"="*60)
    print(f"Total papers: {results['total_papers']}")
    print(f"Manual overrides applied: {results['manual_corrections']}")
    print(f"Algorithmic corrections: {results['algorithmic_corrections']}")
    print(f"No change needed: {results['no_change_needed']}")
    print(f"Conflicts resolved: {results['conflicts_resolved']}")
    
    total_corrections = results['manual_corrections'] + results['algorithmic_corrections']
    accuracy = ((results['total_papers'] - total_corrections) / results['total_papers']) * 100
    print(f"Current accuracy: {accuracy:.1f}% (before corrections)")
    
    print(f"\n🔧 MANUAL OVERRIDES (first 10):")
    for correction in results['sample_manual']:
        print(f"   {correction['current']} → {correction['corrected']}")
        print(f"     {correction['authors']}...")
    
    print(f"\n🤖 ALGORITHMIC CORRECTIONS (first 10):")
    for correction in results['sample_algorithmic']:
        print(f"   {correction['current']} → {correction['corrected']}")
        print(f"     Author: {correction['author_extracted']}")
        print(f"     {correction['authors']}...")
    
    if results['conflicts']:
        print(f"\n⚡ CONFLICTS RESOLVED:")
        for conflict in results['conflicts'][:5]:
            print(f"   {conflict['base']}: {conflict['count']} papers")
    
    print(f"\n💾 'corrected_cite_key' column populated with hybrid approach")
    print(f"   Manual overrides for edge cases + improved algorithm")
    print(f"   Ready for final review and application")
    
    # Save detailed report
    with open('hybrid_cite_key_corrections.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"📄 Detailed report saved to: hybrid_cite_key_corrections.json")
    
    return results

if __name__ == "__main__":
    main()
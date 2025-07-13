#!/usr/bin/env python3
"""
Investigate authors with questionable information that might need updating.
"""

import sqlite3
import re
import logging
from typing import List, Dict, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuestionableAuthorsInvestigator:
    """Investigate and identify potentially questionable author information."""
    
    def __init__(self):
        pass
    
    def find_suspicious_patterns(self) -> Dict[str, List]:
        """Find authors with suspicious patterns that need investigation."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        suspicious_cases = {
            'single_names': [],
            'unusual_formatting': [],
            'potential_institutions': [],
            'very_short_names': [],
            'numbers_or_symbols': [],
            'inconsistent_with_csv': [],
            'potential_typos': [],
            'cite_key_mismatch': []
        }
        
        # Get all papers with authors
        cursor.execute("""
            SELECT cite_key, title, authors, csv_original_authors, corrected_cite_key, year
            FROM papers 
            WHERE authors IS NOT NULL 
            AND authors != '' 
            AND authors != 'Authors unknown'
            ORDER BY cite_key
        """)
        
        papers = cursor.fetchall()
        
        for paper in papers:
            cite_key = paper['cite_key']
            title = paper['title'] or 'NO TITLE'
            authors = paper['authors']
            csv_authors = paper['csv_original_authors']
            corrected_cite_key = paper['corrected_cite_key']
            year = paper['year']
            
            # Check for single names (might be incomplete)
            if self.has_single_names(authors):
                suspicious_cases['single_names'].append({
                    'cite_key': cite_key,
                    'authors': authors,
                    'csv_authors': csv_authors,
                    'issue': 'Contains single names without surnames'
                })
            
            # Check for unusual formatting
            if self.has_unusual_formatting(authors):
                suspicious_cases['unusual_formatting'].append({
                    'cite_key': cite_key,
                    'authors': authors,
                    'csv_authors': csv_authors,
                    'issue': 'Unusual punctuation or formatting'
                })
            
            # Check for potential institution names
            if self.has_potential_institutions(authors):
                suspicious_cases['potential_institutions'].append({
                    'cite_key': cite_key,
                    'authors': authors,
                    'csv_authors': csv_authors,
                    'issue': 'May contain institutional information'
                })
            
            # Check for very short names
            if self.has_very_short_names(authors):
                suspicious_cases['very_short_names'].append({
                    'cite_key': cite_key,
                    'authors': authors,
                    'csv_authors': csv_authors,
                    'issue': 'Contains very short or abbreviated names'
                })
            
            # Check for numbers or unusual symbols
            if self.has_numbers_or_symbols(authors):
                suspicious_cases['numbers_or_symbols'].append({
                    'cite_key': cite_key,
                    'authors': authors,
                    'csv_authors': csv_authors,
                    'issue': 'Contains numbers or unusual symbols'
                })
            
            # Check if significantly different from CSV
            if csv_authors and self.is_inconsistent_with_csv(authors, csv_authors):
                suspicious_cases['inconsistent_with_csv'].append({
                    'cite_key': cite_key,
                    'authors': authors,
                    'csv_authors': csv_authors,
                    'issue': 'Significantly different from CSV reference'
                })
            
            # Check for potential typos
            if self.has_potential_typos(authors):
                suspicious_cases['potential_typos'].append({
                    'cite_key': cite_key,
                    'authors': authors,
                    'csv_authors': csv_authors,
                    'issue': 'May contain typos or formatting errors'
                })
            
            # Check if cite_key doesn't match first author
            if corrected_cite_key and self.cite_key_mismatch(authors, corrected_cite_key, year):
                suspicious_cases['cite_key_mismatch'].append({
                    'cite_key': cite_key,
                    'authors': authors,
                    'corrected_cite_key': corrected_cite_key,
                    'csv_authors': csv_authors,
                    'issue': 'First author doesn\'t match corrected cite_key'
                })
        
        conn.close()
        return suspicious_cases
    
    def has_single_names(self, authors: str) -> bool:
        """Check if authors contains single names without surnames."""
        if not authors:
            return False
        
        author_list = [name.strip() for name in authors.split(',')]
        for author in author_list:
            # Clean the name
            clean_name = re.sub(r'[^\w\s-]', '', author).strip()
            parts = clean_name.split()
            
            # If it's just one word and not obviously an initial
            if len(parts) == 1 and len(parts[0]) > 2 and not parts[0].isupper():
                return True
        
        return False
    
    def has_unusual_formatting(self, authors: str) -> bool:
        """Check for unusual formatting patterns."""
        if not authors:
            return False
        
        # Check for unusual patterns
        patterns = [
            r'[^\w\s,.-]',  # Unusual characters
            r'\s{2,}',      # Multiple spaces
            r',,+',         # Multiple commas
            r'^[,\s]+',     # Starting with comma/space
            r'[,\s]+$',     # Ending with comma/space
            r'\d+$',        # Ending with numbers
            r'^-\s',        # Starting with dash
        ]
        
        for pattern in patterns:
            if re.search(pattern, authors):
                return True
        
        return False
    
    def has_potential_institutions(self, authors: str) -> bool:
        """Check if authors might contain institutional information."""
        if not authors:
            return False
        
        institutional_keywords = [
            'university', 'college', 'institute', 'laboratory', 'research',
            'department', 'school', 'center', 'centre', 'foundation',
            'corporation', 'company', 'group', 'team', 'division'
        ]
        
        authors_lower = authors.lower()
        for keyword in institutional_keywords:
            if keyword in authors_lower:
                return True
        
        return False
    
    def has_very_short_names(self, authors: str) -> bool:
        """Check for very short or abbreviated names."""
        if not authors:
            return False
        
        author_list = [name.strip() for name in authors.split(',')]
        for author in author_list:
            clean_name = re.sub(r'[^\w\s]', '', author).strip()
            if len(clean_name) < 3:  # Very short names
                return True
            
            # Check for names that are mostly initials
            words = clean_name.split()
            if len(words) >= 2:
                initial_count = sum(1 for word in words if len(word) <= 2 and word.isupper())
                if initial_count / len(words) > 0.5:  # More than half are initials
                    return True
        
        return False
    
    def has_numbers_or_symbols(self, authors: str) -> bool:
        """Check for numbers or unusual symbols in author names."""
        if not authors:
            return False
        
        # Check for numbers (except in names like "John Smith II")
        if re.search(r'\d', authors) and not re.search(r'\b(II|III|IV|Jr|Sr|2nd|3rd)\b', authors):
            return True
        
        # Check for unusual symbols
        unusual_symbols = ['@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '{', '}', '|', '\\', '/', '?', '<', '>']
        for symbol in unusual_symbols:
            if symbol in authors:
                return True
        
        return False
    
    def is_inconsistent_with_csv(self, authors: str, csv_authors: str) -> bool:
        """Check if authors are significantly different from CSV reference."""
        if not authors or not csv_authors:
            return False
        
        # Normalize both strings for comparison
        def normalize(text):
            return re.sub(r'[^\w\s]', '', text.lower()).strip()
        
        norm_authors = normalize(authors)
        norm_csv = normalize(csv_authors)
        
        # If they're very different in length
        if abs(len(norm_authors) - len(norm_csv)) > max(len(norm_authors), len(norm_csv)) * 0.5:
            return True
        
        # If they share very few common words
        words_authors = set(norm_authors.split())
        words_csv = set(norm_csv.split())
        
        if len(words_authors) > 0 and len(words_csv) > 0:
            overlap = len(words_authors.intersection(words_csv))
            total_unique = len(words_authors.union(words_csv))
            similarity = overlap / total_unique
            
            if similarity < 0.3:  # Less than 30% similarity
                return True
        
        return False
    
    def has_potential_typos(self, authors: str) -> bool:
        """Check for potential typos or formatting errors."""
        if not authors:
            return False
        
        # Check for common typo patterns
        typo_patterns = [
            r'[a-z][A-Z]',  # Missing space between words
            r'\w{15,}',     # Very long words (might be concatenated)
            r'[A-Z]{4,}',   # Long sequences of capitals
            r'\s[a-z]\s',   # Single lowercase letters (might be formatting errors)
        ]
        
        for pattern in typo_patterns:
            if re.search(pattern, authors):
                return True
        
        return False
    
    def cite_key_mismatch(self, authors: str, corrected_cite_key: str, year: int) -> bool:
        """Check if the first author doesn't match the corrected cite_key."""
        if not authors or not corrected_cite_key:
            return False
        
        # Extract expected lastname from cite_key
        parts = corrected_cite_key.split('_')
        if len(parts) < 2:
            return False
        
        expected_lastname = parts[0].lower()
        expected_year = parts[1]
        
        # Check year mismatch
        if expected_year != str(year):
            return True
        
        # Extract first author's lastname
        first_author = authors.split(',')[0].strip()
        
        # Simple lastname extraction
        name_parts = first_author.split()
        if name_parts:
            actual_lastname = name_parts[-1].lower()
            
            # Remove common suffixes
            actual_lastname = re.sub(r'(jr|sr|ii|iii|iv)$', '', actual_lastname)
            
            # Check if they match
            if actual_lastname != expected_lastname:
                return True
        
        return False
    
    def generate_investigation_report(self, suspicious_cases: Dict) -> None:
        """Generate a detailed investigation report."""
        
        print(f"\n🔍 QUESTIONABLE AUTHORS INVESTIGATION REPORT")
        print(f"=" * 80)
        
        total_issues = sum(len(cases) for cases in suspicious_cases.values())
        print(f"Total questionable cases found: {total_issues}")
        
        for category, cases in suspicious_cases.items():
            if cases:
                print(f"\n⚠️  {category.upper().replace('_', ' ')} ({len(cases)} cases)")
                print("-" * 60)
                
                for i, case in enumerate(cases[:5], 1):  # Show first 5 of each category
                    cite_key = case['cite_key']
                    authors = case['authors']
                    csv_authors = case.get('csv_authors', 'N/A')
                    issue = case['issue']
                    
                    print(f"\n   {i}. 🔑 {cite_key}")
                    print(f"      Issue: {issue}")
                    print(f"      Current: {authors}")
                    if csv_authors and csv_authors != 'N/A':
                        print(f"      CSV Ref: {csv_authors}")
                
                if len(cases) > 5:
                    print(f"\n      ... and {len(cases) - 5} more cases")
    
    def suggest_investigation_priorities(self, suspicious_cases: Dict) -> None:
        """Suggest priorities for manual investigation."""
        
        print(f"\n🎯 INVESTIGATION PRIORITIES")
        print(f"=" * 60)
        
        priorities = [
            ('inconsistent_with_csv', 'HIGH', 'Different from reference data - likely errors'),
            ('cite_key_mismatch', 'HIGH', 'First author doesn\'t match cite_key - affects citations'),
            ('potential_institutions', 'MEDIUM', 'May have institutional contamination'),
            ('numbers_or_symbols', 'MEDIUM', 'Unusual characters suggest extraction errors'),
            ('potential_typos', 'MEDIUM', 'Formatting errors that affect readability'),
            ('single_names', 'LOW', 'Incomplete names but may be accurate'),
            ('unusual_formatting', 'LOW', 'Minor formatting issues'),
            ('very_short_names', 'LOW', 'May be intentionally abbreviated')
        ]
        
        for category, priority, description in priorities:
            count = len(suspicious_cases.get(category, []))
            if count > 0:
                print(f"   {priority:6} | {category:20} | {count:3} cases | {description}")
        
        print(f"\n🔧 RECOMMENDED ACTIONS:")
        print(f"   1. HIGH priority: Manual review and correction")
        print(f"   2. MEDIUM priority: Investigate with Task agent or manual check")
        print(f"   3. LOW priority: Review only if time permits")
        
        print(f"\n🤖 AUTOMATED FIXES POSSIBLE:")
        print(f"   • Remove obvious institutional words")
        print(f"   • Fix common formatting issues")
        print(f"   • Use CSV reference data where available")
        print(f"   • Extract clean names from paper.md files")

def main():
    """Execute questionable authors investigation."""
    logger.info("Investigating questionable author information...")
    
    investigator = QuestionableAuthorsInvestigator()
    
    # Find suspicious patterns
    suspicious_cases = investigator.find_suspicious_patterns()
    
    # Generate report
    investigator.generate_investigation_report(suspicious_cases)
    
    # Suggest priorities
    investigator.suggest_investigation_priorities(suspicious_cases)
    
    # Save detailed report
    import json
    with open('questionable_authors_investigation.json', 'w', encoding='utf-8') as f:
        json.dump(suspicious_cases, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Detailed investigation saved to: questionable_authors_investigation.json")
    print(f"✅ Investigation complete - review priorities above for next steps")

if __name__ == "__main__":
    main()
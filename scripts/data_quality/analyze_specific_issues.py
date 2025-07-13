#!/usr/bin/env python3
"""
Analyze specific author issues and find duplicate papers.
"""

import sqlite3
import json
import logging
from typing import List, Dict, Tuple
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpecificIssuesAnalyzer:
    """Analyze specific author issues and duplicates."""
    
    def __init__(self):
        pass
    
    def analyze_specific_papers(self, cite_keys: List[str]) -> Dict:
        """Analyze specific papers mentioned by user."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        results = {}
        
        for cite_key in cite_keys:
            cursor.execute("""
                SELECT cite_key, title, authors, csv_original_authors, corrected_cite_key, year
                FROM papers 
                WHERE cite_key = ? OR corrected_cite_key = ?
                ORDER BY cite_key
            """, (cite_key, cite_key))
            
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    results[cite_key] = {
                        'cite_key': row['cite_key'],
                        'corrected_cite_key': row['corrected_cite_key'],
                        'title': row['title'],
                        'authors': row['authors'],
                        'csv_original_authors': row['csv_original_authors'],
                        'year': row['year'],
                        'status': 'found'
                    }
            else:
                results[cite_key] = {'status': 'not_found'}
        
        conn.close()
        return results
    
    def find_duplicates(self) -> Dict:
        """Find potential duplicate papers."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all papers
        cursor.execute("""
            SELECT cite_key, title, authors, csv_original_authors, corrected_cite_key, year, doi, url
            FROM papers 
            ORDER BY cite_key
        """)
        
        papers = cursor.fetchall()
        
        # Find duplicates by different criteria
        duplicates = {
            'by_title': defaultdict(list),
            'by_doi': defaultdict(list),
            'by_corrected_cite_key': defaultdict(list),
            'by_similar_title': defaultdict(list)
        }
        
        # Group by exact title
        for paper in papers:
            title = paper['title']
            if title and title.strip():
                clean_title = title.lower().strip()
                duplicates['by_title'][clean_title].append(dict(paper))
        
        # Group by DOI
        for paper in papers:
            doi = paper['doi']
            if doi and doi.strip() and doi != 'N/A':
                duplicates['by_doi'][doi].append(dict(paper))
        
        # Group by corrected cite_key conflicts
        corrected_cite_keys = defaultdict(list)
        for paper in papers:
            corrected = paper['corrected_cite_key']
            if corrected:
                corrected_cite_keys[corrected].append(dict(paper))
        
        # Find actual duplicates (more than one paper per group)
        actual_duplicates = {}
        
        for group_type, groups in duplicates.items():
            actual_duplicates[group_type] = {
                key: papers_list for key, papers_list in groups.items() 
                if len(papers_list) > 1
            }
        
        # Add corrected cite_key conflicts
        actual_duplicates['by_corrected_cite_key'] = {
            key: papers_list for key, papers_list in corrected_cite_keys.items()
            if len(papers_list) > 1
        }
        
        conn.close()
        return actual_duplicates
    
    def find_papers_with_no_authors(self) -> List[Dict]:
        """Find papers with missing or empty authors."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cite_key, title, authors, csv_original_authors, corrected_cite_key
            FROM papers 
            WHERE authors IS NULL 
               OR authors = '' 
               OR authors = 'N/A'
               OR authors = 'unavailable'
               OR LENGTH(TRIM(authors)) < 3
            ORDER BY cite_key
        """)
        
        no_authors = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return no_authors
    
    def generate_comprehensive_report(self) -> None:
        """Generate comprehensive report of all issues."""
        
        # Papers mentioned by user that need attention
        attention_needed = [
            'challenges_2021', 'isws_2019', 'ramal_2024', 'hijazi_2023', 
            'kim_2016', 'klems_2014', 'koutsoubisa_2017', 'kraska_2009',
            'leskinen_2015', 'chen_2023c', 'posillico_2024', 'mandal_2024',
            'dragoni_2023', 'humana_2023', 'charles_2022'
        ]
        
        # Papers mentioned as "more correct"
        more_correct = [
            'fu_2023', 'cudré-mauroux_2020', 'prahlad_2025', 'hendawi_2024',
            'geng_2014', 'schöpfeld_2019', 'tamasauskait_2023', 'sowinski_2024',
            'driskell_2021', 'khorashadizadeh_2024', 'papachristou_2024',
            'chang_2025', 'buzi_2024', 'schmitt_2020', 'wickramarachchi_2021',
            'kessel_2024', 'yang_2025'
        ]
        
        print(f"\n📋 COMPREHENSIVE ISSUES ANALYSIS")
        print(f"=" * 80)
        
        # Analyze specific papers needing attention
        print(f"\n⚠️  PAPERS REQUIRING ATTENTION:")
        print("-" * 60)
        attention_results = self.analyze_specific_papers(attention_needed)
        
        for cite_key in attention_needed:
            result = attention_results.get(cite_key, {})
            if result.get('status') == 'found':
                authors = result['authors'] or 'NO AUTHORS'
                csv_authors = result['csv_original_authors'] or 'NO CSV AUTHORS'
                print(f"\n🔑 {cite_key}")
                print(f"   Title: {result['title'][:80]}...")
                print(f"   Current Authors: {authors}")
                print(f"   CSV Authors: {csv_authors}")
                
                if not result['authors'] or len(result['authors'].strip()) < 3:
                    print(f"   ❌ MISSING AUTHORS")
            else:
                print(f"\n🔑 {cite_key} - NOT FOUND IN DATABASE")
        
        # Analyze "more correct" papers
        print(f"\n✅ PAPERS MARKED AS 'MORE CORRECT':")
        print("-" * 60)
        correct_results = self.analyze_specific_papers(more_correct)
        
        for cite_key in more_correct:
            result = correct_results.get(cite_key, {})
            if result.get('status') == 'found':
                corrected = result['corrected_cite_key']
                status = "CORRECTED" if corrected != result['cite_key'] else "UNCHANGED"
                print(f"\n🔑 {cite_key} → {corrected} ({status})")
                print(f"   Authors: {result['authors'] or 'NO AUTHORS'}")
            else:
                print(f"\n🔑 {cite_key} - NOT FOUND")
        
        # Find papers with no authors
        print(f"\n👤 PAPERS WITH MISSING AUTHORS:")
        print("-" * 60)
        no_authors = self.find_papers_with_no_authors()
        
        for paper in no_authors[:15]:  # Show first 15
            cite_key = paper['cite_key']
            title = paper['title'][:50] + "..." if paper['title'] else "NO TITLE"
            csv_authors = paper['csv_original_authors'] or "NO CSV AUTHORS"
            
            print(f"\n🔑 {cite_key}")
            print(f"   Title: {title}")
            print(f"   CSV Authors: {csv_authors}")
        
        if len(no_authors) > 15:
            print(f"\n   ... and {len(no_authors) - 15} more papers with missing authors")
        
        # Find duplicates
        print(f"\n🔄 DUPLICATE PAPERS ANALYSIS:")
        print("-" * 60)
        duplicates = self.find_duplicates()
        
        for dup_type, groups in duplicates.items():
            if groups:
                print(f"\n📊 {dup_type.upper().replace('_', ' ')}: {len(groups)} groups")
                
                for group_key, papers in list(groups.items())[:5]:  # Show first 5 groups
                    print(f"\n   Group: {group_key[:60]}...")
                    for paper in papers:
                        cite_key = paper['cite_key']
                        corrected = paper['corrected_cite_key']
                        print(f"      • {cite_key} → {corrected}")
                
                if len(groups) > 5:
                    print(f"      ... and {len(groups) - 5} more duplicate groups")
        
        # Save detailed report
        report_data = {
            'attention_needed': attention_results,
            'more_correct': correct_results,
            'missing_authors': no_authors,
            'duplicates': duplicates,
            'summary': {
                'attention_papers': len(attention_needed),
                'more_correct_papers': len(more_correct),
                'missing_authors_count': len(no_authors),
                'duplicate_groups': {k: len(v) for k, v in duplicates.items()}
            }
        }
        
        with open('comprehensive_issues_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Detailed report saved to: comprehensive_issues_report.json")
    
    def find_shen_2020_duplicates(self) -> None:
        """Specifically look for shen_2020 duplicates."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cite_key, title, authors, csv_original_authors, corrected_cite_key, year
            FROM papers 
            WHERE cite_key LIKE 'shen_2020%' OR corrected_cite_key LIKE 'shen_2020%'
            ORDER BY cite_key
        """)
        
        shen_papers = cursor.fetchall()
        
        print(f"\n🔍 SHEN 2020 PAPERS ANALYSIS:")
        print("-" * 60)
        
        for paper in shen_papers:
            cite_key = paper['cite_key']
            corrected = paper['corrected_cite_key']
            title = paper['title'][:60] + "..." if paper['title'] else "NO TITLE"
            authors = paper['authors'] or "NO AUTHORS"
            
            print(f"\n🔑 {cite_key} → {corrected}")
            print(f"   Title: {title}")
            print(f"   Authors: {authors}")
        
        conn.close()

def main():
    """Execute comprehensive issues analysis."""
    logger.info("Comprehensive Issues Analysis...")
    
    analyzer = SpecificIssuesAnalyzer()
    
    # Generate comprehensive report
    analyzer.generate_comprehensive_report()
    
    # Specific analysis for shen_2020 duplicates
    analyzer.find_shen_2020_duplicates()
    
    print(f"\n✅ Comprehensive analysis complete")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Fix critical author and duplicate issues identified.
"""

import sqlite3
import json
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CriticalIssuesFixer:
    """Fix critical author and duplicate issues."""
    
    def __init__(self):
        self.fixes = {
            # Papers with wrong data extraction
            'challenges_2021': {
                'correct_authors': 'Xin Peng, Chong Wang, Mingwei Li',
                'issue': 'extracted_summary_instead_of_authors'
            },
            'isws_2019': {
                'correct_authors': 'A Technical Report from ISWS',
                'issue': 'technical_report_no_specific_authors'
            },
            'chen_2023c': {
                'correct_authors': 'Li Yitong',
                'issue': 'email_extraction_error'
            },
            'fu_2023': {
                'correct_authors': 'Weihao Fu, et al.',
                'issue': 'differential_privacy_text_extracted'
            },
            'cudré-mauroux_2020': {
                'correct_authors': 'Philippe Cudré-Mauroux',
                'issue': 'correct_extraction'
            },
            'hendawi_2024': {
                'correct_authors': 'Rasha Hendawi',
                'issue': 'email_prefix_extraction'
            },
            'geng_2014': {
                'correct_authors': 'Rushan Geng, Cuicui Luo',
                'issue': 'name_concatenation_error'
            },
            'driskell_2021': {
                'correct_authors': 'Tripp Driskell, Eduardo Salas, C. Shawn Burke, James E. Driskell',
                'issue': 'correct_extraction'
            },
            'papachristou_2024': {
                'correct_authors': 'Panagiotis Papachristou, et al.',
                'issue': 'abbreviation_extraction_error'
            },
            'chang_2025': {
                'correct_authors': 'Jee Suk Chang',
                'issue': 'check_for_updates_prefix_error'
            },
            'buzi_2024': {
                'correct_authors': 'Unknown - Check for updates prefix',
                'issue': 'no_clear_authors_identified'
            },
            'kessel_2024': {
                'correct_authors': 'Marcus Kessel',
                'issue': 'additional_keywords_prefix_error'
            }
        }
    
    def get_all_problematic_papers(self) -> List[Dict]:
        """Get papers with clearly problematic author extractions."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Find papers with obvious extraction errors
        cursor.execute("""
            SELECT cite_key, title, authors, csv_original_authors, corrected_cite_key
            FROM papers 
            WHERE 
                -- Authors field contains non-author text
                authors LIKE '%check for updates%' OR
                authors LIKE '%additional key words%' OR
                authors LIKE '%.edu.%' OR
                authors LIKE '%university%' OR
                authors LIKE '%differential privacy%' OR
                authors LIKE '%@%' OR
                authors LIKE '%systems group%' OR
                authors LIKE '%digital humanities%' OR
                authors LIKE '%mechatronic engineering%' OR
                authors LIKE '%his majesty%' OR
                authors LIKE '%.surnam%' OR
                -- Very long author fields (likely extracted abstracts)
                LENGTH(authors) > 200 OR
                -- Authors field is null/empty but should have authors
                (authors IS NULL OR authors = '' OR authors = 'N/A') AND title IS NOT NULL
            ORDER BY cite_key
        """)
        
        problematic = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return problematic
    
    def identify_true_duplicates(self) -> List[Dict]:
        """Identify papers that are true duplicates by title and DOI."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Find exact title duplicates
        cursor.execute("""
            SELECT title, COUNT(*) as count, 
                   GROUP_CONCAT(cite_key) as cite_keys,
                   GROUP_CONCAT(corrected_cite_key) as corrected_keys
            FROM papers 
            WHERE title IS NOT NULL AND title != ''
            GROUP BY LOWER(TRIM(title))
            HAVING COUNT(*) > 1
            ORDER BY count DESC
        """)
        
        title_duplicates = []
        for row in cursor.fetchall():
            title_duplicates.append({
                'title': row['title'],
                'count': row['count'],
                'cite_keys': row['cite_keys'].split(','),
                'corrected_keys': row['corrected_keys'].split(','),
                'type': 'title_duplicate'
            })
        
        # Find DOI duplicates
        cursor.execute("""
            SELECT doi, COUNT(*) as count,
                   GROUP_CONCAT(cite_key) as cite_keys,
                   GROUP_CONCAT(title) as titles
            FROM papers 
            WHERE doi IS NOT NULL AND doi != '' AND doi != 'N/A'
            GROUP BY doi
            HAVING COUNT(*) > 1
            ORDER BY count DESC
        """)
        
        doi_duplicates = []
        for row in cursor.fetchall():
            doi_duplicates.append({
                'doi': row['doi'],
                'count': row['count'],
                'cite_keys': row['cite_keys'].split(','),
                'titles': row['titles'].split(','),
                'type': 'doi_duplicate'
            })
        
        conn.close()
        return title_duplicates + doi_duplicates
    
    def fix_author_extractions(self, commit_changes: bool = False) -> Dict:
        """Fix known author extraction issues."""
        logger.info(f"Fixing author extractions (commit={commit_changes})...")
        
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        fixes_applied = 0
        
        for cite_key, fix_data in self.fixes.items():
            correct_authors = fix_data['correct_authors']
            issue_type = fix_data['issue']
            
            # Update the paper
            cursor.execute("""
                UPDATE papers 
                SET authors = ?,
                    yaml_authors = ?
                WHERE cite_key = ?
            """, (correct_authors, correct_authors, cite_key))
            
            if cursor.rowcount > 0:
                fixes_applied += 1
                logger.info(f"Fixed {cite_key}: {issue_type}")
        
        if commit_changes:
            conn.commit()
            logger.info("✅ Author fixes committed")
        else:
            logger.info("📝 Author fixes prepared but NOT committed")
        
        conn.close()
        
        return {
            'fixes_applied': fixes_applied,
            'total_fixes_available': len(self.fixes)
        }
    
    def generate_action_plan(self) -> None:
        """Generate an action plan for all identified issues."""
        print(f"\n📋 CRITICAL ISSUES ACTION PLAN")
        print(f"=" * 80)
        
        # Get problematic papers
        problematic = self.get_all_problematic_papers()
        duplicates = self.identify_true_duplicates()
        
        print(f"\n🚨 IMMEDIATE ISSUES TO FIX:")
        print(f"   • {len(problematic)} papers with bad author extractions")
        print(f"   • {len(duplicates)} duplicate paper groups")
        print(f"   • {len(self.fixes)} papers with prepared fixes")
        
        print(f"\n🔧 PREPARED FIXES:")
        print("-" * 60)
        for cite_key, fix_data in self.fixes.items():
            print(f"   {cite_key}: {fix_data['issue']}")
            print(f"     → {fix_data['correct_authors']}")
        
        print(f"\n🔍 WORST AUTHOR EXTRACTION ERRORS:")
        print("-" * 60)
        for paper in problematic[:10]:  # Show worst 10
            cite_key = paper['cite_key']
            authors = paper['authors'] or 'NO AUTHORS'
            title = paper['title'][:50] + "..." if paper['title'] else "NO TITLE"
            
            print(f"\n   {cite_key}")
            print(f"     Title: {title}")
            print(f"     Bad Authors: {authors[:100]}...")
        
        print(f"\n🔄 TRUE DUPLICATES FOUND:")
        print("-" * 60)
        for dup in duplicates[:10]:  # Show first 10
            if dup['type'] == 'title_duplicate':
                print(f"\n   Title: {dup['title'][:60]}...")
                print(f"     Cite Keys: {', '.join(dup['cite_keys'])}")
            else:
                print(f"\n   DOI: {dup['doi']}")
                print(f"     Cite Keys: {', '.join(dup['cite_keys'])}")
        
        print(f"\n📊 SUMMARY OF ACTIONS NEEDED:")
        print("-" * 60)
        print(f"   1. Apply {len(self.fixes)} prepared author fixes")
        print(f"   2. Manually review {len(problematic) - len(self.fixes)} remaining bad extractions")
        print(f"   3. Decide on duplicate removal strategy for {len(duplicates)} groups")
        print(f"   4. Re-run cite_key correction after author fixes")
        
        # Save detailed report
        report = {
            'prepared_fixes': self.fixes,
            'problematic_papers': problematic,
            'duplicates': duplicates,
            'summary': {
                'prepared_fixes_count': len(self.fixes),
                'problematic_papers_count': len(problematic),
                'duplicates_count': len(duplicates)
            }
        }
        
        with open('critical_issues_action_plan.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Detailed action plan saved to: critical_issues_action_plan.json")
    
    def show_shen_duplicate_details(self) -> None:
        """Show detailed analysis of shen_2020 duplicates."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cite_key, title, authors, csv_original_authors, corrected_cite_key, doi, url
            FROM papers 
            WHERE cite_key LIKE 'shen_%' OR corrected_cite_key LIKE 'shen_%'
            ORDER BY cite_key
        """)
        
        shen_papers = cursor.fetchall()
        
        print(f"\n🔍 SHEN DUPLICATE ANALYSIS:")
        print("-" * 60)
        
        for paper in shen_papers:
            print(f"\n🔑 {paper['cite_key']} → {paper['corrected_cite_key']}")
            print(f"   Title: {paper['title']}")
            print(f"   Authors: {paper['authors']}")
            print(f"   DOI: {paper['doi']}")
            print(f"   URL: {paper['url'][:80]}..." if paper['url'] else "   URL: None")
        
        conn.close()

def main():
    """Execute critical issues fixing."""
    logger.info("Critical Issues Analysis and Fixing...")
    
    fixer = CriticalIssuesFixer()
    
    # Generate comprehensive action plan
    fixer.generate_action_plan()
    
    # Show shen duplicate details
    fixer.show_shen_duplicate_details()
    
    # Apply prepared fixes (dry run first)
    print(f"\n🔧 APPLYING PREPARED AUTHOR FIXES:")
    print("-" * 60)
    results = fixer.fix_author_extractions(commit_changes=False)
    
    print(f"   Fixes applied: {results['fixes_applied']}/{results['total_fixes_available']}")
    print(f"   Run with commit_changes=True to apply fixes")
    
    print(f"\n✅ Critical issues analysis complete")

if __name__ == "__main__":
    main()
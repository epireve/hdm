#!/usr/bin/env python3
"""
Detailed analysis of differences between current authors and CSV original authors.
"""

import sqlite3
import json
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthorDifferenceAnalyzer:
    """Analyze differences between current and CSV original authors."""
    
    def __init__(self):
        pass
    
    def get_all_differences(self) -> List[Dict]:
        """Get all papers with different authors."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cite_key, authors, csv_original_authors, corrected_cite_key
            FROM papers 
            WHERE csv_original_authors IS NOT NULL 
            AND authors != csv_original_authors 
            ORDER BY cite_key
        """)
        
        differences = []
        for row in cursor.fetchall():
            differences.append({
                'cite_key': row['cite_key'],
                'current_authors': row['authors'],
                'csv_original_authors': row['csv_original_authors'],
                'corrected_cite_key': row['corrected_cite_key']
            })
        
        conn.close()
        return differences
    
    def categorize_differences(self, differences: List[Dict]) -> Dict:
        """Categorize the types of differences."""
        categories = {
            'truncated_with_et_al': [],
            'institutional_contamination': [],
            'formatting_differences': [],
            'name_order_differences': [],
            'missing_authors': [],
            'extra_authors': [],
            'other': []
        }
        
        for diff in differences:
            current = diff['current_authors'] or ''
            csv_original = diff['csv_original_authors'] or ''
            cite_key = diff['cite_key']
            
            # Check for et al truncation
            if 'et al' in current.lower() and 'et al' not in csv_original.lower():
                categories['truncated_with_et_al'].append(diff)
            
            # Check for institutional contamination
            elif any(word in current.lower() for word in ['university', 'lab', 'institute', 'corp']):
                categories['institutional_contamination'].append(diff)
            
            # Check if CSV is just much longer (likely more complete)
            elif len(csv_original) > len(current) * 1.5:
                categories['missing_authors'].append(diff)
            
            # Check if current is much longer
            elif len(current) > len(csv_original) * 1.5:
                categories['extra_authors'].append(diff)
            
            # Check for simple formatting differences
            elif current.replace(' ', '').replace(',', '').lower() == csv_original.replace(' ', '').replace(',', '').lower():
                categories['formatting_differences'].append(diff)
            
            else:
                categories['other'].append(diff)
        
        return categories
    
    def generate_detailed_report(self) -> None:
        """Generate a detailed report of author differences."""
        logger.info("Generating detailed author differences report...")
        
        differences = self.get_all_differences()
        categories = self.categorize_differences(differences)
        
        print(f"\n📊 DETAILED AUTHOR DIFFERENCES ANALYSIS")
        print(f"=" * 80)
        print(f"Total differences found: {len(differences)}")
        
        for category, items in categories.items():
            if items:
                print(f"\n🏷️  {category.upper().replace('_', ' ')}: {len(items)} cases")
                print("-" * 60)
                
                for item in items[:5]:  # Show first 5 of each category
                    cite_key = item['cite_key']
                    current = item['current_authors'][:100] + "..." if len(item['current_authors']) > 100 else item['current_authors']
                    csv_orig = item['csv_original_authors'][:100] + "..." if len(item['csv_original_authors']) > 100 else item['csv_original_authors']
                    
                    print(f"\n   🔑 {cite_key}")
                    print(f"      Current:  {current}")
                    print(f"      CSV Orig: {csv_orig}")
                
                if len(items) > 5:
                    print(f"      ... and {len(items) - 5} more cases")
        
        # Save full report to JSON
        report_data = {
            'total_differences': len(differences),
            'categories': {cat: len(items) for cat, items in categories.items()},
            'detailed_differences': differences
        }
        
        with open('author_differences_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Full report saved to: author_differences_report.json")
    
    def show_statistics(self) -> None:
        """Show overall statistics about authors comparison."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get overall statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_papers,
                COUNT(csv_original_authors) as papers_with_csv_authors,
                SUM(CASE WHEN authors = csv_original_authors THEN 1 ELSE 0 END) as identical_authors,
                SUM(CASE WHEN authors != csv_original_authors AND csv_original_authors IS NOT NULL THEN 1 ELSE 0 END) as different_authors,
                SUM(CASE WHEN csv_original_authors IS NULL THEN 1 ELSE 0 END) as missing_csv_authors
            FROM papers
        """)
        
        stats = cursor.fetchone()
        
        print(f"\n📈 OVERALL AUTHOR STATISTICS")
        print(f"=" * 50)
        print(f"Total papers: {stats['total_papers']}")
        print(f"Papers with CSV authors: {stats['papers_with_csv_authors']}")
        print(f"Identical authors: {stats['identical_authors']}")
        print(f"Different authors: {stats['different_authors']}")
        print(f"Missing CSV authors: {stats['missing_csv_authors']}")
        
        if stats['papers_with_csv_authors'] > 0:
            accuracy = (stats['identical_authors'] / stats['papers_with_csv_authors']) * 100
            print(f"Author accuracy: {accuracy:.1f}%")
        
        conn.close()

def main():
    """Execute author difference analysis."""
    logger.info("Author Difference Analysis...")
    
    analyzer = AuthorDifferenceAnalyzer()
    
    # Show overall statistics
    analyzer.show_statistics()
    
    # Generate detailed report
    analyzer.generate_detailed_report()
    
    print(f"\n✅ Analysis complete - check author_differences_report.json for details")

if __name__ == "__main__":
    main()
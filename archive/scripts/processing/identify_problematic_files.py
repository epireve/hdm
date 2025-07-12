#!/usr/bin/env python3
"""
Identify files with problematic cite keys and titles from the CSV.
"""

import csv
import re
from pathlib import Path

def analyze_csv():
    """Analyze the CSV to find problematic entries."""
    problematic_files = []
    
    with open('research_papers_clean.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            cite_key = row['cite_key']
            title = row['title']
            authors = row['authors']
            year = row['year']
            
            issues = []
            
            # Check for problematic cite keys
            if not cite_key or len(cite_key) < 3:
                issues.append("Missing or very short cite_key")
            elif cite_key.startswith('_') or cite_key.startswith('-'):
                issues.append("Cite key starts with underscore or dash")
            elif cite_key.count('_') == 0:
                issues.append("Cite key missing underscore format")
            
            # Check for problematic titles
            if not title or len(title) < 10:
                issues.append("Missing or very short title")
            elif title.startswith(('1.', '2.', '3.', '4.', '5.')):
                issues.append("Title starts with number (likely section heading)")
            elif 'RECEIVED' in title or 'ACCEPTED' in title or 'PUBLISHED' in title:
                issues.append("Title contains publication status text")
            elif title in ['Original Paper', 'RESEARCH ARTICLE', 'Executive Summary']:
                issues.append("Generic title")
            elif '<span' in title or 'id=' in title:
                issues.append("Title contains HTML markup")
            elif len(title) > 200:
                issues.append("Title too long (might be abstract)")
            
            # Check for missing authors
            if not authors or len(authors) < 3:
                issues.append("Missing or very short authors")
            
            # Check for invalid years
            if not year or not year.isdigit() or int(year) < 1990 or int(year) > 2025:
                issues.append(f"Invalid year: {year}")
            
            if issues:
                problematic_files.append({
                    'cite_key': cite_key,
                    'title': title[:80] + "..." if len(title) > 80 else title,
                    'authors': authors[:50] + "..." if len(authors) > 50 else authors,
                    'year': year,
                    'issues': issues
                })
    
    return problematic_files

def find_markdown_file(cite_key):
    """Find the markdown file corresponding to a cite key."""
    base_dir = Path('/Users/invoture/dev.local/hdm/markdown_papers')
    
    # Search for files that might match
    for folder in base_dir.iterdir():
        if folder.is_dir():
            for md_file in folder.glob("*.md"):
                if not md_file.name.endswith('_meta.json'):
                    # Check if this file might correspond to the cite_key
                    # This is approximate since we don't have a direct mapping
                    return md_file
    return None

def main():
    """Main function."""
    problematic_files = analyze_csv()
    
    print("="*80)
    print("PROBLEMATIC FILES ANALYSIS")
    print("="*80)
    print(f"Total problematic entries found: {len(problematic_files)}")
    print()
    
    # Group by type of issue
    issues_count = {}
    for file_info in problematic_files:
        for issue in file_info['issues']:
            issues_count[issue] = issues_count.get(issue, 0) + 1
    
    print("Issues breakdown:")
    for issue, count in sorted(issues_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {count:3d} files: {issue}")
    
    print("\n" + "="*80)
    print("TOP 20 MOST PROBLEMATIC FILES")
    print("="*80)
    
    # Sort by number of issues
    problematic_files.sort(key=lambda x: len(x['issues']), reverse=True)
    
    for i, file_info in enumerate(problematic_files[:20], 1):
        print(f"\n{i:2d}. CITE_KEY: {file_info['cite_key']}")
        print(f"    TITLE: {file_info['title']}")
        print(f"    AUTHORS: {file_info['authors']}")
        print(f"    YEAR: {file_info['year']}")
        print(f"    ISSUES: {', '.join(file_info['issues'])}")
    
    # Save full list to file
    with open('problematic_files_list.txt', 'w', encoding='utf-8') as f:
        f.write("PROBLEMATIC FILES FULL LIST\n")
        f.write("="*50 + "\n\n")
        
        for i, file_info in enumerate(problematic_files, 1):
            f.write(f"{i}. CITE_KEY: {file_info['cite_key']}\n")
            f.write(f"   TITLE: {file_info['title']}\n")
            f.write(f"   AUTHORS: {file_info['authors']}\n")
            f.write(f"   YEAR: {file_info['year']}\n")
            f.write(f"   ISSUES: {', '.join(file_info['issues'])}\n")
            f.write("-" * 50 + "\n")
    
    print(f"\nFull list saved to: problematic_files_list.txt")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Find the specific 4 papers with 'Authors unknown' and 9 papers with minor issues.
"""

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_authors_unknown_papers():
    """Find the 4 papers marked as 'Authors unknown'."""
    conn = sqlite3.connect('hdm_papers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT cite_key, title, authors, csv_original_authors, corrected_cite_key
        FROM papers 
        WHERE authors = 'Authors unknown'
        ORDER BY cite_key
    """)
    
    unknown_papers = cursor.fetchall()
    
    print(f"\n📋 PAPERS WITH 'AUTHORS UNKNOWN' ({len(unknown_papers)} papers)")
    print(f"=" * 80)
    
    for i, paper in enumerate(unknown_papers, 1):
        cite_key = paper['cite_key']
        title = paper['title'] or 'NO TITLE'
        csv_authors = paper['csv_original_authors'] or 'NO CSV AUTHORS'
        corrected_key = paper['corrected_cite_key']
        
        print(f"\n{i}. 🔑 {cite_key} → {corrected_key}")
        print(f"   Title: {title}")
        print(f"   Current Authors: Authors unknown")
        print(f"   CSV Authors: {csv_authors}")
        
        # Check if we have a paper.md file for this
        paper_file_exists = check_paper_file_exists(cite_key)
        print(f"   Paper.md file: {'✅ EXISTS' if paper_file_exists else '❌ NOT FOUND'}")
    
    conn.close()
    return unknown_papers

def find_minor_issues_papers():
    """Find the 9 papers with minor formatting issues."""
    conn = sqlite3.connect('hdm_papers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Find papers with remaining issues
    cursor.execute("""
        SELECT cite_key, title, authors, csv_original_authors, corrected_cite_key
        FROM papers 
        WHERE 
            -- Still has institutional contamination
            (authors LIKE '%university%' OR
             authors LIKE '%institute%' OR
             authors LIKE '%@%' OR
             authors LIKE '%.edu%' OR
             authors LIKE '%laboratory%' OR
             authors LIKE '%department%' OR
             authors LIKE '%corporation%' OR
             LENGTH(authors) > 200) AND
            -- But not marked as unknown
            authors != 'Authors unknown'
        ORDER BY cite_key
    """)
    
    minor_issues = cursor.fetchall()
    
    print(f"\n⚠️  PAPERS WITH MINOR ISSUES ({len(minor_issues)} papers)")
    print(f"=" * 80)
    
    for i, paper in enumerate(minor_issues, 1):
        cite_key = paper['cite_key']
        title = (paper['title'][:60] + "...") if paper['title'] and len(paper['title']) > 60 else (paper['title'] or 'NO TITLE')
        authors = paper['authors']
        csv_authors = paper['csv_original_authors'] or 'NO CSV AUTHORS'
        corrected_key = paper['corrected_cite_key']
        
        print(f"\n{i}. 🔑 {cite_key} → {corrected_key}")
        print(f"   Title: {title}")
        
        # Identify the specific issue
        issue_type = identify_issue_type(authors)
        print(f"   Issue: {issue_type}")
        print(f"   Current Authors: {authors}")
        
        if csv_authors != 'NO CSV AUTHORS':
            print(f"   CSV Authors: {csv_authors}")
        
        # Check if we have a paper.md file
        paper_file_exists = check_paper_file_exists(cite_key)
        print(f"   Paper.md file: {'✅ EXISTS' if paper_file_exists else '❌ NOT FOUND'}")
    
    conn.close()
    return minor_issues

def identify_issue_type(authors_text):
    """Identify the specific type of issue with the authors field."""
    if not authors_text:
        return "EMPTY AUTHORS"
    
    issues = []
    
    if len(authors_text) > 200:
        issues.append("VERY LONG")
    
    if 'university' in authors_text.lower():
        issues.append("UNIVERSITY CONTAMINATION")
    
    if 'institute' in authors_text.lower():
        issues.append("INSTITUTE CONTAMINATION")
    
    if '@' in authors_text:
        issues.append("EMAIL CONTAMINATION")
    
    if '.edu' in authors_text.lower():
        issues.append("DOMAIN CONTAMINATION")
    
    if 'laboratory' in authors_text.lower() or 'department' in authors_text.lower():
        issues.append("INSTITUTIONAL CONTAMINATION")
    
    if not issues:
        issues.append("OTHER FORMATTING")
    
    return " + ".join(issues)

def check_paper_file_exists(cite_key):
    """Check if paper.md file exists for the cite_key."""
    import os
    from pathlib import Path
    
    papers_dir = Path("markdown_papers")
    possible_paths = [
        papers_dir / cite_key / "paper.md",
        papers_dir / cite_key.replace('_', '-') / "paper.md",
        papers_dir / cite_key.lower() / "paper.md",
    ]
    
    return any(path.exists() for path in possible_paths)

def suggest_extraction_approaches():
    """Suggest approaches for fixing the remaining issues."""
    
    print(f"\n🛠️  SUGGESTED APPROACHES FOR REMAINING ISSUES")
    print(f"=" * 80)
    
    print(f"\n📋 FOR 'AUTHORS UNKNOWN' PAPERS:")
    print(f"   1. Manual search for papers online using title and year")
    print(f"   2. Check if paper.md files exist and contain author info")
    print(f"   3. Search academic databases (Google Scholar, DBLP, etc.)")
    print(f"   4. If truly unknown, keep as 'Authors unknown' for transparency")
    
    print(f"\n⚠️  FOR MINOR ISSUES:")
    print(f"   1. Manual review and cleanup of institutional contamination")
    print(f"   2. Extract clean author names from long text")
    print(f"   3. Use paper.md files if available for better extraction")
    print(f"   4. Pattern-based cleanup for email/domain removal")
    
    print(f"\n🤖 AUTOMATED OPTIONS:")
    print(f"   1. Use Task agent for paper.md files that exist")
    print(f"   2. Web search for papers without local files")
    print(f"   3. Pattern-based text cleaning for institutional contamination")

def main():
    """Find and analyze remaining author issues."""
    logger.info("Finding remaining author extraction issues...")
    
    # Find papers with 'Authors unknown'
    unknown_papers = find_authors_unknown_papers()
    
    # Find papers with minor issues
    minor_issues = find_minor_issues_papers()
    
    # Suggest approaches
    suggest_extraction_approaches()
    
    print(f"\n📊 SUMMARY:")
    print(f"   Papers with 'Authors unknown': {len(unknown_papers)}")
    print(f"   Papers with minor issues: {len(minor_issues)}")
    print(f"   Total remaining work: {len(unknown_papers) + len(minor_issues)} papers")
    
    # Check if we can process any of these with available paper.md files
    papers_with_files = []
    for paper in list(unknown_papers) + list(minor_issues):
        if check_paper_file_exists(paper['cite_key']):
            papers_with_files.append(paper['cite_key'])
    
    if papers_with_files:
        print(f"\n✅ GOOD NEWS: {len(papers_with_files)} papers have paper.md files available")
        print(f"   These can potentially be processed with Task agent:")
        for cite_key in papers_with_files[:5]:  # Show first 5
            print(f"   • {cite_key}")
        if len(papers_with_files) > 5:
            print(f"   • ... and {len(papers_with_files) - 5} more")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Extract full author lists for papers with "et al." or incomplete author information
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

def load_missing_papers():
    """Load missing papers JSON"""
    with open('missing_papers.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def needs_author_update(authors: str) -> bool:
    """Check if authors field needs updating"""
    if not authors:
        return True
    
    authors_lower = authors.lower()
    
    # Check for problematic patterns
    if any(pattern in authors_lower for pattern in ['et al', 'unavailable', 'not available', 'unknown']):
        return True
    
    # Check if it's just a single name (likely incomplete)
    if ',' not in authors and ' and ' not in authors and len(authors.split()) <= 2:
        return True
    
    return False

def extract_authors_from_url(url: str) -> Optional[List[str]]:
    """Try to extract author information from URL patterns"""
    # Common URL patterns that might contain author info
    patterns = [
        r'/([A-Z][a-z]+)-(\d{4})-',  # Name-Year pattern
        r'authors?/([^/]+)',  # Authors in URL path
        r'by-([^/]+)',  # "by-author" pattern
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return [match.group(1)]
    
    return None

def get_paper_suggestions(paper: Dict) -> Dict:
    """Get suggestions for updating paper metadata"""
    suggestions = {}
    
    title = paper.get('Paper Title', '')
    authors = paper.get('Authors', '')
    year = paper.get('Year', '')
    url = paper.get('url', '')
    doi = paper.get('DOI', '')
    
    # Check if authors need updating
    if needs_author_update(authors):
        suggestions['needs_author_update'] = True
        suggestions['current_authors'] = authors
        
        # Try to extract from URL
        url_authors = extract_authors_from_url(url) if url else None
        if url_authors:
            suggestions['url_extracted_authors'] = url_authors
        
        # Provide search suggestions
        suggestions['search_suggestions'] = []
        
        if doi:
            suggestions['search_suggestions'].append(f"Search DOI: {doi}")
        
        if url:
            suggestions['search_suggestions'].append(f"Visit URL: {url}")
        
        if title:
            # Clean title for search
            clean_title = re.sub(r'[^\w\s]', ' ', title)
            clean_title = ' '.join(clean_title.split()[:10])  # First 10 words
            suggestions['search_suggestions'].append(f'Search: "{clean_title}" authors')
    
    return suggestions

def generate_author_update_report():
    """Generate report of papers needing author updates"""
    papers = load_missing_papers()
    
    papers_needing_updates = []
    
    for paper in papers:
        suggestions = get_paper_suggestions(paper)
        if suggestions.get('needs_author_update'):
            papers_needing_updates.append({
                'title': paper.get('Paper Title', ''),
                'current_authors': paper.get('Authors', ''),
                'year': paper.get('Year', ''),
                'url': paper.get('url', ''),
                'doi': paper.get('DOI', ''),
                'suggestions': suggestions
            })
    
    # Save report
    report = {
        'total_papers': len(papers),
        'papers_needing_author_updates': len(papers_needing_updates),
        'papers': papers_needing_updates
    }
    
    with open('author_update_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    # Also create a simple text report
    with open('author_update_report.txt', 'w', encoding='utf-8') as f:
        f.write("Papers Needing Author Updates\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total papers: {report['total_papers']}\n")
        f.write(f"Papers needing updates: {report['papers_needing_author_updates']}\n\n")
        
        for i, paper in enumerate(papers_needing_updates, 1):
            f.write(f"{i}. {paper['title']}\n")
            f.write(f"   Current authors: {paper['current_authors']}\n")
            f.write(f"   Year: {paper['year']}\n")
            
            if paper['url']:
                f.write(f"   URL: {paper['url']}\n")
            
            if paper['doi']:
                f.write(f"   DOI: {paper['doi']}\n")
            
            suggestions = paper['suggestions']
            if suggestions.get('search_suggestions'):
                f.write("   Search suggestions:\n")
                for suggestion in suggestions['search_suggestions']:
                    f.write(f"     - {suggestion}\n")
            
            f.write("\n")
    
    return report

def main():
    print("Analyzing papers for author information...")
    report = generate_author_update_report()
    
    print(f"\nAnalysis complete!")
    print(f"Total papers: {report['total_papers']}")
    print(f"Papers needing author updates: {report['papers_needing_author_updates']}")
    print(f"\nReports saved to:")
    print("  - author_update_report.json")
    print("  - author_update_report.txt")
    
    # Show first few examples
    if report['papers']:
        print("\nFirst few examples:")
        for paper in report['papers'][:5]:
            print(f"\n- {paper['title'][:60]}...")
            print(f"  Current: {paper['current_authors']}")
            if paper.get('doi'):
                print(f"  DOI: {paper['doi']}")

if __name__ == "__main__":
    main()
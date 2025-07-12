#!/usr/bin/env python3
"""
Verify the merge results
"""

import csv
from pathlib import Path

def main():
    project_root = Path(__file__).parent.parent.parent
    merged_file = project_root / "research_papers_merged_final.csv"
    
    # Read merged file
    with open(merged_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
    
    print(f"Total papers in merged file: {len(papers)}")
    
    # Count matched papers
    matched = 0
    match_types = {}
    
    for paper in papers:
        if paper.get('match_score'):
            matched += 1
            mt = paper.get('match_type', 'unknown')
            match_types[mt] = match_types.get(mt, 0) + 1
    
    print(f"\nMatched papers: {matched}")
    print(f"Unmatched papers: {len(papers) - matched}")
    print(f"Match rate: {matched/len(papers)*100:.1f}%")
    
    print("\nMatch types:")
    for mt, count in sorted(match_types.items()):
        print(f"  {mt}: {count}")
    
    # Show sample matched papers
    print("\n=== Sample Matched Papers ===")
    count = 0
    for paper in papers:
        if paper.get('pkg_Papers') and count < 5:
            print(f"\nPrimary title: {paper['title'][:60]}...")
            print(f"Secondary title: {paper['pkg_Papers'][:60]}...")
            print(f"Match score: {paper.get('match_score', 'N/A')}")
            print(f"Secondary authors: {paper.get('pkg_Authors', 'N/A')[:60]}...")
            count += 1

if __name__ == "__main__":
    main()
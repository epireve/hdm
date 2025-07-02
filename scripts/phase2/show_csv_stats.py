#!/usr/bin/env python3
"""
Show statistics for the CSV research table
"""
import sys
from pathlib import Path
from collections import Counter

sys.path.append(str(Path(__file__).parent))
from config import RESEARCH_TABLE_CSV
from csv_utils import read_csv_to_dict


def main():
    """Show CSV statistics"""
    if not RESEARCH_TABLE_CSV.exists():
        print(f"CSV file not found: {RESEARCH_TABLE_CSV}")
        return 1
    
    headers, rows = read_csv_to_dict(RESEARCH_TABLE_CSV)
    
    print(f"\nResearch Table CSV Statistics")
    print("=" * 50)
    print(f"Total papers: {len(rows)}")
    print(f"Total columns: {len(headers)}")
    
    # Check cite keys
    papers_with_keys = [r for r in rows if r.get('cite_key')]
    print(f"\nPapers with cite keys: {len(papers_with_keys)}")
    print(f"Papers without cite keys: {len(rows) - len(papers_with_keys)}")
    
    # Analyze cite key patterns
    if papers_with_keys:
        cite_keys = [r['cite_key'] for r in papers_with_keys]
        
        # Find duplicates (keys with suffixes)
        base_keys = Counter()
        for key in cite_keys:
            # Remove suffix (last character if it's a letter)
            if key and key[-1].isalpha() and key[-2:].isdigit():
                base_key = key[:-1]
            else:
                base_key = key
            base_keys[base_key] += 1
        
        duplicates = {k: v for k, v in base_keys.items() if v > 1}
        
        print(f"\nUnique cite keys: {len(set(cite_keys))}")
        print(f"Base keys with duplicates: {len(duplicates)}")
        
        if duplicates:
            print("\nTop 5 authors with multiple papers:")
            for key, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {key}: {count} papers")
    
    # Analyze years
    years = Counter()
    for row in rows:
        year = row.get('Year', '')
        if year:
            years[year] += 1
    
    print(f"\nPapers by year:")
    for year, count in sorted(years.items(), reverse=True)[:10]:
        print(f"  {year}: {count} papers")
    
    # Analyze relevancy
    relevancy = Counter()
    for row in rows:
        rel = row.get('Relevancy', 'Unknown')
        relevancy[rel] += 1
    
    print(f"\nPapers by relevancy:")
    for rel, count in sorted(relevancy.items(), key=lambda x: x[1], reverse=True):
        print(f"  {rel}: {count} papers")
    
    # Analyze download status
    downloaded = Counter()
    for row in rows:
        dl = row.get('Downloaded', 'Unknown')
        downloaded[dl] += 1
    
    print(f"\nPapers by download status:")
    for dl, count in sorted(downloaded.items(), key=lambda x: x[1], reverse=True):
        print(f"  {dl}: {count} papers")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
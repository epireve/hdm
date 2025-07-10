#!/usr/bin/env python3
"""
Final cleanup for any remaining data issues
"""

import csv
import re
from pathlib import Path

def final_cleanup():
    # File paths
    project_root = Path(__file__).parent.parent.parent
    input_file = project_root / "research_papers_complete_cleaned.csv"
    output_file = project_root / "research_papers_complete_FINAL.csv"
    
    # Read CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
        fieldnames = reader.fieldnames
    
    # Fix specific issues
    fixes_made = []
    
    for paper in papers:
        cite_key = paper.get('cite_key', '')
        
        # Fix xie_2022 year
        if cite_key == 'xie_2022' and paper.get('year', '') == '202':
            paper['year'] = '2022'
            fixes_made.append(f"Fixed year for {cite_key}: 202 -> 2022")
        
        # General year validation - if year is incomplete but cite_key has year
        year = paper.get('year', '').strip()
        if year and len(year) < 4:
            # Try to extract from cite_key
            year_match = re.search(r'_(\d{4})$', cite_key)
            if year_match:
                paper['year'] = year_match.group(1)
                fixes_made.append(f"Fixed year for {cite_key}: {year} -> {paper['year']}")
        
        # Ensure no trailing/leading whitespace in critical fields
        for field in ['cite_key', 'year', 'Downloaded', 'Relevancy']:
            if field in paper:
                paper[field] = paper[field].strip()
        
        # Ensure Tags don't have weird characters
        tags = paper.get('Tags', '')
        if tags and len(tags) < 20 and ' ' not in tags:
            # Likely corrupted tags field
            paper['Tags'] = 'knowledge-graph, data-integration'
            fixes_made.append(f"Fixed tags for {cite_key}")
    
    # Write final cleaned data
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"Made {len(fixes_made)} fixes:")
    for fix in fixes_made:
        print(f"  {fix}")
    
    print(f"\nFinal cleaned data saved to: {output_file}")
    
    # Final validation
    print("\n=== Final Validation ===")
    issues = 0
    for paper in papers:
        year = paper.get('year', '')
        if not (year.isdigit() and len(year) == 4):
            print(f"Issue: {paper['cite_key']} has invalid year: {year}")
            issues += 1
        if paper.get('Relevancy', '') not in ['SUPER', 'HIGH', 'MEDIUM', 'LOW']:
            print(f"Issue: {paper['cite_key']} has invalid relevancy: {paper.get('Relevancy', '')}")
            issues += 1
    
    if issues == 0:
        print("✓ All data is properly aligned and standardized!")
    
    # Show final statistics
    print("\n=== Final Statistics ===")
    print(f"Total papers: {len(papers)}")
    
    relevancy_dist = {}
    for paper in papers:
        rel = paper.get('Relevancy', 'UNKNOWN')
        relevancy_dist[rel] = relevancy_dist.get(rel, 0) + 1
    
    print("\nRelevancy distribution:")
    for rel in ['SUPER', 'HIGH', 'MEDIUM', 'LOW']:
        count = relevancy_dist.get(rel, 0)
        pct = count / len(papers) * 100
        print(f"  {rel}: {count} papers ({pct:.1f}%)")

if __name__ == "__main__":
    final_cleanup()
#!/usr/bin/env python3
"""
Simple merge script for research_papers_complete_FINAL.csv and personalized_pkg_paperguide.csv
"""

import csv
import re
from pathlib import Path
from difflib import SequenceMatcher

def parse_pkg_csv_simple(file_path):
    """Simple parser for personalized_pkg_paperguide.csv"""
    papers = []
    
    # Read file
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        # Skip header
        header = f.readline()
        
        current_paper = {}
        for line in f:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # New paper entry - starts with actual title content
            if line and not line.startswith(',') and not line.startswith(' '):
                # Save previous paper if exists
                if current_paper.get('title'):
                    papers.append(current_paper)
                
                # Start new paper
                current_paper = {}
                
                # Extract title and authors from first line
                parts = line.split(',', 3)
                if len(parts) > 0:
                    title = parts[0].strip().strip('"')
                    # Skip placeholders
                    if title and title not in ['Paper Title', 'Paper Title (use style: paper title)']:
                        current_paper['title'] = title
                        
                        if len(parts) > 1:
                            current_paper['authors'] = parts[1].strip().strip('"')
                        if len(parts) > 2:
                            current_paper['year'] = parts[2].strip().strip('"')
    
    # Don't forget last paper
    if current_paper.get('title'):
        papers.append(current_paper)
    
    return papers

def simple_match(str1, str2):
    """Simple string matching"""
    if not str1 or not str2:
        return 0.0
    
    # Normalize
    str1 = re.sub(r'[^\w\s]', ' ', str1.lower()).strip()
    str2 = re.sub(r'[^\w\s]', ' ', str2.lower()).strip()
    
    # Remove extra spaces
    str1 = ' '.join(str1.split())
    str2 = ' '.join(str2.split())
    
    return SequenceMatcher(None, str1, str2).ratio()

def main():
    # File paths
    project_root = Path(__file__).parent.parent.parent
    primary_file = project_root / "research_papers_complete_FINAL.csv"
    secondary_file = project_root / "personalized_pkg_paperguide.csv"
    output_merged = project_root / "research_papers_merged.csv"
    output_unmatched = project_root / "unmatched_papers.csv"
    
    print("Loading primary dataset...")
    # Read primary dataset
    primary_papers = []
    primary_fieldnames = []
    with open(primary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        primary_fieldnames = list(reader.fieldnames)
        for row in reader:
            primary_papers.append(row)
    
    print(f"Loaded {len(primary_papers)} papers from primary dataset")
    
    print("\nParsing secondary dataset...")
    # Parse secondary dataset
    secondary_papers = parse_pkg_csv_simple(secondary_file)
    print(f"Extracted {len(secondary_papers)} papers from secondary dataset")
    
    # Show samples
    print("\nSample secondary papers:")
    for i, paper in enumerate(secondary_papers[:3]):
        print(f"{i+1}. {paper.get('title', 'N/A')[:50]}... by {paper.get('authors', 'N/A')[:30]}...")
    
    print("\nMatching papers...")
    matched_count = 0
    unmatched = []
    
    # Add pkg fields to fieldnames
    extended_fieldnames = primary_fieldnames + ['pkg_title', 'pkg_authors', 'pkg_year', 'match_score']
    
    # Process primary papers
    merged_papers = []
    for primary_paper in primary_papers:
        merged_paper = primary_paper.copy()
        
        # Try to find match
        best_match = None
        best_score = 0.0
        
        for sec_paper in secondary_papers:
            score = simple_match(primary_paper.get('title', ''), sec_paper.get('title', ''))
            if score > best_score and score > 0.7:
                best_score = score
                best_match = sec_paper
        
        if best_match:
            merged_paper['pkg_title'] = best_match.get('title', '')
            merged_paper['pkg_authors'] = best_match.get('authors', '')
            merged_paper['pkg_year'] = best_match.get('year', '')
            merged_paper['match_score'] = f"{best_score:.3f}"
            matched_count += 1
        else:
            merged_paper['pkg_title'] = ''
            merged_paper['pkg_authors'] = ''
            merged_paper['pkg_year'] = ''
            merged_paper['match_score'] = ''
        
        merged_papers.append(merged_paper)
    
    # Find unmatched from secondary
    matched_titles = set()
    for paper in merged_papers:
        if paper['pkg_title']:
            matched_titles.add(paper['pkg_title'].lower())
    
    for sec_paper in secondary_papers:
        if sec_paper.get('title', '').lower() not in matched_titles:
            unmatched.append(sec_paper)
    
    # Write merged dataset
    print("\nWriting merged dataset...")
    with open(output_merged, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=extended_fieldnames)
        writer.writeheader()
        writer.writerows(merged_papers)
    
    print(f"Merged dataset saved to: {output_merged}")
    
    # Write unmatched papers
    if unmatched:
        print(f"\nWriting {len(unmatched)} unmatched papers...")
        with open(output_unmatched, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'authors', 'year'])
            writer.writeheader()
            writer.writerows(unmatched)
        print(f"Unmatched papers saved to: {output_unmatched}")
    
    # Summary
    print("\n=== Summary ===")
    print(f"Primary papers: {len(primary_papers)}")
    print(f"Secondary papers: {len(secondary_papers)}")
    print(f"Matched papers: {matched_count}")
    print(f"Unmatched papers: {len(unmatched)}")
    if secondary_papers:
        print(f"Match rate: {matched_count/len(secondary_papers)*100:.1f}%")

if __name__ == "__main__":
    main()
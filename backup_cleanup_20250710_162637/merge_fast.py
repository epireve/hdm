#!/usr/bin/env python3
"""
Fast merge script with timeout handling
"""

import csv
import re
from pathlib import Path
from difflib import SequenceMatcher
import time

def normalize_title(title):
    """Fast title normalization"""
    if not title:
        return ""
    # Quick normalization
    title = title.lower()
    # Remove common chars
    title = re.sub(r'[^\w\s]', ' ', title)
    # Single space
    title = ' '.join(title.split())
    return title

def quick_parse_secondary(file_path, limit=500):
    """Quickly parse secondary CSV, limit entries for performance"""
    papers = []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Skip header
        f.readline()
        
        count = 0
        for line in f:
            if count >= limit:
                break
                
            line = line.strip()
            if not line or line.startswith(','):
                continue
                
            # Quick check for paper entry
            parts = line.split(',', 3)
            if len(parts) >= 2:
                title = parts[0].strip(' "')
                if title and len(title) > 10 and 'Paper Title' not in title:
                    papers.append({
                        'title': title,
                        'authors': parts[1].strip(' "') if len(parts) > 1 else '',
                        'year': parts[2].strip(' "') if len(parts) > 2 else ''
                    })
                    count += 1
    
    return papers

def main():
    start_time = time.time()
    
    # File paths
    project_root = Path(__file__).parent.parent.parent
    primary_file = project_root / "research_papers_complete_FINAL.csv"
    secondary_file = project_root / "personalized_pkg_paperguide.csv"
    output_merged = project_root / "research_papers_merged.csv"
    output_unmatched = project_root / "unmatched_papers.csv"
    
    print("Loading primary dataset...")
    primary_papers = []
    primary_fieldnames = []
    
    with open(primary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        primary_fieldnames = list(reader.fieldnames)
        primary_papers = list(reader)
    
    print(f"Loaded {len(primary_papers)} papers from primary dataset")
    
    print("\nParsing secondary dataset (limited for performance)...")
    secondary_papers = quick_parse_secondary(secondary_file, limit=200)
    print(f"Extracted {len(secondary_papers)} papers from secondary dataset")
    
    # Create normalized title lookup for primary papers
    print("\nBuilding lookup index...")
    primary_lookup = {}
    for idx, paper in enumerate(primary_papers):
        norm_title = normalize_title(paper.get('title', ''))
        if norm_title:
            primary_lookup[norm_title] = idx
    
    # Match papers
    print("\nMatching papers...")
    matched_count = 0
    unmatched = []
    
    # Extend fieldnames
    extended_fieldnames = primary_fieldnames + ['pkg_title', 'pkg_authors', 'pkg_year', 'match_score']
    
    # Create merged papers list (copy of primary)
    merged_papers = []
    for paper in primary_papers:
        merged_paper = paper.copy()
        merged_paper['pkg_title'] = ''
        merged_paper['pkg_authors'] = ''
        merged_paper['pkg_year'] = ''
        merged_paper['match_score'] = ''
        merged_papers.append(merged_paper)
    
    # Match secondary papers
    for sec_paper in secondary_papers:
        sec_norm = normalize_title(sec_paper.get('title', ''))
        
        if sec_norm in primary_lookup:
            # Exact match
            idx = primary_lookup[sec_norm]
            merged_papers[idx]['pkg_title'] = sec_paper.get('title', '')
            merged_papers[idx]['pkg_authors'] = sec_paper.get('authors', '')
            merged_papers[idx]['pkg_year'] = sec_paper.get('year', '')
            merged_papers[idx]['match_score'] = '1.000'
            matched_count += 1
        else:
            # Try fuzzy match on top 10 candidates
            best_idx = None
            best_score = 0.7  # Minimum threshold
            
            for prim_norm, idx in list(primary_lookup.items())[:100]:  # Limit search
                score = SequenceMatcher(None, sec_norm, prim_norm).ratio()
                if score > best_score:
                    best_score = score
                    best_idx = idx
            
            if best_idx is not None:
                merged_papers[best_idx]['pkg_title'] = sec_paper.get('title', '')
                merged_papers[best_idx]['pkg_authors'] = sec_paper.get('authors', '')
                merged_papers[best_idx]['pkg_year'] = sec_paper.get('year', '')
                merged_papers[best_idx]['match_score'] = f'{best_score:.3f}'
                matched_count += 1
            else:
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
    elapsed = time.time() - start_time
    print(f"\n=== Summary (completed in {elapsed:.1f}s) ===")
    print(f"Primary papers: {len(primary_papers)}")
    print(f"Secondary papers parsed: {len(secondary_papers)}")
    print(f"Matched papers: {matched_count}")
    print(f"Unmatched papers: {len(unmatched)}")
    if secondary_papers:
        print(f"Match rate: {matched_count/len(secondary_papers)*100:.1f}%")
    
    # Show samples
    print("\n=== Sample Matches ===")
    count = 0
    for paper in merged_papers:
        if paper['pkg_title'] and count < 5:
            print(f"\nPrimary: {paper['title'][:60]}...")
            print(f"Secondary: {paper['pkg_title'][:60]}...")
            print(f"Score: {paper['match_score']}")
            count += 1

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Sort cite keys and fix duplicates by appending letters (a, b, c, etc.)
Then update the cite_key column in the CSV file.
"""

import csv
from collections import defaultdict
from typing import List, Dict

def read_csv_file(filepath: str) -> List[Dict]:
    """Read CSV file and return list of dictionaries."""
    papers = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
    return papers

def generate_cite_key(authors: str, year: str) -> str:
    """Generate cite key from authors and year."""
    if not authors or not year:
        return f"unknown_{year}" if year else "unknown_0000"
    
    # Extract first author's last name
    authors = authors.strip()
    
    # Handle various author formats
    if ',' in authors:
        # Format: "Last, First" or "Last, First, Second Author"
        first_author = authors.split(',')[0].strip()
    elif ' and ' in authors:
        # Format: "First Last and Second Author"
        first_author = authors.split(' and ')[0].strip()
    elif ';' in authors:
        # Format: "Author1; Author2"
        first_author = authors.split(';')[0].strip()
    else:
        # Single author or other format
        first_author = authors
    
    # Extract last name (assume last word is the last name)
    words = first_author.split()
    if words:
        last_name = words[-1].lower()
        # Remove common prefixes/suffixes and special characters
        last_name = last_name.replace(',', '').replace('.', '').replace('(', '').replace(')', '')
        # Remove non-alphabetic characters except hyphens
        last_name = ''.join(c for c in last_name if c.isalpha() or c == '-')
        if last_name:
            return f"{last_name}_{year}"
    
    return f"unknown_{year}"

def fix_duplicate_cite_keys(papers: List[Dict]) -> List[Dict]:
    """Fix duplicate cite keys by appending letters."""
    # Count occurrences of each cite key
    cite_key_counts = defaultdict(int)
    cite_key_usage = defaultdict(int)
    
    # First pass: count all cite keys
    for paper in papers:
        cite_key = paper.get('cite_key', '')
        if cite_key:
            cite_key_counts[cite_key] += 1
    
    # Second pass: fix duplicates
    fixed_papers = []
    for paper in papers:
        cite_key = paper.get('cite_key', '')
        
        if not cite_key:
            # Generate cite key if missing
            authors = paper.get('authors', '')
            year = paper.get('year', '')
            cite_key = generate_cite_key(authors, year)
        
        # If this cite key appears multiple times, append letter
        if cite_key_counts[cite_key] > 1:
            cite_key_usage[cite_key] += 1
            if cite_key_usage[cite_key] == 1:
                # First occurrence keeps original
                new_cite_key = cite_key
            else:
                # Subsequent occurrences get letters appended
                letter = chr(ord('a') + cite_key_usage[cite_key] - 2)  # b, c, d, etc.
                new_cite_key = f"{cite_key}{letter}"
        else:
            new_cite_key = cite_key
        
        # Update the paper with new cite key
        paper_copy = paper.copy()
        paper_copy['cite_key'] = new_cite_key
        fixed_papers.append(paper_copy)
    
    return fixed_papers

def write_csv_file(filepath: str, papers: List[Dict], fieldnames: List[str]):
    """Write papers to CSV file."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)

def main():
    """Main function to fix cite keys."""
    input_file = '/Users/invoture/dev.local/hdm/research_papers_clean.csv'
    output_file = '/Users/invoture/dev.local/hdm/research_papers_clean_fixed.csv'
    
    print("Reading CSV file...")
    papers = read_csv_file(input_file)
    
    print(f"Found {len(papers)} papers")
    
    # Get original fieldnames
    if papers:
        fieldnames = list(papers[0].keys())
    else:
        print("No papers found!")
        return
    
    # Find duplicate cite keys before fixing
    cite_key_counts = defaultdict(int)
    for paper in papers:
        cite_key = paper.get('cite_key', '')
        if cite_key:
            cite_key_counts[cite_key] += 1
    
    duplicates = {k: v for k, v in cite_key_counts.items() if v > 1}
    if duplicates:
        print(f"\nFound {len(duplicates)} duplicate cite keys:")
        for cite_key, count in sorted(duplicates.items()):
            print(f"  {cite_key}: {count} occurrences")
    else:
        print("\nNo duplicate cite keys found")
    
    # Fix duplicates
    print("\nFixing duplicate cite keys...")
    fixed_papers = fix_duplicate_cite_keys(papers)
    
    # Sort papers by cite key
    print("Sorting papers by cite key...")
    fixed_papers.sort(key=lambda x: x.get('cite_key', ''))
    
    # Write to output file
    print(f"Writing fixed papers to {output_file}...")
    write_csv_file(output_file, fixed_papers, fieldnames)
    
    # Show some examples of fixes
    print("\nExamples of fixed cite keys:")
    for i, (original, fixed) in enumerate(zip(papers, fixed_papers)):
        orig_key = original.get('cite_key', '')
        fixed_key = fixed.get('cite_key', '')
        if orig_key != fixed_key:
            print(f"  {orig_key} -> {fixed_key}")
            if i >= 9:  # Show first 10 examples
                break
    
    # Verify no duplicates remain
    final_cite_keys = [paper.get('cite_key', '') for paper in fixed_papers]
    final_duplicates = defaultdict(int)
    for cite_key in final_cite_keys:
        if cite_key:
            final_duplicates[cite_key] += 1
    
    remaining_duplicates = {k: v for k, v in final_duplicates.items() if v > 1}
    if remaining_duplicates:
        print(f"\nWARNING: {len(remaining_duplicates)} duplicate cite keys still remain:")
        for cite_key, count in remaining_duplicates.items():
            print(f"  {cite_key}: {count} occurrences")
    else:
        print("\n✓ All cite keys are now unique!")
    
    print(f"\nSummary:")
    print(f"  Input file: {input_file}")
    print(f"  Output file: {output_file}")
    print(f"  Total papers: {len(fixed_papers)}")
    print(f"  Original duplicates: {len(duplicates)}")
    print(f"  Remaining duplicates: {len(remaining_duplicates)}")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Extract actual paper entries from personalized_pkg_paperguide.csv
Using the correct pattern: Title,"Authors",Year,Journal,...
"""

import csv
import re
from pathlib import Path

def extract_papers_correctly(input_file, output_file):
    """Extract papers using the correct pattern"""
    
    papers = []
    
    print("Extracting papers from PKG file...")
    with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
        # Read all lines
        lines = f.readlines()
    
    # Get headers from first line
    headers = lines[0].strip().split(',')
    headers = [h.strip('"') for h in headers]
    
    # Pattern to match paper entries:
    # Starts with uppercase letter, has title, quoted authors, year
    paper_pattern = re.compile(r'^[A-Z][^,]+,"[^"]+",\d{4},')
    
    for i, line in enumerate(lines[1:], 1):  # Skip header
        line = line.strip()
        
        if paper_pattern.match(line):
            # This is a paper entry
            # Use CSV reader to properly parse the fields
            reader = csv.reader([line])
            try:
                fields = next(reader)
                
                # Create paper dict
                paper = {}
                for j, field in enumerate(fields):
                    if j < len(headers):
                        paper[headers[j]] = field.strip()
                
                # Validate paper has essential fields
                if (paper.get('Papers') and 
                    len(paper.get('Papers', '')) > 20 and
                    'Paper Title' not in paper.get('Papers', '')):
                    
                    papers.append(paper)
                    
                    if len(papers) % 100 == 0:
                        print(f"  Extracted {len(papers)} papers...")
                        
            except Exception as e:
                # Skip malformed lines
                continue
    
    print(f"Extracted {len(papers)} valid papers")
    
    # Write clean CSV
    print(f"\nWriting to {output_file}...")
    
    # Ensure we have all necessary columns
    all_columns = set()
    for paper in papers:
        all_columns.update(paper.keys())
    
    # Order columns sensibly
    ordered_columns = ['Papers', 'Authors', 'Published Year', 'Journal', 'DOI']
    for col in sorted(all_columns):
        if col not in ordered_columns:
            ordered_columns.append(col)
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=ordered_columns)
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"Saved {len(papers)} papers to clean CSV")
    
    # Show samples
    print("\n=== Sample Papers ===")
    for i, paper in enumerate(papers[:5]):
        print(f"\n{i+1}. Title: {paper.get('Papers', 'N/A')[:80]}...")
        print(f"   Authors: {paper.get('Authors', 'N/A')}")
        print(f"   Year: {paper.get('Published Year', 'N/A')}")

def main():
    project_root = Path(__file__).parent.parent.parent
    input_file = project_root / "personalized_pkg_paperguide.csv"
    output_file = project_root / "pkg_papers_clean.csv"
    
    extract_papers_correctly(input_file, output_file)

if __name__ == "__main__":
    main()
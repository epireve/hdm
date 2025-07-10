#!/usr/bin/env python3
"""
Transform personalized_pkg_paperguide.csv into a clean, properly formatted CSV
"""

import csv
import re
from pathlib import Path

def parse_multiline_entry(lines, start_idx, headers):
    """Parse a multi-line paper entry"""
    paper = {}
    current_field_idx = 0
    field_content = []
    
    # Process lines for this paper
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if we've hit the next paper
        if i > start_idx and is_paper_title_line(line):
            break
            
        if not line:
            i += 1
            continue
        
        # Parse CSV fields from line
        fields = parse_csv_line(line)
        
        # First line of paper entry
        if i == start_idx:
            # Map fields directly to headers
            for j, field in enumerate(fields):
                if j < len(headers) and field.strip():
                    paper[headers[j]] = field.strip()
        else:
            # Continuation lines - append to existing fields
            for j, field in enumerate(fields):
                if field.strip():
                    # Determine which header this belongs to
                    if j < len(headers):
                        if headers[j] in paper:
                            paper[headers[j]] += '\n' + field.strip()
                        else:
                            paper[headers[j]] = field.strip()
        
        i += 1
    
    return paper, i

def is_paper_title_line(line):
    """Check if a line starts a new paper entry"""
    if not line or line.startswith(',') or line.startswith(' '):
        return False
    
    # Check first field
    parts = line.split(',', 1)
    if not parts:
        return False
        
    first_field = parts[0].strip(' "')
    
    # Should be a substantial title
    if len(first_field) > 20:
        # Avoid known non-title patterns
        skip_patterns = [
            'paper title (use style',
            'results:',
            'methods:',
            'conclusion:',
            'limitations:',
            'http://',
            'https://',
            'doi:',
            'isbn:'
        ]
        
        first_lower = first_field.lower()
        if not any(pattern in first_lower for pattern in skip_patterns):
            # Additional check - should have some uppercase letters (proper title)
            if any(c.isupper() for c in first_field):
                return True
    
    return False

def parse_csv_line(line):
    """Parse a CSV line handling quotes properly"""
    reader = csv.reader([line])
    try:
        return next(reader)
    except:
        # Fallback to simple split
        return line.split(',')

def clean_field_content(content):
    """Clean up field content"""
    if not content:
        return ""
    
    # Remove excessive newlines
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    
    # Join with single newline
    return '\n'.join(cleaned_lines)

def transform_pkg_csv(input_file, output_file):
    """Transform the PKG CSV file into a clean format"""
    
    print("Reading input file...")
    with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
        all_lines = f.readlines()
    
    # Parse header
    headers = parse_csv_line(all_lines[0].strip())
    headers = [h.strip('"') for h in headers]
    print(f"Found {len(headers)} headers: {headers[:5]}...")
    
    # Parse papers
    papers = []
    i = 1
    paper_count = 0
    
    print("Parsing papers...")
    while i < len(all_lines):
        line = all_lines[i].strip()
        
        if is_paper_title_line(line):
            # Parse this paper entry
            paper, next_idx = parse_multiline_entry(all_lines, i, headers)
            
            # Validate paper
            if paper.get('Papers') and len(paper.get('Papers', '')) > 20:
                # Clean all fields
                for key in paper:
                    paper[key] = clean_field_content(paper[key])
                
                papers.append(paper)
                paper_count += 1
                
                if paper_count % 100 == 0:
                    print(f"  Processed {paper_count} papers...")
            
            i = next_idx
        else:
            i += 1
    
    print(f"Extracted {len(papers)} valid papers")
    
    # Write clean CSV
    print(f"\nWriting clean CSV to {output_file}...")
    
    # Use all headers found in any paper
    all_headers = set()
    for paper in papers:
        all_headers.update(paper.keys())
    
    # Ensure key fields are first
    ordered_headers = ['Papers', 'Authors', 'Published Year', 'Journal', 'DOI']
    for header in sorted(all_headers):
        if header not in ordered_headers:
            ordered_headers.append(header)
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=ordered_headers)
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"Clean CSV saved with {len(papers)} papers")
    
    # Show sample papers
    print("\n=== Sample Papers ===")
    for i, paper in enumerate(papers[:5]):
        print(f"\n{i+1}. Title: {paper.get('Papers', 'N/A')[:80]}...")
        print(f"   Authors: {paper.get('Authors', 'N/A')[:60]}...")
        print(f"   Year: {paper.get('Published Year', 'N/A')}")

def main():
    project_root = Path(__file__).parent.parent.parent
    input_file = project_root / "personalized_pkg_paperguide.csv"
    output_file = project_root / "personalized_pkg_paperguide_clean.csv"
    
    transform_pkg_csv(input_file, output_file)
    
    print("\nTransformation complete!")
    print(f"Clean file saved to: {output_file}")

if __name__ == "__main__":
    main()
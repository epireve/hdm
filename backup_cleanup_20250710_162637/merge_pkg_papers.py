#!/usr/bin/env python3
"""
Merge research_papers_complete_FINAL.csv with personalized_pkg_paperguide.csv
Match papers by title or authors using fuzzy matching
Track unmatched papers from secondary file
"""

import csv
import re
from pathlib import Path
from difflib import SequenceMatcher
import json

def parse_multiline_csv(file_path):
    """Parse the complex multi-line CSV format of personalized_pkg_paperguide.csv"""
    papers = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into potential paper entries
    # Look for lines that start with non-comma content (paper titles)
    lines = content.split('\n')
    
    # First line is header
    header_line = lines[0]
    headers = []
    
    # Parse headers more carefully
    in_quotes = False
    current_header = ""
    for char in header_line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            headers.append(current_header.strip('"'))
            current_header = ""
        else:
            current_header += char
    if current_header:
        headers.append(current_header.strip('"'))
    
    print(f"Found headers: {headers}")
    
    # Process paper entries
    i = 1
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Check if this could be a paper title line (non-empty first field)
        if line and not line.startswith(',') and not line.startswith(' '):
            # This might be a paper entry
            paper = {}
            
            # Collect all lines for this paper until we hit the next paper or end
            paper_lines = [line]
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if not next_line:
                    j += 1
                    continue
                # If line starts with text (not comma), it's likely a new paper
                if next_line and not next_line.startswith(',') and not next_line.startswith(' '):
                    # Check if it looks like a paper title by examining content
                    if any(keyword in next_line for keyword in ['Paper Title', 'reference-manager']):
                        break
                    # Also check if it contains multiple commas (likely data row)
                    if next_line.count(',') >= 3:
                        break
                paper_lines.append(next_line)
                j += 1
            
            # Parse the collected lines into paper data
            full_text = '\n'.join(paper_lines)
            
            # Try to extract fields
            # Papers field is usually the first non-empty value
            if 'Paper Title' in line or line.count('"') >= 2:
                # Extract paper title from quoted text
                title_match = re.search(r'"([^"]+)"', line)
                if title_match:
                    paper['Papers'] = title_match.group(1)
                else:
                    # First field before comma
                    parts = line.split(',', 1)
                    if parts[0].strip():
                        paper['Papers'] = parts[0].strip()
            
            # Extract other fields from the multi-line content
            # Look for patterns like "field_name: value" or quoted values
            for header in headers[1:]:  # Skip 'Papers' as we handled it
                # Try to find this field in the content
                field_pattern = rf'{re.escape(header)}[:\s]*"?([^",\n]+)'
                match = re.search(field_pattern, full_text, re.IGNORECASE)
                if match:
                    paper[header] = match.group(1).strip()
            
            # Also try to extract from structured lines
            all_values = []
            for pline in paper_lines:
                # Extract quoted values
                quoted = re.findall(r'"([^"]+)"', pline)
                all_values.extend(quoted)
                # Extract comma-separated values
                parts = pline.split(',')
                all_values.extend([p.strip() for p in parts if p.strip()])
            
            # Map values to headers if we have the right count
            if len(all_values) >= len(headers):
                for h_idx, header in enumerate(headers):
                    if h_idx < len(all_values) and header not in paper:
                        paper[header] = all_values[h_idx]
            
            # Only add if we have meaningful data
            if paper.get('Papers') or paper.get('Authors'):
                papers.append(paper)
                print(f"Extracted paper: {paper.get('Papers', 'Unknown')[:60]}...")
            
            i = j
        else:
            i += 1
    
    return papers

def fuzzy_match(str1, str2, threshold=0.8):
    """Calculate similarity between two strings"""
    if not str1 or not str2:
        return 0.0
    
    # Normalize strings
    str1 = str1.lower().strip()
    str2 = str2.lower().strip()
    
    # Remove common academic prefixes/suffixes
    for pattern in [r'\s*:\s*', r'\s*-\s*', r'^(a|an|the)\s+', r'\s*\(.*?\)\s*$']:
        str1 = re.sub(pattern, ' ', str1).strip()
        str2 = re.sub(pattern, ' ', str2).strip()
    
    # Calculate similarity
    return SequenceMatcher(None, str1, str2).ratio()

def extract_authors_list(authors_str):
    """Extract individual authors from author string"""
    if not authors_str:
        return []
    
    # Handle various separators
    authors_str = authors_str.replace(' and ', ', ')
    authors_str = authors_str.replace(';', ',')
    
    # Split and clean
    authors = [a.strip() for a in authors_str.split(',') if a.strip()]
    return authors

def match_papers(primary_papers, secondary_papers):
    """Match papers between primary and secondary datasets"""
    matched = []
    unmatched = []
    
    # Create lookup structures for primary papers
    primary_by_title = {}
    primary_by_authors = {}
    
    for idx, paper in enumerate(primary_papers):
        title = paper.get('title', '').lower().strip()
        if title:
            primary_by_title[title] = idx
        
        authors = extract_authors_list(paper.get('authors', ''))
        for author in authors:
            author_key = author.lower().strip()
            if author_key not in primary_by_authors:
                primary_by_authors[author_key] = []
            primary_by_authors[author_key].append(idx)
    
    # Match each secondary paper
    for sec_paper in secondary_papers:
        sec_title = sec_paper.get('Papers', '').strip()
        sec_authors = sec_paper.get('Authors', '').strip()
        
        if not sec_title and not sec_authors:
            continue
        
        best_match_idx = None
        best_score = 0.0
        
        # Try title matching first
        if sec_title:
            for prim_idx, prim_paper in enumerate(primary_papers):
                prim_title = prim_paper.get('title', '')
                score = fuzzy_match(sec_title, prim_title)
                
                if score > best_score:
                    best_score = score
                    best_match_idx = prim_idx
        
        # If no good title match, try author matching
        if best_score < 0.8 and sec_authors:
            sec_author_list = extract_authors_list(sec_authors)
            
            for sec_author in sec_author_list:
                sec_author_key = sec_author.lower().strip()
                
                # Check if this author appears in primary
                if sec_author_key in primary_by_authors:
                    for prim_idx in primary_by_authors[sec_author_key]:
                        # Verify with title if available
                        if sec_title:
                            prim_title = primary_papers[prim_idx].get('title', '')
                            score = fuzzy_match(sec_title, prim_title, threshold=0.6)
                            if score > 0.6:
                                best_score = score
                                best_match_idx = prim_idx
                                break
                        else:
                            # Just author match
                            best_score = 0.7
                            best_match_idx = prim_idx
                            break
        
        if best_match_idx is not None and best_score >= 0.7:
            matched.append({
                'primary_idx': best_match_idx,
                'secondary_paper': sec_paper,
                'match_score': best_score
            })
        else:
            unmatched.append(sec_paper)
    
    return matched, unmatched

def rename_secondary_columns(paper_data, prefix='pkg_'):
    """Rename columns from secondary dataset to avoid conflicts"""
    renamed = {}
    for key, value in paper_data.items():
        renamed[f"{prefix}{key}"] = value
    return renamed

def main():
    # File paths
    project_root = Path(__file__).parent.parent.parent
    primary_file = project_root / "research_papers_complete_FINAL.csv"
    secondary_file = project_root / "personalized_pkg_paperguide.csv"
    output_merged = project_root / "research_papers_merged.csv"
    output_unmatched = project_root / "unmatched_papers.csv"
    
    print("Loading primary dataset...")
    # Read primary dataset
    with open(primary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        primary_papers = list(reader)
        primary_fieldnames = list(reader.fieldnames)
    
    print(f"Loaded {len(primary_papers)} papers from primary dataset")
    
    print("\nParsing secondary dataset (multi-line format)...")
    # Parse secondary dataset
    secondary_papers = parse_multiline_csv(secondary_file)
    print(f"Extracted {len(secondary_papers)} papers from secondary dataset")
    
    if not secondary_papers:
        print("WARNING: No papers extracted from secondary file!")
        return
    
    print("\nMatching papers...")
    # Match papers
    matched, unmatched = match_papers(primary_papers, secondary_papers)
    
    print(f"\nMatching results:")
    print(f"  Matched: {len(matched)} papers")
    print(f"  Unmatched: {len(unmatched)} papers")
    
    # Create merged dataset
    print("\nCreating merged dataset...")
    
    # Get all unique column names from secondary dataset
    secondary_columns = set()
    for paper in secondary_papers:
        secondary_columns.update(paper.keys())
    
    # Create extended fieldnames
    extended_fieldnames = list(primary_fieldnames)
    for col in sorted(secondary_columns):
        extended_fieldnames.append(f"pkg_{col}")
    
    # Add match_score to fieldnames
    extended_fieldnames.append('match_score')
    
    # Merge data
    merged_papers = []
    
    # Add match information to primary papers
    for idx, primary_paper in enumerate(primary_papers):
        merged_paper = primary_paper.copy()
        
        # Find if this paper was matched
        match_info = None
        for match in matched:
            if match['primary_idx'] == idx:
                match_info = match
                break
        
        if match_info:
            # Add secondary data with renamed columns
            secondary_data = rename_secondary_columns(match_info['secondary_paper'])
            merged_paper.update(secondary_data)
            merged_paper['match_score'] = f"{match_info['match_score']:.3f}"
        else:
            # Fill with empty values
            for col in extended_fieldnames:
                if col not in merged_paper:
                    merged_paper[col] = ""
        
        merged_papers.append(merged_paper)
    
    # Write merged dataset
    with open(output_merged, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=extended_fieldnames)
        writer.writeheader()
        writer.writerows(merged_papers)
    
    print(f"\nMerged dataset saved to: {output_merged}")
    
    # Write unmatched papers
    if unmatched:
        print(f"\nWriting {len(unmatched)} unmatched papers...")
        
        # Get fieldnames from unmatched papers
        unmatched_fieldnames = set()
        for paper in unmatched:
            unmatched_fieldnames.update(paper.keys())
        unmatched_fieldnames = sorted(list(unmatched_fieldnames))
        
        with open(output_unmatched, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=unmatched_fieldnames)
            writer.writeheader()
            writer.writerows(unmatched)
        
        print(f"Unmatched papers saved to: {output_unmatched}")
    
    # Print summary statistics
    print("\n=== Summary ===")
    print(f"Primary papers: {len(primary_papers)}")
    print(f"Secondary papers: {len(secondary_papers)}")
    print(f"Matched papers: {len(matched)}")
    print(f"Unmatched papers: {len(unmatched)}")
    if secondary_papers:
        print(f"Match rate: {len(matched)/len(secondary_papers)*100:.1f}%")
    
    # Show some examples of matches
    if matched:
        print("\n=== Sample Matches (top 5) ===")
        for match in matched[:5]:
            primary = primary_papers[match['primary_idx']]
            secondary = match['secondary_paper']
            print(f"\nScore: {match['match_score']:.3f}")
            print(f"Primary: {primary.get('title', 'N/A')[:80]}...")
            print(f"Secondary: {secondary.get('Papers', 'N/A')[:80]}...")

if __name__ == "__main__":
    main()
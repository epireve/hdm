#!/usr/bin/env python3
"""
Merge research_papers_complete_FINAL.csv with personalized_pkg_paperguide.csv
Match papers by title or authors using fuzzy matching
Track unmatched papers from secondary file
Final version - Properly handles multi-row paper format
"""

import csv
import re
from pathlib import Path
from difflib import SequenceMatcher
import json

def parse_personalized_pkg_csv(file_path):
    """Parse the personalized_pkg_paperguide.csv with its multi-row format"""
    papers = []
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Split into lines
    lines = content.split('\n')
    
    # First line is header
    headers = lines[0].split(',')
    # Clean headers
    headers = [h.strip().strip('"') for h in headers]
    print(f"Headers: {headers}")
    
    # Track current paper being built
    current_paper = None
    current_field_idx = 0
    
    i = 1
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # Check if this is a new paper (has content in first column)
        if line and not line.startswith(',') and not line.startswith('"'):
            # If there's non-empty content that doesn't start with comma
            # it's likely a new paper entry
            
            # Save previous paper if complete
            if current_paper and current_paper.get('Papers'):
                papers.append(current_paper)
            
            # Start new paper
            current_paper = {}
            current_field_idx = 0
            
            # Extract title - handle titles with commas inside quotes
            if line.startswith('"'):
                # Find closing quote
                end_quote = line.find('"', 1)
                if end_quote > 0:
                    current_paper['Papers'] = line[1:end_quote]
                    # Continue processing rest of line
                    rest_of_line = line[end_quote+1:].lstrip(',')
                    if rest_of_line:
                        # Extract authors if present
                        if rest_of_line.startswith('"'):
                            end_quote2 = rest_of_line.find('"', 1)
                            if end_quote2 > 0:
                                current_paper['Authors'] = rest_of_line[1:end_quote2]
                        else:
                            # Split by comma
                            parts = rest_of_line.split(',', 1)
                            if parts[0]:
                                current_paper['Authors'] = parts[0].strip()
            else:
                # Simple case - no quotes
                parts = line.split(',', 2)
                if len(parts) > 0:
                    current_paper['Papers'] = parts[0].strip()
                if len(parts) > 1:
                    current_paper['Authors'] = parts[1].strip()
                if len(parts) > 2:
                    current_paper['Published Year'] = parts[2].strip()
        
        # Otherwise, it's a continuation line
        elif line.startswith(',') or line.startswith(' '):
            if current_paper is not None:
                # This is additional content for the current paper
                # Parse it and add to appropriate fields
                parts = line.split(',')
                
                # Map parts to remaining headers
                for j, part in enumerate(parts):
                    if part.strip():
                        # Find which header this corresponds to
                        header_idx = current_field_idx + j
                        if header_idx < len(headers):
                            header = headers[header_idx]
                            if header not in current_paper or not current_paper[header]:
                                current_paper[header] = part.strip().strip('"')
                            else:
                                # Append to existing content
                                current_paper[header] += '\n' + part.strip().strip('"')
        
        i += 1
    
    # Don't forget last paper
    if current_paper and current_paper.get('Papers'):
        papers.append(current_paper)
    
    # Clean up papers - ensure proper field mapping
    cleaned_papers = []
    for paper in papers:
        # Only include papers with meaningful data
        if paper.get('Papers') or paper.get('Authors'):
            cleaned_papers.append(paper)
    
    return cleaned_papers

def fuzzy_match(str1, str2, threshold=0.8):
    """Calculate similarity between two strings"""
    if not str1 or not str2:
        return 0.0
    
    # Normalize strings
    str1 = str1.lower().strip()
    str2 = str2.lower().strip()
    
    # Remove common patterns
    patterns = [
        r'\s*:\s*',           # colons
        r'\s*-\s*',           # dashes
        r'^(a|an|the)\s+',   # articles
        r'\s*\(.*?\)\s*',     # parentheses
        r'[^\w\s]',           # special chars
        r'\s+',               # multiple spaces
    ]
    
    for pattern in patterns:
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
    authors = []
    for a in authors_str.split(','):
        a = a.strip()
        if a and len(a) > 2:  # Skip single letters
            authors.append(a)
    
    return authors

def match_papers(primary_papers, secondary_papers):
    """Match papers between primary and secondary datasets"""
    matched = []
    unmatched = []
    used_primary_indices = set()
    
    # Process each secondary paper
    for sec_paper in secondary_papers:
        sec_title = sec_paper.get('Papers', '').strip()
        sec_authors = sec_paper.get('Authors', '').strip()
        
        # Skip if no meaningful data
        if not sec_title and not sec_authors:
            unmatched.append(sec_paper)
            continue
        
        # Skip if title is just "Paper Title" or similar placeholder
        if sec_title in ['Paper Title', 'Paper Title (use style: paper title)', '']:
            unmatched.append(sec_paper)
            continue
        
        best_match_idx = None
        best_score = 0.0
        
        # Try to match with each primary paper
        for prim_idx, prim_paper in enumerate(primary_papers):
            if prim_idx in used_primary_indices:
                continue
                
            prim_title = prim_paper.get('title', '')
            prim_authors = prim_paper.get('authors', '')
            
            # Calculate title similarity
            title_score = 0.0
            if sec_title and prim_title:
                title_score = fuzzy_match(sec_title, prim_title)
            
            # Calculate author similarity
            author_score = 0.0
            if sec_authors and prim_authors:
                sec_author_list = extract_authors_list(sec_authors)
                prim_author_list = extract_authors_list(prim_authors)
                
                # Check for common authors
                for sec_auth in sec_author_list:
                    for prim_auth in prim_author_list:
                        auth_sim = fuzzy_match(sec_auth, prim_auth)
                        if auth_sim > 0.8:
                            author_score = max(author_score, auth_sim)
            
            # Combined score (heavily weighted towards title)
            combined_score = (title_score * 0.85) + (author_score * 0.15)
            
            if combined_score > best_score:
                best_score = combined_score
                best_match_idx = prim_idx
        
        # Accept match if score is high enough
        if best_match_idx is not None and best_score >= 0.7:
            matched.append({
                'primary_idx': best_match_idx,
                'secondary_paper': sec_paper,
                'match_score': best_score
            })
            used_primary_indices.add(best_match_idx)
        else:
            unmatched.append(sec_paper)
    
    return matched, unmatched

def rename_secondary_columns(paper_data, prefix='pkg_'):
    """Rename columns from secondary dataset to avoid conflicts"""
    renamed = {}
    for key, value in paper_data.items():
        if value:  # Only include non-empty values
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
    secondary_papers = parse_personalized_pkg_csv(secondary_file)
    print(f"Extracted {len(secondary_papers)} papers from secondary dataset")
    
    # Debug: Show first few papers
    print("\nFirst 5 papers from secondary dataset:")
    for i, paper in enumerate(secondary_papers[:5]):
        print(f"\nPaper {i+1}:")
        print(f"  Title: {paper.get('Papers', 'N/A')[:60]}...")
        print(f"  Authors: {paper.get('Authors', 'N/A')[:60]}...")
        print(f"  Year: {paper.get('Published Year', 'N/A')}")
    
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
        prefixed_col = f"pkg_{col}"
        if prefixed_col not in extended_fieldnames:
            extended_fieldnames.append(prefixed_col)
    
    # Add match_score if not present
    if 'match_score' not in extended_fieldnames:
        extended_fieldnames.append('match_score')
    
    # Merge data
    merged_papers = []
    
    # Process all primary papers
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
            # Fill with empty values for consistency
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
        
        # Ensure essential fields are included
        essential_fields = ['Papers', 'Authors', 'Published Year', 'Journal', 'DOI']
        for field in essential_fields:
            if field not in unmatched_fieldnames:
                unmatched_fieldnames.insert(0, field)
        
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
        for i, match in enumerate(matched[:5]):
            primary = primary_papers[match['primary_idx']]
            secondary = match['secondary_paper']
            print(f"\n{i+1}. Score: {match['match_score']:.3f}")
            print(f"   Primary: {primary.get('title', 'N/A')[:60]}...")
            print(f"   Secondary: {secondary.get('Papers', 'N/A')[:60]}...")
    
    # Show some unmatched for review
    if unmatched:
        print("\n=== Sample Unmatched (top 5) ===")
        for i, paper in enumerate(unmatched[:5]):
            if paper.get('Papers') and paper.get('Papers') != 'Paper Title':
                print(f"\n{i+1}. Title: {paper.get('Papers', 'N/A')[:60]}...")
                print(f"   Authors: {paper.get('Authors', 'N/A')[:60]}...")
                print(f"   Year: {paper.get('Published Year', 'N/A')}")

if __name__ == "__main__":
    main()
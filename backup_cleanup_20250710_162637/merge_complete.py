#!/usr/bin/env python3
"""
Complete merge script for research_papers_complete_FINAL.csv and personalized_pkg_paperguide.csv
Handles complex multi-line format and improves matching accuracy
"""

import csv
import re
from pathlib import Path
from difflib import SequenceMatcher
import time

def parse_pkg_csv_complete(file_path):
    """Parse the complete personalized_pkg_paperguide.csv with multi-line handling"""
    papers = []
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        # Read header
        header_line = f.readline().strip()
        headers = header_line.split(',')
        headers = [h.strip('"') for h in headers]
        print(f"Headers: {headers[:5]}...")  # Show first 5 headers
        
        # Read all content
        content = f.read()
        
    # Split into potential paper entries
    # Look for lines that start with actual paper titles
    lines = content.split('\n')
    
    current_paper = {}
    current_field_content = []
    field_index = 0
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue
            
        # Check if this is a new paper entry
        # New papers typically have a non-empty first field and look like titles
        if is_new_paper_line(line):
            # Save previous paper if exists
            if current_paper and current_paper.get('Papers'):
                # Skip placeholder entries
                if 'Paper Title (use style' not in current_paper.get('Papers', ''):
                    papers.append(current_paper)
            
            # Start new paper
            current_paper = {}
            field_index = 0
            
            # Parse the line carefully
            fields = parse_csv_line(line)
            
            # Map fields to headers
            for j, field in enumerate(fields):
                if j < len(headers) and field:
                    current_paper[headers[j]] = field.strip()
        
        elif line and current_paper:
            # This is a continuation line
            # Parse and add to current paper
            fields = parse_csv_line(line)
            
            for j, field in enumerate(fields):
                if field and j < len(headers):
                    header = headers[j]
                    if header in current_paper:
                        # Append to existing content
                        current_paper[header] += '\n' + field.strip()
                    else:
                        current_paper[header] = field.strip()
    
    # Don't forget last paper
    if current_paper and current_paper.get('Papers'):
        if 'Paper Title (use style' not in current_paper.get('Papers', ''):
            papers.append(current_paper)
    
    return papers

def is_new_paper_line(line):
    """Check if a line represents a new paper entry"""
    if not line or line.startswith(',') or line.startswith(' '):
        return False
    
    # Check if it looks like a paper title (has substantial text in first field)
    parts = line.split(',', 1)
    if parts:
        first_field = parts[0].strip(' "')
        # Should be a meaningful title
        if len(first_field) > 20 and not all(c in '.,;:()[]{}' for c in first_field):
            # Avoid common non-title patterns
            if not any(pattern in first_field.lower() for pattern in 
                      ['results:', 'methods:', 'conclusion:', 'primary outcome:', 
                       'limitations:', 'et al.', 'https://', 'doi.org']):
                return True
    
    return False

def parse_csv_line(line):
    """Parse a CSV line handling quotes and commas properly"""
    fields = []
    current_field = ''
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            fields.append(current_field)
            current_field = ''
        else:
            current_field += char
    
    # Don't forget the last field
    fields.append(current_field)
    
    return fields

def normalize_for_matching(text):
    """Aggressive normalization for matching"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove all punctuation and special characters
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove common stop words that might differ
    stop_words = ['the', 'a', 'an', 'of', 'for', 'and', 'or', 'in', 'on', 'at', 'to', 'using', 'with', 'based']
    words = text.split()
    words = [w for w in words if w not in stop_words]
    text = ' '.join(words)
    
    return text

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts"""
    if not text1 or not text2:
        return 0.0
    
    # Normalize both texts
    norm1 = normalize_for_matching(text1)
    norm2 = normalize_for_matching(text2)
    
    if not norm1 or not norm2:
        return 0.0
    
    # Check for exact match after normalization
    if norm1 == norm2:
        return 1.0
    
    # Check if one contains the other (substring match)
    if norm1 in norm2 or norm2 in norm1:
        # Give high score for substring matches
        return 0.85
    
    # Use sequence matcher for fuzzy matching
    return SequenceMatcher(None, norm1, norm2).ratio()

def match_by_authors(authors1, authors2):
    """Match papers by authors"""
    if not authors1 or not authors2:
        return 0.0
    
    # Extract individual authors
    authors1_list = [a.strip().lower() for a in re.split(r'[,;]', authors1) if a.strip()]
    authors2_list = [a.strip().lower() for a in re.split(r'[,;]', authors2) if a.strip()]
    
    # Check for common authors
    matches = 0
    for a1 in authors1_list:
        for a2 in authors2_list:
            # Check last names
            a1_parts = a1.split()
            a2_parts = a2.split()
            if a1_parts and a2_parts:
                # Compare last names
                if a1_parts[-1] == a2_parts[-1] and len(a1_parts[-1]) > 2:
                    matches += 1
                    break
    
    if matches > 0:
        # Calculate score based on proportion of matching authors
        return matches / max(len(authors1_list), len(authors2_list))
    
    return 0.0

def find_best_match(primary_paper, secondary_papers, used_indices):
    """Find the best match for a primary paper from secondary papers"""
    best_match = None
    best_score = 0.0
    best_idx = -1
    match_type = None
    
    prim_title = primary_paper.get('title', '')
    prim_authors = primary_paper.get('authors', '')
    
    for idx, sec_paper in enumerate(secondary_papers):
        if idx in used_indices:
            continue
            
        sec_title = sec_paper.get('Papers', '')
        sec_authors = sec_paper.get('Authors', '')
        
        # Calculate title similarity
        title_score = calculate_similarity(prim_title, sec_title)
        
        # Calculate author similarity
        author_score = match_by_authors(prim_authors, sec_authors)
        
        # Combined score (prioritize title matches)
        if title_score >= 0.8:
            # Strong title match
            combined_score = title_score
            current_match_type = 'title'
        elif title_score >= 0.6 and author_score >= 0.5:
            # Moderate title match with author confirmation
            combined_score = (title_score * 0.7) + (author_score * 0.3)
            current_match_type = 'title+author'
        elif author_score >= 0.7:
            # Strong author match
            combined_score = author_score * 0.8  # Slightly penalize author-only matches
            current_match_type = 'author'
        else:
            combined_score = 0.0
            current_match_type = None
        
        if combined_score > best_score and combined_score >= 0.6:
            best_score = combined_score
            best_match = sec_paper
            best_idx = idx
            match_type = current_match_type
    
    return best_match, best_score, best_idx, match_type

def main():
    start_time = time.time()
    
    # File paths
    project_root = Path(__file__).parent.parent.parent
    primary_file = project_root / "research_papers_complete_FINAL.csv"
    secondary_file = project_root / "personalized_pkg_paperguide.csv"
    output_merged = project_root / "research_papers_merged_complete.csv"
    output_unmatched = project_root / "unmatched_papers_complete.csv"
    output_report = project_root / "merge_report.txt"
    
    print("Loading primary dataset...")
    # Read primary dataset
    primary_papers = []
    primary_fieldnames = []
    with open(primary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        primary_fieldnames = list(reader.fieldnames)
        primary_papers = list(reader)
    
    print(f"Loaded {len(primary_papers)} papers from primary dataset")
    
    print("\nParsing secondary dataset (complete file)...")
    # Parse secondary dataset
    secondary_papers = parse_pkg_csv_complete(secondary_file)
    print(f"Extracted {len(secondary_papers)} valid papers from secondary dataset")
    
    # Show sample papers
    print("\nSample papers from secondary dataset:")
    for i, paper in enumerate(secondary_papers[:3]):
        print(f"\n{i+1}. Title: {paper.get('Papers', 'N/A')[:80]}...")
        print(f"   Authors: {paper.get('Authors', 'N/A')[:80]}...")
    
    # Match papers
    print("\nMatching papers...")
    matches = []
    used_secondary_indices = set()
    match_types_count = {'title': 0, 'author': 0, 'title+author': 0}
    
    # Process each primary paper
    for i, prim_paper in enumerate(primary_papers):
        if i % 50 == 0:
            print(f"  Processing paper {i+1}/{len(primary_papers)}...")
        
        best_match, score, sec_idx, match_type = find_best_match(
            prim_paper, secondary_papers, used_secondary_indices
        )
        
        if best_match:
            matches.append({
                'primary_idx': i,
                'secondary_idx': sec_idx,
                'score': score,
                'match_type': match_type,
                'primary_title': prim_paper.get('title', ''),
                'secondary_title': best_match.get('Papers', '')
            })
            used_secondary_indices.add(sec_idx)
            match_types_count[match_type] += 1
    
    print(f"\nMatched {len(matches)} papers")
    print(f"Match types: {match_types_count}")
    
    # Find unmatched secondary papers
    unmatched_secondary = []
    for idx, paper in enumerate(secondary_papers):
        if idx not in used_secondary_indices:
            unmatched_secondary.append(paper)
    
    # Get all unique columns from secondary papers
    secondary_columns = set()
    for paper in secondary_papers:
        secondary_columns.update(paper.keys())
    
    # Create extended fieldnames
    extended_fieldnames = list(primary_fieldnames)
    for col in sorted(secondary_columns):
        pkg_col = f"pkg_{col}"
        if pkg_col not in extended_fieldnames:
            extended_fieldnames.append(pkg_col)
    
    if 'match_score' not in extended_fieldnames:
        extended_fieldnames.append('match_score')
    if 'match_type' not in extended_fieldnames:
        extended_fieldnames.append('match_type')
    
    # Create merged dataset
    print("\nCreating merged dataset...")
    merged_papers = []
    
    for i, prim_paper in enumerate(primary_papers):
        merged_paper = prim_paper.copy()
        
        # Find if this paper was matched
        match_info = None
        for match in matches:
            if match['primary_idx'] == i:
                match_info = match
                sec_paper = secondary_papers[match['secondary_idx']]
                
                # Add secondary data with pkg_ prefix
                for key, value in sec_paper.items():
                    if value:
                        merged_paper[f"pkg_{key}"] = value
                
                merged_paper['match_score'] = f"{match['score']:.3f}"
                merged_paper['match_type'] = match['match_type']
                break
        
        if not match_info:
            # Fill empty values for unmatched papers
            for col in extended_fieldnames:
                if col not in merged_paper:
                    merged_paper[col] = ""
        
        merged_papers.append(merged_paper)
    
    # Write merged dataset
    with open(output_merged, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=extended_fieldnames)
        writer.writeheader()
        writer.writerows(merged_papers)
    
    print(f"Merged dataset saved to: {output_merged}")
    
    # Write unmatched papers
    if unmatched_secondary:
        print(f"\nWriting {len(unmatched_secondary)} unmatched papers...")
        
        # Get all fieldnames from unmatched papers
        unmatched_fieldnames = set()
        for paper in unmatched_secondary:
            unmatched_fieldnames.update(paper.keys())
        unmatched_fieldnames = sorted(list(unmatched_fieldnames))
        
        with open(output_unmatched, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=unmatched_fieldnames)
            writer.writeheader()
            writer.writerows(unmatched_secondary)
        
        print(f"Unmatched papers saved to: {output_unmatched}")
    
    # Write detailed report
    print("\nWriting merge report...")
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write("=== Merge Report ===\n\n")
        f.write(f"Processing completed in: {time.time() - start_time:.1f} seconds\n\n")
        f.write(f"Primary dataset: {len(primary_papers)} papers\n")
        f.write(f"Secondary dataset: {len(secondary_papers)} papers\n")
        f.write(f"Matched papers: {len(matches)}\n")
        f.write(f"Unmatched secondary papers: {len(unmatched_secondary)}\n")
        f.write(f"Match rate: {len(matches)/len(secondary_papers)*100:.1f}%\n\n")
        
        f.write("Match types breakdown:\n")
        for match_type, count in match_types_count.items():
            f.write(f"  {match_type}: {count} papers\n")
        
        f.write("\n=== Sample Matches ===\n")
        for i, match in enumerate(matches[:20]):
            f.write(f"\n{i+1}. Score: {match['score']:.3f} (Type: {match['match_type']})\n")
            f.write(f"   Primary: {match['primary_title'][:100]}\n")
            f.write(f"   Secondary: {match['secondary_title'][:100]}\n")
        
        # Show some high-confidence matches
        f.write("\n=== High Confidence Matches (score >= 0.9) ===\n")
        high_conf = [m for m in matches if m['score'] >= 0.9]
        for i, match in enumerate(high_conf[:10]):
            f.write(f"\n{i+1}. Score: {match['score']:.3f}\n")
            f.write(f"   Primary: {match['primary_title'][:100]}\n")
            f.write(f"   Secondary: {match['secondary_title'][:100]}\n")
    
    print(f"Merge report saved to: {output_report}")
    
    # Final summary
    print(f"\n=== Final Summary ===")
    print(f"Total processing time: {time.time() - start_time:.1f} seconds")
    print(f"Match rate: {len(matches)/len(secondary_papers)*100:.1f}%")
    print(f"High confidence matches (>= 0.9): {len([m for m in matches if m['score'] >= 0.9])}")

if __name__ == "__main__":
    main()
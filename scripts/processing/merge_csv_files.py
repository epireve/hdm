#!/usr/bin/env python3
"""
Merge research_papers_clean.csv with research_table_with_citekeys.csv
Matching based on title and author similarity while preserving cite_keys.
"""

import csv
import difflib
import re
from collections import defaultdict
from typing import List, Dict, Tuple, Optional

def normalize_text(text: str) -> str:
    """Normalize text for comparison by removing punctuation and converting to lowercase."""
    if not text:
        return ""
    # Remove common punctuation and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def normalize_authors(authors: str) -> str:
    """Normalize authors string for comparison."""
    if not authors:
        return ""
    # Remove common separators and normalize
    authors = re.sub(r'[;&]', ',', authors)
    authors = re.sub(r'\s+and\s+', ', ', authors, flags=re.IGNORECASE)
    authors = re.sub(r'\s*,\s*', ', ', authors)
    return normalize_text(authors)

def extract_main_authors(authors: str) -> List[str]:
    """Extract main author names from author string."""
    if not authors:
        return []
    
    # Split by common separators
    author_list = re.split(r'[,;&]|\sand\s', authors, flags=re.IGNORECASE)
    main_authors = []
    
    for author in author_list:
        author = author.strip()
        if not author:
            continue
            
        # Extract last name (assume last word before any institutional affiliation)
        words = author.split()
        if words:
            # Find the last name (typically the last word before institutional info)
            last_name = words[-1] if len(words) == 1 else words[0]
            # Remove common prefixes/suffixes
            last_name = re.sub(r'^(dr|prof|mr|ms|mrs)\.?\s*', '', last_name.lower())
            last_name = re.sub(r'\s*(jr|sr|iii?|phd|md)\.?\s*$', '', last_name.lower())
            if len(last_name) > 2:  # Only meaningful names
                main_authors.append(last_name)
    
    return main_authors[:3]  # Take first 3 authors for comparison

def calculate_similarity(title1: str, authors1: str, title2: str, authors2: str) -> float:
    """Calculate similarity between two papers based on title and authors."""
    # Normalize inputs
    norm_title1 = normalize_text(title1)
    norm_title2 = normalize_text(title2)
    norm_authors1 = normalize_authors(authors1)
    norm_authors2 = normalize_authors(authors2)
    
    # Title similarity (primary factor)
    title_similarity = difflib.SequenceMatcher(None, norm_title1, norm_title2).ratio()
    
    # Author similarity
    authors1_list = extract_main_authors(authors1)
    authors2_list = extract_main_authors(authors2)
    
    author_similarity = 0.0
    if authors1_list and authors2_list:
        # Check for overlap in main authors
        common_authors = set(authors1_list) & set(authors2_list)
        if common_authors:
            author_similarity = len(common_authors) / max(len(authors1_list), len(authors2_list))
        else:
            # Fallback to string similarity
            author_similarity = difflib.SequenceMatcher(None, norm_authors1, norm_authors2).ratio()
    
    # Combined similarity (title weighted more heavily)
    combined_similarity = (title_similarity * 0.7) + (author_similarity * 0.3)
    
    return combined_similarity

def find_best_match(target_paper: Dict, candidate_papers: List[Dict], threshold: float = 0.8) -> Optional[Tuple[Dict, float]]:
    """Find the best matching paper from candidates."""
    best_match = None
    best_score = 0.0
    
    target_title = target_paper.get('title', '') or target_paper.get('Paper Title', '')
    target_authors = target_paper.get('authors', '') or target_paper.get('Authors', '')
    
    for candidate in candidate_papers:
        candidate_title = candidate.get('title', '') or candidate.get('Paper Title', '')
        candidate_authors = candidate.get('authors', '') or candidate.get('Authors', '')
        
        similarity = calculate_similarity(target_title, target_authors, candidate_title, candidate_authors)
        
        if similarity >= threshold and similarity > best_score:
            best_score = similarity
            best_match = candidate
    
    return (best_match, best_score) if best_match else None

def merge_csv_files():
    """Main function to merge the two CSV files."""
    
    # Read research_papers_clean.csv
    clean_papers = []
    with open('/Users/invoture/dev.local/hdm/research_papers_clean.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        clean_papers = list(reader)
    
    # Read research_table_with_citekeys.csv
    table_papers = []
    with open('/Users/invoture/dev.local/hdm/research_table_with_citekeys.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        table_papers = list(reader)
    
    print(f"Loaded {len(clean_papers)} papers from research_papers_clean.csv")
    print(f"Loaded {len(table_papers)} papers from research_table_with_citekeys.csv")
    
    # Get all column names from both files
    clean_columns = set(clean_papers[0].keys()) if clean_papers else set()
    table_columns = set(table_papers[0].keys()) if table_papers else set()
    all_columns = sorted(clean_columns | table_columns)
    
    # Track matches and non-matches
    matches = []
    unmatched_clean = []
    unmatched_table = []
    used_table_indices = set()
    
    # For each paper in clean_papers, try to find a match in table_papers
    for clean_paper in clean_papers:
        available_table_papers = [
            table_papers[i] for i in range(len(table_papers)) 
            if i not in used_table_indices
        ]
        
        match_result = find_best_match(clean_paper, available_table_papers, threshold=0.75)
        
        if match_result:
            table_match, score = match_result
            
            # Find the index of the matched paper
            table_index = next(
                i for i, paper in enumerate(table_papers) 
                if paper is table_match
            )
            used_table_indices.add(table_index)
            
            # Merge the papers (table data takes precedence for overlapping columns)
            merged_paper = {}
            
            # Start with clean paper data
            for col in all_columns:
                merged_paper[col] = clean_paper.get(col, '')
            
            # Override with table paper data where available
            for col in all_columns:
                table_value = table_match.get(col, '')
                if table_value and table_value.strip():
                    merged_paper[col] = table_value
            
            # Ensure cite_key is preserved from the source that has it
            if clean_paper.get('cite_key'):
                merged_paper['cite_key'] = clean_paper['cite_key']
            elif table_match.get('cite_key'):
                merged_paper['cite_key'] = table_match['cite_key']
            
            matches.append({
                'merged': merged_paper,
                'score': score,
                'clean_title': clean_paper.get('title', ''),
                'table_title': table_match.get('Paper Title', ''),
                'clean_cite_key': clean_paper.get('cite_key', ''),
                'table_cite_key': table_match.get('cite_key', '')
            })
            
            print(f"MATCH (score: {score:.3f}): {clean_paper.get('cite_key', 'N/A')} <-> {table_match.get('cite_key', 'N/A')}")
        else:
            unmatched_clean.append(clean_paper)
    
    # Add unmatched papers from table_papers
    for i, table_paper in enumerate(table_papers):
        if i not in used_table_indices:
            # Convert table paper to match all_columns format
            merged_paper = {}
            for col in all_columns:
                merged_paper[col] = table_paper.get(col, '')
            unmatched_table.append(merged_paper)
    
    # Combine all papers
    final_papers = []
    
    # Add matched papers
    for match in matches:
        final_papers.append(match['merged'])
    
    # Add unmatched papers from clean file
    for paper in unmatched_clean:
        merged_paper = {}
        for col in all_columns:
            merged_paper[col] = paper.get(col, '')
        final_papers.append(merged_paper)
    
    # Add unmatched papers from table file
    final_papers.extend(unmatched_table)
    
    # Write merged CSV
    output_file = '/Users/invoture/dev.local/hdm/research_papers_merged.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_columns)
        writer.writeheader()
        writer.writerows(final_papers)
    
    # Generate summary report
    print(f"\n=== MERGE SUMMARY ===")
    print(f"Total papers in merged file: {len(final_papers)}")
    print(f"Matched papers: {len(matches)}")
    print(f"Unmatched from clean file: {len(unmatched_clean)}")
    print(f"Unmatched from table file: {len(unmatched_table)}")
    print(f"Output written to: {output_file}")
    
    # Show match details
    if matches:
        print(f"\n=== MATCH DETAILS ===")
        for i, match in enumerate(matches[:10]):  # Show first 10 matches
            print(f"{i+1}. Score: {match['score']:.3f}")
            print(f"   Clean: {match['clean_cite_key']} - {match['clean_title'][:80]}...")
            print(f"   Table: {match['table_cite_key']} - {match['table_title'][:80]}...")
            print()
    
    # Show some unmatched papers for manual review
    if unmatched_clean:
        print(f"\n=== SAMPLE UNMATCHED FROM CLEAN FILE ===")
        for i, paper in enumerate(unmatched_clean[:5]):
            print(f"{i+1}. {paper.get('cite_key', 'N/A')} - {paper.get('title', '')[:80]}...")
    
    if unmatched_table:
        print(f"\n=== SAMPLE UNMATCHED FROM TABLE FILE ===")
        for i, paper in enumerate(unmatched_table[:5]):
            print(f"{i+1}. {paper.get('cite_key', 'N/A')} - {paper.get('Paper Title', '')[:80]}...")

if __name__ == '__main__':
    merge_csv_files()
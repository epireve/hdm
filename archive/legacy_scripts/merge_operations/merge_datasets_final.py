#!/usr/bin/env python3
"""
Final consolidated merge script for HDM project datasets
Combines functionality from multiple merge scripts into one clean implementation
"""

import csv
import re
from pathlib import Path
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional

def normalize_title(title: str) -> str:
    """Normalize title for matching"""
    if not title:
        return ""
    
    # Convert to lowercase
    title = title.lower()
    
    # Remove punctuation and special characters
    title = re.sub(r'[^\w\s]', ' ', title)
    
    # Remove extra whitespace
    title = ' '.join(title.split())
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    words = [w for w in title.split() if w not in stop_words]
    
    return ' '.join(words)

def calculate_similarity(title1: str, title2: str) -> float:
    """Calculate similarity between two titles"""
    norm1 = normalize_title(title1)
    norm2 = normalize_title(title2)
    
    # Exact match after normalization
    if norm1 == norm2:
        return 1.0
    
    # Substring match for longer titles
    if len(norm1) > 10 and len(norm2) > 10:
        if norm1 in norm2 or norm2 in norm1:
            return 0.9
    
    # Use SequenceMatcher for fuzzy matching
    return SequenceMatcher(None, norm1, norm2).ratio()

def extract_papers_from_complex_csv(file_path: Path) -> List[Dict]:
    """Extract papers from complex multi-line CSV format"""
    papers = []
    
    # Pattern to identify start of a paper entry
    paper_pattern = re.compile(r'^[A-Z][^,]+,"[^"]+",\d{4},')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    current_paper = []
    in_paper = False
    
    for line in lines:
        if paper_pattern.match(line):
            # Process previous paper if exists
            if current_paper:
                paper_text = '\n'.join(current_paper)
                try:
                    # Parse the CSV line
                    reader = csv.DictReader([paper_text])
                    paper = next(reader)
                    papers.append(paper)
                except:
                    pass
            
            # Start new paper
            current_paper = [line]
            in_paper = True
        elif in_paper and line.strip():
            # Continue current paper
            current_paper.append(line)
    
    # Process last paper
    if current_paper:
        paper_text = '\n'.join(current_paper)
        try:
            reader = csv.DictReader([paper_text])
            paper = next(reader)
            papers.append(paper)
        except:
            pass
    
    return papers

def merge_datasets(primary_file: Path, secondary_file: Path, output_file: Path, 
                  unmatched_file: Optional[Path] = None, similarity_threshold: float = 0.85) -> Dict:
    """
    Merge two CSV datasets based on paper title matching
    
    Args:
        primary_file: Main dataset CSV file
        secondary_file: Secondary dataset to merge (can be complex format)
        output_file: Output merged CSV file
        unmatched_file: Optional file to save unmatched papers
        similarity_threshold: Minimum similarity score for fuzzy matching
    
    Returns:
        Dictionary with merge statistics
    """
    
    # Read primary dataset
    print(f"Reading primary dataset: {primary_file}")
    with open(primary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        primary_papers = list(reader)
        primary_fieldnames = reader.fieldnames
    
    print(f"Loaded {len(primary_papers)} papers from primary dataset")
    
    # Check if secondary file is complex format
    print(f"\nReading secondary dataset: {secondary_file}")
    
    # Try standard CSV first
    try:
        with open(secondary_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            secondary_papers = list(reader)
            secondary_fieldnames = reader.fieldnames
    except:
        # Fall back to complex format extraction
        print("Detected complex CSV format, using specialized parser...")
        secondary_papers = extract_papers_from_complex_csv(secondary_file)
        if secondary_papers:
            secondary_fieldnames = list(secondary_papers[0].keys())
        else:
            secondary_fieldnames = []
    
    print(f"Loaded {len(secondary_papers)} papers from secondary dataset")
    
    # Create normalized title index for primary papers
    print("\nBuilding search index...")
    primary_index = {}
    for i, paper in enumerate(primary_papers):
        if 'title' in paper:
            norm_title = normalize_title(paper['title'])
            if norm_title:
                primary_index[norm_title] = i
    
    # Merge statistics
    stats = {
        'total_primary': len(primary_papers),
        'total_secondary': len(secondary_papers),
        'exact_matches': 0,
        'fuzzy_matches': 0,
        'unmatched': 0,
        'match_details': []
    }
    
    # Process secondary papers
    print("\nMatching papers...")
    unmatched_papers = []
    
    for sec_paper in secondary_papers:
        matched = False
        match_info = None
        
        # Try to find matching paper
        sec_title = sec_paper.get('Papers') or sec_paper.get('title') or ''
        if not sec_title:
            continue
        
        norm_sec_title = normalize_title(sec_title)
        
        # Check exact match first
        if norm_sec_title in primary_index:
            primary_idx = primary_index[norm_sec_title]
            matched = True
            match_info = ('exact_title', 1.0)
            stats['exact_matches'] += 1
        else:
            # Try fuzzy matching
            best_score = 0
            best_idx = -1
            
            for norm_title, idx in primary_index.items():
                score = calculate_similarity(sec_title, primary_papers[idx]['title'])
                if score > best_score:
                    best_score = score
                    best_idx = idx
            
            if best_score >= similarity_threshold:
                primary_idx = best_idx
                matched = True
                match_info = ('fuzzy_title', best_score)
                stats['fuzzy_matches'] += 1
        
        if matched:
            # Add secondary data to primary paper with prefix
            primary_paper = primary_papers[primary_idx]
            
            # Add match metadata
            primary_paper['match_type'] = match_info[0]
            primary_paper['match_score'] = str(match_info[1])
            
            # Add secondary fields with prefix
            for field in secondary_fieldnames:
                if field not in primary_fieldnames:
                    prefixed_field = f"pkg_{field}"
                    primary_paper[prefixed_field] = sec_paper.get(field, '')
            
            stats['match_details'].append({
                'primary_title': primary_paper['title'],
                'secondary_title': sec_title,
                'match_type': match_info[0],
                'score': match_info[1]
            })
        else:
            stats['unmatched'] += 1
            unmatched_papers.append(sec_paper)
    
    # Calculate all fieldnames for output
    all_fieldnames = list(primary_fieldnames)
    
    # Add match metadata fields
    if 'match_type' not in all_fieldnames:
        all_fieldnames.append('match_type')
    if 'match_score' not in all_fieldnames:
        all_fieldnames.append('match_score')
    
    # Add prefixed secondary fields
    for field in secondary_fieldnames:
        if field not in primary_fieldnames:
            prefixed_field = f"pkg_{field}"
            if prefixed_field not in all_fieldnames:
                all_fieldnames.append(prefixed_field)
    
    # Write merged dataset
    print(f"\nWriting merged dataset to: {output_file}")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_fieldnames)
        writer.writeheader()
        writer.writerows(primary_papers)
    
    # Write unmatched papers if requested
    if unmatched_file and unmatched_papers:
        print(f"\nWriting {len(unmatched_papers)} unmatched papers to: {unmatched_file}")
        with open(unmatched_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=secondary_fieldnames)
            writer.writeheader()
            writer.writerows(unmatched_papers)
    
    # Print statistics
    print("\n=== Merge Statistics ===")
    print(f"Primary papers: {stats['total_primary']}")
    print(f"Secondary papers: {stats['total_secondary']}")
    print(f"Exact matches: {stats['exact_matches']}")
    print(f"Fuzzy matches: {stats['fuzzy_matches']}")
    print(f"Total matched: {stats['exact_matches'] + stats['fuzzy_matches']}")
    print(f"Unmatched: {stats['unmatched']}")
    
    if stats['total_secondary'] > 0:
        match_rate = (stats['exact_matches'] + stats['fuzzy_matches']) / stats['total_secondary'] * 100
        print(f"Match rate: {match_rate:.1f}%")
    
    return stats

def main():
    """Main function with example usage"""
    project_root = Path(__file__).parent.parent.parent
    
    # Define file paths
    primary_file = project_root / "research_papers_complete_FINAL_normalized_tags.csv"
    secondary_file = project_root / "personalized_pkg_paperguide_clean.csv"
    output_file = project_root / "research_papers_merged_final.csv"
    unmatched_file = project_root / "unmatched_papers.csv"
    
    # Check if files exist
    if not primary_file.exists():
        print(f"Error: Primary file not found: {primary_file}")
        return
    
    if not secondary_file.exists():
        print(f"Error: Secondary file not found: {secondary_file}")
        return
    
    # Perform merge
    stats = merge_datasets(
        primary_file=primary_file,
        secondary_file=secondary_file,
        output_file=output_file,
        unmatched_file=unmatched_file,
        similarity_threshold=0.85
    )
    
    print("\nMerge completed successfully!")

if __name__ == "__main__":
    main()
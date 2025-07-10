#!/usr/bin/env python3
"""
Final merge script using clean CSV files
"""

import csv
import re
from pathlib import Path
from difflib import SequenceMatcher
import time

def normalize_title(title):
    """Normalize title for matching"""
    if not title:
        return ""
    
    # Convert to lowercase
    title = title.lower()
    
    # Remove all punctuation
    title = re.sub(r'[^\w\s]', ' ', title)
    
    # Remove extra spaces
    title = ' '.join(title.split())
    
    # Remove common words
    stop_words = ['the', 'a', 'an', 'of', 'for', 'and', 'in', 'on', 'using', 'with', 'via', 'through']
    words = [w for w in title.split() if w not in stop_words]
    
    return ' '.join(words)

def calculate_similarity(title1, title2):
    """Calculate similarity between titles"""
    norm1 = normalize_title(title1)
    norm2 = normalize_title(title2)
    
    if not norm1 or not norm2:
        return 0.0
    
    # Exact match
    if norm1 == norm2:
        return 1.0
    
    # Substring match
    if len(norm1) > 10 and len(norm2) > 10:
        if norm1 in norm2 or norm2 in norm1:
            return 0.9
    
    # Fuzzy match
    return SequenceMatcher(None, norm1, norm2).ratio()

def match_by_authors(authors1, authors2):
    """Match by author names"""
    if not authors1 or not authors2:
        return 0.0
    
    # Extract last names
    def get_last_names(authors):
        names = []
        for author in re.split(r'[,;]', authors):
            author = author.strip()
            if author:
                parts = author.split()
                if parts:
                    # Last word is usually last name
                    last_name = parts[-1].lower()
                    if len(last_name) > 2:
                        names.append(last_name)
        return names
    
    names1 = get_last_names(authors1)
    names2 = get_last_names(authors2)
    
    if not names1 or not names2:
        return 0.0
    
    # Count common last names
    common = set(names1) & set(names2)
    if common:
        return len(common) / min(len(names1), len(names2))
    
    return 0.0

def main():
    start_time = time.time()
    
    # File paths
    project_root = Path(__file__).parent.parent.parent
    primary_file = project_root / "research_papers_complete_FINAL.csv"
    secondary_file = project_root / "pkg_papers_clean.csv"
    output_merged = project_root / "research_papers_merged_final.csv"
    output_unmatched = project_root / "unmatched_papers_final.csv"
    output_report = project_root / "merge_report_final.txt"
    
    # Load primary dataset
    print("Loading primary dataset...")
    with open(primary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        primary_papers = list(reader)
        primary_fieldnames = list(reader.fieldnames)
    print(f"Loaded {len(primary_papers)} papers from primary dataset")
    
    # Load secondary dataset
    print("\nLoading secondary dataset...")
    with open(secondary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        secondary_papers = list(reader)
        secondary_fieldnames = list(reader.fieldnames)
    print(f"Loaded {len(secondary_papers)} papers from secondary dataset")
    
    # Create lookup index
    print("\nBuilding search index...")
    primary_titles_norm = {}
    for i, paper in enumerate(primary_papers):
        norm = normalize_title(paper.get('title', ''))
        if norm:
            primary_titles_norm[norm] = i
    
    # Match papers
    print("\nMatching papers...")
    matches = []
    unmatched = []
    used_primary = set()
    
    for j, sec_paper in enumerate(secondary_papers):
        if j % 50 == 0:
            print(f"  Processing {j}/{len(secondary_papers)}...")
        
        sec_title = sec_paper.get('Papers', '')
        sec_authors = sec_paper.get('Authors', '')
        
        best_idx = None
        best_score = 0.0
        match_type = None
        
        # Try title matching
        if sec_title:
            # Check normalized exact match first
            sec_norm = normalize_title(sec_title)
            if sec_norm in primary_titles_norm:
                idx = primary_titles_norm[sec_norm]
                if idx not in used_primary:
                    best_idx = idx
                    best_score = 1.0
                    match_type = 'exact_title'
            
            # If no exact match, try fuzzy
            if not best_idx:
                for i, prim_paper in enumerate(primary_papers):
                    if i in used_primary:
                        continue
                    
                    prim_title = prim_paper.get('title', '')
                    
                    # Calculate similarity
                    score = calculate_similarity(prim_title, sec_title)
                    
                    if score > best_score and score >= 0.7:
                        best_score = score
                        best_idx = i
                        match_type = 'fuzzy_title'
        
        # Try author matching if no good title match
        if best_score < 0.8 and sec_authors:
            for i, prim_paper in enumerate(primary_papers):
                if i in used_primary:
                    continue
                
                prim_authors = prim_paper.get('authors', '')
                author_score = match_by_authors(prim_authors, sec_authors)
                
                if author_score >= 0.5:
                    # Verify with title if possible
                    title_score = calculate_similarity(
                        prim_paper.get('title', ''), 
                        sec_title
                    ) if sec_title else 0
                    
                    combined = (author_score * 0.4) + (title_score * 0.6)
                    
                    if combined > best_score and combined >= 0.6:
                        best_score = combined
                        best_idx = i
                        match_type = 'author+title'
        
        # Record match or unmatched
        if best_idx is not None and best_score >= 0.6:
            matches.append({
                'primary_idx': best_idx,
                'secondary_paper': sec_paper,
                'score': best_score,
                'match_type': match_type
            })
            used_primary.add(best_idx)
        else:
            unmatched.append(sec_paper)
    
    print(f"\nMatched {len(matches)} papers")
    print(f"Unmatched {len(unmatched)} papers")
    
    # Create extended fieldnames
    extended_fieldnames = list(primary_fieldnames)
    for field in secondary_fieldnames:
        pkg_field = f"pkg_{field}"
        if pkg_field not in extended_fieldnames:
            extended_fieldnames.append(pkg_field)
    
    # Add match info fields
    if 'match_score' not in extended_fieldnames:
        extended_fieldnames.append('match_score')
    if 'match_type' not in extended_fieldnames:
        extended_fieldnames.append('match_type')
    
    # Create merged dataset
    print("\nCreating merged dataset...")
    merged_papers = []
    
    for i, prim_paper in enumerate(primary_papers):
        merged_paper = prim_paper.copy()
        
        # Find match
        match_found = False
        for match in matches:
            if match['primary_idx'] == i:
                # Add secondary data
                for key, value in match['secondary_paper'].items():
                    merged_paper[f"pkg_{key}"] = value
                
                merged_paper['match_score'] = f"{match['score']:.3f}"
                merged_paper['match_type'] = match['match_type']
                match_found = True
                break
        
        if not match_found:
            # Fill empty values
            for field in extended_fieldnames:
                if field not in merged_paper:
                    merged_paper[field] = ""
        
        merged_papers.append(merged_paper)
    
    # Write merged dataset
    with open(output_merged, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=extended_fieldnames)
        writer.writeheader()
        writer.writerows(merged_papers)
    
    print(f"Merged dataset saved to: {output_merged}")
    
    # Write unmatched papers
    if unmatched:
        with open(output_unmatched, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=secondary_fieldnames)
            writer.writeheader()
            writer.writerows(unmatched)
        
        print(f"Unmatched papers saved to: {output_unmatched}")
    
    # Write report
    elapsed = time.time() - start_time
    
    with open(output_report, 'w') as f:
        f.write("=== Final Merge Report ===\n\n")
        f.write(f"Processing time: {elapsed:.1f} seconds\n\n")
        f.write(f"Primary dataset: {len(primary_papers)} papers\n")
        f.write(f"Secondary dataset: {len(secondary_papers)} papers\n")
        f.write(f"Matched: {len(matches)} papers\n")
        f.write(f"Unmatched: {len(unmatched)} papers\n")
        f.write(f"Match rate (from primary): {len(matches)/len(primary_papers)*100:.1f}%\n")
        f.write(f"Match rate (from secondary): {len(matches)/len(secondary_papers)*100:.1f}%\n\n")
        
        # Match type breakdown
        match_types = {}
        for match in matches:
            mt = match['match_type']
            match_types[mt] = match_types.get(mt, 0) + 1
        
        f.write("Match types:\n")
        for mt, count in sorted(match_types.items()):
            f.write(f"  {mt}: {count}\n")
        
        # High confidence matches
        f.write("\n=== High Confidence Matches (score >= 0.9) ===\n")
        high_conf = sorted([m for m in matches if m['score'] >= 0.9], 
                          key=lambda x: x['score'], reverse=True)
        
        for i, match in enumerate(high_conf[:20]):
            prim = primary_papers[match['primary_idx']]
            sec = match['secondary_paper']
            f.write(f"\n{i+1}. Score: {match['score']:.3f} ({match['match_type']})\n")
            f.write(f"   Primary: {prim.get('title', '')[:80]}\n")
            f.write(f"   Secondary: {sec.get('Papers', '')[:80]}\n")
    
    print(f"\nReport saved to: {output_report}")
    
    # Summary
    print(f"\n=== Final Summary ===")
    print(f"Processing time: {elapsed:.1f} seconds")
    print(f"Match rate from primary perspective: {len(matches)/len(primary_papers)*100:.1f}%")
    print(f"Match rate from secondary perspective: {len(matches)/len(secondary_papers)*100:.1f}%")
    print(f"High confidence matches (>= 0.9): {len([m for m in matches if m['score'] >= 0.9])}")

if __name__ == "__main__":
    main()
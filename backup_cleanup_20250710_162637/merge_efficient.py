#!/usr/bin/env python3
"""
Efficient merge script with chunked processing
"""

import csv
import re
from pathlib import Path
from difflib import SequenceMatcher
import time

def extract_paper_entries(file_path, max_papers=None):
    """Extract paper entries more efficiently"""
    papers = []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Skip header
        header = f.readline()
        
        paper_count = 0
        for line in f:
            if max_papers and paper_count >= max_papers:
                break
                
            line = line.strip()
            if not line:
                continue
            
            # Quick check for paper title pattern
            if (not line.startswith(',') and 
                not line.startswith(' ') and 
                len(line) > 50 and
                ',' in line):
                
                # Extract first few fields
                parts = line.split(',', 4)
                if len(parts) >= 3:
                    title = parts[0].strip(' "')
                    authors = parts[1].strip(' "') if len(parts) > 1 else ''
                    year = parts[2].strip(' "') if len(parts) > 2 else ''
                    
                    # Filter out non-paper entries
                    if (title and 
                        'Paper Title' not in title and
                        len(title) > 20 and
                        not title.startswith('http')):
                        
                        papers.append({
                            'Papers': title,
                            'Authors': authors,
                            'Published Year': year
                        })
                        paper_count += 1
    
    return papers

def normalize_text(text):
    """Fast text normalization"""
    if not text:
        return ""
    # Quick normalization
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return ' '.join(text.split())

def quick_match(text1, text2, threshold=0.7):
    """Quick matching algorithm"""
    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)
    
    if not norm1 or not norm2:
        return 0.0
    
    # Quick exact match check
    if norm1 == norm2:
        return 1.0
    
    # Quick substring check
    if len(norm1) > 10 and len(norm2) > 10:
        if norm1 in norm2 or norm2 in norm1:
            return 0.85
    
    # Only do expensive matching for promising candidates
    if abs(len(norm1) - len(norm2)) / max(len(norm1), len(norm2)) > 0.5:
        return 0.0  # Too different in length
    
    return SequenceMatcher(None, norm1, norm2).ratio()

def main():
    start_time = time.time()
    
    # File paths
    project_root = Path(__file__).parent.parent.parent
    primary_file = project_root / "research_papers_complete_FINAL.csv"
    secondary_file = project_root / "personalized_pkg_paperguide.csv"
    output_merged = project_root / "research_papers_merged_efficient.csv"
    output_unmatched = project_root / "unmatched_papers_efficient.csv"
    output_report = project_root / "merge_report_efficient.txt"
    
    print("Loading primary dataset...")
    primary_papers = []
    primary_fieldnames = []
    with open(primary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        primary_fieldnames = list(reader.fieldnames)
        primary_papers = list(reader)
    
    print(f"Loaded {len(primary_papers)} papers from primary dataset")
    
    print("\nExtracting papers from secondary dataset...")
    # Extract papers more efficiently
    secondary_papers = extract_paper_entries(secondary_file, max_papers=None)
    print(f"Extracted {len(secondary_papers)} papers from secondary dataset")
    
    # Create title index for faster lookup
    print("\nBuilding search index...")
    primary_index = {}
    for i, paper in enumerate(primary_papers):
        norm_title = normalize_text(paper.get('title', ''))
        if norm_title:
            # Store first few words as key for faster lookup
            key_words = norm_title.split()[:5]
            key = ' '.join(key_words)
            if key not in primary_index:
                primary_index[key] = []
            primary_index[key].append(i)
    
    # Match papers
    print("\nMatching papers...")
    matches = []
    unmatched = []
    matched_primary = set()
    
    for j, sec_paper in enumerate(secondary_papers):
        if j % 100 == 0:
            print(f"  Processing {j}/{len(secondary_papers)}...")
        
        sec_title = sec_paper.get('Papers', '')
        if not sec_title:
            unmatched.append(sec_paper)
            continue
        
        # Find best match
        best_idx = None
        best_score = 0.0
        
        # Get normalized title
        norm_sec = normalize_text(sec_title)
        if not norm_sec:
            unmatched.append(sec_paper)
            continue
        
        # Look for potential matches using index
        sec_words = norm_sec.split()[:5]
        sec_key = ' '.join(sec_words)
        
        # Check exact key match first
        if sec_key in primary_index:
            for idx in primary_index[sec_key]:
                if idx not in matched_primary:
                    score = quick_match(
                        primary_papers[idx].get('title', ''), 
                        sec_title
                    )
                    if score > best_score:
                        best_score = score
                        best_idx = idx
        
        # If no good match, try broader search
        if best_score < 0.7:
            # Try first 3 words only
            sec_key_short = ' '.join(sec_words[:3])
            for key in primary_index:
                if sec_key_short in key or key in sec_key_short:
                    for idx in primary_index[key]:
                        if idx not in matched_primary:
                            score = quick_match(
                                primary_papers[idx].get('title', ''), 
                                sec_title
                            )
                            if score > best_score:
                                best_score = score
                                best_idx = idx
        
        if best_idx is not None and best_score >= 0.7:
            matches.append({
                'primary_idx': best_idx,
                'secondary_paper': sec_paper,
                'score': best_score
            })
            matched_primary.add(best_idx)
        else:
            unmatched.append(sec_paper)
    
    print(f"\nMatched {len(matches)} papers")
    print(f"Unmatched {len(unmatched)} papers")
    
    # Create merged dataset
    print("\nCreating merged dataset...")
    
    # Add pkg columns
    extended_fieldnames = primary_fieldnames + [
        'pkg_Papers', 'pkg_Authors', 'pkg_Published Year', 'match_score'
    ]
    
    # Build merged papers
    merged_papers = []
    for i, prim_paper in enumerate(primary_papers):
        merged_paper = prim_paper.copy()
        
        # Find match
        match_found = False
        for match in matches:
            if match['primary_idx'] == i:
                sec_paper = match['secondary_paper']
                merged_paper['pkg_Papers'] = sec_paper.get('Papers', '')
                merged_paper['pkg_Authors'] = sec_paper.get('Authors', '')
                merged_paper['pkg_Published Year'] = sec_paper.get('Published Year', '')
                merged_paper['match_score'] = f"{match['score']:.3f}"
                match_found = True
                break
        
        if not match_found:
            merged_paper['pkg_Papers'] = ''
            merged_paper['pkg_Authors'] = ''
            merged_paper['pkg_Published Year'] = ''
            merged_paper['match_score'] = ''
        
        merged_papers.append(merged_paper)
    
    # Write merged dataset
    with open(output_merged, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=extended_fieldnames)
        writer.writeheader()
        writer.writerows(merged_papers)
    
    print(f"Merged dataset saved to: {output_merged}")
    
    # Write unmatched
    if unmatched:
        with open(output_unmatched, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Papers', 'Authors', 'Published Year'])
            writer.writeheader()
            writer.writerows(unmatched)
        print(f"Unmatched papers saved to: {output_unmatched}")
    
    # Write report
    with open(output_report, 'w') as f:
        f.write(f"=== Merge Report ===\n\n")
        f.write(f"Completed in: {time.time() - start_time:.1f} seconds\n\n")
        f.write(f"Primary papers: {len(primary_papers)}\n")
        f.write(f"Secondary papers: {len(secondary_papers)}\n")
        f.write(f"Matched: {len(matches)}\n")
        f.write(f"Unmatched: {len(unmatched)}\n")
        f.write(f"Match rate: {len(matches)/len(secondary_papers)*100:.1f}%\n\n")
        
        f.write("=== Top Matches ===\n")
        sorted_matches = sorted(matches, key=lambda x: x['score'], reverse=True)
        for i, match in enumerate(sorted_matches[:20]):
            prim = primary_papers[match['primary_idx']]
            sec = match['secondary_paper']
            f.write(f"\n{i+1}. Score: {match['score']:.3f}\n")
            f.write(f"   Primary: {prim.get('title', '')[:80]}\n")
            f.write(f"   Secondary: {sec.get('Papers', '')[:80]}\n")
    
    print(f"Report saved to: {output_report}")
    
    # Summary
    elapsed = time.time() - start_time
    print(f"\n=== Summary (completed in {elapsed:.1f}s) ===")
    print(f"Match rate: {len(matches)/len(secondary_papers)*100:.1f}%")
    print(f"High confidence matches (>= 0.9): {len([m for m in matches if m['score'] >= 0.9])}")

if __name__ == "__main__":
    main()
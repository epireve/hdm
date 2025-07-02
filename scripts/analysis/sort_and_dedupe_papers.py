#!/usr/bin/env python3
"""
Sort papers alphabetically by title and identify duplicates for removal
"""

import csv
import os
from collections import defaultdict
import difflib

def read_csv_papers(csv_path):
    """Read the CSV file and return list of papers"""
    papers = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)
    
    return papers

def normalize_title(title):
    """Normalize title for comparison (lowercase, remove extra spaces, punctuation)"""
    import re
    # Convert to lowercase
    normalized = title.lower()
    # Remove common punctuation and extra spaces
    normalized = re.sub(r'[^\w\s]', ' ', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized

def find_duplicates(papers):
    """Find potential duplicate papers based on title similarity"""
    duplicates = defaultdict(list)
    cite_key_duplicates = defaultdict(list)
    
    # Group by normalized title
    title_groups = defaultdict(list)
    for paper in papers:
        normalized_title = normalize_title(paper['title'])
        title_groups[normalized_title].append(paper)
    
    # Find exact title matches
    for normalized_title, paper_list in title_groups.items():
        if len(paper_list) > 1:
            duplicates[f"Exact title match: {normalized_title}"] = paper_list
    
    # Group by cite_key
    for paper in papers:
        cite_key_duplicates[paper['cite_key']].append(paper)
    
    # Find cite_key duplicates
    cite_key_dups = {}
    for cite_key, paper_list in cite_key_duplicates.items():
        if len(paper_list) > 1:
            cite_key_dups[f"Duplicate cite_key: {cite_key}"] = paper_list
    
    # Find similar titles (fuzzy matching)
    similar_titles = defaultdict(list)
    paper_titles = [(paper, normalize_title(paper['title'])) for paper in papers]
    
    for i, (paper1, title1) in enumerate(paper_titles):
        for paper2, title2 in paper_titles[i+1:]:
            # Use difflib to find similar titles (threshold: 0.8 similarity)
            similarity = difflib.SequenceMatcher(None, title1, title2).ratio()
            if similarity > 0.8 and title1 != title2:
                key = f"Similar titles ({similarity:.2f}): {title1[:50]}..."
                similar_titles[key].extend([paper1, paper2])
    
    return duplicates, cite_key_dups, similar_titles

def write_sorted_csv(papers, output_path):
    """Write papers sorted alphabetically by title to new CSV"""
    # Sort papers by title (case-insensitive)
    sorted_papers = sorted(papers, key=lambda x: x['title'].lower())
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        if sorted_papers:
            fieldnames = sorted_papers[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_papers)
    
    return sorted_papers

def write_duplicate_report(duplicates, cite_key_dups, similar_titles, output_path):
    """Write a detailed duplicate analysis report"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Duplicate Papers Analysis Report\n\n")
        f.write(f"Generated on: {os.popen('date').read().strip()}\n\n")
        
        # Exact title duplicates
        f.write("## 1. Exact Title Duplicates\n\n")
        if duplicates:
            for group_name, papers in duplicates.items():
                f.write(f"### {group_name}\n")
                for paper in papers:
                    f.write(f"- **Cite Key:** {paper['cite_key']}\n")
                    f.write(f"  **Title:** {paper['title']}\n")
                    f.write(f"  **Authors:** {paper['authors']}\n")
                    f.write(f"  **Year:** {paper['year']}\n\n")
                f.write("**Recommendation:** Keep the most complete entry, remove others.\n\n")
        else:
            f.write("No exact title duplicates found.\n\n")
        
        # Cite key duplicates
        f.write("## 2. Duplicate Cite Keys\n\n")
        if cite_key_dups:
            for group_name, papers in cite_key_dups.items():
                f.write(f"### {group_name}\n")
                for paper in papers:
                    f.write(f"- **Title:** {paper['title']}\n")
                    f.write(f"  **Authors:** {paper['authors']}\n")
                    f.write(f"  **Year:** {paper['year']}\n\n")
                f.write("**Recommendation:** Rename cite keys to make them unique.\n\n")
        else:
            f.write("No duplicate cite keys found.\n\n")
        
        # Similar titles
        f.write("## 3. Similar Titles (Potential Duplicates)\n\n")
        if similar_titles:
            processed_pairs = set()
            for group_name, papers in similar_titles.items():
                # Remove duplicates from the similar titles list
                unique_papers = []
                seen_cite_keys = set()
                for paper in papers:
                    if paper['cite_key'] not in seen_cite_keys:
                        unique_papers.append(paper)
                        seen_cite_keys.add(paper['cite_key'])
                
                if len(unique_papers) >= 2:
                    # Create a unique identifier for this pair
                    pair_id = tuple(sorted([p['cite_key'] for p in unique_papers[:2]]))
                    if pair_id not in processed_pairs:
                        processed_pairs.add(pair_id)
                        f.write(f"### {group_name}\n")
                        for paper in unique_papers[:2]:  # Only show first 2 similar papers
                            f.write(f"- **Cite Key:** {paper['cite_key']}\n")
                            f.write(f"  **Title:** {paper['title']}\n")
                            f.write(f"  **Authors:** {paper['authors']}\n")
                            f.write(f"  **Year:** {paper['year']}\n\n")
                        f.write("**Recommendation:** Review manually to determine if these are the same paper.\n\n")
        else:
            f.write("No similar titles found.\n\n")
        
        # Summary
        total_exact_dups = sum(len(papers) for papers in duplicates.values())
        total_cite_key_dups = sum(len(papers) for papers in cite_key_dups.values())
        total_similar = len(processed_pairs) * 2 if similar_titles else 0
        
        f.write("## Summary\n\n")
        f.write(f"- **Exact title duplicates:** {total_exact_dups} papers in {len(duplicates)} groups\n")
        f.write(f"- **Cite key duplicates:** {total_cite_key_dups} papers in {len(cite_key_dups)} groups\n")
        f.write(f"- **Similar titles:** {len(processed_pairs)} potential duplicate pairs\n")
        f.write(f"- **Total papers requiring review:** {total_exact_dups + total_cite_key_dups + total_similar}\n")

def main():
    """Main function"""
    input_csv = "/Users/invoture/dev.local/hdm/research_papers_clean.csv"
    output_csv = "/Users/invoture/dev.local/hdm/research_papers_sorted.csv"
    duplicate_report = "/Users/invoture/dev.local/hdm/duplicate_analysis_report.md"
    
    print("=== SORTING AND DUPLICATE ANALYSIS ===")
    print("Reading papers from CSV...")
    
    # Read papers
    papers = read_csv_papers(input_csv)
    print(f"Found {len(papers)} papers")
    
    # Find duplicates
    print("Analyzing duplicates...")
    duplicates, cite_key_dups, similar_titles = find_duplicates(papers)
    
    # Write sorted CSV
    print("Sorting papers alphabetically by title...")
    sorted_papers = write_sorted_csv(papers, output_csv)
    print(f"Sorted CSV written to: {output_csv}")
    
    # Write duplicate report
    print("Generating duplicate analysis report...")
    write_duplicate_report(duplicates, cite_key_dups, similar_titles, duplicate_report)
    print(f"Duplicate report written to: {duplicate_report}")
    
    # Summary
    total_exact_dups = sum(len(papers) for papers in duplicates.values())
    total_cite_key_dups = sum(len(papers) for papers in cite_key_dups.values())
    
    print(f"\n=== SUMMARY ===")
    print(f"Papers sorted alphabetically: {len(sorted_papers)}")
    print(f"Exact title duplicates: {total_exact_dups} papers in {len(duplicates)} groups")
    print(f"Cite key duplicates: {total_cite_key_dups} papers in {len(cite_key_dups)} groups")
    print(f"Similar title pairs: {len(similar_titles)} potential duplicates")
    print(f"\nReview the duplicate report for detailed analysis and removal recommendations.")

if __name__ == "__main__":
    main()
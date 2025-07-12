#!/usr/bin/env python3
"""
Compare old and new CSV files to:
1. Find any missing papers from the old list
2. Merge analysis columns from old CSV into new CSV
"""
import csv
import json
from pathlib import Path

def normalize_title(title):
    """Normalize title for comparison"""
    if not title:
        return ""
    # Remove extra spaces and convert to lowercase
    return ' '.join(title.lower().strip().split())

def load_old_csv(filepath):
    """Load the old CSV with all analysis columns"""
    papers = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)
    return papers

def load_new_csv(filepath):
    """Load the new cleaned CSV"""
    papers = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)
    return papers

def find_missing_papers(old_papers, new_papers):
    """Find papers that exist in old list but not in new"""
    # Create lookup sets based on normalized titles
    new_titles = {normalize_title(p['title']) for p in new_papers}
    
    missing = []
    for old_paper in old_papers:
        old_title = normalize_title(old_paper.get('Paper Title', ''))
        if old_title and old_title not in new_titles:
            missing.append(old_paper)
    
    return missing

def merge_analysis_columns(old_papers, new_papers):
    """Merge analysis columns from old CSV into new CSV"""
    # Analysis columns to merge
    analysis_columns = [
        'Downloaded', 'Relevancy', 'Relevancy Justification', 
        'Insights', 'TL;DR', 'Summary', 'Research Question',
        'Methodology', 'Key Findings', 'Primary Outcomes',
        'Limitations', 'Conclusion', 'Research Gaps',
        'Future Work', 'Implementation Insights', 'url', 'DOI', 'Tags'
    ]
    
    # Create lookup by normalized title
    old_by_title = {}
    for paper in old_papers:
        title = normalize_title(paper.get('Paper Title', ''))
        if title:
            old_by_title[title] = paper
    
    # Merge data
    merged_papers = []
    matches_found = 0
    
    for new_paper in new_papers:
        merged = new_paper.copy()
        new_title = normalize_title(new_paper['title'])
        
        # Find matching old paper
        if new_title in old_by_title:
            old_paper = old_by_title[new_title]
            matches_found += 1
            
            # Merge analysis columns
            for col in analysis_columns:
                if col in old_paper:
                    merged[col] = old_paper[col]
        else:
            # Initialize empty analysis columns
            for col in analysis_columns:
                merged[col] = ""
        
        merged_papers.append(merged)
    
    return merged_papers, matches_found

def save_merged_csv(papers, filepath):
    """Save merged data to CSV"""
    if not papers:
        return
    
    # Define column order
    columns = ['cite_key', 'title', 'authors', 'year', 
               'Downloaded', 'Relevancy', 'Relevancy Justification',
               'Insights', 'TL;DR', 'Summary', 'Research Question',
               'Methodology', 'Key Findings', 'Primary Outcomes',
               'Limitations', 'Conclusion', 'Research Gaps',
               'Future Work', 'Implementation Insights', 'url', 'DOI', 'Tags']
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(papers)

def main():
    # Load both CSV files
    print("Loading CSV files...")
    old_papers = load_old_csv('research_table_with_citekeys.csv')
    new_papers = load_new_csv('research_papers_clean_final.csv')
    
    print(f"Old CSV has {len(old_papers)} papers")
    print(f"New CSV has {len(new_papers)} papers")
    
    # Find missing papers
    print("\nChecking for missing papers...")
    missing = find_missing_papers(old_papers, new_papers)
    
    if missing:
        print(f"\nFound {len(missing)} papers in old list but not in new:")
        for i, paper in enumerate(missing, 1):
            print(f"{i}. {paper.get('Paper Title', 'Unknown')} ({paper.get('Year', '?')})")
            print(f"   Authors: {paper.get('Authors', 'Unknown')}")
            print(f"   Cite Key: {paper.get('cite_key', 'N/A')}")
            print()
        
        # Save missing papers list
        with open('missing_papers.json', 'w', encoding='utf-8') as f:
            json.dump(missing, f, indent=2)
        print(f"Detailed missing papers list saved to: missing_papers.json")
    else:
        print("No missing papers found - all papers from old list are in new list!")
    
    # Merge analysis columns
    print("\nMerging analysis columns from old CSV...")
    merged_papers, matches = merge_analysis_columns(old_papers, new_papers)
    
    print(f"Successfully matched {matches} out of {len(new_papers)} papers")
    
    # Save merged CSV
    output_file = 'research_papers_merged_final.csv'
    save_merged_csv(merged_papers, output_file)
    print(f"\nMerged CSV saved to: {output_file}")
    
    # Summary report
    print("\n" + "="*50)
    print("MERGE SUMMARY")
    print("="*50)
    print(f"Papers in old CSV: {len(old_papers)}")
    print(f"Papers in new CSV: {len(new_papers)}")
    print(f"Missing from new: {len(missing)}")
    print(f"Successfully merged: {matches}")
    print(f"Papers without analysis data: {len(new_papers) - matches}")

if __name__ == "__main__":
    main()
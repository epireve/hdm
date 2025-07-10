#!/usr/bin/env python3
"""
Merge processed relevancy data back into the complete dataset
"""

import csv
import json
from pathlib import Path

def merge_processed_data():
    project_root = Path(__file__).parent.parent.parent
    
    # Files
    original_csv = project_root / "research_papers_complete.csv"
    checkpoint_file = Path(__file__).parent / "relevancy_checkpoint.json"
    output_csv = project_root / "research_papers_complete_final.csv"
    
    # Load checkpoint to get processed papers
    with open(checkpoint_file, 'r') as f:
        checkpoint = json.load(f)
    processed_cite_keys = set(checkpoint['processed'])
    
    print(f"Total papers processed: {len(processed_cite_keys)}")
    
    # Read all papers
    with open(original_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
        fieldnames = reader.fieldnames
    
    # Read processed data from any temporary files
    # First, let's find all papers that were processed
    processed_data = {}
    
    # Check if there's a partial update file
    partial_update = project_root / "research_papers_complete_updated.csv"
    if partial_update.exists():
        with open(partial_update, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['cite_key'] in processed_cite_keys:
                    processed_data[row['cite_key']] = row
    
    # Also check test output
    test_output = project_root / "research_papers_test_output.csv"
    if test_output.exists():
        with open(test_output, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['cite_key'] in processed_cite_keys and row['cite_key'] not in processed_data:
                    processed_data[row['cite_key']] = row
    
    print(f"Found {len(processed_data)} papers with updated data")
    
    # Merge the data
    updated_count = 0
    for paper in papers:
        cite_key = paper['cite_key']
        if cite_key in processed_data:
            # Update relevancy and justification
            paper['Relevancy'] = processed_data[cite_key].get('Relevancy', paper.get('Relevancy', ''))
            paper['Relevancy Justification'] = processed_data[cite_key].get('Relevancy Justification', paper.get('Relevancy Justification', ''))
            updated_count += 1
    
    print(f"Updated {updated_count} papers in the complete dataset")
    
    # Write the complete updated dataset
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"Complete dataset saved to: {output_csv}")
    
    # Show statistics
    relevancy_stats = {'SUPER': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'Missing': 0}
    justification_count = 0
    
    for paper in papers:
        rel = paper.get('Relevancy', '').strip().upper()
        if rel in relevancy_stats:
            relevancy_stats[rel] += 1
        else:
            relevancy_stats['Missing'] += 1
        
        just = paper.get('Relevancy Justification', '').strip()
        if just and just.lower() not in ['', 'none', 'null', 'not available']:
            justification_count += 1
    
    print("\n=== Final Statistics ===")
    print(f"Total papers: {len(papers)}")
    print(f"Papers with relevancy ratings:")
    for level, count in relevancy_stats.items():
        if level != 'Missing':
            print(f"  {level}: {count}")
    print(f"Papers missing relevancy: {relevancy_stats['Missing']}")
    print(f"Papers with justifications: {justification_count}")
    print(f"Papers missing justifications: {len(papers) - justification_count}")

if __name__ == "__main__":
    merge_processed_data()
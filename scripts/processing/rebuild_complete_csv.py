#!/usr/bin/env python3
"""
Rebuild the complete CSV with all processed relevancy data
"""

import csv
import json
from pathlib import Path

def rebuild_complete_csv():
    project_root = Path(__file__).parent.parent.parent
    
    # Files
    original_csv = project_root / "research_papers_complete.csv"
    test_output = project_root / "research_papers_test_output.csv"
    partial_update = project_root / "research_papers_complete_updated.csv"
    checkpoint_file = Path(__file__).parent / "relevancy_checkpoint.json"
    output_csv = project_root / "research_papers_complete_with_relevancy.csv"
    
    # Load checkpoint to get processed papers
    print("Loading checkpoint data...")
    with open(checkpoint_file, 'r') as f:
        checkpoint = json.load(f)
    processed_cite_keys = set(checkpoint['processed'])
    print(f"Total papers processed: {len(processed_cite_keys)}")
    
    # Read all original papers
    print("Reading original dataset...")
    with open(original_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_papers = list(reader)
        fieldnames = reader.fieldnames
    print(f"Total papers in dataset: {len(all_papers)}")
    
    # Create a map of processed data
    processed_data = {}
    
    # Read test output if exists
    if test_output.exists():
        print("Reading test output data...")
        with open(test_output, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cite_key = row.get('cite_key')
                if cite_key and cite_key in processed_cite_keys:
                    processed_data[cite_key] = {
                        'Relevancy': row.get('Relevancy', ''),
                        'Relevancy Justification': row.get('Relevancy Justification', '')
                    }
    
    # Read partial update if exists
    if partial_update.exists():
        print("Reading partial update data...")
        with open(partial_update, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cite_key = row.get('cite_key')
                if cite_key and cite_key in processed_cite_keys:
                    processed_data[cite_key] = {
                        'Relevancy': row.get('Relevancy', ''),
                        'Relevancy Justification': row.get('Relevancy Justification', '')
                    }
    
    print(f"Found processed data for {len(processed_data)} papers")
    
    # Now, since we have 225 processed papers but only found data for some,
    # let's run through the papers and update what we can
    updated_count = 0
    for paper in all_papers:
        cite_key = paper.get('cite_key')
        if cite_key in processed_data:
            paper['Relevancy'] = processed_data[cite_key]['Relevancy']
            paper['Relevancy Justification'] = processed_data[cite_key]['Relevancy Justification']
            updated_count += 1
    
    print(f"Updated {updated_count} papers with new relevancy data")
    
    # Write the complete dataset
    print(f"Writing complete dataset to: {output_csv}")
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_papers)
    
    # Show statistics
    print("\n=== Statistics ===")
    relevancy_counts = {'SUPER': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    missing_relevancy = 0
    missing_justification = 0
    
    for paper in all_papers:
        rel = paper.get('Relevancy', '').strip().upper()
        if rel in relevancy_counts:
            relevancy_counts[rel] += 1
        elif not rel:
            missing_relevancy += 1
        
        just = paper.get('Relevancy Justification', '').strip()
        if not just or just.lower() in ['', 'none', 'null', 'not available']:
            missing_justification += 1
    
    print(f"Total papers: {len(all_papers)}")
    print("\nRelevancy distribution:")
    for level, count in relevancy_counts.items():
        print(f"  {level}: {count}")
    print(f"  Missing: {missing_relevancy}")
    print(f"\nPapers with justifications: {len(all_papers) - missing_justification}")
    print(f"Papers missing justifications: {missing_justification}")
    
    if missing_relevancy > 0 or missing_justification > 0:
        print(f"\nWARNING: Some papers are still missing data!")
        print(f"This might be because the processing output files don't contain all the processed data.")
        print(f"You may need to re-run the processing script with the fixed version.")

if __name__ == "__main__":
    rebuild_complete_csv()
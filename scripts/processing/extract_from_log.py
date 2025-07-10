#!/usr/bin/env python3
"""
Extract relevancy and justification data from the processing log
"""

import re
import csv
import json
from pathlib import Path
from collections import defaultdict

def extract_data_from_log():
    log_file = Path(__file__).parent / "relevancy_analysis.log"
    output_file = Path(__file__).parent.parent.parent / "research_papers_complete_extracted.csv"
    
    # Pattern to match processing lines
    processing_pattern = r"Processing paper \d+/\d+: (\w+)"
    relevancy_pattern = r"Relevancy: (SUPER|HIGH|MEDIUM|LOW)"
    
    # Read log file
    print("Reading log file...")
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Extract data
    extracted_data = {}
    current_paper = None
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for processing start
        match = re.search(processing_pattern, line)
        if match:
            current_paper = match.group(1)
            extracted_data[current_paper] = {'relevancy': None, 'justification': None}
        
        # Check for relevancy
        if current_paper and "Relevancy:" in line:
            match = re.search(relevancy_pattern, line)
            if match:
                extracted_data[current_paper]['relevancy'] = match.group(1)
        
        # Check for justification generation
        if current_paper and "Generated justification" in line:
            extracted_data[current_paper]['has_justification'] = True
        
        i += 1
    
    print(f"Extracted data for {len(extracted_data)} papers")
    
    # Now read the original CSV and update it
    project_root = Path(__file__).parent.parent.parent
    original_csv = project_root / "research_papers_complete.csv"
    
    with open(original_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
        fieldnames = reader.fieldnames
    
    # Update papers with extracted data
    updated_count = 0
    for paper in papers:
        cite_key = paper.get('cite_key')
        if cite_key in extracted_data:
            data = extracted_data[cite_key]
            if data['relevancy']:
                paper['Relevancy'] = data['relevancy']
                updated_count += 1
    
    print(f"Updated {updated_count} papers with relevancy data")
    
    # Clean fieldnames and write output
    clean_fieldnames = [f for f in fieldnames if f is not None]
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=clean_fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"Output saved to: {output_file}")
    
    # Statistics
    stats = defaultdict(int)
    for data in extracted_data.values():
        if data['relevancy']:
            stats[data['relevancy']] += 1
    
    print("\nRelevancy distribution from log:")
    for level, count in sorted(stats.items()):
        print(f"  {level}: {count}")
    
    return extracted_data

if __name__ == "__main__":
    extract_data_from_log()
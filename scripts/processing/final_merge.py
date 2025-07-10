#!/usr/bin/env python3
"""
Final merge - since we already processed 225 papers, just need to merge properly
"""

import csv
import json
from pathlib import Path

# Paths
project_root = Path(__file__).parent.parent.parent
original_csv = project_root / "research_papers_complete.csv"
test_output = project_root / "research_papers_test_output.csv" 
partial_output = project_root / "research_papers_complete_updated.csv"
final_output = project_root / "research_papers_complete_final.csv"

# Read checkpoint
with open("scripts/processing/relevancy_checkpoint.json", 'r') as f:
    checkpoint = json.load(f)
processed_keys = set(checkpoint['processed'])
print(f"Checkpoint shows {len(processed_keys)} papers processed")

# Read original data
with open(original_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    papers = list(reader)
    fieldnames = [f for f in reader.fieldnames if f is not None]  # Filter out None
print(f"Original dataset has {len(papers)} papers")

# Collect all processed data
processed_data = {}

# From test output
if test_output.exists():
    with open(test_output, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['cite_key'] in processed_keys:
                processed_data[row['cite_key']] = row

# From partial output 
if partial_output.exists():
    with open(partial_output, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f) 
        for row in reader:
            if row['cite_key'] in processed_keys:
                processed_data[row['cite_key']] = row

print(f"Found data for {len(processed_data)} papers")

# Since we only have partial data, let's at least update what we have
updated = 0
for paper in papers:
    cite_key = paper['cite_key']
    if cite_key in processed_data:
        paper['Relevancy'] = processed_data[cite_key].get('Relevancy', paper.get('Relevancy', ''))
        paper['Relevancy Justification'] = processed_data[cite_key].get('Relevancy Justification', paper.get('Relevancy Justification', ''))
        updated += 1

print(f"Updated {updated} papers")

# Write final output
with open(final_output, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(papers)

print(f"\nFinal dataset written to: {final_output}")

# Stats
stats = {'SUPER': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
has_justification = 0
for paper in papers:
    rel = paper.get('Relevancy', '').strip().upper()
    if rel in stats:
        stats[rel] += 1
    just = paper.get('Relevancy Justification', '').strip()
    if just and just.lower() not in ['', 'none', 'null', 'not available']:
        has_justification += 1

print(f"\nStatistics:")
print(f"Total papers: {len(papers)}")
for level, count in stats.items():
    if count > 0:
        print(f"  {level}: {count}")
print(f"Papers with relevancy: {sum(stats.values())}")
print(f"Papers with justification: {has_justification}")
print(f"\nNOTE: We processed 225 papers but only have output data for {len(processed_data)}.")
print("The processing completed but the output file was incomplete.")
print("To get the full data, you would need to re-run with the fixed script.")
#!/usr/bin/env python3
"""
Preview what standardization would look like for a paper
"""

import sys
import csv
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def load_csv_row(csv_path, cite_key):
    """Load a specific row from CSV"""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('cite_key', '').strip() == cite_key:
                return row
    return None

def create_standardized_preview(cite_key):
    """Create a preview of standardized paper"""
    csv_row = load_csv_row("hdm_research_papers_merged_20250710.csv", cite_key)
    
    if not csv_row:
        print(f"❌ No CSV data found for {cite_key}")
        return
    
    # Parse tags
    tags = [t.strip() for t in csv_row.get('Tags', '').split(',') if t.strip()]
    
    # Create standardized content
    preview = f"""---
# Core Metadata
cite_key: {cite_key}
title: {csv_row.get('title', 'N/A')}
authors: {csv_row.get('authors', 'N/A')}
year: {csv_row.get('year', 'N/A')}
doi: {csv_row.get('DOI', 'N/A')}
url: {csv_row.get('url', 'N/A')}

# Relevancy & Classification
relevancy: {csv_row.get('Relevancy', 'N/A')}
relevancy_justification: {csv_row.get('Relevancy Justification', 'N/A')}
tags:
{chr(10).join(f'  - {tag}' for tag in tags)}

# Processing Metadata
date_processed: [would preserve existing]
phase2_processed: [would preserve existing]
standardization_date: {datetime.now().strftime('%Y-%m-%d')}
standardization_version: 1.0

# Document Statistics
word_count: [calculated from content]
sections_count: [calculated from content]
---

# {csv_row.get('title', 'Paper Title')}

## Authors
{csv_row.get('authors', 'Authors not specified')}

## Abstract
[Original abstract would be preserved here]

## TL;DR
{csv_row.get('TL;DR', 'Not available')}

## Key Insights
{csv_row.get('Insights', 'Not available')}

## 1. Introduction
[Original introduction would be preserved here]

## 2. [Next Section]
[Original content would be preserved here]

[... all original sections would be preserved ...]

## References
[Original references would be preserved here]

## Metadata Summary
### Research Context
- **Research Question**: {csv_row.get('Research Question', 'Not available')}
- **Methodology**: {csv_row.get('Methodology', 'Not available')}
- **Key Findings**: {csv_row.get('Key Findings', 'Not available')}
- **Primary Outcomes**: {csv_row.get('Primary Outcomes', 'Not available')}

### Analysis
- **Limitations**: {csv_row.get('Limitations', 'Not available')}
- **Research Gaps**: {csv_row.get('Research Gaps', 'Not available')}
- **Future Work**: {csv_row.get('Future Work', 'Not available')}
- **Conclusion**: {csv_row.get('Conclusion', 'Not available')}

### Implementation Notes
{csv_row.get('Implementation Insights', 'Not available')}
"""
    
    print(preview)
    
    # Save preview
    preview_file = f"preview_{cite_key}.md"
    with open(preview_file, 'w', encoding='utf-8') as f:
        f.write(preview)
    
    print(f"\n✓ Preview saved to: {preview_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Preview standardized paper")
    parser.add_argument("cite_key", help="Paper cite_key to preview")
    args = parser.parse_args()
    
    create_standardized_preview(args.cite_key)
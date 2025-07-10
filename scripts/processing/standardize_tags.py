#!/usr/bin/env python3
"""
Standardize Tags column to use comma separation only (no arrays)
"""

import csv
import re
from pathlib import Path

def standardize_tags(tags_value):
    """Convert various tag formats to comma-separated string"""
    if not tags_value:
        return ""
    
    # Remove array brackets and quotes
    tags = tags_value.strip()
    
    # Handle array format like ['tag1', 'tag2'] or ["tag1", "tag2"]
    if tags.startswith('[') and tags.endswith(']'):
        # Remove brackets
        tags = tags[1:-1]
        
        # Remove quotes around individual tags
        # Handle both single and double quotes
        tags = re.sub(r"['\"]", '', tags)
        
        # Clean up any extra spaces
        tags = re.sub(r'\s*,\s*', ', ', tags)
        
    # Handle already comma-separated but might have quotes
    else:
        # Remove any quotes
        tags = tags.replace('"', '').replace("'", '')
        
        # Standardize comma spacing
        tags = re.sub(r'\s*,\s*', ', ', tags)
    
    # Clean up any double spaces
    tags = re.sub(r'\s+', ' ', tags)
    
    # Remove any trailing/leading whitespace
    tags = tags.strip()
    
    return tags

def process_file(input_file, output_file):
    """Process CSV file to standardize Tags column"""
    
    print(f"Reading {input_file}...")
    
    # Read the CSV
    papers = []
    fieldnames = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        papers = list(reader)
    
    print(f"Loaded {len(papers)} papers")
    
    # Process Tags column
    print("\nStandardizing Tags column...")
    
    tags_standardized = 0
    sample_changes = []
    
    for paper in papers:
        if 'Tags' in paper and paper['Tags']:
            original = paper['Tags']
            standardized = standardize_tags(original)
            
            if original != standardized:
                tags_standardized += 1
                if len(sample_changes) < 5:
                    sample_changes.append({
                        'original': original[:100] + '...' if len(original) > 100 else original,
                        'standardized': standardized[:100] + '...' if len(standardized) > 100 else standardized
                    })
                
                paper['Tags'] = standardized
    
    print(f"Standardized {tags_standardized} tag entries")
    
    if sample_changes:
        print("\n=== Sample Changes ===")
        for i, change in enumerate(sample_changes, 1):
            print(f"\n{i}. Original: {change['original']}")
            print(f"   Standardized: {change['standardized']}")
    
    # Write the updated CSV
    print(f"\nWriting to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"Saved {len(papers)} papers with standardized tags")
    
    # Show tag statistics
    print("\n=== Tag Statistics ===")
    
    tag_counts = {}
    papers_with_tags = 0
    
    for paper in papers:
        if 'Tags' in paper and paper['Tags']:
            papers_with_tags += 1
            tags = [t.strip() for t in paper['Tags'].split(',') if t.strip()]
            
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    print(f"Papers with tags: {papers_with_tags}")
    print(f"Unique tags: {len(tag_counts)}")
    
    # Show most common tags
    if tag_counts:
        print("\nTop 20 most common tags:")
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        for tag, count in sorted_tags[:20]:
            print(f"  {tag}: {count}")

def main():
    project_root = Path(__file__).parent.parent.parent
    
    # Process the merged file
    input_file = project_root / "research_papers_merged_final.csv"
    output_file = project_root / "research_papers_merged_final_clean_tags.csv"
    
    print("=== Processing Merged File ===")
    process_file(input_file, output_file)
    
    # Also process the original complete file if needed
    original_file = project_root / "research_papers_complete_FINAL.csv"
    if original_file.exists():
        print("\n\n=== Processing Original Complete File ===")
        output_original = project_root / "research_papers_complete_FINAL_clean_tags.csv"
        process_file(original_file, output_original)

if __name__ == "__main__":
    main()
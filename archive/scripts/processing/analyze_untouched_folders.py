#!/usr/bin/env python3
"""
Analyze untouched folders to extract metadata and check for duplicates
"""
import os
import json
import csv
import re
from pathlib import Path
from collections import defaultdict

def extract_metadata_from_markdown(md_file):
    """Extract YAML frontmatter from markdown file"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if file has YAML frontmatter
        if content.startswith('---\n'):
            # Find the ending --- 
            end_idx = content.find('\n---\n', 4)
            if end_idx != -1:
                yaml_content = content[4:end_idx]
                # Parse YAML manually
                metadata = {}
                current_key = None
                for line in yaml_content.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if line.startswith('- '):
                        # List item
                        if current_key and current_key not in metadata:
                            metadata[current_key] = []
                        if current_key and isinstance(metadata[current_key], list):
                            metadata[current_key].append(line[2:].strip())
                    elif ':' in line:
                        # Key-value pair
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Handle quoted strings
                        if value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        elif value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        
                        if value:
                            metadata[key] = value
                        else:
                            current_key = key
                            
                return metadata
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
    return None

def load_existing_data():
    """Load existing CSV files to check for duplicates"""
    existing_papers = {}
    
    # Load research_papers_clean.csv
    csv_file = 'research_papers_clean.csv'
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_papers[row['cite_key']] = {
                    'title': row['title'],
                    'authors': row['authors'],
                    'year': row['year']
                }
    
    # Load research_table_with_citekeys.csv if exists
    table_file = 'research_table_with_citekeys.csv'
    if os.path.exists(table_file):
        with open(table_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('cite_key') and row['cite_key'] not in existing_papers:
                    existing_papers[row['cite_key']] = {
                        'title': row.get('Paper Title', ''),
                        'authors': row.get('Authors', ''),
                        'year': row.get('Year', '')
                    }
    
    return existing_papers

def analyze_untouched_folders():
    """Analyze all untouched folders"""
    # Read list of untouched folders
    with open('untouched_folders_complete_list.txt', 'r') as f:
        untouched_folders = [line.strip() for line in f if line.strip()]
    
    # Load existing papers
    existing_papers = load_existing_data()
    
    # Results storage
    folder_metadata = {}
    duplicates = defaultdict(list)
    missing_metadata = []
    
    markdown_papers_dir = Path('markdown_papers')
    
    for folder_name in untouched_folders:
        folder_path = markdown_papers_dir / folder_name
        
        if not folder_path.exists():
            print(f"Warning: Folder {folder_name} not found")
            continue
            
        # Find markdown file
        md_files = list(folder_path.glob('*.md'))
        if not md_files:
            print(f"Warning: No markdown file in {folder_name}")
            missing_metadata.append(folder_name)
            continue
            
        # Use first markdown file found
        md_file = md_files[0]
        metadata = extract_metadata_from_markdown(md_file)
        
        if metadata:
            folder_metadata[folder_name] = metadata
            
            # Check if this is a duplicate of existing papers
            cite_key = metadata.get('cite_key', '')
            if cite_key and cite_key in existing_papers:
                duplicates[cite_key].append(folder_name)
        else:
            missing_metadata.append(folder_name)
    
    # Find papers with same title but different cite_keys
    title_map = defaultdict(list)
    for folder_name, metadata in folder_metadata.items():
        title = metadata.get('title', '').lower().strip()
        if title:
            title_map[title].append((folder_name, metadata))
    
    # Save results
    results = {
        'total_untouched': len(untouched_folders),
        'folders_analyzed': len(folder_metadata),
        'missing_metadata': missing_metadata,
        'duplicates_by_cite_key': dict(duplicates),
        'duplicates_by_title': {title: folders for title, folders in title_map.items() if len(folders) > 1},
        'folder_metadata': folder_metadata
    }
    
    # Save detailed results
    with open('untouched_folders_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Create summary report
    create_summary_report(results)
    
    return results

def create_summary_report(results):
    """Create a summary markdown report"""
    report = []
    report.append("# Untouched Folders Analysis Report\n")
    report.append(f"## Summary Statistics\n")
    report.append(f"- Total untouched folders: {results['total_untouched']}")
    report.append(f"- Folders with metadata: {results['folders_analyzed']}")
    report.append(f"- Folders missing metadata: {len(results['missing_metadata'])}")
    report.append(f"- Duplicate cite_keys found: {len(results['duplicates_by_cite_key'])}")
    report.append(f"- Papers with same title: {len(results['duplicates_by_title'])}\n")
    
    if results['duplicates_by_cite_key']:
        report.append("## Duplicates by Cite Key\n")
        for cite_key, folders in results['duplicates_by_cite_key'].items():
            report.append(f"### {cite_key}")
            report.append(f"- Folders: {', '.join(folders)}\n")
    
    if results['duplicates_by_title']:
        report.append("## Duplicates by Title\n")
        for title, folders_data in results['duplicates_by_title'].items():
            report.append(f"### {title}")
            for folder_name, metadata in folders_data:
                cite_key = metadata.get('cite_key', 'no_cite_key')
                report.append(f"- {folder_name} (cite_key: {cite_key})")
            report.append("")
    
    if results['missing_metadata']:
        report.append("## Folders Missing Metadata\n")
        for folder in results['missing_metadata']:
            report.append(f"- {folder}")
    
    # Save report
    with open('untouched_folders_summary.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"Analysis complete. Results saved to:")
    print(f"- untouched_folders_analysis.json (detailed data)")
    print(f"- untouched_folders_summary.md (summary report)")

if __name__ == "__main__":
    analyze_untouched_folders()
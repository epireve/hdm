#!/usr/bin/env python3
"""
Analyze papers for duplicates and export to CSV
Checks for duplicate titles, authors, DOIs, and similar cite_keys
"""
import csv
import json
import re
from pathlib import Path
from datetime import datetime
import difflib

def extract_yaml_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not yaml_match:
        return None
    
    yaml_str = yaml_match.group(1)
    yaml_data = {}
    
    # Parse YAML manually
    current_key = None
    for line in yaml_str.split('\n'):
        if line.strip():
            if ':' in line and not line.startswith(' ') and not line.startswith('-'):
                parts = line.split(':', 1)
                current_key = parts[0].strip()
                value = parts[1].strip().strip('"').strip("'")
                yaml_data[current_key] = value
            elif current_key == 'tags' and line.startswith('  -'):
                if 'tags' not in yaml_data:
                    yaml_data['tags'] = []
                tag = line.replace('  -', '').strip().strip('"').strip("'")
                yaml_data['tags'].append(tag)
    
    # Convert tags list to string
    if 'tags' in yaml_data and isinstance(yaml_data['tags'], list):
        yaml_data['tags'] = ', '.join(yaml_data['tags'])
    
    return yaml_data

def normalize_title(title):
    """Normalize title for comparison"""
    if not title:
        return ""
    # Remove quotes, convert to lowercase, remove extra spaces
    title = re.sub(r'["\']', '', title)
    title = re.sub(r'\s+', ' ', title)
    return title.lower().strip()

def normalize_authors(authors):
    """Normalize authors for comparison"""
    if not authors:
        return ""
    # Remove extra spaces, convert to lowercase
    authors = re.sub(r'\s+', ' ', authors)
    return authors.lower().strip()

def find_similar_strings(strings, threshold=0.85):
    """Find similar strings using difflib"""
    similar_groups = []
    processed = set()
    
    for i, s1 in enumerate(strings):
        if i in processed:
            continue
        
        group = [i]
        for j, s2 in enumerate(strings[i+1:], i+1):
            if j not in processed:
                ratio = difflib.SequenceMatcher(None, s1, s2).ratio()
                if ratio >= threshold:
                    group.append(j)
                    processed.add(j)
        
        if len(group) > 1:
            similar_groups.append(group)
            processed.add(i)
    
    return similar_groups

def main():
    """Main function to analyze duplicates"""
    markdown_papers = Path('markdown_papers')
    all_papers = []
    
    print("Analyzing papers for duplicates...")
    print("=" * 60)
    
    # Collect all paper data
    for folder in sorted(markdown_papers.iterdir()):
        if folder.is_dir():
            paper_path = folder / 'paper.md'
            if paper_path.exists():
                try:
                    with open(paper_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    yaml_data = extract_yaml_frontmatter(content)
                    if yaml_data:
                        paper_info = {
                            'folder': folder.name,
                            'cite_key': yaml_data.get('cite_key', ''),
                            'title': yaml_data.get('title', ''),
                            'authors': yaml_data.get('authors', ''),
                            'year': yaml_data.get('year', ''),
                            'doi': yaml_data.get('doi', ''),
                            'url': yaml_data.get('url', ''),
                            'tags': yaml_data.get('tags', ''),
                            'relevancy': yaml_data.get('relevancy', ''),
                            'title_normalized': normalize_title(yaml_data.get('title', '')),
                            'authors_normalized': normalize_authors(yaml_data.get('authors', ''))
                        }
                        all_papers.append(paper_info)
                except Exception as e:
                    print(f"Error reading {folder.name}: {e}")
    
    print(f"Total papers analyzed: {len(all_papers)}")
    
    # Find duplicates
    duplicates = {
        'exact_title': {},
        'exact_doi': {},
        'similar_title': [],
        'same_cite_key': {},
        'similar_cite_key': []
    }
    
    # Check for exact title matches
    for i, paper in enumerate(all_papers):
        if paper['title_normalized']:
            key = paper['title_normalized']
            if key not in duplicates['exact_title']:
                duplicates['exact_title'][key] = []
            duplicates['exact_title'][key].append(i)
    
    # Check for exact DOI matches
    for i, paper in enumerate(all_papers):
        if paper['doi'] and paper['doi'].strip():
            key = paper['doi'].strip()
            if key not in duplicates['exact_doi']:
                duplicates['exact_doi'][key] = []
            duplicates['exact_doi'][key].append(i)
    
    # Check for same cite_key
    for i, paper in enumerate(all_papers):
        if paper['cite_key']:
            key = paper['cite_key']
            if key not in duplicates['same_cite_key']:
                duplicates['same_cite_key'][key] = []
            duplicates['same_cite_key'][key].append(i)
    
    # Find similar titles
    titles = [p['title_normalized'] for p in all_papers]
    similar_title_groups = find_similar_strings(titles, threshold=0.85)
    duplicates['similar_title'] = similar_title_groups
    
    # Find similar cite_keys
    cite_keys = [p['cite_key'] for p in all_papers]
    similar_cite_key_groups = find_similar_strings(cite_keys, threshold=0.90)
    duplicates['similar_cite_key'] = similar_cite_key_groups
    
    # Print duplicate summary
    print("\nDUPLICATE ANALYSIS")
    print("=" * 60)
    
    # Exact title duplicates
    exact_title_count = sum(1 for group in duplicates['exact_title'].values() if len(group) > 1)
    print(f"Papers with exact same title: {exact_title_count}")
    
    # Exact DOI duplicates
    exact_doi_count = sum(1 for group in duplicates['exact_doi'].values() if len(group) > 1)
    print(f"Papers with exact same DOI: {exact_doi_count}")
    
    # Same cite_key
    same_cite_key_count = sum(1 for group in duplicates['same_cite_key'].values() if len(group) > 1)
    print(f"Papers with same cite_key: {same_cite_key_count}")
    
    # Similar titles
    print(f"Groups of similar titles: {len(duplicates['similar_title'])}")
    
    # Export to CSV
    csv_file = Path('papers_analysis.csv')
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['folder', 'cite_key', 'title', 'authors', 'year', 'doi', 'url', 
                     'tags', 'relevancy', 'duplicate_status', 'duplicate_with']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, paper in enumerate(all_papers):
            row = paper.copy()
            row.pop('title_normalized')
            row.pop('authors_normalized')
            
            # Check duplicate status
            duplicate_status = []
            duplicate_with = []
            
            # Check exact title
            for group in duplicates['exact_title'].values():
                if len(group) > 1 and i in group:
                    duplicate_status.append('exact_title')
                    for idx in group:
                        if idx != i:
                            duplicate_with.append(f"{all_papers[idx]['folder']} (title)")
            
            # Check exact DOI
            for group in duplicates['exact_doi'].values():
                if len(group) > 1 and i in group:
                    duplicate_status.append('exact_doi')
                    for idx in group:
                        if idx != i:
                            duplicate_with.append(f"{all_papers[idx]['folder']} (DOI)")
            
            # Check same cite_key
            for group in duplicates['same_cite_key'].values():
                if len(group) > 1 and i in group:
                    duplicate_status.append('same_cite_key')
                    for idx in group:
                        if idx != i:
                            duplicate_with.append(f"{all_papers[idx]['folder']} (cite_key)")
            
            row['duplicate_status'] = '; '.join(duplicate_status) if duplicate_status else ''
            row['duplicate_with'] = '; '.join(set(duplicate_with)) if duplicate_with else ''
            
            writer.writerow(row)
    
    print(f"\nCSV exported to: {csv_file}")
    
    # Export detailed duplicate report
    report_file = Path('duplicate_report.txt')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("DETAILED DUPLICATE REPORT\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 80 + "\n\n")
        
        # Exact title duplicates
        f.write("EXACT TITLE DUPLICATES\n")
        f.write("-" * 40 + "\n")
        for title, indices in duplicates['exact_title'].items():
            if len(indices) > 1:
                f.write(f"\nTitle: {title[:100]}...\n")
                for idx in indices:
                    p = all_papers[idx]
                    f.write(f"  - {p['folder']} (cite_key: {p['cite_key']}, year: {p['year']})\n")
        
        # Exact DOI duplicates
        f.write("\n\nEXACT DOI DUPLICATES\n")
        f.write("-" * 40 + "\n")
        for doi, indices in duplicates['exact_doi'].items():
            if len(indices) > 1:
                f.write(f"\nDOI: {doi}\n")
                for idx in indices:
                    p = all_papers[idx]
                    f.write(f"  - {p['folder']} (cite_key: {p['cite_key']}, title: {p['title'][:80]}...)\n")
        
        # Same cite_key
        f.write("\n\nSAME CITE_KEY\n")
        f.write("-" * 40 + "\n")
        for cite_key, indices in duplicates['same_cite_key'].items():
            if len(indices) > 1:
                f.write(f"\nCite Key: {cite_key}\n")
                for idx in indices:
                    p = all_papers[idx]
                    f.write(f"  - {p['folder']} (title: {p['title'][:80]}...)\n")
        
        # Similar titles
        f.write("\n\nSIMILAR TITLES (85%+ similarity)\n")
        f.write("-" * 40 + "\n")
        for group in duplicates['similar_title']:
            f.write("\nSimilar group:\n")
            for idx in group:
                p = all_papers[idx]
                f.write(f"  - {p['folder']}: {p['title'][:100]}...\n")
    
    print(f"Detailed report saved to: {report_file}")
    
    # Summary statistics
    print("\nSUMMARY")
    print("-" * 40)
    print(f"Total unique titles: {len(set(p['title_normalized'] for p in all_papers if p['title_normalized']))}")
    print(f"Total unique DOIs: {len(set(p['doi'] for p in all_papers if p['doi']))}")
    print(f"Total unique cite_keys: {len(set(p['cite_key'] for p in all_papers if p['cite_key']))}")

if __name__ == '__main__':
    main()
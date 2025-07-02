#!/usr/bin/env python3
"""
Update research_papers_complete.csv with current data from:
1. Current markdown paper metadata (359 papers)
2. papers_clean.csv data
3. missing_papers.json data

Goal: Keep existing structure but update with our cleaned cite_keys and current metadata
"""
import csv
import json
import re
from pathlib import Path
from datetime import datetime

def extract_yaml_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not yaml_match:
        return None
    
    yaml_str = yaml_match.group(1)
    yaml_data = {}
    
    # Parse YAML manually
    current_key = None
    tags_list = []
    in_tags = False
    keywords_list = []
    in_keywords = False
    multiline_value = []
    in_multiline = False
    
    for line in yaml_str.split('\n'):
        if line.strip():
            # Check for tags or keywords sections
            if line.strip() == 'tags:':
                in_tags = True
                in_keywords = False
                in_multiline = False
                current_key = 'tags'
                continue
            elif line.strip() == 'keywords:':
                in_keywords = True
                in_tags = False
                in_multiline = False
                current_key = 'keywords'
                continue
            elif line.startswith('  -'):
                # Handle list items
                item = line.replace('  -', '').strip().strip('"').strip("'")
                if in_tags:
                    tags_list.append(item)
                elif in_keywords:
                    keywords_list.append(item)
            elif ':' in line and not line.startswith(' ') and not line.startswith('-'):
                # Handle key-value pairs
                in_tags = False
                in_keywords = False
                parts = line.split(':', 1)
                current_key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ''
                
                # Check for multiline indicator
                if value == '|':
                    in_multiline = True
                    multiline_value = []
                else:
                    # Clean quotes from value
                    value = value.strip('"').strip("'")
                    yaml_data[current_key] = value
                    in_multiline = False
            elif in_multiline and line.startswith('  '):
                # Collect multiline content
                multiline_value.append(line[2:])
            elif in_multiline and current_key:
                # End of multiline, save it
                yaml_data[current_key] = '\n'.join(multiline_value)
                in_multiline = False
                multiline_value = []
                # Process this line again as a new key
                if ':' in line:
                    parts = line.split(':', 1)
                    current_key = parts[0].strip()
                    value = parts[1].strip() if len(parts) > 1 else ''
                    value = value.strip('"').strip("'")
                    yaml_data[current_key] = value
    
    # Save any remaining multiline content
    if in_multiline and current_key and multiline_value:
        yaml_data[current_key] = '\n'.join(multiline_value)
    
    if tags_list:
        yaml_data['tags'] = tags_list
    if keywords_list:
        yaml_data['keywords'] = keywords_list
    
    return yaml_data

def get_current_paper_metadata():
    """Get metadata from all current markdown papers"""
    markdown_papers = Path('markdown_papers')
    paper_metadata = {}
    
    for folder in sorted(markdown_papers.iterdir()):
        if folder.is_dir():
            paper_path = folder / 'paper.md'
            if paper_path.exists():
                try:
                    with open(paper_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    yaml_data = extract_yaml_frontmatter(content)
                    if yaml_data:
                        cite_key = yaml_data.get('cite_key', folder.name)
                        paper_metadata[cite_key] = {
                            'folder': folder.name,
                            'metadata': yaml_data
                        }
                except Exception as e:
                    print(f"Error reading {folder.name}: {e}")
    
    return paper_metadata

def load_papers_clean_csv():
    """Load papers_clean.csv data"""
    clean_data = {}
    clean_path = Path('papers_clean.csv')
    
    if clean_path.exists():
        with open(clean_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cite_key = row.get('cite_key', '').strip()
                if cite_key:
                    clean_data[cite_key] = row
    
    return clean_data

def load_missing_papers():
    """Load missing_papers.json data"""
    missing_papers = {}
    missing_path = Path('missing_papers.json')
    
    if missing_path.exists():
        with open(missing_path, 'r', encoding='utf-8') as f:
            papers = json.load(f)
            for paper in papers:
                cite_key = paper.get('cite_key', '').strip()
                if cite_key:
                    missing_papers[cite_key] = paper
    
    return missing_papers

def load_existing_csv():
    """Load existing research_papers_complete.csv"""
    existing_data = {}
    csv_path = Path('research_papers_complete.csv')
    
    if csv_path.exists():
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cite_key = row.get('cite_key', '').strip()
                if cite_key:
                    existing_data[cite_key] = row
    
    return existing_data

def update_paper_data(existing_data, current_metadata, clean_data, missing_data):
    """Update existing data with current information"""
    
    # Start with current papers (our 359 papers)
    updated_papers = {}
    
    # Process each current paper
    for cite_key, paper_info in current_metadata.items():
        meta = paper_info['metadata']
        
        # Start with existing data if available
        if cite_key in existing_data:
            paper_data = existing_data[cite_key].copy()
        else:
            # Create new entry
            paper_data = {
                'cite_key': cite_key,
                'title': '',
                'authors': '',
                'year': '',
                'Downloaded': '',
                'Relevancy': '',
                'Relevancy Justification': '',
                'Insights': '',
                'TL;DR': '',
                'Summary': '',
                'Research Question': '',
                'Methodology': '',
                'Key Findings': '',
                'Primary Outcomes': '',
                'Limitations': '',
                'Conclusion': '',
                'Research Gaps': '',
                'Future Work': '',
                'Implementation Insights': '',
                'url': '',
                'DOI': '',
                'Tags': ''
            }
        
        # Update with current metadata
        if meta.get('title'):
            paper_data['title'] = meta['title']
        if meta.get('authors'):
            paper_data['authors'] = meta['authors']
        if meta.get('year'):
            paper_data['year'] = str(meta['year'])
        
        # Downloaded status
        paper_data['Downloaded'] = 'Yes'
        
        # Update URL and DOI
        if meta.get('url'):
            paper_data['url'] = meta['url']
        if meta.get('doi'):
            paper_data['DOI'] = meta['doi']
        
        # Update descriptive fields from metadata
        metadata_mapping = {
            'relevancy': 'Relevancy',
            'relevancy_justification': 'Relevancy Justification',
            'insights': 'Insights',
            'tldr': 'TL;DR',
            'summary': 'Summary',
            'research_question': 'Research Question',
            'methodology': 'Methodology',
            'key_findings': 'Key Findings',
            'primary_outcomes': 'Primary Outcomes',
            'limitations': 'Limitations',
            'conclusion': 'Conclusion',
            'research_gaps': 'Research Gaps',
            'future_work': 'Future Work',
            'implementation_insights': 'Implementation Insights'
        }
        
        for meta_key, csv_key in metadata_mapping.items():
            if meta.get(meta_key):
                paper_data[csv_key] = meta[meta_key]
        
        # Handle tags
        if meta.get('tags'):
            if isinstance(meta['tags'], list):
                paper_data['Tags'] = ', '.join(meta['tags'])
            else:
                paper_data['Tags'] = meta['tags']
        
        # Update with clean CSV data if available
        if cite_key in clean_data:
            clean_row = clean_data[cite_key]
            for key, value in clean_row.items():
                if value and value.strip() and (not paper_data.get(key) or paper_data.get(key) == ''):
                    paper_data[key] = value
        
        # Update with missing papers data if available
        if cite_key in missing_data:
            missing_paper = missing_data[cite_key]
            
            field_mapping = {
                'Paper Title': 'title',
                'Authors': 'authors',
                'Year': 'year',
                'Downloaded': 'Downloaded',
                'Relevancy': 'Relevancy',
                'Relevancy Justification': 'Relevancy Justification',
                'Insights': 'Insights',
                'TL;DR': 'TL;DR',
                'Summary': 'Summary',
                'Research Question': 'Research Question',
                'Methodology': 'Methodology',
                'Key Findings': 'Key Findings',
                'Primary Outcomes': 'Primary Outcomes',
                'Limitations': 'Limitations',
                'Conclusion': 'Conclusion',
                'Research Gaps': 'Research Gaps',
                'Future Work': 'Future Work',
                'Implementation Insights': 'Implementation Insights',
                'url': 'url',
                'DOI': 'DOI',
                'Tags': 'Tags'
            }
            
            for missing_key, csv_key in field_mapping.items():
                if missing_paper.get(missing_key) and (not paper_data.get(csv_key) or paper_data.get(csv_key) == ''):
                    paper_data[csv_key] = missing_paper[missing_key]
        
        updated_papers[cite_key] = paper_data
    
    return updated_papers

def main():
    """Main function"""
    print("Updating Research Papers Complete CSV")
    print("=" * 60)
    
    # Load all data sources
    print("Loading current paper metadata...")
    current_metadata = get_current_paper_metadata()
    print(f"Found {len(current_metadata)} current papers")
    
    print("Loading papers_clean.csv...")
    clean_data = load_papers_clean_csv()
    print(f"Loaded {len(clean_data)} papers from clean CSV")
    
    print("Loading missing_papers.json...")
    missing_data = load_missing_papers()
    print(f"Loaded {len(missing_data)} papers from missing papers JSON")
    
    print("Loading existing research_papers_complete.csv...")
    existing_data = load_existing_csv()
    print(f"Loaded {len(existing_data)} papers from existing CSV")
    
    # Update the data
    print("\nUpdating paper data...")
    updated_papers = update_paper_data(existing_data, current_metadata, clean_data, missing_data)
    print(f"Updated {len(updated_papers)} papers")
    
    # Define column order (same as original)
    columns = [
        'cite_key', 'title', 'authors', 'year', 'Downloaded',
        'Relevancy', 'Relevancy Justification', 'Insights', 'TL;DR',
        'Summary', 'Research Question', 'Methodology', 'Key Findings',
        'Primary Outcomes', 'Limitations', 'Conclusion', 'Research Gaps',
        'Future Work', 'Implementation Insights', 'url', 'DOI', 'Tags'
    ]
    
    # Write updated CSV
    output_path = Path('research_papers_complete_updated.csv')
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        
        # Sort by cite_key and write
        sorted_papers = sorted(updated_papers.values(), key=lambda x: x.get('cite_key', ''))
        for paper in sorted_papers:
            # Ensure all columns exist
            row = {col: paper.get(col, '') for col in columns}
            writer.writerow(row)
    
    print(f"\nUpdated CSV written to: {output_path}")
    
    # Generate statistics
    stats = {
        'total': len(updated_papers),
        'downloaded': sum(1 for p in updated_papers.values() if p.get('Downloaded') == 'Yes'),
        'high_relevancy': sum(1 for p in updated_papers.values() if p.get('Relevancy') == 'High'),
        'with_doi': sum(1 for p in updated_papers.values() if p.get('DOI') and p.get('DOI').strip()),
        'with_url': sum(1 for p in updated_papers.values() if p.get('url') and p.get('url').strip()),
        'with_tags': sum(1 for p in updated_papers.values() if p.get('Tags') and p.get('Tags').strip()),
        'with_insights': sum(1 for p in updated_papers.values() if p.get('Insights') and p.get('Insights').strip()),
        'with_summary': sum(1 for p in updated_papers.values() if p.get('Summary') and p.get('Summary').strip())
    }
    
    print("\nStatistics:")
    print(f"  Total papers: {stats['total']}")
    print(f"  Downloaded: {stats['downloaded']} ({stats['downloaded']/stats['total']*100:.1f}%)")
    print(f"  High relevancy: {stats['high_relevancy']} ({stats['high_relevancy']/stats['total']*100:.1f}%)")
    print(f"  With DOI: {stats['with_doi']} ({stats['with_doi']/stats['total']*100:.1f}%)")
    print(f"  With URL: {stats['with_url']} ({stats['with_url']/stats['total']*100:.1f}%)")
    print(f"  With tags: {stats['with_tags']} ({stats['with_tags']/stats['total']*100:.1f}%)")
    print(f"  With insights: {stats['with_insights']} ({stats['with_insights']/stats['total']*100:.1f}%)")
    print(f"  With summary: {stats['with_summary']} ({stats['with_summary']/stats['total']*100:.1f}%)")
    
    # Create update report
    report_path = Path('research_csv_update_report.txt')
    with open(report_path, 'w') as f:
        f.write(f"Research Papers Complete CSV Update Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Data Sources:\n")
        f.write(f"  - Current markdown papers: {len(current_metadata)} papers\n")
        f.write(f"  - Papers clean CSV: {len(clean_data)} papers\n")
        f.write(f"  - Missing papers JSON: {len(missing_data)} papers\n")
        f.write(f"  - Original research papers complete: {len(existing_data)} papers\n")
        f.write(f"\nUpdate Results:\n")
        f.write(f"  - Total papers: {stats['total']}\n")
        f.write(f"  - Downloaded: {stats['downloaded']} ({stats['downloaded']/stats['total']*100:.1f}%)\n")
        f.write(f"  - High relevancy: {stats['high_relevancy']} ({stats['high_relevancy']/stats['total']*100:.1f}%)\n")
        f.write(f"  - With DOI: {stats['with_doi']} ({stats['with_doi']/stats['total']*100:.1f}%)\n")
        f.write(f"  - With URL: {stats['with_url']} ({stats['with_url']/stats['total']*100:.1f}%)\n")
        f.write(f"  - With tags: {stats['with_tags']} ({stats['with_tags']/stats['total']*100:.1f}%)\n")
        f.write(f"  - With insights: {stats['with_insights']} ({stats['with_insights']/stats['total']*100:.1f}%)\n")
        f.write(f"  - With summary: {stats['with_summary']} ({stats['with_summary']/stats['total']*100:.1f}%)\n")
        f.write(f"\nFocus: Updated existing structure with current 359 papers and cleaned metadata\n")
    
    print(f"\nUpdate report saved to: {report_path}")

if __name__ == '__main__':
    main()
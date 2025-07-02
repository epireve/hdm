#!/usr/bin/env python3
"""
Create final comprehensive research papers CSV by merging:
1. Current research_papers_complete.csv
2. Data from missing_papers.json
3. Current paper metadata from markdown files
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

def load_existing_csv(csv_path):
    """Load existing CSV data into a dictionary keyed by cite_key"""
    existing_data = {}
    
    if csv_path.exists():
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cite_key = row.get('cite_key', '').strip()
                if cite_key:
                    existing_data[cite_key] = row
    
    return existing_data

def load_missing_papers(json_path):
    """Load missing papers from JSON file"""
    missing_papers = {}
    
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            papers = json.load(f)
            for paper in papers:
                cite_key = paper.get('cite_key', '').strip()
                if cite_key:
                    missing_papers[cite_key] = paper
    
    return missing_papers

def get_paper_metadata():
    """Get metadata from all markdown papers"""
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

def merge_paper_data(existing, missing, metadata):
    """Merge data from all sources"""
    all_papers = {}
    
    # Start with existing data
    for cite_key, data in existing.items():
        all_papers[cite_key] = data.copy()
    
    # Add missing papers data
    for cite_key, paper in missing.items():
        if cite_key in all_papers:
            # Update existing entry with missing paper data
            for key, value in paper.items():
                if value and (not all_papers[cite_key].get(key) or all_papers[cite_key].get(key) == ''):
                    all_papers[cite_key][key] = value
        else:
            # Add new entry
            all_papers[cite_key] = {
                'cite_key': cite_key,
                'title': paper.get('Paper Title', paper.get('title', '')),
                'authors': paper.get('Authors', paper.get('authors', '')),
                'year': paper.get('Year', paper.get('year', '')),
                'Downloaded': paper.get('Downloaded', ''),
                'Relevancy': paper.get('Relevancy', ''),
                'Relevancy Justification': paper.get('Relevancy Justification', ''),
                'Insights': paper.get('Insights', ''),
                'TL;DR': paper.get('TL;DR', ''),
                'Summary': paper.get('Summary', ''),
                'Research Question': paper.get('Research Question', ''),
                'Methodology': paper.get('Methodology', ''),
                'Key Findings': paper.get('Key Findings', ''),
                'Primary Outcomes': paper.get('Primary Outcomes', ''),
                'Limitations': paper.get('Limitations', ''),
                'Conclusion': paper.get('Conclusion', ''),
                'Research Gaps': paper.get('Research Gaps', ''),
                'Future Work': paper.get('Future Work', ''),
                'Implementation Insights': paper.get('Implementation Insights', ''),
                'url': paper.get('url', ''),
                'DOI': paper.get('DOI', ''),
                'Tags': paper.get('Tags', '')
            }
    
    # Update with current metadata
    for cite_key, paper_info in metadata.items():
        meta = paper_info['metadata']
        
        if cite_key not in all_papers:
            all_papers[cite_key] = {'cite_key': cite_key}
        
        # Update basic fields
        all_papers[cite_key]['title'] = meta.get('title', all_papers[cite_key].get('title', ''))
        all_papers[cite_key]['authors'] = meta.get('authors', all_papers[cite_key].get('authors', ''))
        all_papers[cite_key]['year'] = meta.get('year', all_papers[cite_key].get('year', ''))
        
        # Update URL and DOI
        if meta.get('url'):
            all_papers[cite_key]['url'] = meta.get('url')
        if meta.get('doi'):
            all_papers[cite_key]['DOI'] = meta.get('doi')
        
        # Update descriptive fields if they exist in metadata
        if meta.get('relevancy'):
            all_papers[cite_key]['Relevancy'] = meta.get('relevancy')
        if meta.get('relevancy_justification'):
            all_papers[cite_key]['Relevancy Justification'] = meta.get('relevancy_justification')
        if meta.get('tldr'):
            all_papers[cite_key]['TL;DR'] = meta.get('tldr')
        if meta.get('insights'):
            all_papers[cite_key]['Insights'] = meta.get('insights')
        if meta.get('summary'):
            all_papers[cite_key]['Summary'] = meta.get('summary')
        if meta.get('research_question'):
            all_papers[cite_key]['Research Question'] = meta.get('research_question')
        if meta.get('methodology'):
            all_papers[cite_key]['Methodology'] = meta.get('methodology')
        if meta.get('key_findings'):
            all_papers[cite_key]['Key Findings'] = meta.get('key_findings')
        if meta.get('primary_outcomes'):
            all_papers[cite_key]['Primary Outcomes'] = meta.get('primary_outcomes')
        if meta.get('limitations'):
            all_papers[cite_key]['Limitations'] = meta.get('limitations')
        if meta.get('conclusion'):
            all_papers[cite_key]['Conclusion'] = meta.get('conclusion')
        if meta.get('research_gaps'):
            all_papers[cite_key]['Research Gaps'] = meta.get('research_gaps')
        if meta.get('future_work'):
            all_papers[cite_key]['Future Work'] = meta.get('future_work')
        if meta.get('implementation_insights'):
            all_papers[cite_key]['Implementation Insights'] = meta.get('implementation_insights')
        
        # Handle tags
        if meta.get('tags'):
            if isinstance(meta['tags'], list):
                all_papers[cite_key]['Tags'] = ', '.join(meta['tags'])
            else:
                all_papers[cite_key]['Tags'] = meta['tags']
        
        # Check if paper exists in markdown_papers
        if paper_info['folder'] and (Path('markdown_papers') / paper_info['folder'] / 'paper.md').exists():
            all_papers[cite_key]['Downloaded'] = 'Yes'
    
    return all_papers

def main():
    """Main function"""
    print("Creating Final Research Papers CSV")
    print("=" * 60)
    
    # Load existing data
    existing_csv = Path('research_papers_complete.csv')
    existing_data = load_existing_csv(existing_csv)
    print(f"Loaded {len(existing_data)} papers from existing CSV")
    
    # Load papers_clean.csv
    clean_csv = Path('papers_clean.csv')
    clean_data = load_existing_csv(clean_csv)
    print(f"Loaded {len(clean_data)} papers from papers_clean.csv")
    
    # Load missing papers
    missing_json = Path('missing_papers.json')
    missing_papers = load_missing_papers(missing_json)
    print(f"Loaded {len(missing_papers)} papers from missing_papers.json")
    
    # Get current metadata
    paper_metadata = get_paper_metadata()
    print(f"Found {len(paper_metadata)} papers in markdown_papers directory")
    
    # Merge all data - first merge existing with clean data
    for cite_key, data in clean_data.items():
        if cite_key in existing_data:
            # Update existing with clean data
            existing_data[cite_key].update(data)
        else:
            existing_data[cite_key] = data
    
    # Then merge with missing papers and metadata
    all_papers = merge_paper_data(existing_data, missing_papers, paper_metadata)
    print(f"\nTotal papers after merge: {len(all_papers)}")
    
    # Define column order
    columns = [
        'cite_key', 'title', 'authors', 'year', 'Downloaded', 
        'Relevancy', 'Relevancy Justification', 'Insights', 'TL;DR', 
        'Summary', 'Research Question', 'Methodology', 'Key Findings', 
        'Primary Outcomes', 'Limitations', 'Conclusion', 'Research Gaps', 
        'Future Work', 'Implementation Insights', 'url', 'DOI', 'Tags'
    ]
    
    # Write final CSV
    output_path = Path('research_papers_final.csv')
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        
        # Sort by cite_key and write
        sorted_papers = sorted(all_papers.values(), key=lambda x: x.get('cite_key', ''))
        for paper in sorted_papers:
            # Ensure all columns exist
            row = {col: paper.get(col, '') for col in columns}
            writer.writerow(row)
    
    print(f"\nFinal CSV written to: {output_path}")
    
    # Generate summary statistics
    stats = {
        'total': len(all_papers),
        'downloaded': sum(1 for p in all_papers.values() if p.get('Downloaded') == 'Yes'),
        'high_relevancy': sum(1 for p in all_papers.values() if p.get('Relevancy') == 'High'),
        'with_doi': sum(1 for p in all_papers.values() if p.get('DOI')),
        'with_url': sum(1 for p in all_papers.values() if p.get('url')),
        'with_tags': sum(1 for p in all_papers.values() if p.get('Tags')),
        'complete_metadata': sum(1 for p in all_papers.values() 
                                if all(p.get(col) for col in ['title', 'authors', 'year', 'DOI']))
    }
    
    print("\nStatistics:")
    print(f"  Downloaded papers: {stats['downloaded']} ({stats['downloaded']/stats['total']*100:.1f}%)")
    print(f"  High relevancy: {stats['high_relevancy']} ({stats['high_relevancy']/stats['total']*100:.1f}%)")
    print(f"  Papers with DOI: {stats['with_doi']} ({stats['with_doi']/stats['total']*100:.1f}%)")
    print(f"  Papers with URL: {stats['with_url']} ({stats['with_url']/stats['total']*100:.1f}%)")
    print(f"  Papers with tags: {stats['with_tags']} ({stats['with_tags']/stats['total']*100:.1f}%)")
    print(f"  Complete metadata: {stats['complete_metadata']} ({stats['complete_metadata']/stats['total']*100:.1f}%)")
    
    # Create summary report
    report_path = Path('research_csv_merge_report.txt')
    with open(report_path, 'w') as f:
        f.write(f"Research Papers CSV Merge Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Data Sources:\n")
        f.write(f"  - Research papers complete CSV: {existing_csv.name}\n")
        f.write(f"  - Papers clean CSV: {clean_csv.name}\n")
        f.write(f"  - Missing papers JSON: {len(missing_papers)} papers\n")
        f.write(f"  - Markdown papers: {len(paper_metadata)} papers\n")
        f.write(f"\nFinal Results:\n")
        f.write(f"  - Total papers: {stats['total']}\n")
        f.write(f"  - Downloaded: {stats['downloaded']} ({stats['downloaded']/stats['total']*100:.1f}%)\n")
        f.write(f"  - High relevancy: {stats['high_relevancy']} ({stats['high_relevancy']/stats['total']*100:.1f}%)\n")
        f.write(f"  - With DOI: {stats['with_doi']} ({stats['with_doi']/stats['total']*100:.1f}%)\n")
        f.write(f"  - With URL: {stats['with_url']} ({stats['with_url']/stats['total']*100:.1f}%)\n")
        f.write(f"  - With tags: {stats['with_tags']} ({stats['with_tags']/stats['total']*100:.1f}%)\n")
        f.write(f"  - Complete metadata: {stats['complete_metadata']} ({stats['complete_metadata']/stats['total']*100:.1f}%)\n")
    
    print(f"\nReport saved to: {report_path}")

if __name__ == '__main__':
    main()
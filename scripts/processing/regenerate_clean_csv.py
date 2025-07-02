#!/usr/bin/env python3
"""
Regenerate clean CSV with all updated metadata
"""
import re
import csv
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
    
    for line in yaml_str.split('\n'):
        if line.strip():
            if line.strip() == 'tags:':
                in_tags = True
                current_key = 'tags'
                continue
            elif in_tags and line.startswith('  -'):
                tag = line.replace('  -', '').strip().strip('"').strip("'")
                tags_list.append(tag)
            elif ':' in line and not line.startswith(' ') and not line.startswith('-'):
                in_tags = False
                parts = line.split(':', 1)
                current_key = parts[0].strip()
                value = parts[1].strip().strip('"').strip("'")
                yaml_data[current_key] = value
    
    if tags_list:
        yaml_data['tags'] = tags_list
    
    return yaml_data

def validate_doi(doi):
    """Check if DOI looks valid"""
    if not doi:
        return "missing"
    doi = doi.strip()
    if doi in ['10.1145/nnnnnnn.nnnnnnn', '10.1109/RpJC.2020.DOI', '']:
        return "placeholder"
    if not doi.startswith('10.'):
        return "invalid_format"
    return "valid"

def calculate_quality_score(paper_data):
    """Calculate quality score and identify issues"""
    score = 10
    issues = []
    
    # Required fields
    required_fields = ['cite_key', 'title', 'authors', 'year']
    for field in required_fields:
        if not paper_data.get(field):
            score -= 2
            issues.append(f"{field}_missing")
    
    # DOI validation
    doi_status = validate_doi(paper_data.get('doi'))
    if doi_status == "missing":
        score -= 1
        issues.append("doi_missing")
    elif doi_status == "placeholder":
        score -= 1
        issues.append("doi_placeholder")
    elif doi_status == "invalid_format":
        score -= 1
        issues.append("doi_invalid_format")
    
    # Year validation
    year = paper_data.get('year', '')
    if year:
        try:
            year_int = int(year)
            if year_int < 2000 or year_int > 2025:
                score -= 1
                issues.append("year_suspicious")
        except:
            score -= 2
            issues.append("year_invalid")
    
    # Folder/cite_key match
    if paper_data.get('folder') != paper_data.get('cite_key'):
        score -= 1
        issues.append("folder_mismatch")
    
    return score, issues

def main():
    """Main function to generate clean CSV"""
    markdown_papers = Path('markdown_papers')
    all_papers = []
    
    print("Regenerating clean CSV with all metadata updates...")
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
                        # Prepare paper data
                        paper_data = {
                            'folder': folder.name,
                            'cite_key': yaml_data.get('cite_key', ''),
                            'title': yaml_data.get('title', ''),
                            'authors': yaml_data.get('authors', ''),
                            'year': yaml_data.get('year', ''),
                            'doi': yaml_data.get('doi', ''),
                            'url': yaml_data.get('url', ''),
                            'tags': yaml_data.get('tags', []),
                            'relevancy': yaml_data.get('relevancy', ''),
                            'folder_matches_cite_key': 'Yes' if folder.name == yaml_data.get('cite_key', '') else 'No'
                        }
                        
                        # Calculate quality score
                        score, issues = calculate_quality_score(paper_data)
                        paper_data['quality_issues'] = ', '.join(issues) if issues else 'None'
                        paper_data['quality_score'] = f"{score}/10"
                        
                        # Format tags for CSV
                        if isinstance(paper_data['tags'], list):
                            paper_data['tags'] = ', '.join(paper_data['tags'])
                        
                        all_papers.append(paper_data)
                except Exception as e:
                    print(f"Error reading {folder.name}: {e}")
    
    # Sort by cite_key
    all_papers.sort(key=lambda x: x['cite_key'])
    
    # Export to CSV
    csv_path = Path('papers_clean_updated.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['folder', 'cite_key', 'title', 'authors', 'year', 'doi', 'url', 
                     'tags', 'relevancy', 'folder_matches_cite_key', 'quality_issues', 'quality_score']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_papers)
    
    print(f"CSV exported to: {csv_path}")
    
    # Generate summary statistics
    print("\nSUMMARY STATISTICS")
    print("-" * 40)
    print(f"Total papers: {len(all_papers)}")
    
    # Quality score distribution
    perfect_papers = [p for p in all_papers if p['quality_score'] == '10/10']
    good_papers = [p for p in all_papers if p['quality_score'] in ['9/10', '8/10']]
    needs_attention = [p for p in all_papers if int(p['quality_score'].split('/')[0]) < 8]
    
    print(f"Papers with perfect metadata (10/10): {len(perfect_papers)} ({len(perfect_papers)/len(all_papers)*100:.1f}%)")
    print(f"Papers with minor issues (8-9/10): {len(good_papers)} ({len(good_papers)/len(all_papers)*100:.1f}%)")
    print(f"Papers needing attention (<8/10): {len(needs_attention)} ({len(needs_attention)/len(all_papers)*100:.1f}%)")
    
    # Issue breakdown
    issue_counts = {}
    for paper in all_papers:
        if paper['quality_issues'] != 'None':
            for issue in paper['quality_issues'].split(', '):
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
    
    if issue_counts:
        print("\nIssue breakdown:")
        for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {issue}: {count} papers")
    
    # Metadata completion stats
    papers_with_tags = [p for p in all_papers if p['tags']]
    papers_with_url = [p for p in all_papers if p['url']]
    papers_with_relevancy = [p for p in all_papers if p['relevancy']]
    papers_with_doi = [p for p in all_papers if p['doi']]
    
    print("\nMetadata completion:")
    print(f"  - Papers with tags: {len(papers_with_tags)} ({len(papers_with_tags)/len(all_papers)*100:.1f}%)")
    print(f"  - Papers with URL: {len(papers_with_url)} ({len(papers_with_url)/len(all_papers)*100:.1f}%)")
    print(f"  - Papers with relevancy: {len(papers_with_relevancy)} ({len(papers_with_relevancy)/len(all_papers)*100:.1f}%)")
    print(f"  - Papers with DOI: {len(papers_with_doi)} ({len(papers_with_doi)/len(all_papers)*100:.1f}%)")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Generate a clean CSV with all papers after duplicate removal
Includes additional quality checks and metadata validation
"""
import csv
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
    
    for line in yaml_str.split('\n'):
        if line.strip():
            # Check if we're in tags section
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
    
    # Add tags if we collected any
    if tags_list:
        yaml_data['tags'] = ', '.join(tags_list)
    
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

def validate_year(year):
    """Check if year is reasonable"""
    if not year:
        return "missing"
    try:
        year_int = int(year)
        if year_int < 2000 or year_int > 2025:
            return "suspicious"
        return "valid"
    except:
        return "invalid"

def check_data_quality(paper_data):
    """Assess data quality for a paper"""
    issues = []
    
    # Check required fields
    required_fields = ['title', 'authors', 'year', 'cite_key']
    for field in required_fields:
        if not paper_data.get(field):
            issues.append(f"missing_{field}")
    
    # Validate DOI
    doi_status = validate_doi(paper_data.get('doi'))
    if doi_status != "valid":
        issues.append(f"doi_{doi_status}")
    
    # Validate year
    year_status = validate_year(paper_data.get('year'))
    if year_status != "valid":
        issues.append(f"year_{year_status}")
    
    # Check for placeholder values
    if paper_data.get('title', '').startswith('**'):
        issues.append('title_has_markdown')
    
    # Check cite_key format
    cite_key = paper_data.get('cite_key', '')
    if cite_key and not re.match(r'^[a-z]+_\d{4}[a-z]?$', cite_key):
        issues.append('cite_key_format')
    
    return issues

def main():
    """Generate clean CSV with quality checks"""
    markdown_papers = Path('markdown_papers')
    all_papers = []
    
    print("Generating clean CSV with quality checks...")
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
                        # Check folder/cite_key alignment
                        folder_matches_cite_key = folder.name == yaml_data.get('cite_key', '')
                        
                        # Get quality issues
                        quality_issues = check_data_quality(yaml_data)
                        
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
                            'folder_matches_cite_key': 'Yes' if folder_matches_cite_key else 'No',
                            'quality_issues': '; '.join(quality_issues) if quality_issues else 'None',
                            'quality_score': f"{10 - len(quality_issues)}/10"
                        }
                        all_papers.append(paper_info)
                except Exception as e:
                    print(f"Error reading {folder.name}: {e}")
    
    # Sort by cite_key
    all_papers.sort(key=lambda x: x['cite_key'])
    
    # Generate statistics
    total_papers = len(all_papers)
    papers_with_issues = sum(1 for p in all_papers if p['quality_issues'] != 'None')
    perfect_papers = sum(1 for p in all_papers if p['quality_issues'] == 'None')
    misaligned_folders = sum(1 for p in all_papers if p['folder_matches_cite_key'] == 'No')
    
    # Count specific issues
    issue_counts = {}
    for paper in all_papers:
        if paper['quality_issues'] != 'None':
            for issue in paper['quality_issues'].split('; '):
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
    
    # Export to CSV
    csv_file = Path('papers_clean.csv')
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['folder', 'cite_key', 'title', 'authors', 'year', 'doi', 'url', 
                     'tags', 'relevancy', 'folder_matches_cite_key', 'quality_issues', 'quality_score']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_papers)
    
    print(f"CSV exported to: {csv_file}")
    
    # Generate summary report
    report = []
    report.append("CLEAN PAPERS REPORT")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("=" * 60)
    report.append(f"\nTotal papers: {total_papers}")
    report.append(f"Papers with perfect metadata: {perfect_papers} ({perfect_papers/total_papers*100:.1f}%)")
    report.append(f"Papers with issues: {papers_with_issues} ({papers_with_issues/total_papers*100:.1f}%)")
    report.append(f"Folders not matching cite_key: {misaligned_folders}")
    
    report.append("\nIssue breakdown:")
    for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
        report.append(f"  - {issue}: {count} papers")
    
    # List papers with critical issues
    report.append("\nPapers with critical issues (score <= 7/10):")
    critical_papers = [p for p in all_papers if int(p['quality_score'].split('/')[0]) <= 7]
    for paper in critical_papers[:10]:  # Show first 10
        report.append(f"  - {paper['cite_key']}: {paper['quality_issues']}")
    if len(critical_papers) > 10:
        report.append(f"  ... and {len(critical_papers) - 10} more")
    
    # Papers with misaligned folders
    report.append("\nFolders not matching cite_keys:")
    misaligned = [p for p in all_papers if p['folder_matches_cite_key'] == 'No']
    for paper in misaligned[:10]:
        report.append(f"  - Folder: {paper['folder']} → Cite key: {paper['cite_key']}")
    if len(misaligned) > 10:
        report.append(f"  ... and {len(misaligned) - 10} more")
    
    # Save report
    report_path = Path('clean_papers_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print("\n" + '\n'.join(report))
    print(f"\nReport saved to: {report_path}")

if __name__ == '__main__':
    main()
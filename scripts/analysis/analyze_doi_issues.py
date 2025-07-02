#!/usr/bin/env python3
"""
Analyze and report on papers with DOI issues
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
    for line in yaml_str.split('\n'):
        if line.strip() and ':' in line and not line.startswith(' ') and not line.startswith('-'):
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip().strip('"').strip("'")
            yaml_data[key] = value
    
    return yaml_data

def extract_doi_from_content(content):
    """Try to extract DOI from paper content"""
    doi_patterns = [
        r'doi\.org/([10]\.[0-9]{4,}[-._;()/:\w]+)',
        r'doi:\s*([10]\.[0-9]{4,}[-._;()/:\w]+)',
        r'DOI:\s*([10]\.[0-9]{4,}[-._;()/:\w]+)',
        r'https?://dx\.doi\.org/([10]\.[0-9]{4,}[-._;()/:\w]+)',
        r'\b(10\.[0-9]{4,}[-._;()/:\w]+)\b'
    ]
    
    for pattern in doi_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            # Return the first valid-looking DOI
            for match in matches:
                if match.startswith('10.') and len(match) > 7:
                    # Clean up common suffixes
                    doi = match.rstrip('.,;)')
                    return doi
    
    return None

def main():
    """Main analysis function"""
    markdown_papers = Path('markdown_papers')
    
    report = []
    report.append("DOI ISSUES ANALYSIS")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("=" * 70)
    
    # Categories of DOI issues
    missing_doi = []
    placeholder_doi = []
    found_in_content = []
    truly_missing = []
    
    # Analyze all papers
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
                        title = yaml_data.get('title', 'Unknown')[:80]
                        doi = yaml_data.get('doi', '').strip()
                        
                        # Check DOI status
                        if not doi:
                            # Try to find DOI in content
                            content_doi = extract_doi_from_content(content)
                            if content_doi:
                                found_in_content.append({
                                    'cite_key': cite_key,
                                    'folder': folder.name,
                                    'title': title,
                                    'found_doi': content_doi
                                })
                            else:
                                truly_missing.append({
                                    'cite_key': cite_key,
                                    'folder': folder.name,
                                    'title': title
                                })
                            missing_doi.append({
                                'cite_key': cite_key,
                                'folder': folder.name,
                                'title': title
                            })
                        elif doi in ['10.1145/nnnnnnn.nnnnnnn', '10.1109/RpJC.2020.DOI']:
                            # Placeholder DOI
                            placeholder_doi.append({
                                'cite_key': cite_key,
                                'folder': folder.name,
                                'title': title,
                                'placeholder': doi
                            })
                            # Try to find real DOI in content
                            content_doi = extract_doi_from_content(content)
                            if content_doi and content_doi != doi:
                                found_in_content.append({
                                    'cite_key': cite_key,
                                    'folder': folder.name,
                                    'title': title,
                                    'found_doi': content_doi
                                })
                
                except Exception as e:
                    print(f"Error reading {folder.name}: {e}")
    
    # Generate report
    report.append(f"\nSUMMARY")
    report.append("-" * 40)
    report.append(f"Total papers analyzed: {len(list(markdown_papers.iterdir()))}")
    report.append(f"Papers missing DOI: {len(missing_doi)}")
    report.append(f"Papers with placeholder DOI: {len(placeholder_doi)}")
    report.append(f"DOIs found in content: {len(found_in_content)}")
    report.append(f"Truly missing DOIs: {len(truly_missing)}")
    
    # Papers with placeholder DOIs
    report.append(f"\n\n1. PAPERS WITH PLACEHOLDER DOIs ({len(placeholder_doi)} papers)")
    report.append("-" * 70)
    for paper in placeholder_doi:
        report.append(f"\n{paper['cite_key']} (folder: {paper['folder']})")
        report.append(f"  Title: {paper['title']}...")
        report.append(f"  Placeholder: {paper['placeholder']}")
    
    # DOIs found in content
    if found_in_content:
        report.append(f"\n\n2. DOIs FOUND IN CONTENT ({len(found_in_content)} papers)")
        report.append("-" * 70)
        report.append("These papers can be automatically fixed:")
        for paper in found_in_content[:20]:  # Show first 20
            report.append(f"\n{paper['cite_key']} (folder: {paper['folder']})")
            report.append(f"  Title: {paper['title']}...")
            report.append(f"  Found DOI: {paper['found_doi']}")
    
    # Truly missing DOIs (sample)
    report.append(f"\n\n3. TRULY MISSING DOIs (sample of {min(20, len(truly_missing))} from {len(truly_missing)} papers)")
    report.append("-" * 70)
    report.append("These papers have no DOI in metadata or content:")
    for paper in truly_missing[:20]:
        report.append(f"\n{paper['cite_key']} (folder: {paper['folder']})")
        report.append(f"  Title: {paper['title']}...")
    
    # Export fixable DOIs to CSV
    if found_in_content:
        csv_path = Path('dois_to_fix.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['cite_key', 'folder', 'title', 'found_doi']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(found_in_content)
        report.append(f"\n\nFixable DOIs exported to: {csv_path}")
    
    # Save report
    report_path = Path('doi_issues_analysis.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print('\n'.join(report))
    print(f"\nReport saved to: {report_path}")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Analyze similar title groups and papers with missing/incomplete metadata
"""
import re
import csv
import difflib
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

def normalize_title(title):
    """Normalize title for comparison"""
    if not title:
        return ""
    # Remove quotes, markdown formatting, convert to lowercase
    title = re.sub(r'["\'\*\#]', '', title)
    title = re.sub(r'\s+', ' ', title)
    return title.lower().strip()

def find_similar_titles(papers, threshold=0.80):
    """Find groups of papers with similar titles"""
    similar_groups = []
    processed = set()
    
    for i, paper1 in enumerate(papers):
        if i in processed:
            continue
        
        group = [i]
        title1 = normalize_title(paper1['title'])
        
        for j, paper2 in enumerate(papers[i+1:], i+1):
            if j not in processed:
                title2 = normalize_title(paper2['title'])
                ratio = difflib.SequenceMatcher(None, title1, title2).ratio()
                if ratio >= threshold:
                    group.append(j)
                    processed.add(j)
        
        if len(group) > 1:
            similar_groups.append(group)
            processed.add(i)
    
    return similar_groups

def check_metadata_completeness(paper_data):
    """Check metadata completeness and quality"""
    issues = []
    warnings = []
    
    # Required fields
    required_fields = {
        'title': 'Missing title',
        'authors': 'Missing authors',
        'year': 'Missing year',
        'cite_key': 'Missing cite_key'
    }
    
    for field, message in required_fields.items():
        if not paper_data.get(field):
            issues.append(message)
    
    # Important but not required fields
    important_fields = {
        'doi': 'Missing DOI',
        'url': 'Missing URL',
        'tags': 'Missing tags',
        'relevancy': 'Missing relevancy'
    }
    
    for field, message in important_fields.items():
        if not paper_data.get(field):
            warnings.append(message)
    
    # Check data quality
    if paper_data.get('doi', '').strip() in ['10.1145/nnnnnnn.nnnnnnn', '10.1109/RpJC.2020.DOI']:
        warnings.append('Placeholder DOI')
    
    if paper_data.get('title', '').startswith('**'):
        issues.append('Title has markdown formatting')
    
    if paper_data.get('authors', '').lower() in ['', 'unknown', 'n/a', 'not available']:
        issues.append('Invalid authors field')
    
    year = paper_data.get('year', '')
    if year:
        try:
            year_int = int(year)
            if year_int < 2000 or year_int > 2025:
                warnings.append(f'Suspicious year: {year}')
        except:
            issues.append('Invalid year format')
    
    return issues, warnings

def main():
    """Main analysis function"""
    markdown_papers = Path('markdown_papers')
    all_papers = []
    
    print("Analyzing papers for similar titles and incomplete metadata...")
    print("=" * 70)
    
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
                        issues, warnings = check_metadata_completeness(yaml_data)
                        
                        paper_info = {
                            'folder': folder.name,
                            'cite_key': yaml_data.get('cite_key', ''),
                            'title': yaml_data.get('title', ''),
                            'authors': yaml_data.get('authors', ''),
                            'year': yaml_data.get('year', ''),
                            'doi': yaml_data.get('doi', ''),
                            'url': yaml_data.get('url', ''),
                            'tags': yaml_data.get('tags', []) if isinstance(yaml_data.get('tags'), list) else yaml_data.get('tags', ''),
                            'relevancy': yaml_data.get('relevancy', ''),
                            'issues': issues,
                            'warnings': warnings
                        }
                        all_papers.append(paper_info)
                except Exception as e:
                    print(f"Error reading {folder.name}: {e}")
    
    # Generate report
    report = []
    report.append("SIMILAR TITLES AND INCOMPLETE METADATA ANALYSIS")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("=" * 70)
    
    # 1. Similar Titles Analysis
    report.append("\n1. SIMILAR TITLES ANALYSIS (80%+ similarity)")
    report.append("-" * 70)
    
    similar_groups = find_similar_titles(all_papers, threshold=0.80)
    
    if similar_groups:
        for i, group in enumerate(similar_groups, 1):
            report.append(f"\nSimilar Group {i}:")
            for idx in group:
                paper = all_papers[idx]
                report.append(f"  - {paper['cite_key']} ({paper['year']})")
                report.append(f"    Title: {paper['title'][:80]}...")
                report.append(f"    Authors: {paper['authors'][:60]}...")
                if paper['doi']:
                    report.append(f"    DOI: {paper['doi']}")
            
            # Check if they might be duplicates
            titles = [all_papers[idx]['title'] for idx in group]
            authors = [all_papers[idx]['authors'] for idx in group]
            dois = [all_papers[idx]['doi'] for idx in group if all_papers[idx]['doi']]
            
            if len(set(normalize_title(t) for t in titles)) == 1:
                report.append("    ⚠️  EXACT SAME TITLE (normalized)")
            if len(set(authors)) == 1 and authors[0]:
                report.append("    ⚠️  SAME AUTHORS")
            if len(dois) > 1 and len(set(dois)) == 1:
                report.append("    ⚠️  SAME DOI")
    else:
        report.append("No similar title groups found at 80% threshold")
    
    # 2. Papers with Critical Metadata Issues
    report.append("\n\n2. PAPERS WITH CRITICAL METADATA ISSUES")
    report.append("-" * 70)
    
    critical_papers = [p for p in all_papers if p['issues']]
    
    if critical_papers:
        # Sort by number of issues
        critical_papers.sort(key=lambda x: len(x['issues']), reverse=True)
        
        for paper in critical_papers[:20]:  # Show top 20
            report.append(f"\n{paper['cite_key']} (folder: {paper['folder']})")
            report.append(f"  Issues: {', '.join(paper['issues'])}")
            if paper['title']:
                report.append(f"  Title: {paper['title'][:60]}...")
    else:
        report.append("No papers with critical metadata issues found")
    
    # 3. Papers with Warnings
    report.append("\n\n3. PAPERS WITH METADATA WARNINGS")
    report.append("-" * 70)
    
    warning_papers = [p for p in all_papers if p['warnings'] and not p['issues']]
    
    # Count warning types
    warning_counts = {}
    for paper in all_papers:
        for warning in paper['warnings']:
            warning_counts[warning] = warning_counts.get(warning, 0) + 1
    
    report.append("\nWarning Summary:")
    for warning, count in sorted(warning_counts.items(), key=lambda x: x[1], reverse=True):
        report.append(f"  - {warning}: {count} papers")
    
    # Show papers with multiple warnings
    multi_warning_papers = [p for p in warning_papers if len(p['warnings']) >= 2]
    if multi_warning_papers:
        report.append(f"\nPapers with multiple warnings ({len(multi_warning_papers)} total):")
        for paper in multi_warning_papers[:10]:
            report.append(f"  - {paper['cite_key']}: {', '.join(paper['warnings'])}")
    
    # 4. Statistics Summary
    report.append("\n\n4. OVERALL STATISTICS")
    report.append("-" * 70)
    report.append(f"Total papers analyzed: {len(all_papers)}")
    report.append(f"Papers with critical issues: {len(critical_papers)}")
    report.append(f"Papers with warnings only: {len(warning_papers)}")
    report.append(f"Papers with perfect metadata: {len([p for p in all_papers if not p['issues'] and not p['warnings']])}")
    report.append(f"Similar title groups found: {len(similar_groups)}")
    
    # Save detailed report
    report_path = Path('similar_and_incomplete_analysis.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print('\n'.join(report))
    print(f"\nDetailed report saved to: {report_path}")
    
    # Export problem papers to CSV for easy review
    problem_csv = Path('papers_needing_attention.csv')
    with open(problem_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['cite_key', 'folder', 'title', 'authors', 'year', 'doi', 'issues', 'warnings']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for paper in all_papers:
            if paper['issues'] or paper['warnings']:
                row = {
                    'cite_key': paper['cite_key'],
                    'folder': paper['folder'],
                    'title': paper['title'][:100],
                    'authors': paper['authors'][:60],
                    'year': paper['year'],
                    'doi': paper['doi'],
                    'issues': '; '.join(paper['issues']),
                    'warnings': '; '.join(paper['warnings'])
                }
                writer.writerow(row)
    
    print(f"Problem papers CSV exported to: {problem_csv}")

if __name__ == '__main__':
    main()
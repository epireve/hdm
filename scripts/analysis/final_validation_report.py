#!/usr/bin/env python3
"""
Generate final validation report for all papers
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from collections import Counter

MARKDOWN_PAPERS = Path("markdown_papers")
FINAL_REPORT = Path("final_validation_report.md")

def extract_yaml_data(content: str) -> Optional[Dict]:
    """Extract data from YAML frontmatter"""
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    
    if not yaml_match:
        return None
    
    yaml_str = yaml_match.group(1)
    yaml_data = {}
    in_tags = False
    tags_list = []
    
    for line in yaml_str.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if in_tags:
            if line.startswith('- '):
                tag = line[2:].strip().strip('"').strip("'")
                tags_list.append(tag)
                continue
            else:
                yaml_data['tags'] = tags_list
                in_tags = False
        
        if ':' in line and not line.startswith('-'):
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip().strip('"').strip("'")
                
                if key == 'tags' and not value:
                    in_tags = True
                    tags_list = []
                    continue
                
                yaml_data[key] = value
    
    if in_tags and tags_list:
        yaml_data['tags'] = tags_list
    
    return yaml_data

def validate_paper(yaml_data: Dict) -> Dict:
    """Validate a paper's metadata"""
    issues = []
    
    # Required fields
    required = ['cite_key', 'title', 'authors', 'year']
    for field in required:
        if field not in yaml_data or not yaml_data[field]:
            issues.append(f"Missing required field: {field}")
    
    # Check cite_key format
    if 'cite_key' in yaml_data:
        cite_key = yaml_data['cite_key']
        if not re.match(r'^[a-z]+_\d{4}[a-z]?$', cite_key):
            issues.append(f"Invalid cite_key format: {cite_key}")
    
    # Check for "et al." in authors
    if 'authors' in yaml_data:
        authors = yaml_data['authors']
        if 'et al' in authors.lower():
            issues.append("Authors contains 'et al.'")
        if '&' in authors:
            issues.append("Authors contains '&' instead of comma")
    
    # Check year is numeric
    if 'year' in yaml_data:
        try:
            int(yaml_data['year'])
        except:
            issues.append(f"Year is not numeric: {yaml_data['year']}")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'has_all_fields': all(field in yaml_data for field in [
            'cite_key', 'title', 'authors', 'year', 'doi', 'url', 
            'relevancy', 'tldr', 'insights', 'summary', 'tags'
        ])
    }

def main():
    """Generate final validation report"""
    papers = []
    issues_list = []
    stats = {
        'total': 0,
        'valid': 0,
        'has_yaml': 0,
        'has_all_fields': 0,
        'missing_authors': 0,
        'missing_year': 0,
        'invalid_cite_key': 0
    }
    
    # Analyze all papers
    for folder in sorted(MARKDOWN_PAPERS.iterdir()):
        if folder.is_dir():
            md_path = folder / "paper.md"
            if md_path.exists():
                stats['total'] += 1
                
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    yaml_data = extract_yaml_data(content)
                    
                    if yaml_data:
                        stats['has_yaml'] += 1
                        validation = validate_paper(yaml_data)
                        
                        if validation['valid']:
                            stats['valid'] += 1
                        else:
                            for issue in validation['issues']:
                                if 'authors' in issue:
                                    stats['missing_authors'] += 1
                                elif 'year' in issue:
                                    stats['missing_year'] += 1
                                elif 'cite_key format' in issue:
                                    stats['invalid_cite_key'] += 1
                        
                        if validation['has_all_fields']:
                            stats['has_all_fields'] += 1
                        
                        papers.append({
                            'folder': folder.name,
                            'cite_key': yaml_data.get('cite_key', ''),
                            'title': yaml_data.get('title', ''),
                            'authors': yaml_data.get('authors', ''),
                            'year': yaml_data.get('year', ''),
                            'valid': validation['valid'],
                            'issues': validation['issues']
                        })
                        
                        if validation['issues']:
                            issues_list.append({
                                'folder': folder.name,
                                'issues': validation['issues']
                            })
                    
                except Exception as e:
                    issues_list.append({
                        'folder': folder.name,
                        'issues': [f"Error: {str(e)}"]
                    })
    
    # Check for duplicate cite_keys
    cite_keys = [p['cite_key'] for p in papers if p['cite_key']]
    cite_key_counts = Counter(cite_keys)
    duplicates = {k: v for k, v in cite_key_counts.items() if v > 1}
    
    # Generate report
    from datetime import datetime
    report = f"""# Final Validation Report

Generated: {datetime.now().isoformat()}

## Summary Statistics

- **Total papers**: {stats['total']}
- **Papers with YAML frontmatter**: {stats['has_yaml']}
- **Valid papers**: {stats['valid']}
- **Papers with all recommended fields**: {stats['has_all_fields']}

## Issues Found

- **Missing authors**: {stats['missing_authors']}
- **Missing year**: {stats['missing_year']}
- **Invalid cite_key format**: {stats['invalid_cite_key']}
- **Duplicate cite_keys**: {len(duplicates)}

## Folder/Cite Key Alignment

"""

    # Check folder/cite_key alignment
    misaligned = []
    for paper in papers:
        if paper['cite_key'] and paper['folder'] != paper['cite_key']:
            misaligned.append(paper)
    
    report += f"- **Folders matching cite_keys**: {len(papers) - len(misaligned)}/{len(papers)}\n"
    report += f"- **Misaligned folders**: {len(misaligned)}\n\n"
    
    if misaligned:
        report += "### Misaligned Folders\n\n"
        for paper in misaligned[:10]:
            report += f"- Folder: `{paper['folder']}` → Cite key: `{paper['cite_key']}`\n"
        if len(misaligned) > 10:
            report += f"- ... and {len(misaligned) - 10} more\n"
        report += "\n"
    
    # List papers with issues
    if issues_list:
        report += "## Papers with Issues\n\n"
        for item in issues_list[:20]:
            report += f"### {item['folder']}\n"
            for issue in item['issues']:
                report += f"- {issue}\n"
            report += "\n"
        
        if len(issues_list) > 20:
            report += f"... and {len(issues_list) - 20} more papers with issues\n\n"
    
    # Show cite_key distribution by year
    years = [p['year'] for p in papers if p['year']]
    year_counts = Counter(years)
    
    report += "## Papers by Year\n\n"
    for year in sorted(year_counts.keys(), reverse=True)[:10]:
        report += f"- **{year}**: {year_counts[year]} papers\n"
    
    # Show sample of valid papers
    valid_papers = [p for p in papers if p['valid']][:5]
    if valid_papers:
        report += "\n## Sample Valid Papers\n\n"
        for paper in valid_papers:
            report += f"- **{paper['cite_key']}**: {paper['title'][:80]}...\n"
            report += f"  - Authors: {paper['authors'][:60]}...\n"
            report += f"  - Year: {paper['year']}\n\n"
    
    # Write report
    with open(FINAL_REPORT, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Final validation report generated: {FINAL_REPORT}")
    print(f"\nQuick Summary:")
    print(f"- Total papers: {stats['total']}")
    print(f"- Valid papers: {stats['valid']} ({stats['valid']/stats['total']*100:.1f}%)")
    print(f"- Papers with all fields: {stats['has_all_fields']} ({stats['has_all_fields']/stats['total']*100:.1f}%)")
    print(f"- Misaligned folders: {len(misaligned)}")

if __name__ == "__main__":
    main()
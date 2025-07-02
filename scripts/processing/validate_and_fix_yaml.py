#!/usr/bin/env python3
"""
Validate and fix YAML frontmatter in all markdown papers
Cross-reference with missing_papers.json for accuracy
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import difflib
from datetime import datetime

MARKDOWN_PAPERS = Path("markdown_papers")
MISSING_PAPERS_JSON = Path("missing_papers.json")
VALIDATION_REPORT = Path("yaml_validation_report.json")
FIXES_LOG = Path("yaml_fixes_log.json")

# Required YAML fields
REQUIRED_FIELDS = {
    'cite_key', 'title', 'authors', 'year'
}

# Recommended fields
RECOMMENDED_FIELDS = {
    'doi', 'url', 'relevancy', 'tldr', 'insights', 
    'summary', 'tags', 'research_question', 'methodology',
    'key_findings', 'limitations', 'conclusion', 'future_work',
    'implementation_insights'
}

def load_missing_papers() -> Dict[str, Dict]:
    """Load missing papers data"""
    with open(MISSING_PAPERS_JSON, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # Create lookup by title and cite_key
    lookup_by_title = {}
    lookup_by_cite_key = {}
    
    for paper in papers:
        title = paper.get('Paper Title', '').strip()
        if title:
            lookup_by_title[title.lower()] = paper
        
        cite_key = paper.get('cite_key', '').strip()
        if cite_key:
            lookup_by_cite_key[cite_key] = paper
    
    return lookup_by_title, lookup_by_cite_key, papers

def extract_yaml_frontmatter(content: str) -> Tuple[Optional[Dict], Optional[str], str]:
    """Extract YAML frontmatter from markdown content"""
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    
    if not yaml_match:
        return None, None, content
    
    yaml_str = yaml_match.group(1)
    rest_content = content[yaml_match.end():]
    
    # Parse YAML manually (simple parser for our use case)
    yaml_data = {}
    current_key = None
    in_tags = False
    tags_list = []
    
    for line in yaml_str.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Handle tags list
        if in_tags:
            if line.startswith('- '):
                tag = line[2:].strip().strip('"').strip("'")
                tags_list.append(tag)
                continue
            else:
                yaml_data['tags'] = tags_list
                in_tags = False
        
        # Parse key: value pairs
        if ':' in line and not line.startswith('-'):
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                
                if key == 'tags' and not value:
                    in_tags = True
                    tags_list = []
                    continue
                
                # Remove quotes
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                # Convert year to int if possible
                if key == 'year':
                    try:
                        value = int(value)
                    except:
                        pass
                
                yaml_data[key] = value
    
    # Add remaining tags if any
    if in_tags and tags_list:
        yaml_data['tags'] = tags_list
    
    return yaml_data, yaml_str, rest_content

def clean_authors(authors: str) -> str:
    """Clean and standardize author names"""
    if not authors:
        return ""
    
    # Remove "et al."
    authors = re.sub(r'\s+et al\.?', '', authors, flags=re.IGNORECASE)
    
    # Replace semicolons and ampersands with commas
    authors = authors.replace(';', ',').replace(' & ', ', ').replace('&', ', ')
    
    # Remove "Authors unavailable" or similar
    if 'unavailable' in authors.lower() or 'not available' in authors.lower():
        return ""
    
    # Clean up multiple commas and spaces
    authors = re.sub(r',\s*,', ',', authors)
    authors = re.sub(r'\s+', ' ', authors)
    authors = authors.strip()
    
    # Remove trailing comma
    if authors.endswith(','):
        authors = authors[:-1].strip()
    
    return authors

def generate_cite_key(authors: str, year: str) -> str:
    """Generate cite key from authors and year"""
    if not authors or not year:
        return ""
    
    # Get first author's last name
    first_author = authors.split(',')[0].strip()
    
    # Extract last name (assume last word is last name)
    last_name = first_author.split()[-1] if first_author else "unknown"
    
    # Clean last name
    last_name = re.sub(r'[^a-zA-Z]', '', last_name).lower()
    
    return f"{last_name}_{year}"

def find_best_match(title: str, lookup_by_title: Dict) -> Optional[Dict]:
    """Find best matching paper by title using fuzzy matching"""
    if not title:
        return None
    
    title_lower = title.lower().strip()
    
    # Exact match
    if title_lower in lookup_by_title:
        return lookup_by_title[title_lower]
    
    # Fuzzy match
    best_match = None
    best_ratio = 0.0
    
    for ref_title, paper in lookup_by_title.items():
        ratio = difflib.SequenceMatcher(None, title_lower, ref_title).ratio()
        if ratio > 0.85 and ratio > best_ratio:  # 85% similarity threshold
            best_ratio = ratio
            best_match = paper
    
    return best_match

def validate_and_fix_paper(md_path: Path, lookup_by_title: Dict, 
                          lookup_by_cite_key: Dict) -> Dict:
    """Validate and fix YAML frontmatter for a single paper"""
    issues = []
    fixes = []
    
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        yaml_data, yaml_str, rest_content = extract_yaml_frontmatter(content)
        
        if yaml_data is None:
            issues.append("No valid YAML frontmatter found")
            return {
                'path': str(md_path),
                'issues': issues,
                'fixes': fixes,
                'status': 'error'
            }
        
        # Track original values
        original_yaml = yaml_data.copy() if yaml_data else {}
        
        # Find matching paper in missing_papers.json
        title = yaml_data.get('title', '')
        matched_paper = find_best_match(title, lookup_by_title)
        
        if not matched_paper and yaml_data.get('cite_key'):
            # Try matching by cite_key
            cite_key = yaml_data.get('cite_key', '')
            if cite_key in lookup_by_cite_key:
                matched_paper = lookup_by_cite_key[cite_key]
        
        # Fix missing or incorrect fields
        if matched_paper:
            # Update title
            if 'Paper Title' in matched_paper:
                correct_title = matched_paper['Paper Title'].strip()
                if title != correct_title:
                    yaml_data['title'] = correct_title
                    fixes.append(f"Updated title: {title} -> {correct_title}")
            
            # Update authors
            if 'Authors' in matched_paper:
                correct_authors = clean_authors(matched_paper['Authors'])
                current_authors = yaml_data.get('authors', '')
                
                # Check if current authors look like email prefixes
                if re.match(r'^[a-z]+(?:,\s*[a-z]+)*$', current_authors) or not current_authors:
                    if correct_authors and correct_authors != current_authors:
                        yaml_data['authors'] = correct_authors
                        fixes.append(f"Updated authors: {current_authors} -> {correct_authors}")
            
            # Update year
            if 'Year' in matched_paper:
                correct_year = str(matched_paper['Year'])
                if yaml_data.get('year') != correct_year and yaml_data.get('year') != int(correct_year):
                    yaml_data['year'] = int(correct_year)
                    fixes.append(f"Updated year: {yaml_data.get('year')} -> {correct_year}")
            
            # Add missing recommended fields
            field_mapping = {
                'doi': 'DOI',
                'url': 'url',
                'relevancy': 'Relevancy',
                'tldr': 'TL;DR',
                'insights': 'Insights',
                'summary': 'Summary',
                'research_question': 'Research Question',
                'methodology': 'Methodology',
                'key_findings': 'Key Findings',
                'limitations': 'Limitations',
                'conclusion': 'Conclusion',
                'future_work': 'Future Work',
                'implementation_insights': 'Implementation Insights'
            }
            
            for yaml_field, json_field in field_mapping.items():
                if json_field in matched_paper and matched_paper[json_field]:
                    value = matched_paper[json_field].strip()
                    if value and (yaml_field not in yaml_data or not yaml_data[yaml_field]):
                        yaml_data[yaml_field] = value
                        fixes.append(f"Added {yaml_field}")
            
            # Handle tags
            if 'Tags' in matched_paper and matched_paper['Tags']:
                tags = [tag.strip() for tag in matched_paper['Tags'].split(',') if tag.strip()]
                if tags and ('tags' not in yaml_data or not yaml_data['tags']):
                    yaml_data['tags'] = tags
                    fixes.append("Added tags")
        
        # Validate required fields
        for field in REQUIRED_FIELDS:
            if field not in yaml_data or not yaml_data[field]:
                issues.append(f"Missing required field: {field}")
        
        # Generate/fix cite_key if needed
        if 'authors' in yaml_data and 'year' in yaml_data:
            expected_cite_key = generate_cite_key(
                yaml_data.get('authors', ''), 
                str(yaml_data.get('year', ''))
            )
            
            current_cite_key = yaml_data.get('cite_key', '')
            
            # Only update if current is empty or looks wrong
            if not current_cite_key or current_cite_key.startswith('_'):
                yaml_data['cite_key'] = expected_cite_key
                fixes.append(f"Generated cite_key: {expected_cite_key}")
            elif not re.match(r'^[a-z]+_\d{4}[a-z]?$', current_cite_key):
                # Current cite_key doesn't match expected format
                yaml_data['cite_key'] = expected_cite_key
                fixes.append(f"Fixed cite_key format: {current_cite_key} -> {expected_cite_key}")
        
        # Write back if changes were made
        if fixes:
            # Rebuild YAML string
            yaml_lines = ['---']
            
            # Order fields nicely
            field_order = ['cite_key', 'title', 'authors', 'year', 'doi', 'url', 
                          'relevancy', 'tldr', 'insights', 'summary', 'research_question',
                          'methodology', 'key_findings', 'primary_outcomes', 'limitations',
                          'conclusion', 'research_gaps', 'future_work', 'implementation_insights', 'tags']
            
            # Write fields in order
            for field in field_order:
                if field in yaml_data and yaml_data[field]:
                    value = yaml_data[field]
                    if field == 'tags' and isinstance(value, list):
                        yaml_lines.append('tags:')
                        for tag in value:
                            yaml_lines.append(f'  - "{tag}"')
                    else:
                        # Escape quotes in string values
                        if isinstance(value, str) and '"' in value:
                            value = value.replace('"', '\\"')
                        if isinstance(value, str):
                            yaml_lines.append(f'{field}: "{value}"')
                        else:
                            yaml_lines.append(f'{field}: {value}')
            
            # Add any remaining fields
            for field, value in yaml_data.items():
                if field not in field_order and value:
                    if isinstance(value, str):
                        yaml_lines.append(f'{field}: "{value}"')
                    else:
                        yaml_lines.append(f'{field}: {value}')
            
            yaml_lines.append('---')
            
            # Write updated content
            new_content = '\n'.join(yaml_lines) + '\n' + rest_content
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return {
            'path': str(md_path),
            'folder': md_path.parent.name,
            'issues': issues,
            'fixes': fixes,
            'status': 'fixed' if fixes else 'valid',
            'matched_paper': matched_paper.get('Paper Title') if matched_paper else None
        }
        
    except Exception as e:
        return {
            'path': str(md_path),
            'issues': [f"Error processing file: {str(e)}"],
            'fixes': [],
            'status': 'error'
        }

def main():
    """Validate and fix all YAML frontmatter"""
    print("Loading missing papers data...")
    lookup_by_title, lookup_by_cite_key, all_papers = load_missing_papers()
    print(f"Loaded {len(all_papers)} papers from missing_papers.json")
    
    print("\nValidating YAML frontmatter in all papers...")
    
    results = []
    stats = {
        'total': 0,
        'valid': 0,
        'fixed': 0,
        'errors': 0,
        'total_fixes': 0
    }
    
    # Process all markdown papers
    for folder in sorted(MARKDOWN_PAPERS.iterdir()):
        if folder.is_dir():
            md_path = folder / "paper.md"
            if md_path.exists():
                stats['total'] += 1
                result = validate_and_fix_paper(md_path, lookup_by_title, lookup_by_cite_key)
                results.append(result)
                
                if result['status'] == 'valid':
                    stats['valid'] += 1
                elif result['status'] == 'fixed':
                    stats['fixed'] += 1
                    stats['total_fixes'] += len(result['fixes'])
                    print(f"✓ Fixed: {folder.name}")
                    for fix in result['fixes'][:3]:  # Show first 3 fixes
                        print(f"  - {fix}")
                    if len(result['fixes']) > 3:
                        print(f"  ... and {len(result['fixes']) - 3} more fixes")
                elif result['status'] == 'error':
                    stats['errors'] += 1
                    print(f"✗ Error: {folder.name}")
                    print(f"  {result['issues'][0]}")
    
    # Generate report
    report = {
        'timestamp': datetime.now().isoformat(),
        'statistics': stats,
        'papers_with_issues': [r for r in results if r['issues']],
        'papers_fixed': [r for r in results if r['fixes']],
        'cite_key_updates': [r for r in results if any('cite_key' in fix for fix in r.get('fixes', []))]
    }
    
    with open(VALIDATION_REPORT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    # Save detailed fixes log
    fixes_log = {
        'timestamp': datetime.now().isoformat(),
        'fixes': [r for r in results if r['fixes']]
    }
    
    with open(FIXES_LOG, 'w', encoding='utf-8') as f:
        json.dump(fixes_log, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("YAML Validation Summary:")
    print(f"Total papers processed: {stats['total']}")
    print(f"Valid papers: {stats['valid']}")
    print(f"Papers fixed: {stats['fixed']}")
    print(f"Total fixes applied: {stats['total_fixes']}")
    print(f"Errors: {stats['errors']}")
    print(f"\nReports saved to:")
    print(f"  - {VALIDATION_REPORT}")
    print(f"  - {FIXES_LOG}")

if __name__ == "__main__":
    main()
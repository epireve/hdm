#!/usr/bin/env python3
"""
Fix DOIs that were found in paper content
"""
import re
import csv
from pathlib import Path
from datetime import datetime

def update_yaml_doi(content, new_doi):
    """Update DOI in YAML frontmatter"""
    # Check if there's already a doi field
    doi_pattern = r'(---\n.*?)(doi:\s*[^\n]*\n)?(.*?\n---\n)'
    match = re.search(doi_pattern, content, re.DOTALL)
    
    if match:
        if match.group(2):  # DOI field exists
            # Replace existing DOI
            updated_content = content.replace(match.group(2), f'doi: {new_doi}\n')
        else:
            # Add DOI field after year
            yaml_part = match.group(1) + match.group(3)
            # Find where to insert (after year field)
            year_pattern = r'(year:\s*[^\n]*\n)'
            year_match = re.search(year_pattern, yaml_part)
            if year_match:
                insert_pos = yaml_part.find(year_match.group(0)) + len(year_match.group(0))
                updated_yaml = yaml_part[:insert_pos] + f'doi: {new_doi}\n' + yaml_part[insert_pos:]
                updated_content = content.replace(yaml_part, updated_yaml)
            else:
                # Insert before the closing ---
                insert_pos = yaml_part.rfind('\n---\n')
                updated_yaml = yaml_part[:insert_pos] + f'\ndoi: {new_doi}\n' + yaml_part[insert_pos:]
                updated_content = content.replace(yaml_part, updated_yaml)
        
        return updated_content
    
    return content

def add_url_if_missing(content, doi):
    """Add URL field if missing"""
    # Check if URL field exists
    url_pattern = r'(---\n.*?)url:\s*[^\n]*\n(.*?\n---\n)'
    if not re.search(url_pattern, content, re.DOTALL):
        # Add URL after DOI
        doi_pattern = r'(doi:\s*' + re.escape(doi) + r'\n)'
        match = re.search(doi_pattern, content)
        if match:
            insert_pos = match.end()
            url = f'url: https://doi.org/{doi}\n'
            content = content[:insert_pos] + url + content[insert_pos:]
    
    return content

def main():
    """Main function to fix found DOIs"""
    markdown_papers = Path('markdown_papers')
    
    report = []
    report.append("FIXING FOUND DOIs")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("=" * 70)
    
    # Read DOIs to fix
    dois_to_fix = []
    csv_path = Path('dois_to_fix.csv')
    if csv_path.exists():
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            dois_to_fix = list(reader)
    
    report.append(f"\nDOIs to fix: {len(dois_to_fix)}")
    report.append("-" * 40)
    
    fixed_count = 0
    
    # Fix each paper
    for paper_info in dois_to_fix:
        folder = paper_info['folder']
        found_doi = paper_info['found_doi']
        paper_path = markdown_papers / folder / 'paper.md'
        
        if paper_path.exists():
            try:
                # Read content
                with open(paper_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update DOI
                updated_content = update_yaml_doi(content, found_doi)
                
                # Add URL if missing
                updated_content = add_url_if_missing(updated_content, found_doi)
                
                # Write back
                with open(paper_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                report.append(f"\n{paper_info['cite_key']} (folder: {folder})")
                report.append(f"  ✓ Added DOI: {found_doi}")
                report.append(f"  ✓ Added URL: https://doi.org/{found_doi}")
                fixed_count += 1
                
            except Exception as e:
                report.append(f"\n{paper_info['cite_key']}: Error - {str(e)}")
    
    # Now check the placeholder DOIs
    report.append(f"\n\nPLACEHOLDER DOIs TO MANUALLY CHECK")
    report.append("-" * 40)
    
    placeholder_papers = [
        ('ghani_2020b', '10.1109/RpJC.2020.DOI'),
        ('ren_2025', '10.1145/nnnnnnn.nnnnnnn'),
        ('saad_2017', '10.1145/nnnnnnn.nnnnnnn')
    ]
    
    for folder, placeholder in placeholder_papers:
        paper_path = markdown_papers / folder / 'paper.md'
        if paper_path.exists():
            report.append(f"\n{folder}:")
            report.append(f"  Current placeholder: {placeholder}")
            report.append(f"  Action needed: Find real DOI or confirm if preprint/no DOI")
    
    # Summary
    report.append(f"\n\nSUMMARY")
    report.append("-" * 40)
    report.append(f"DOIs fixed: {fixed_count}")
    report.append(f"Placeholder DOIs needing attention: {len(placeholder_papers)}")
    
    # Save report
    report_path = Path('doi_fixes_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print('\n'.join(report))
    print(f"\nReport saved to: {report_path}")

if __name__ == '__main__':
    main()
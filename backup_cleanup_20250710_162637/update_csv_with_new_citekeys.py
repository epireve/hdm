#!/usr/bin/env python3
"""
Update CSV files to add the new papers with updated cite_keys
"""
import json
import csv
from pathlib import Path
from datetime import datetime

def load_rename_report():
    """Load the rename report to get new cite_keys"""
    with open('conflicting_folders_fix_report.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_metadata_from_markdown(md_file):
    """Extract metadata from markdown file"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if content.startswith('---\n'):
            end_idx = content.find('\n---\n', 4)
            if end_idx != -1:
                yaml_content = content[4:end_idx]
                metadata = {}
                
                for line in yaml_content.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if ':' in line and not line.startswith('- '):
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        elif value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        
                        if value:
                            metadata[key] = value
                            
                return metadata
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
    return None

def update_csv_files():
    """Update CSV files with new cite_keys"""
    rename_report = load_rename_report()
    markdown_papers_dir = Path('markdown_papers')
    
    # Collect new papers data
    new_papers = []
    
    for rename_info in rename_report['renamed']:
        new_folder = rename_info['new_folder']
        folder_path = markdown_papers_dir / new_folder
        
        # Find markdown file
        md_files = list(folder_path.glob('*.md'))
        if md_files:
            metadata = extract_metadata_from_markdown(md_files[0])
            if metadata:
                new_papers.append({
                    'cite_key': metadata.get('cite_key', new_folder),
                    'title': metadata.get('title', ''),
                    'authors': metadata.get('authors', ''),
                    'year': metadata.get('year', '')
                })
    
    # Load existing research_papers_clean.csv
    existing_cite_keys = set()
    if Path('research_papers_clean.csv').exists():
        with open('research_papers_clean.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            existing_cite_keys = {row['cite_key'] for row in rows}
    else:
        rows = []
    
    # Add new papers that aren't already in the CSV
    added_count = 0
    for paper in new_papers:
        if paper['cite_key'] not in existing_cite_keys:
            rows.append(paper)
            added_count += 1
            print(f"Added: {paper['cite_key']} - {paper['title'][:60]}...")
    
    # Sort by cite_key
    rows.sort(key=lambda x: x.get('cite_key', ''))
    
    # Write updated CSV
    if added_count > 0:
        # Backup original
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if Path('research_papers_clean.csv').exists():
            backup_path = f'research_papers_clean_backup_{timestamp}.csv'
            import shutil
            shutil.copy('research_papers_clean.csv', backup_path)
            print(f"\nBacked up original to: {backup_path}")
        
        # Write new CSV
        with open('research_papers_clean.csv', 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['cite_key', 'title', 'authors', 'year']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"\nUpdated research_papers_clean.csv with {added_count} new entries")
    else:
        print("\nNo new entries needed - all papers already in CSV")
    
    # Create a summary report
    report = {
        'timestamp': datetime.now().isoformat(),
        'papers_renamed': len(rename_report['renamed']),
        'papers_added_to_csv': added_count,
        'total_papers_in_csv': len(rows),
        'new_cite_keys': [p['cite_key'] for p in new_papers]
    }
    
    with open('csv_update_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved: csv_update_report.json")
    print(f"Total papers in CSV: {len(rows)}")

if __name__ == "__main__":
    update_csv_files()
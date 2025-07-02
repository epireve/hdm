#!/usr/bin/env python3
"""
Update CSV file to reflect the new a/b cite_key format
"""
import csv
import shutil
from datetime import datetime

def update_csv_with_abc_format():
    """Update research_papers_clean.csv with new cite_keys"""
    
    # Mapping of old cite_keys to new ones
    cite_key_mapping = {
        # Original to 'a'
        'schmitt_2020': 'schmitt_2020a',
        'zhang_2021': 'zhang_2021a',
        'lin_2024': 'lin_2024a',
        'xie_2024': 'xie_2024a',
        'ghani_2020': 'ghani_2020a',
        'wang_2022': 'wang_2022a',
        'ilkou_2022': 'ilkou_2022a',
        'li_2022': 'li_2022a',
        'li_2023': 'li_2023a',
        'xie_2022': 'xie_2022a',
        'wang_2024': 'wang_2024a',
        'chen_2023': 'chen_2023a',
        'chen_2024': 'chen_2024a',
        'yang_2024': 'yang_2024a',
        # Previous renames to 'b'
        'schmitt_2020_2': 'schmitt_2020b',
        'zhang_2021_2': 'zhang_2021b',
        'lin_2024_2': 'lin_2024b',
        'xie_2024_2': 'xie_2024b',
        'ghani_2020_arxiv2004': 'ghani_2020b',
        'wang_2022_arxiv2022': 'wang_2022b',
        'ilkou_2022_arxiv2203': 'ilkou_2022b',
        'li_2022_arxiv2203': 'li_2022b',
        'li_2023_arxiv2304': 'li_2023b',
        'xie_2022_arxiv2412': 'xie_2022b',
        'wang_2024_arxiv2409': 'wang_2024b',
        'chen_2023_2': 'chen_2023b',
        'chen_2024_2': 'chen_2024b',
        'yang_2024_2': 'yang_2024b'
    }
    
    # Backup original
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f'research_papers_clean_backup_abc_{timestamp}.csv'
    shutil.copy('research_papers_clean.csv', backup_path)
    print(f"Backed up original to: {backup_path}")
    
    # Read CSV
    with open('research_papers_clean.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Update cite_keys
    updated_count = 0
    for row in rows:
        old_cite_key = row['cite_key']
        if old_cite_key in cite_key_mapping:
            new_cite_key = cite_key_mapping[old_cite_key]
            row['cite_key'] = new_cite_key
            print(f"Updated: {old_cite_key} → {new_cite_key}")
            updated_count += 1
    
    # Sort by cite_key
    rows.sort(key=lambda x: x.get('cite_key', ''))
    
    # Write updated CSV
    with open('research_papers_clean.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['cite_key', 'title', 'authors', 'year']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n=== Summary ===")
    print(f"Updated {updated_count} cite_keys in research_papers_clean.csv")
    print(f"Total entries: {len(rows)}")
    
    # Also update research_table_with_citekeys.csv if it exists
    if os.path.exists('research_table_with_citekeys.csv'):
        print("\nUpdating research_table_with_citekeys.csv...")
        
        backup_path2 = f'research_table_with_citekeys_backup_abc_{timestamp}.csv'
        shutil.copy('research_table_with_citekeys.csv', backup_path2)
        print(f"Backed up to: {backup_path2}")
        
        with open('research_table_with_citekeys.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows2 = list(reader)
        
        updated_count2 = 0
        for row in rows2:
            old_cite_key = row.get('cite_key', '')
            if old_cite_key in cite_key_mapping:
                row['cite_key'] = cite_key_mapping[old_cite_key]
                updated_count2 += 1
        
        with open('research_table_with_citekeys.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows2)
        
        print(f"Updated {updated_count2} cite_keys in research_table_with_citekeys.csv")

if __name__ == "__main__":
    import os
    update_csv_with_abc_format()
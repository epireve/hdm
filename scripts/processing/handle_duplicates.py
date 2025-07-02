#!/usr/bin/env python3
"""
Handle duplicate papers identified in the analysis
"""
import shutil
from pathlib import Path
from datetime import datetime
import json

def create_backup(folder_path):
    """Create a backup of the folder before deletion"""
    backup_dir = Path('duplicate_backups') / datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    dest = backup_dir / folder_path.name
    shutil.copytree(folder_path, dest)
    return dest

def main():
    """Main function to handle duplicates"""
    markdown_papers = Path('markdown_papers')
    
    # Create a summary report
    report = []
    report.append("DUPLICATE HANDLING REPORT")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("=" * 60)
    
    # 1. Handle ghani_2020a/ghani_2020b - appear to be mislabeled
    report.append("\n1. GHANI PAPERS ISSUE")
    report.append("-" * 40)
    report.append("Issue: ghani_2020a has wrong title but same content as ghani_2020b")
    report.append("Original folder for ghani_2020a matches ghani_2020b title")
    report.append("Action: Keep ghani_2020b (correct metadata), remove ghani_2020a")
    
    ghani_a = markdown_papers / 'ghani_2020a'
    ghani_b = markdown_papers / 'ghani_2020b'
    
    if ghani_a.exists() and ghani_b.exists():
        backup = create_backup(ghani_a)
        report.append(f"✓ Backed up ghani_2020a to: {backup}")
        shutil.rmtree(ghani_a)
        report.append("✓ Removed ghani_2020a")
    
    # 2. Handle ilkou_2022a/ilkou_2022b - same paper, different sources
    report.append("\n2. ILKOU PAPERS ISSUE")
    report.append("-" * 40)
    report.append("Issue: Same paper from different sources")
    report.append("ilkou_2022a has proper DOI: 10.1145/3487553.3524196")
    report.append("ilkou_2022b has placeholder DOI: 10.1145/nnnnnnn.nnnnnnn")
    report.append("Action: Keep ilkou_2022a (proper DOI), remove ilkou_2022b")
    
    ilkou_a = markdown_papers / 'ilkou_2022a'
    ilkou_b = markdown_papers / 'ilkou_2022b'
    
    if ilkou_a.exists() and ilkou_b.exists():
        backup = create_backup(ilkou_b)
        report.append(f"✓ Backed up ilkou_2022b to: {backup}")
        shutil.rmtree(ilkou_b)
        report.append("✓ Removed ilkou_2022b")
    
    # 3. Handle li_2012/li_2022b - same title, different years
    report.append("\n3. LI PAPERS ISSUE")
    report.append("-" * 40)
    report.append("Issue: Same title 'Auditing Privacy Defenses in Federated Learning'")
    report.append("li_2012 has incorrect year 2012 (arXiv shows 2022)")
    report.append("li_2022b has correct year 2022")
    report.append("Action: Keep li_2022b (correct year), remove li_2012")
    
    li_2012 = markdown_papers / 'li_2012'
    li_2022b = markdown_papers / 'li_2022b'
    
    if li_2012.exists() and li_2022b.exists():
        backup = create_backup(li_2012)
        report.append(f"✓ Backed up li_2012 to: {backup}")
        shutil.rmtree(li_2012)
        report.append("✓ Removed li_2012")
    
    # 4. Fix placeholder DOIs
    report.append("\n4. PLACEHOLDER DOIs")
    report.append("-" * 40)
    report.append("Papers with placeholder DOI '10.1145/nnnnnnn.nnnnnnn':")
    
    placeholder_doi_papers = ['ren_2025', 'saad_2017']
    for paper in placeholder_doi_papers:
        paper_path = markdown_papers / paper / 'paper.md'
        if paper_path.exists():
            report.append(f"- {paper}: Needs proper DOI")
    
    # 5. Similar titles that might be related
    report.append("\n5. SIMILAR TITLES (Manual Review Needed)")
    report.append("-" * 40)
    report.append("- chen_2024a & li_2021: Temporal Knowledge Graph Reasoning papers")
    report.append("- e065929_full & joosse_2023: Sustainable Development Goal papers")
    report.append("- wu_2022 & yan_2024a: Federated Graph Neural Network papers")
    
    # Save report
    report_path = Path('duplicate_handling_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print('\n'.join(report))
    print(f"\nReport saved to: {report_path}")
    
    # Update CSV with removed papers
    update_csv_after_removal()

def update_csv_after_removal():
    """Update the CSV file after removing duplicates"""
    import csv
    
    removed_papers = ['ghani_2020a', 'ilkou_2022b', 'li_2012']
    
    # Read current CSV
    csv_path = Path('papers_analysis.csv')
    if not csv_path.exists():
        return
    
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['folder'] not in removed_papers:
                rows.append(row)
    
    # Write updated CSV
    if rows:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"Updated CSV: removed {len(removed_papers)} duplicate entries")

if __name__ == '__main__':
    main()
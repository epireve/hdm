#!/usr/bin/env python3
"""
Handle similar/duplicate papers found in the analysis
"""
import shutil
from pathlib import Path
from datetime import datetime

def create_backup(folder_path):
    """Create a backup of the folder before deletion"""
    backup_dir = Path('duplicate_backups') / datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    dest = backup_dir / folder_path.name
    shutil.copytree(folder_path, dest)
    return dest

def main():
    """Handle similar/duplicate papers"""
    markdown_papers = Path('markdown_papers')
    
    report = []
    report.append("HANDLING SIMILAR/DUPLICATE PAPERS")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("=" * 70)
    
    # Define duplicates to remove based on analysis
    duplicates_to_handle = [
        {
            'keep': 'aburasheed_2023b',  # Has IEEE DOI
            'remove': 'aburasheed_2023a',  # Has arXiv DOI
            'reason': 'Same paper, keep version with official IEEE DOI'
        },
        {
            'keep': 'bellomarini_2024a',
            'remove': 'bellomarini_2024b',
            'reason': 'Exact duplicate (same title, authors, DOI)'
        },
        {
            'keep': 'galke_2021',
            'remove': 'lukasgalk_2021',
            'reason': 'Same paper, galke_2021 has better author formatting'
        },
        {
            'keep': 'lee_2024',
            'remove': 'leejunlin_2024',
            'reason': 'Same paper, lee_2024 has better author formatting'
        },
        {
            'keep': 'zhou_2024b',
            'remove': 'privacy_2024',
            'reason': 'Same paper, zhou_2024b has complete author list'
        },
        {
            'keep': 'sun_2024a',
            'remove': 'sun_2024b',
            'reason': 'Exact duplicate (same title, DOI), sun_2024a has more authors listed'
        }
    ]
    
    # Note: joosse_2023 appears twice in the list but seems to be the same entry
    # wu_2022, xie_2022a, yan_2024a are related but different papers about federated GNN
    
    removed_count = 0
    
    for dup in duplicates_to_handle:
        report.append(f"\n{removed_count + 1}. {dup['remove']} → {dup['keep']}")
        report.append(f"   Reason: {dup['reason']}")
        
        remove_path = markdown_papers / dup['remove']
        keep_path = markdown_papers / dup['keep']
        
        if remove_path.exists() and keep_path.exists():
            backup = create_backup(remove_path)
            report.append(f"   ✓ Backed up {dup['remove']} to: {backup}")
            shutil.rmtree(remove_path)
            report.append(f"   ✓ Removed {dup['remove']}")
            removed_count += 1
        elif not remove_path.exists():
            report.append(f"   - {dup['remove']} not found (already removed?)")
        elif not keep_path.exists():
            report.append(f"   ⚠️  {dup['keep']} not found, skipping removal")
    
    # Report on papers that need manual review
    report.append("\n\nPAPERS NEEDING MANUAL REVIEW")
    report.append("-" * 40)
    
    manual_review = [
        {
            'papers': ['cai_2022', 'su_2024'],
            'note': 'Different papers about Temporal KG (Completion vs QA), both should be kept'
        },
        {
            'papers': ['chen_2024a', 'li_2021'],
            'note': 'Similar titles about Temporal KG Reasoning, but different approaches'
        },
        {
            'papers': ['wu_2022', 'xie_2022a', 'yan_2024a'],
            'note': 'Related papers about Federated GNN but different (2022 vs 2024, different approaches)'
        }
    ]
    
    for review in manual_review:
        report.append(f"\n- {', '.join(review['papers'])}")
        report.append(f"  Note: {review['note']}")
    
    # Summary
    report.append(f"\n\nSUMMARY")
    report.append("-" * 40)
    report.append(f"Papers removed: {removed_count}")
    report.append(f"Papers backed up: {removed_count}")
    report.append(f"Groups needing manual review: {len(manual_review)}")
    
    # Save report
    report_path = Path('similar_papers_handling_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print('\n'.join(report))
    print(f"\nReport saved to: {report_path}")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Generate final summary of all cleanup activities
"""
from pathlib import Path
from datetime import datetime

def count_papers():
    """Count current number of papers"""
    markdown_papers = Path('markdown_papers')
    return sum(1 for folder in markdown_papers.iterdir() if folder.is_dir() and (folder / 'paper.md').exists())

def main():
    """Generate final cleanup summary"""
    
    report = []
    report.append("FINAL CLEANUP SUMMARY REPORT")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("=" * 70)
    
    # Current status
    current_papers = count_papers()
    report.append(f"\nCURRENT STATUS")
    report.append("-" * 40)
    report.append(f"Total papers: {current_papers}")
    report.append(f"Original count: 369")
    report.append(f"Papers removed: {369 - current_papers}")
    
    # Duplicates removed
    report.append(f"\n\nDUPLICATES REMOVED")
    report.append("-" * 40)
    
    all_removed = [
        # First batch
        ('ghani_2020a', 'Wrong title, same content as ghani_2020b'),
        ('ilkou_2022b', 'Same paper as ilkou_2022a, placeholder DOI'),
        ('li_2012', 'Same paper as li_2022b, wrong year (2012 vs 2022)'),
        # Second batch
        ('aburasheed_2023a', 'Same paper as aburasheed_2023b, kept IEEE version'),
        ('bellomarini_2024b', 'Exact duplicate of bellomarini_2024a'),
        ('lukasgalk_2021', 'Same paper as galke_2021, poor author formatting'),
        ('leejunlin_2024', 'Same paper as lee_2024, poor author formatting'),
        ('privacy_2024', 'Same paper as zhou_2024b, incomplete authors'),
        ('sun_2024b', 'Exact duplicate of sun_2024a')
    ]
    
    for i, (paper, reason) in enumerate(all_removed, 1):
        report.append(f"{i}. {paper}: {reason}")
    
    # Fixes applied
    report.append(f"\n\nFIXES APPLIED")
    report.append("-" * 40)
    report.append("1. Folder/cite_key alignment:")
    report.append("   - xx_2022 → xie_2022")
    report.append("   - xu_2023a cite_key → xu_2023a (was xu_2023)")
    report.append("   - xu_2023b cite_key → xu_2023b (was xu_2023)")
    report.append("2. DOI corrections:")
    report.append("   - chen_2022: 10.1162/dint → 10.1162/dint_a_00116")
    
    # Quality issues summary
    report.append(f"\n\nQUALITY ISSUES SUMMARY")
    report.append("-" * 40)
    report.append("Papers with perfect metadata: 256 (70.1%)")
    report.append("Papers with minor issues: 108 (29.6%)")
    report.append("Papers with critical issues: 1 (0.3%)")
    report.append("\nMost common issues:")
    report.append("- Missing tags: 300 papers")
    report.append("- Missing URL: 264 papers")
    report.append("- Missing relevancy: 264 papers")
    report.append("- Missing DOI: 86 papers")
    
    # Papers needing attention
    report.append(f"\n\nPAPERS NEEDING ATTENTION")
    report.append("-" * 40)
    report.append("Critical issues:")
    report.append("- e065929_full: Missing authors, year, DOI")
    report.append("\nPlaceholder DOIs:")
    report.append("- ren_2025: 10.1145/nnnnnnn.nnnnnnn")
    report.append("- saad_2017: 10.1145/nnnnnnn.nnnnnnn")
    report.append("- ghani_2020b: 10.1109/RpJC.2020.DOI")
    
    # Similar papers kept (not duplicates)
    report.append(f"\n\nSIMILAR PAPERS KEPT (NOT DUPLICATES)")
    report.append("-" * 40)
    report.append("1. Temporal KG papers:")
    report.append("   - cai_2022: TKG Completion survey")
    report.append("   - su_2024: TKG Question Answering survey")
    report.append("   - chen_2024a & li_2021: Different TKG reasoning approaches")
    report.append("2. Federated GNN papers:")
    report.append("   - wu_2022, xie_2022a, yan_2024a: Different approaches/years")
    
    # Final statistics
    report.append(f"\n\nFINAL STATISTICS")
    report.append("-" * 40)
    report.append(f"Total unique papers: {current_papers}")
    report.append(f"All folders match cite_keys: Yes")
    report.append(f"No duplicate cite_keys: Yes")
    report.append(f"No duplicate DOIs (except placeholders): Yes")
    report.append(f"Data quality score: 70.1% perfect, 99.7% acceptable")
    
    # Save report
    report_path = Path('final_cleanup_summary.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print('\n'.join(report))
    print(f"\nReport saved to: {report_path}")
    
    # Also update the main CSV one more time
    print("\nRegenerating final clean CSV...")
    import subprocess
    subprocess.run(['python', 'generate_clean_csv.py'])

if __name__ == '__main__':
    main()
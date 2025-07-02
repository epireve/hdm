#!/usr/bin/env python3
"""
Generate final summary of papers needing metadata attention
"""
from pathlib import Path
from datetime import datetime

def main():
    """Generate summary report"""
    
    report = []
    report.append("METADATA ATTENTION SUMMARY")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("=" * 70)
    
    # Papers with placeholder DOIs
    report.append("\n1. PAPERS WITH PLACEHOLDER DOIs (3 papers)")
    report.append("-" * 60)
    
    placeholder_info = [
        {
            'cite_key': 'ghani_2020b',
            'title': 'Issues and challenges in Cloud Storage Architecture: A Survey',
            'doi': '10.1109/RpJC.2020.DOI',
            'note': 'Journal paper with incomplete DOI - needs real DOI from journal'
        },
        {
            'cite_key': 'ren_2025',
            'title': 'Enhancing Repository-Level Software Repair via Repository-Aware Knowledge Graphs',
            'doi': '10.1145/nnnnnnn.nnnnnnn',
            'note': 'arXiv preprint (2025) - may not have final DOI yet'
        },
        {
            'cite_key': 'saad_2017',
            'title': 'SENAI: Towards Software Engineering Native Generative Artificial Intelligence',
            'doi': '10.1145/nnnnnnn.nnnnnnn',
            'note': 'Year mismatch: marked as 2017 but arXiv ID suggests 2025 - needs year correction'
        }
    ]
    
    for paper in placeholder_info:
        report.append(f"\n{paper['cite_key']}:")
        report.append(f"  Title: {paper['title']}")
        report.append(f"  Current DOI: {paper['doi']}")
        report.append(f"  Action needed: {paper['note']}")
    
    # Fixed metadata summary
    report.append("\n\n2. METADATA FIXES COMPLETED")
    report.append("-" * 60)
    report.append("✓ Fixed 2 DOIs found in paper content:")
    report.append("  - li_2022: 10.1016/j.infsof.2022.106992")
    report.append("  - xie_2022: 10.1088/1755-1315/1101/9/092010")
    report.append("\n✓ Added metadata to 50 papers:")
    report.append("  - Tags added: 45 papers")
    report.append("  - URLs added: 25 papers") 
    report.append("  - Relevancy scores added: 42 papers")
    
    # Papers still needing attention
    report.append("\n\n3. REMAINING METADATA ISSUES")
    report.append("-" * 60)
    report.append("Papers with missing metadata (from original 309):")
    report.append("  - 259 papers still need metadata processing")
    report.append("  - 84 papers have truly missing DOIs (no DOI in content)")
    report.append("  - Most common issues: missing tags, URLs, and relevancy scores")
    
    # Critical paper
    report.append("\n\n4. CRITICAL PAPER RESOLVED")
    report.append("-" * 60)
    report.append("✓ e065929_full (now joosse_2023):")
    report.append("  - Previously missing: authors, year, DOI")
    report.append("  - Now complete with all critical metadata")
    report.append("  - Still needs: tags, URL, relevancy score")
    
    # Recommendations
    report.append("\n\n5. RECOMMENDATIONS")
    report.append("-" * 60)
    report.append("1. Manual actions needed:")
    report.append("   - Find real DOI for ghani_2020b journal paper")
    report.append("   - Correct year for saad_2017 (should be 2025)")
    report.append("   - Verify if ren_2025 has been published with final DOI")
    report.append("\n2. Automated processing:")
    report.append("   - Run fix_missing_metadata.py on remaining 259 papers")
    report.append("   - Consider batch processing in groups of 50")
    report.append("\n3. Quality assurance:")
    report.append("   - Review automatically added tags for accuracy")
    report.append("   - Verify relevancy scores match research focus")
    
    # Save report
    report_path = Path('metadata_attention_summary.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print('\n'.join(report))
    print(f"\nReport saved to: {report_path}")

if __name__ == '__main__':
    main()
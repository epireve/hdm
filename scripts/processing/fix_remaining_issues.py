#!/usr/bin/env python3
"""
Fix remaining issues found in the clean CSV generation
"""
import shutil
from pathlib import Path
import re

def fix_cite_key_in_paper(paper_path, new_cite_key):
    """Update cite_key in paper.md file"""
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update cite_key in YAML frontmatter
    content = re.sub(
        r'^cite_key:.*$',
        f'cite_key: {new_cite_key}',
        content,
        count=1,
        flags=re.MULTILINE
    )
    
    with open(paper_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Fix remaining issues"""
    markdown_papers = Path('markdown_papers')
    
    print("FIXING REMAINING ISSUES")
    print("=" * 60)
    
    # 1. Fix folder/cite_key misalignments
    print("\n1. Fixing folder/cite_key misalignments:")
    
    # Fix xx_2022 → xie_2022
    old_folder = markdown_papers / 'xx_2022'
    new_folder = markdown_papers / 'xie_2022'
    if old_folder.exists() and not new_folder.exists():
        shutil.move(str(old_folder), str(new_folder))
        print(f"✓ Renamed folder: xx_2022 → xie_2022")
    
    # 2. Fix duplicate cite_keys for xu papers
    print("\n2. Fixing duplicate cite_keys:")
    
    # xu_2023a and xu_2023b both have cite_key: xu_2023
    # Need to make them unique
    xu_2023a = markdown_papers / 'xu_2023a' / 'paper.md'
    xu_2023b = markdown_papers / 'xu_2023b' / 'paper.md'
    
    if xu_2023a.exists():
        fix_cite_key_in_paper(xu_2023a, 'xu_2023a')
        print("✓ Updated cite_key in xu_2023a/paper.md to 'xu_2023a'")
    
    if xu_2023b.exists():
        fix_cite_key_in_paper(xu_2023b, 'xu_2023b')
        print("✓ Updated cite_key in xu_2023b/paper.md to 'xu_2023b'")
    
    # 3. Report on e065929_full - needs manual attention
    print("\n3. Papers needing manual attention:")
    print("- e065929_full: Missing critical metadata (authors, year, DOI)")
    print("  This paper needs manual review to add missing information")
    
    # 4. Report on papers with placeholder DOIs
    print("\n4. Papers with placeholder DOIs needing updates:")
    placeholder_doi_papers = ['ren_2025', 'saad_2017', 'ghani_2020b']
    for paper in placeholder_doi_papers:
        paper_path = markdown_papers / paper / 'paper.md'
        if paper_path.exists():
            print(f"- {paper}: Has placeholder DOI, needs real DOI")
    
    print("\n✓ Fixes completed!")
    print("Run generate_clean_csv.py again to see updated results")

if __name__ == '__main__':
    main()
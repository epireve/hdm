#!/usr/bin/env python3
"""
Show a side-by-side comparison of original vs standardized paper
"""

import sys
from pathlib import Path
from datetime import datetime

def show_comparison(cite_key):
    """Show before and after comparison"""
    
    # Paths
    original_path = Path(f"markdown_papers/{cite_key}/paper.md")
    backup_path = list(Path(".").glob(f"backup_{cite_key}_*.md"))
    standardized_path = Path(f"standardized_{cite_key}.md")
    
    if not backup_path:
        print(f"❌ No backup found for {cite_key}")
        return
    
    backup_path = backup_path[0]
    
    # Read files
    with open(backup_path, 'r', encoding='utf-8') as f:
        original = f.read()
    
    if standardized_path.exists():
        with open(standardized_path, 'r', encoding='utf-8') as f:
            standardized = f.read()
            # Remove markdown code block wrapper if present
            if standardized.startswith('```markdown'):
                standardized = standardized[11:]
            if standardized.endswith('```'):
                standardized = standardized[:-3]
            standardized = standardized.strip()
    else:
        print(f"❌ No standardized version found")
        return
    
    print(f"\n{'='*80}")
    print(f"COMPARISON FOR: {cite_key}")
    print(f"{'='*80}")
    
    print(f"\n📄 ORIGINAL (first 1500 chars):")
    print("-" * 80)
    print(original[:1500])
    print("-" * 80)
    
    print(f"\n✨ STANDARDIZED (first 2000 chars):")
    print("-" * 80)
    print(standardized[:2000])
    print("-" * 80)
    
    # Stats
    original_lines = original.count('\n')
    standardized_lines = standardized.count('\n')
    
    print(f"\n📊 STATISTICS:")
    print(f"  Original: {len(original)} chars, {original_lines} lines")
    print(f"  Standardized: {len(standardized)} chars, {standardized_lines} lines")
    
    # Show what was added
    print(f"\n➕ NEW SECTIONS ADDED:")
    new_sections = ['## TL;DR', '## Key Insights', '## Metadata Summary']
    for section in new_sections:
        if section in standardized and section not in original:
            print(f"  ✓ {section}")
    
    # Clean standardized version (remove code block wrapper)
    clean_path = Path(f"clean_{cite_key}.md")
    with open(clean_path, 'w', encoding='utf-8') as f:
        f.write(standardized)
    
    print(f"\n✅ Clean standardized version saved to: {clean_path}")
    print(f"   This is what would replace the original paper.md")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compare original and standardized papers")
    parser.add_argument("cite_key", help="Paper cite_key to compare")
    args = parser.parse_args()
    
    show_comparison(args.cite_key)
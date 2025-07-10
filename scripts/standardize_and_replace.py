#!/usr/bin/env python3
"""
Standardize and replace paper.md files in-place
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

# Add parent directory
sys.path.append(str(Path(__file__).parent.parent))

from scripts.process_single_paper import SinglePaperProcessor

def standardize_in_place(cite_key):
    """Standardize a paper and replace the original file"""
    
    print(f"\n{'='*60}")
    print(f"Standardizing: {cite_key}")
    print(f"{'='*60}")
    
    # Path to the actual paper.md file
    paper_path = Path(f"markdown_papers/{cite_key}/paper.md")
    
    if not paper_path.exists():
        print(f"❌ Paper not found: {paper_path}")
        return False
    
    # Create processor
    processor = SinglePaperProcessor()
    
    # Get CSV data
    csv_row = processor.csv_data.get(cite_key, {})
    if not csv_row:
        print(f"❌ No CSV data for {cite_key}")
        return False
    
    # Read original content
    with open(paper_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    print(f"✓ Read original: {len(original_content)} characters")
    
    # Create timestamped backup in a backup directory
    backup_dir = Path(f"paper_backups/{cite_key}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_file = backup_dir / f"paper_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(original_content)
    
    print(f"✓ Backup saved: {backup_file}")
    
    # Process with API
    print("🤖 Calling Gemini API to standardize...")
    prompt = processor.create_standardization_prompt(original_content, csv_row, cite_key)
    standardized_content = processor.call_gemini_api(prompt)
    
    if not standardized_content:
        print("❌ Failed to get standardized content")
        return False
    
    # Clean response
    if standardized_content.startswith('```markdown'):
        standardized_content = standardized_content[11:]
    if standardized_content.endswith('```'):
        standardized_content = standardized_content[:-3]
    standardized_content = standardized_content.strip()
    
    # REPLACE THE ORIGINAL FILE
    with open(paper_path, 'w', encoding='utf-8') as f:
        f.write(standardized_content)
    
    print(f"✅ REPLACED original paper.md with standardized version")
    print(f"   File: {paper_path}")
    print(f"   New size: {len(standardized_content)} characters")
    
    # Show what changed
    print(f"\n📊 Changes:")
    print(f"   Original size: {len(original_content)} chars")
    print(f"   New size: {len(standardized_content)} chars")
    
    # Check for new sections
    new_sections = []
    if "## TL;DR" in standardized_content and "## TL;DR" not in original_content:
        new_sections.append("TL;DR")
    if "## Key Insights" in standardized_content and "## Key Insights" not in original_content:
        new_sections.append("Key Insights")
    if "## Metadata Summary" in standardized_content:
        new_sections.append("Metadata Summary")
    
    if new_sections:
        print(f"   Added sections: {', '.join(new_sections)}")
    
    print(f"\n✅ Success! The paper.md has been standardized in-place.")
    print(f"   Original backed up to: {backup_file}")
    
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Standardize paper.md files in-place")
    parser.add_argument("cite_key", help="Paper cite_key to standardize")
    
    args = parser.parse_args()
    
    success = standardize_in_place(args.cite_key)
    
    if success:
        print(f"\n✨ Paper {args.cite_key} has been standardized!")
        print(f"   Check: markdown_papers/{args.cite_key}/paper.md")
    else:
        print(f"\n❌ Failed to standardize {args.cite_key}")


if __name__ == "__main__":
    main()
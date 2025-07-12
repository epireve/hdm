#!/usr/bin/env python3
"""
Test script for paper reformatter with KiloCode - processes a single paper for verification
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.paper_reformatter import PaperReformatter

def test_single_paper():
    """Test reformatting on a single paper using KiloCode."""
    
    # Initialize reformatter with KiloCode
    try:
        reformatter = PaperReformatter()
        print(f"✓ KiloCode configuration loaded successfully")
        print(f"  Using model: {reformatter.model}")
        print(f"  API endpoint: {reformatter.config.openrouter_url}")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        return 1
        
    # Find a test paper with known issues
    test_paper = Path("markdown_papers/ho_2024/paper.md")
    
    if not test_paper.exists():
        # Find any paper
        papers = list(Path("markdown_papers").glob("*/paper.md"))
        if papers:
            test_paper = papers[0]
        else:
            print("No papers found to test")
            return 1
            
    print(f"\nTesting on: {test_paper}")
    
    # Extract current content for comparison
    frontmatter, content = reformatter.extract_frontmatter_and_content(test_paper)
    print(f"Current cite_key: {frontmatter.get('cite_key', 'none')}")
    
    # Check for issues
    has_html = '<sup>' in content or '<sub>' in content or '<span' in content
    has_broken_refs = '[[' in content or '\\[' in content or '#page-' in content
    
    print(f"Has HTML tags: {has_html}")
    print(f"Has broken references: {has_broken_refs}")
    
    # Show sample of content with issues
    if has_html or has_broken_refs:
        print("\nSample of issues found:")
        lines = content.split('\n')
        issue_count = 0
        for i, line in enumerate(lines):
            if issue_count >= 3:  # Show max 3 examples
                break
            if '<sup>' in line or '<span' in line or '[[' in line or '#page-' in line:
                print(f"  Line {i+1}: {line[:100]}...")
                issue_count += 1
    
    print("\n" + "="*60)
    print("Processing paper...")
    print("="*60 + "\n")
    
    # Process the paper
    result = reformatter.reformat_paper(test_paper, set())
    
    if result.success:
        print("✓ Reformatting successful!")
        print(f"  Original cite_key: {result.original_cite_key}")
        if result.new_cite_key:
            print(f"  New cite_key: {result.new_cite_key}")
        if result.folder_renamed:
            print(f"  Folder renamed: Yes")
        if result.changes_made:
            print("  Changes made:")
            for change in result.changes_made:
                print(f"    - {change}")
                
        # Verify changes
        print("\nVerifying changes...")
        new_frontmatter, new_content = reformatter.extract_frontmatter_and_content(result.paper_path)
        
        still_has_html = '<sup>' in new_content or '<sub>' in new_content or '<span' in new_content
        still_has_broken_refs = '[[' in new_content or '\\[' in new_content or '#page-' in new_content
        
        print(f"  Still has HTML tags: {still_has_html}")
        print(f"  Still has broken references: {still_has_broken_refs}")
        
        if not still_has_html and not still_has_broken_refs:
            print("\n✓ All issues successfully resolved!")
        else:
            print("\n⚠ Some issues may still remain - manual review recommended")
            
    else:
        print("✗ Reformatting failed!")
        print("  Errors:")
        for error in result.errors:
            print(f"    - {error}")
            
    return 0 if result.success else 1


if __name__ == "__main__":
    exit(test_single_paper())
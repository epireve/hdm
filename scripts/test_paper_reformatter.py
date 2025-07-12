#!/usr/bin/env python3
"""
Test script for paper reformatter - processes a single paper for verification
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.paper_reformatter import PaperReformatter

def test_single_paper():
    """Test reformatting on a single paper."""
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set")
        return 1
        
    # Initialize reformatter
    reformatter = PaperReformatter(api_key)
    
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
            
    print(f"Testing on: {test_paper}")
    
    # Extract current content for comparison
    frontmatter, content = reformatter.extract_frontmatter_and_content(test_paper)
    print(f"Current cite_key: {frontmatter.get('cite_key', 'none')}")
    
    # Check for issues
    has_html = '<sup>' in content or '<sub>' in content or '<span' in content
    has_broken_refs = '[[' in content or '\\[' in content or '#page-' in content
    
    print(f"Has HTML tags: {has_html}")
    print(f"Has broken references: {has_broken_refs}")
    
    # Process the paper
    result = reformatter.reformat_paper(test_paper, set())
    
    if result.success:
        print("\nReformatting successful!")
        print(f"Original cite_key: {result.original_cite_key}")
        if result.new_cite_key:
            print(f"New cite_key: {result.new_cite_key}")
        if result.folder_renamed:
            print(f"Folder renamed: Yes")
        if result.changes_made:
            print("Changes made:")
            for change in result.changes_made:
                print(f"  - {change}")
    else:
        print("\nReformatting failed!")
        print("Errors:")
        for error in result.errors:
            print(f"  - {error}")
            
    return 0 if result.success else 1


if __name__ == "__main__":
    exit(test_single_paper())
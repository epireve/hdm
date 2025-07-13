#!/usr/bin/env python3
"""
Process only the failed papers from the production run
"""

import os
import sys
from pathlib import Path

# Add the scripts directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_reformatter import EnhancedPaperReformatter

def get_failed_papers():
    """Get list of papers that failed in the production run"""
    markdown_dir = Path("/Users/invoture/dev.local/hdm/markdown_papers")
    output_dir = Path("/Users/invoture/dev.local/hdm/production_final_reformatted_1752365947")
    
    # Get all paper folders
    all_papers = set(folder.name for folder in markdown_dir.iterdir() if folder.is_dir())
    
    # Get processed papers
    processed_papers = set(folder.name for folder in output_dir.iterdir() if folder.is_dir())
    
    # Find failed papers
    failed_papers = all_papers - processed_papers
    
    return sorted(failed_papers)

def main():
    """Process failed papers"""
    failed_papers = get_failed_papers()
    print(f"📊 Found {len(failed_papers)} failed papers to process")
    
    # Use the same output directory to continue
    output_dir = Path("/Users/invoture/dev.local/hdm/production_final_reformatted_1752365947")
    
    # Create reformatter instance
    reformatter = EnhancedPaperReformatter(output_dir=output_dir)
    
    # Process failed papers with single worker to avoid rate limits
    markdown_dir = Path("/Users/invoture/dev.local/hdm/markdown_papers")
    paper_files = []
    
    for paper_name in failed_papers:
        paper_path = markdown_dir / paper_name / "paper.md"
        if paper_path.exists():
            paper_files.append(paper_path)
    
    print(f"📚 Processing {len(paper_files)} failed papers...")
    
    # Process with single worker to avoid rate limits
    reformatter.process_papers_from_list(paper_files, max_workers=1)

if __name__ == "__main__":
    main()
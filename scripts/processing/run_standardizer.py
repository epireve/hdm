#!/usr/bin/env python3
"""
Run the markdown standardizer without interactive prompts
"""
import sys
from pathlib import Path

# Import the standardizer functions
sys.path.insert(0, str(Path(__file__).parent))
from markdown_standardizer_improved import process_paper, Path

def main():
    """Main function"""
    print("Running Markdown Standardizer")
    print("=" * 60)
    
    markdown_papers = Path('markdown_papers')
    
    # Get papers to process
    if len(sys.argv) > 1:
        # Specific papers provided
        papers_to_process = []
        for arg in sys.argv[1:]:
            paper_path = markdown_papers / arg / 'paper.md'
            if paper_path.exists():
                papers_to_process.append(paper_path)
            else:
                print(f"Warning: {arg} not found")
    else:
        # Process sample papers
        sample_papers = ['zha_2024', 'liu_2024b', 'vassiliou_2023']
        papers_to_process = []
        for paper in sample_papers:
            paper_path = markdown_papers / paper / 'paper.md'
            if paper_path.exists():
                papers_to_process.append(paper_path)
    
    print(f"Papers to process: {len(papers_to_process)}")
    print("=" * 60)
    
    # Process each paper
    processed = 0
    for paper_path in papers_to_process:
        if process_paper(paper_path):
            processed += 1
    
    print("\n" + "=" * 60)
    print(f"Processing complete: {processed}/{len(papers_to_process)} papers standardized")

if __name__ == '__main__':
    main()
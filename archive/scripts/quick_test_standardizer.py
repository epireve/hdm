#!/usr/bin/env python3
"""
Quick test of the standardizer on a single paper
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.standardize_all_papers_concurrent import ConcurrentPaperStandardizer

def quick_test():
    """Test on a single paper"""
    
    # Clean up any existing state
    if Path("standardization_state.json").exists():
        Path("standardization_state.json").unlink()
    
    # Create standardizer with just 1 worker
    standardizer = ConcurrentPaperStandardizer(
        csv_path="hdm_research_papers_merged_20250710.csv",
        max_workers=1
    )
    
    # Process just one paper
    test_paper = "abdallah_2021"
    
    print(f"Testing standardizer on {test_paper}")
    print("="*60)
    
    # Create backup first
    paper_path = Path(f"markdown_papers/{test_paper}/paper.md")
    backup_path = Path(f"test_backup_{test_paper}.md")
    backup_path.write_text(paper_path.read_text())
    print(f"✓ Created backup: {backup_path}")
    
    # Process the paper
    result = standardizer.process_paper_worker(test_paper, 0)
    
    print(f"\nResult: {result['status']}")
    if result['status'] == 'success':
        print("✅ Test successful!")
        
        # Check the standardized paper
        standardized = paper_path.read_text()
        print(f"\nStandardized paper preview (first 500 chars):")
        print("-"*60)
        print(standardized[:500])
        print("-"*60)
        
        # Restore backup
        paper_path.write_text(backup_path.read_text())
        print(f"\n✓ Restored original from backup")
        
    else:
        print(f"❌ Test failed: {result.get('error', 'Unknown error')}")
    
    # Clean up
    backup_path.unlink()
    if Path("standardization_state.json").exists():
        Path("standardization_state.json").unlink()

if __name__ == "__main__":
    quick_test()
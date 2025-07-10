#!/usr/bin/env python3
"""
Test the concurrent standardizer with a small batch
"""

import sys
import subprocess
from pathlib import Path

def test_standardizer():
    """Test with a small batch of papers"""
    
    print("Testing Concurrent Paper Standardizer")
    print("="*60)
    
    # Get a few test papers
    papers_dir = Path("markdown_papers")
    test_papers = []
    
    for paper_dir in papers_dir.iterdir():
        if paper_dir.is_dir() and (paper_dir / "paper.md").exists():
            test_papers.append(paper_dir.name)
            if len(test_papers) >= 5:
                break
    
    print(f"Found {len(test_papers)} test papers: {', '.join(test_papers)}")
    
    # First, backup these papers manually
    print("\nCreating manual test backups...")
    test_backup_dir = Path("test_backups")
    test_backup_dir.mkdir(exist_ok=True)
    
    for cite_key in test_papers:
        src = papers_dir / cite_key / "paper.md"
        dst = test_backup_dir / f"{cite_key}_original.md"
        dst.write_text(src.read_text())
        print(f"  Backed up: {cite_key}")
    
    # Now run the standardizer with just 2 workers
    print("\nRunning standardizer with 2 workers on 5 papers...")
    print("-"*60)
    
    # Create a test state file to limit processing
    import json
    
    # Mark all papers except test papers as "completed"
    all_papers = [d.name for d in papers_dir.iterdir() if d.is_dir()]
    fake_completed = [p for p in all_papers if p not in test_papers]
    
    test_state = {
        "start_time": "2025-07-10T00:00:00",
        "completed": fake_completed,
        "failed": {},
        "in_progress": [],
        "last_update": "2025-07-10T00:00:00"
    }
    
    with open("standardization_state.json", 'w') as f:
        json.dump(test_state, f)
    
    # Run the standardizer
    cmd = [
        sys.executable,
        "scripts/standardize_all_papers_concurrent.py",
        "--workers", "2",
        "--resume"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Test completed successfully!")
        
        # Check results
        print("\nChecking results...")
        for cite_key in test_papers:
            original = (test_backup_dir / f"{cite_key}_original.md").read_text()
            standardized = (papers_dir / cite_key / "paper.md").read_text()
            
            print(f"\n{cite_key}:")
            print(f"  Original size: {len(original)} chars")
            print(f"  Standardized size: {len(standardized)} chars")
            
            # Check for key sections
            if "## TL;DR" in standardized:
                print("  ✓ TL;DR section added")
            if "## Key Insights" in standardized:
                print("  ✓ Key Insights section added")
            if "## Metadata Summary" in standardized:
                print("  ✓ Metadata Summary section added")
        
        # Clean up test state
        Path("standardization_state.json").unlink()
        
        print("\n" + "="*60)
        print("TEST SUCCESSFUL!")
        print("You can now run the full standardization with:")
        print("  python scripts/standardize_all_papers_concurrent.py --workers 20")
        print("="*60)
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Test failed: {e}")
        print("Check logs/ directory for details")
        
        # Restore backups
        print("\nRestoring original files...")
        for cite_key in test_papers:
            src = test_backup_dir / f"{cite_key}_original.md"
            dst = papers_dir / cite_key / "paper.md"
            dst.write_text(src.read_text())
            print(f"  Restored: {cite_key}")
        
        # Clean up test state
        if Path("standardization_state.json").exists():
            Path("standardization_state.json").unlink()

if __name__ == "__main__":
    test_standardizer()
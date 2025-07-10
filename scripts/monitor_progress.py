#!/usr/bin/env python3
"""Monitor standardization progress and continue processing"""

import json
import time
import subprocess
import sys
from pathlib import Path

def get_progress():
    """Get current progress"""
    if not Path("standardization_progress.json").exists():
        return {"completed": [], "failed": {}}
    
    with open("standardization_progress.json", 'r') as f:
        return json.load(f)

def count_total_papers():
    """Count total papers to process"""
    return len(list(Path("markdown_papers").glob("*/paper.md")))

def run_batch(batch_size=5):
    """Run a batch of papers"""
    try:
        result = subprocess.run(
            ["python", "scripts/standardize_papers_batch.py", "--limit", str(batch_size)],
            timeout=300,  # 5 minutes
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False

def main():
    total_papers = count_total_papers()
    print(f"Total papers to process: {total_papers}")
    
    batch_num = 1
    while True:
        progress = get_progress()
        completed = len(progress["completed"])
        failed = len(progress["failed"])
        
        print(f"\n=== Batch {batch_num} ===")
        print(f"Progress: {completed}/{total_papers} completed, {failed} failed")
        
        if completed >= total_papers - 10:  # Nearly done
            print("Standardization appears to be complete!")
            break
        
        print("Running batch...")
        success = run_batch(5)
        
        if not success:
            print("Batch timed out, but progress was likely saved")
        
        batch_num += 1
        time.sleep(5)  # Brief pause
        
        # Safety check - don't run forever
        if batch_num > 100:
            print("Safety limit reached, stopping")
            break
    
    # Final report
    final_progress = get_progress()
    print(f"\nFinal Status:")
    print(f"Completed: {len(final_progress['completed'])} papers")
    print(f"Failed: {len(final_progress['failed'])} papers")
    
    if final_progress['failed']:
        print("\nFailed papers:")
        for cite_key, error in final_progress['failed'].items():
            print(f"  - {cite_key}: {error}")

if __name__ == "__main__":
    main()
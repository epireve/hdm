#!/usr/bin/env python3
"""
Run batch conversion with automatic restarts
"""
import subprocess
import json
import time
from pathlib import Path

def get_progress():
    """Get current conversion progress"""
    with open('new_papers_checkpoint.json') as f:
        checkpoint = json.load(f)
    
    total = 55
    completed = len(checkpoint['completed'])
    failed = len(checkpoint.get('failed', {}))
    skipped = len(checkpoint.get('skipped', []))
    remaining = total - completed - failed - skipped
    
    return {
        'total': total,
        'completed': completed,
        'failed': failed,
        'skipped': skipped,
        'remaining': remaining
    }

def main():
    print("Starting batch conversion of new papers...")
    print("="*60)
    
    max_runs = 20
    run_count = 0
    
    while run_count < max_runs:
        run_count += 1
        progress = get_progress()
        
        if progress['remaining'] <= 0:
            print("\nAll papers processed!")
            break
        
        print(f"\nRun #{run_count}")
        print(f"Progress: {progress['completed']}/{progress['total']} completed")
        print(f"Remaining: {progress['remaining']} papers")
        print("-"*40)
        
        # Run converter with timeout
        try:
            subprocess.run(['python', 'convert_new_papers.py'], timeout=120)
        except subprocess.TimeoutExpired:
            print("Converter timed out after 120 seconds, restarting...")
        except Exception as e:
            print(f"Error: {e}")
        
        # Small delay before next run
        time.sleep(2)
    
    # Show final results
    progress = get_progress()
    print("\n" + "="*60)
    print("BATCH CONVERSION COMPLETE")
    print("="*60)
    print(f"Total papers: {progress['total']}")
    print(f"Successfully converted: {progress['completed']}")
    print(f"Failed: {progress['failed']}")
    print(f"Skipped: {progress['skipped']}")
    
    # List converted folders
    with open('new_papers_checkpoint.json') as f:
        checkpoint = json.load(f)
    
    if checkpoint['completed']:
        print(f"\nConverted {len(checkpoint['completed'])} papers to markdown:")
        for pdf_path in checkpoint['completed'][-20:]:  # Show last 20
            folder_name = Path(pdf_path).stem
            print(f"  ✓ markdown_papers/{folder_name}/")
    
    if checkpoint.get('failed'):
        print(f"\nFailed conversions:")
        for pdf, error in checkpoint['failed'].items():
            print(f"  ✗ {Path(pdf).name}: {error}")

if __name__ == "__main__":
    main()
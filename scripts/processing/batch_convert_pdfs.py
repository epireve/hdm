#!/usr/bin/env python3
"""
Batch PDF to Markdown converter with better error handling
Processes PDFs in smaller batches to avoid timeouts
"""

import subprocess
import json
import time
from pathlib import Path
import sys

def get_pending_pdfs(batch_size=50):
    """Get PDFs that haven't been processed yet"""
    papers_dir = Path("papers")
    checkpoint_file = Path("checkpoint_markdown_papers.json")
    
    # Get all PDFs > 100KB
    all_pdfs = [p for p in papers_dir.glob("*.pdf") if p.stat().st_size > 100 * 1024]
    
    # Filter out completed ones
    completed = set()
    failed = set()
    
    if checkpoint_file.exists():
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
            completed = set(checkpoint.get('completed', []))
            failed = set(checkpoint.get('failed', {}).keys())
    
    # Get pending PDFs (not completed, not failed)
    pending = [p for p in all_pdfs if str(p) not in completed and str(p) not in failed]
    
    return pending[:batch_size]

def run_batch_conversion(batch_num, batch_size=50):
    """Run conversion for a batch of PDFs"""
    print(f"\n{'='*70}")
    print(f"BATCH {batch_num} - Processing up to {batch_size} PDFs")
    print(f"{'='*70}")
    
    pending = get_pending_pdfs(batch_size)
    
    if not pending:
        print("No more PDFs to process!")
        return False
    
    print(f"Found {len(pending)} PDFs to process")
    print(f"First few: {[p.name for p in pending[:5]]}")
    
    # Run converter with shorter timeout and fewer workers
    cmd = [
        "./venv/bin/python", "pdf-markdown-converter.py",
        "--mode", "descriptions",
        "--fast",
        "--enhance",
        "--workers", "4",  # Reduced workers to avoid overload
        "--progress",
        "--min-size", "100",
        "--limit", str(len(pending)),
        "--timeout", "60"  # Shorter timeout per PDF
    ]
    
    print(f"\nRunning: {' '.join(cmd)}")
    
    try:
        # Run with a batch timeout
        process = subprocess.run(
            cmd,
            capture_output=False,
            text=True,
            timeout=batch_size * 90  # 90 seconds per PDF max
        )
        print(f"\nBatch {batch_num} completed with return code: {process.returncode}")
    except subprocess.TimeoutExpired:
        print(f"\nBatch {batch_num} timed out - will continue with next batch")
    except Exception as e:
        print(f"\nBatch {batch_num} error: {e}")
    
    # Wait a bit between batches
    time.sleep(5)
    return True

def main():
    """Main batch processing loop"""
    print("HDM PDF Batch Converter")
    print("Processing PDFs in batches to avoid timeouts")
    
    batch_size = 50
    max_batches = 10
    
    for batch_num in range(1, max_batches + 1):
        if not run_batch_conversion(batch_num, batch_size):
            break
        
        # Show progress
        checkpoint_file = Path("checkpoint_markdown_papers.json")
        if checkpoint_file.exists():
            with open(checkpoint_file, 'r') as f:
                checkpoint = json.load(f)
                completed = len(checkpoint.get('completed', []))
                failed = len(checkpoint.get('failed', {}))
                print(f"\nProgress: {completed} completed, {failed} failed")
    
    print("\n" + "="*70)
    print("BATCH PROCESSING COMPLETE")
    print("="*70)
    
    # Final statistics
    subprocess.run(["python", "extract_failed_pdfs.py"])

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Batch process large papers efficiently using the single paper processor
"""

import subprocess
import json
import time
from pathlib import Path


def get_failed_papers():
    """Get list of papers marked as failed (which are actually just skipped large papers)"""
    try:
        with open('standardization_progress.json', 'r') as f:
            data = json.load(f)
        return list(data.get('failed', {}).keys())
    except FileNotFoundError:
        return []


def get_completed_papers():
    """Get list of completed papers"""
    try:
        with open('standardization_progress.json', 'r') as f:
            data = json.load(f)
        return data.get('completed', [])
    except FileNotFoundError:
        return []


def process_paper_batch(papers, max_papers=10):
    """Process a batch of papers"""
    print(f"🚀 Processing batch of {min(len(papers), max_papers)} papers...")
    
    successful = 0
    failed = 0
    
    for i, paper in enumerate(papers[:max_papers]):
        print(f"\n[{i+1}/{min(len(papers), max_papers)}] Processing {paper}")
        
        try:
            # Run the single paper processor
            result = subprocess.run(
                ["python3", "scripts/process_one_large_paper.py", paper],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                print(f"  ✅ {paper} processed successfully")
                successful += 1
            else:
                print(f"  ❌ {paper} failed: {result.stderr}")
                failed += 1
                
        except subprocess.TimeoutExpired:
            print(f"  ⏰ {paper} timed out")
            failed += 1
        except Exception as e:
            print(f"  ❌ {paper} error: {e}")
            failed += 1
        
        # Brief pause between papers
        time.sleep(2)
    
    return successful, failed


def main():
    print("🎯 Batch Processing Large Papers")
    print("=" * 50)
    
    # Get current status
    completed = get_completed_papers()
    failed_papers = get_failed_papers()
    
    print(f"📊 Current Status:")
    print(f"   Completed: {len(completed)}")
    print(f"   Failed/Skipped: {len(failed_papers)}")
    
    if not failed_papers:
        print("\n🎉 No failed papers to process!")
        return
    
    print(f"\n📋 Processing {len(failed_papers)} papers in batches...")
    
    total_successful = 0
    total_failed = 0
    batch_size = 10
    
    # Process in batches
    for batch_start in range(0, len(failed_papers), batch_size):
        batch = failed_papers[batch_start:batch_start + batch_size]
        batch_num = (batch_start // batch_size) + 1
        
        print(f"\n🔄 Batch {batch_num} - Papers {batch_start + 1} to {min(batch_start + batch_size, len(failed_papers))}")
        
        successful, failed = process_paper_batch(batch, batch_size)
        total_successful += successful
        total_failed += failed
        
        print(f"\n📈 Batch {batch_num} Results: {successful} successful, {failed} failed")
        
        # Show current overall progress
        current_completed = len(get_completed_papers())
        print(f"📊 Overall Progress: {current_completed}/359 papers completed ({(current_completed/359)*100:.1f}%)")
        
        # Brief pause between batches
        if batch_start + batch_size < len(failed_papers):
            print("\n⏸️  Pausing 10 seconds before next batch...")
            time.sleep(10)
    
    # Final summary
    print("\n" + "=" * 50)
    print("🎉 BATCH PROCESSING COMPLETE!")
    print(f"📈 Results: {total_successful} successful, {total_failed} failed")
    
    final_completed = len(get_completed_papers())
    print(f"📊 Final Status: {final_completed}/359 papers completed ({(final_completed/359)*100:.1f}%)")
    
    remaining_failed = len(get_failed_papers())
    print(f"📋 Remaining: {remaining_failed} papers still need processing")


if __name__ == "__main__":
    main()
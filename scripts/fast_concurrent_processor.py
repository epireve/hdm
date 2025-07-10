#!/usr/bin/env python3
"""
Fast concurrent processor for remaining large papers
Uses ThreadPoolExecutor for maximum speed
"""

import json
import subprocess
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


class FastConcurrentProcessor:
    def __init__(self, max_workers=8):
        self.max_workers = max_workers
        self.progress_file = "standardization_progress.json"
        self.lock = threading.Lock()
        self.completed_count = 0
        self.failed_count = 0
        
    def get_failed_papers(self):
        """Get list of papers that need processing"""
        try:
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
            return list(data.get('failed', {}).keys())
        except FileNotFoundError:
            return []
    
    def process_single_paper(self, paper_key):
        """Process a single paper with timeout"""
        try:
            print(f"🔄 Processing {paper_key}")
            
            # Run the single paper processor
            result = subprocess.run(
                ["python3", "scripts/process_one_large_paper.py", paper_key],
                capture_output=True,
                text=True,
                timeout=240  # 4 minutes timeout for speed
            )
            
            if result.returncode == 0:
                with self.lock:
                    self.completed_count += 1
                print(f"✅ {paper_key} completed ({self.completed_count} total)")
                return True, paper_key
            else:
                with self.lock:
                    self.failed_count += 1
                print(f"❌ {paper_key} failed: {result.stderr[:100]}")
                return False, paper_key
                
        except subprocess.TimeoutExpired:
            with self.lock:
                self.failed_count += 1
            print(f"⏰ {paper_key} timed out")
            return False, paper_key
        except Exception as e:
            with self.lock:
                self.failed_count += 1
            print(f"❌ {paper_key} error: {e}")
            return False, paper_key
    
    def run_concurrent_processing(self):
        """Run concurrent processing with progress tracking"""
        failed_papers = self.get_failed_papers()
        
        if not failed_papers:
            print("🎉 No papers to process!")
            return
        
        print(f"🚀 Starting concurrent processing of {len(failed_papers)} papers")
        print(f"⚡ Using {self.max_workers} workers for maximum speed")
        print(f"⏱️  Estimated completion: ~{len(failed_papers) * 4 / self.max_workers / 60:.1f} minutes")
        print("=" * 60)
        
        start_time = time.time()
        
        # Process papers concurrently
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all papers
            future_to_paper = {
                executor.submit(self.process_single_paper, paper): paper 
                for paper in failed_papers
            }
            
            # Process results as they complete
            for future in as_completed(future_to_paper):
                paper = future_to_paper[future]
                try:
                    success, paper_key = future.result()
                    
                    # Print progress every 10 completions
                    total_processed = self.completed_count + self.failed_count
                    if total_processed % 10 == 0:
                        elapsed = time.time() - start_time
                        rate = total_processed / elapsed * 60  # papers per minute
                        remaining = len(failed_papers) - total_processed
                        eta = remaining / rate if rate > 0 else 0
                        
                        print(f"📊 Progress: {total_processed}/{len(failed_papers)} "
                              f"({total_processed/len(failed_papers)*100:.1f}%) "
                              f"| Rate: {rate:.1f}/min | ETA: {eta:.1f}min")
                        
                except Exception as e:
                    print(f"❌ Future error for {paper}: {e}")
        
        # Final summary
        elapsed = time.time() - start_time
        total_processed = self.completed_count + self.failed_count
        
        print("\n" + "=" * 60)
        print(f"🏁 CONCURRENT PROCESSING COMPLETE!")
        print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
        print(f"✅ Completed: {self.completed_count}")
        print(f"❌ Failed: {self.failed_count}")
        print(f"📈 Rate: {total_processed/elapsed*60:.1f} papers/minute")
        print(f"🚀 Speed improvement: ~{self.max_workers}x faster than sequential")


def main():
    processor = FastConcurrentProcessor(max_workers=8)  # 8 concurrent workers
    processor.run_concurrent_processing()


if __name__ == "__main__":
    main()
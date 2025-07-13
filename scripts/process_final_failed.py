#!/usr/bin/env python3
"""
Process the final 38 failed papers with better error handling
"""

import os
import sys
import json
import time
from pathlib import Path

# Add the scripts directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_reformatter import EnhancedPaperReformatter

def get_failed_papers():
    """Get list of papers that failed in the production run"""
    # Load processing results
    results_file = Path("/Users/invoture/dev.local/hdm/production_final_reformatted_1752365947/processing_results.json")
    
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Extract failed papers
    failed_papers = []
    for result in results:
        if not result['success']:
            cite_key = result.get('cite_key', result.get('original_cite_key'))
            if cite_key:
                failed_papers.append(cite_key)
    
    return failed_papers

def main():
    """Process failed papers with aggressive retry logic"""
    failed_papers = get_failed_papers()
    print(f"📊 Found {len(failed_papers)} failed papers to process")
    print("Failed papers:", ', '.join(failed_papers[:10]), '...' if len(failed_papers) > 10 else '')
    
    # Use the same output directory to continue
    output_dir = Path("/Users/invoture/dev.local/hdm/production_final_reformatted_1752365947")
    
    # Create reformatter instance
    reformatter = EnhancedPaperReformatter(output_dir=output_dir)
    
    # Process failed papers one by one with aggressive retry
    markdown_dir = Path("/Users/invoture/dev.local/hdm/markdown_papers")
    
    processed_count = 0
    still_failed = []
    
    for i, paper_name in enumerate(failed_papers, 1):
        paper_path = markdown_dir / paper_name / "paper.md"
        
        if not paper_path.exists():
            print(f"⚠️  {paper_name}: paper.md not found")
            still_failed.append(paper_name)
            continue
        
        print(f"\n📄 Processing {i}/{len(failed_papers)}: {paper_name}")
        
        # Try processing with aggressive retry logic
        max_retries = 5
        base_delay = 10  # Start with 10 seconds
        
        for retry in range(max_retries):
            try:
                # Add delay before each attempt to avoid rate limits
                if retry > 0:
                    delay = base_delay * (2 ** (retry - 1))  # Exponential backoff
                    print(f"   ⏳ Waiting {delay}s before retry {retry + 1}/{max_retries}...")
                    time.sleep(delay)
                else:
                    # Even on first attempt, wait a bit
                    time.sleep(3)
                
                result = reformatter.reformat_paper(paper_path)
                
                if result["success"]:
                    processed_count += 1
                    if result.get("cite_key_corrected"):
                        print(f"   ✅ Success! Cite key: {result.get('original_cite_key')} → {result.get('correct_cite_key')}")
                    else:
                        print(f"   ✅ Success! Cite key: {result.get('cite_key', paper_name)}")
                    break
                else:
                    error_msg = str(result.get("error", ""))
                    if "418" in error_msg or "Too many concurrent requests" in error_msg:
                        print(f"   ⚠️  Rate limit hit")
                        continue  # Will retry
                    else:
                        print(f"   ❌ Failed: {error_msg[:100]}")
                        if retry == max_retries - 1:
                            still_failed.append(paper_name)
                        
            except Exception as e:
                print(f"   ❌ Exception: {str(e)[:100]}")
                if retry == max_retries - 1:
                    still_failed.append(paper_name)
    
    print(f"\n🎉 Final processing complete!")
    print(f"   ✅ Successfully processed: {processed_count}/{len(failed_papers)}")
    print(f"   ❌ Still failed: {len(still_failed)}")
    
    if still_failed:
        print(f"\nPapers that still failed:")
        for paper in still_failed:
            print(f"   - {paper}")
    
    # Update cite key corrections file
    corrections_file = output_dir / "cite_key_corrections.json"
    if corrections_file.exists():
        with open(corrections_file, 'r') as f:
            corrections = json.load(f)
        print(f"\n🔑 Total cite key corrections: {len(corrections)}")

if __name__ == "__main__":
    main()
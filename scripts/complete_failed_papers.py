#!/usr/bin/env python3
"""
Complete processing of failed papers with better error handling and retries
"""

import os
import sys
import time
from pathlib import Path

# Add the scripts directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_reformatter import EnhancedPaperReformatter

def get_remaining_papers():
    """Get list of papers that still need processing"""
    markdown_dir = Path("/Users/invoture/dev.local/hdm/markdown_papers")
    output_dir = Path("/Users/invoture/dev.local/hdm/production_final_reformatted_1752365947")
    
    # Get all paper folders
    all_papers = set(folder.name for folder in markdown_dir.iterdir() if folder.is_dir())
    
    # Get processed papers
    processed_papers = set(folder.name for folder in output_dir.iterdir() if folder.is_dir())
    
    # Find remaining papers
    remaining_papers = all_papers - processed_papers
    
    return sorted(remaining_papers)

def main():
    """Process remaining papers with retry logic"""
    remaining_papers = get_remaining_papers()
    print(f"📊 Found {len(remaining_papers)} remaining papers to process")
    
    if not remaining_papers:
        print("✅ All papers have been processed!")
        return
    
    # Use the same output directory to continue
    output_dir = Path("/Users/invoture/dev.local/hdm/production_final_reformatted_1752365947")
    
    # Create reformatter instance
    reformatter = EnhancedPaperReformatter(output_dir=output_dir)
    
    # Process remaining papers one by one with retry logic
    markdown_dir = Path("/Users/invoture/dev.local/hdm/markdown_papers")
    
    processed_count = 0
    failed_count = 0
    
    for i, paper_name in enumerate(remaining_papers, 1):
        paper_path = markdown_dir / paper_name / "paper.md"
        
        if not paper_path.exists():
            print(f"⚠️  {paper_name}: paper.md not found")
            continue
        
        print(f"\n📄 Processing {i}/{len(remaining_papers)}: {paper_name}")
        
        # Try processing with retry logic
        max_retries = 3
        retry_delay = 5  # seconds
        
        for retry in range(max_retries):
            try:
                result = reformatter.reformat_paper(paper_path)
                
                if result["success"]:
                    processed_count += 1
                    if result.get("cite_key_corrected"):
                        print(f"   ✅ Success! Cite key: {result.get('original_cite_key')} → {result.get('correct_cite_key')}")
                    else:
                        print(f"   ✅ Success! Cite key: {result.get('cite_key')}")
                    break
                else:
                    if "418" in str(result.get("error", "")) or "Too many concurrent requests" in str(result.get("error", "")):
                        print(f"   ⏳ Rate limit hit, waiting {retry_delay}s before retry {retry + 1}/{max_retries}...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                    else:
                        print(f"   ❌ Failed: {result.get('error')}")
                        failed_count += 1
                        break
                        
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                if retry < max_retries - 1:
                    print(f"   ⏳ Waiting {retry_delay}s before retry {retry + 1}/{max_retries}...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    failed_count += 1
        
        # Add delay between papers to avoid rate limits
        if i < len(remaining_papers):
            time.sleep(2)
    
    print(f"\n🎉 Processing complete!")
    print(f"   ✅ Successfully processed: {processed_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   📊 Total completion: {len(processed_papers) + processed_count}/{len(all_papers)}")

if __name__ == "__main__":
    main()
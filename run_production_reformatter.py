#!/usr/bin/env python3
"""
Production run script for paper reformatting
Runs the simple reformatter with optimal settings
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from scripts.simple_reformatter import SimplePaperReformatter

def main():
    """Run production reformatting"""
    print("🚀 Starting Production Paper Reformatting")
    print("="*50)
    
    # Configuration
    output_dir = Path(f"production_reformatted_papers_final_{int(time.time())}")
    max_papers = 20  # Start with first 20 papers
    max_workers = 2   # Conservative to avoid API rate limits
    
    print(f"📁 Output directory: {output_dir}")
    print(f"📚 Processing: {max_papers} papers")
    print(f"⚡ Workers: {max_workers}")
    print(f"🤖 Model: google/gemini-2.5-flash")
    print()
    
    try:
        reformatter = SimplePaperReformatter(output_dir=output_dir)
        reformatter.process_papers(max_papers=max_papers, max_workers=max_workers)
        
        print()
        print("✅ Production run completed successfully!")
        print(f"📂 Results saved to: {output_dir}")
        
    except KeyboardInterrupt:
        print("\n🛑 Processing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
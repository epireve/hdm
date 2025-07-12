#!/usr/bin/env python3
"""
Test script to check paper analysis functionality without API calls
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.paper_reformatter import PaperReformatter

def test_analysis():
    """Test the paper analysis functionality"""
    
    print("🔍 Testing Paper Analysis Functionality\n")
    
    # Create reformatter instance (without API)
    try:
        reformatter = PaperReformatter(model="test", output_dir=Path("test_analysis"))
        print("✅ Reformatter initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize reformatter: {e}")
        return
    
    # Find papers to analyze
    markdown_dir = Path("markdown_papers") 
    paper_files = list(markdown_dir.glob("*/paper.md"))[:10]  # Test first 10
    
    print(f"📚 Found {len(paper_files)} papers to analyze\n")
    
    # Analyze each paper
    needs_reform_count = 0
    skip_count = 0
    
    for paper_path in paper_files:
        try:
            needs_reform, issues = reformatter.needs_reformatting(paper_path)
            
            print(f"📄 {paper_path.parent.name}:")
            if needs_reform:
                print(f"   🔧 Needs reformatting: {', '.join(issues)}")
                needs_reform_count += 1
            else:
                print(f"   ✅ Already properly formatted")
                skip_count += 1
            print()
            
        except Exception as e:
            print(f"   ❌ Error analyzing: {e}")
            print()
    
    print("📊 Analysis Summary:")
    print(f"   🔧 Need reformatting: {needs_reform_count}")
    print(f"   ✅ Already good: {skip_count}")
    print(f"   📈 Efficiency: {skip_count}/{len(paper_files)} papers can be skipped")

if __name__ == "__main__":
    test_analysis()
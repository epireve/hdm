#!/usr/bin/env python3
"""
Standalone test of paper analysis functionality
"""

import re
from pathlib import Path
from typing import Tuple, List

def needs_reformatting(paper_path: Path) -> Tuple[bool, List[str]]:
    """Check if a paper needs reformatting based on content analysis."""
    try:
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Check for HTML tags
        html_patterns = [
            r'<sup>.*?</sup>',
            r'<sub>.*?</sub>', 
            r'<span[^>]*>.*?</span>',
            r'<em>.*?</em>',
            r'<strong>.*?</strong>',
            r'<i>.*?</i>',
            r'<b>.*?</b>'
        ]
        
        for pattern in html_patterns:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                issues.append("Contains HTML tags")
                break
        
        # Check for broken references
        broken_ref_patterns = [
            r'\[\[(\d+)\]\]\(#page-\d+-\d+\)',  # [[1]](#page-1-0)
            r'\[(\d+)\]\(#page-\d+-\d+\)',      # [1](#page-1-0)
            r'\[\\\[(\d+)\\\]\]\(#page-\d+-\d+\)',  # [\[1\]](#page-1-0)
        ]
        
        for pattern in broken_ref_patterns:
            if re.search(pattern, content):
                issues.append("Has broken references")
                break
        
        # Check for logo/image references that need removal
        logo_patterns = [
            r'!\[.*?logo.*?\]',
            r'!\[.*?Logo.*?\]',
            r'<!-- Image Description:.*?logo.*?-->',
        ]
        
        for pattern in logo_patterns:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                issues.append("Contains logo references")
                break
        
        # Check for non-clickable references (should be [[1]](#ref-1) format)
        citation_pattern = r'\[(\d+)\](?!\(#ref-\d+\))'
        if re.search(citation_pattern, content):
            issues.append("Has non-clickable references")
        
        # Check for poor formatting
        if re.search(r'\n\s*\n\s*\n\s*\n', content):
            issues.append("Has excessive whitespace")
        
        if re.search(r'#{5,}', content):
            issues.append("Has malformed headers")
        
        needs_reform = len(issues) > 0
        return needs_reform, issues
        
    except Exception as e:
        print(f"Error checking {paper_path}: {e}")
        return False, ["Error reading file"]

def main():
    """Test paper analysis"""
    print("🔍 Testing Paper Analysis Functionality\n")
    
    # Find papers to analyze
    markdown_dir = Path("markdown_papers") 
    if not markdown_dir.exists():
        print(f"❌ Directory not found: {markdown_dir}")
        return
        
    paper_files = list(markdown_dir.glob("*/paper.md"))[:20]  # Test first 20
    
    print(f"📚 Found {len(paper_files)} papers to analyze\n")
    
    # Analyze each paper
    needs_reform_count = 0
    skip_count = 0
    
    for paper_path in paper_files:
        needs_reform, issues = needs_reformatting(paper_path)
        
        print(f"📄 {paper_path.parent.name}:")
        if needs_reform:
            print(f"   🔧 Needs reformatting: {', '.join(issues)}")
            needs_reform_count += 1
        else:
            print(f"   ✅ Already properly formatted")
            skip_count += 1
        print()
    
    print("📊 Analysis Summary:")
    print(f"   🔧 Need reformatting: {needs_reform_count}")
    print(f"   ✅ Already good: {skip_count}")
    print(f"   📈 Efficiency: {skip_count}/{len(paper_files)} papers can be skipped")
    
    efficiency = (skip_count / len(paper_files)) * 100 if paper_files else 0
    print(f"   🎯 Skip rate: {efficiency:.1f}%")

if __name__ == "__main__":
    main()
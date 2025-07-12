#!/usr/bin/env python3
"""
Author extraction and cite key correction system
Analyzes paper content to extract correct author names and fix cite keys
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class AuthorExtractor:
    """Extract correct author information from paper content"""
    
    def __init__(self, markdown_dir: Path = None):
        self.markdown_dir = markdown_dir or Path("/Users/invoture/dev.local/hdm/markdown_papers")
        self.results = []
        
    def extract_authors_from_content(self, content: str) -> List[str]:
        """Extract author names from paper content using multiple patterns"""
        
        # Remove YAML frontmatter first
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
        
        authors = []
        
        # Pattern 1: Standard academic format with superscripts
        # Carlo Humana1, Anton H Bassona2*, Karel Krugera3
        pattern1 = r'([A-Z][a-z]+ [A-Z]\.? [A-Z][a-z]+\d*[\*]?)'
        matches1 = re.findall(pattern1, content[:2000])  # Search in first 2000 chars
        
        # Pattern 2: Email-based extraction  
        # carlohuman@gmail.com, ahb@sun.ac.za
        email_pattern = r'(\w+)@[\w\.]+'
        email_matches = re.findall(email_pattern, content[:2000])
        
        # Pattern 3: Name followed by affiliation number
        # John Smith1, Jane Doe2
        pattern3 = r'([A-Z][a-z]+ [A-Z]\.? [A-Z][a-z]+)\d+'
        matches3 = re.findall(pattern3, content[:2000])
        
        # Pattern 4: Names in title area (after first header)
        lines = content.split('\n')
        header_found = False
        for line in lines[:50]:  # Check first 50 lines
            if line.startswith('#') and not header_found:
                header_found = True
                continue
            if header_found and line.strip():
                # Look for name patterns in lines after title
                name_matches = re.findall(r'([A-Z][a-z]+ [A-Z]\.? ?[A-Z][a-z]+)', line)
                for match in name_matches:
                    if len(match.split()) >= 2:  # At least first and last name
                        authors.append(match.strip())
                if len(authors) >= 3:  # Stop after finding reasonable number
                    break
        
        # Clean and deduplicate authors
        cleaned_authors = []
        for author in set(authors):  # Remove duplicates
            # Clean up author name
            author = re.sub(r'\d+[\*]*$', '', author)  # Remove trailing numbers/asterisks
            author = author.strip()
            if len(author.split()) >= 2 and len(author) > 5:  # Valid name check
                cleaned_authors.append(author)
        
        return cleaned_authors[:5]  # Return max 5 authors
    
    def extract_year_from_content(self, content: str) -> Optional[int]:
        """Extract publication year from paper content"""
        
        # Pattern 1: arXiv format - arXiv:2501.00136v1 [cs.CV] 30 Dec 2024
        arxiv_pattern = r'arXiv:\d+\.\d+v?\d*.*?(\d{4})'
        arxiv_match = re.search(arxiv_pattern, content[:3000])
        if arxiv_match:
            return int(arxiv_match.group(1))
        
        # Pattern 2: Copyright year - © 2024
        copyright_pattern = r'©\s*(\d{4})'
        copyright_match = re.search(copyright_pattern, content[:3000])
        if copyright_match:
            return int(copyright_match.group(1))
        
        # Pattern 3: Publication year in text
        year_pattern = r'\b(20[01]\d|19[89]\d)\b'
        year_matches = re.findall(year_pattern, content[:3000])
        if year_matches:
            # Return the most recent reasonable year
            years = [int(y) for y in year_matches]
            current_year = datetime.now().year
            valid_years = [y for y in years if 1990 <= y <= current_year]
            if valid_years:
                return max(valid_years)
        
        return None
    
    def generate_cite_key(self, authors: List[str], year: int) -> str:
        """Generate proper cite key from authors and year"""
        if not authors:
            return f"unknown_{year}"
        
        # Extract first author's last name
        first_author = authors[0]
        name_parts = first_author.split()
        
        # Handle different name formats
        if len(name_parts) >= 2:
            # Standard: "John Smith" -> "smith"
            last_name = name_parts[-1].lower()
        else:
            # Single name fallback
            last_name = first_author.lower()
        
        # Clean last name (remove special characters)
        last_name = re.sub(r'[^a-z]', '', last_name)
        
        return f"{last_name}_{year}"
    
    def analyze_paper(self, paper_path: Path) -> Dict:
        """Analyze a single paper for correct author information"""
        
        try:
            with open(paper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract YAML frontmatter
            frontmatter = {}
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    for line in yaml_content.strip().split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            frontmatter[key.strip()] = value.strip().strip('"\'')
            
            current_cite_key = frontmatter.get('cite_key', paper_path.parent.name)
            current_authors = frontmatter.get('authors', '')
            current_year = frontmatter.get('year', '')
            
            # Extract correct information from content
            extracted_authors = self.extract_authors_from_content(content)
            extracted_year = self.extract_year_from_content(content)
            
            # Generate correct cite key
            if extracted_authors and extracted_year:
                correct_cite_key = self.generate_cite_key(extracted_authors, extracted_year)
            else:
                correct_cite_key = current_cite_key
            
            # Determine if correction is needed
            needs_correction = (
                current_cite_key != correct_cite_key or
                not extracted_authors or
                str(current_year) != str(extracted_year) if extracted_year else False
            )
            
            result = {
                "paper_path": str(paper_path),
                "folder_name": paper_path.parent.name,
                "current_cite_key": current_cite_key,
                "current_authors": current_authors,
                "current_year": current_year,
                "extracted_authors": extracted_authors,
                "extracted_year": extracted_year,
                "correct_cite_key": correct_cite_key,
                "needs_correction": needs_correction,
                "confidence": "high" if len(extracted_authors) >= 2 else "medium" if extracted_authors else "low"
            }
            
            return result
            
        except Exception as e:
            return {
                "paper_path": str(paper_path),
                "folder_name": paper_path.parent.name,
                "error": str(e),
                "needs_correction": False
            }
    
    def analyze_all_papers(self, max_papers: int = None) -> List[Dict]:
        """Analyze all papers for author extraction issues"""
        
        paper_files = list(self.markdown_dir.glob("*/paper.md"))
        if max_papers:
            paper_files = paper_files[:max_papers]
        
        print(f"🔍 Analyzing {len(paper_files)} papers for author extraction issues...")
        
        results = []
        issues_found = 0
        
        for i, paper_path in enumerate(paper_files):
            if i % 20 == 0:
                print(f"   Progress: {i}/{len(paper_files)} papers analyzed")
            
            result = self.analyze_paper(paper_path)
            results.append(result)
            
            if result.get("needs_correction", False):
                issues_found += 1
        
        print(f"✅ Analysis complete: {issues_found} papers need author correction")
        
        # Sort by confidence and issues
        results.sort(key=lambda x: (x.get("needs_correction", False), x.get("confidence", "low")), reverse=True)
        
        return results
    
    def generate_report(self, results: List[Dict], output_file: str = "author_extraction_report.json"):
        """Generate detailed report of author extraction issues"""
        
        # Statistics
        total_papers = len(results)
        needs_correction = sum(1 for r in results if r.get("needs_correction", False))
        high_confidence = sum(1 for r in results if r.get("confidence") == "high")
        
        # Group by issue type
        cite_key_issues = [r for r in results if r.get("needs_correction") and r.get("current_cite_key") != r.get("correct_cite_key")]
        author_issues = [r for r in results if r.get("needs_correction") and not r.get("extracted_authors")]
        year_issues = [r for r in results if r.get("needs_correction") and str(r.get("current_year", "")) != str(r.get("extracted_year", ""))]
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_papers": total_papers,
                "needs_correction": needs_correction,
                "high_confidence_extractions": high_confidence,
                "cite_key_issues": len(cite_key_issues),
                "author_issues": len(author_issues),
                "year_issues": len(year_issues)
            },
            "top_issues": results[:20],  # Top 20 issues
            "all_results": results
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {output_file}")
        
        # Print summary
        print()
        print("📊 Author Extraction Analysis Summary")
        print("="*40)
        print(f"📚 Total papers analyzed: {total_papers}")
        print(f"🔧 Need correction: {needs_correction}")
        print(f"📝 High confidence extractions: {high_confidence}")
        print()
        print("Issue breakdown:")
        print(f"   🔑 Cite key issues: {len(cite_key_issues)}")
        print(f"   👤 Author extraction issues: {len(author_issues)}")
        print(f"   📅 Year issues: {len(year_issues)}")
        
        if cite_key_issues:
            print()
            print("🔑 Top Cite Key Issues:")
            for issue in cite_key_issues[:5]:
                current = issue.get("current_cite_key", "unknown")
                correct = issue.get("correct_cite_key", "unknown")
                authors = ", ".join(issue.get("extracted_authors", [])[:2])
                print(f"   {current} → {correct} ({authors})")
        
        return report

def main():
    """Main function for testing"""
    extractor = AuthorExtractor()
    
    # Test with specific problematic papers first
    test_papers = ["engineering_2020", "das_2025", "wang_2022a"]
    
    print("🧪 Testing author extraction on known papers...")
    for paper_name in test_papers:
        paper_path = Path(f"/Users/invoture/dev.local/hdm/markdown_papers/{paper_name}/paper.md")
        if paper_path.exists():
            result = extractor.analyze_paper(paper_path)
            print(f"\n📄 {paper_name}:")
            print(f"   Current: {result.get('current_cite_key')} | {result.get('current_authors')}")
            print(f"   Extracted: {result.get('correct_cite_key')} | {', '.join(result.get('extracted_authors', []))}")
            print(f"   Needs correction: {result.get('needs_correction')}")
    
    print("\n" + "="*50)
    
    # Analyze first 50 papers
    results = extractor.analyze_all_papers(max_papers=50)
    report = extractor.generate_report(results)
    
    return report

if __name__ == "__main__":
    main()
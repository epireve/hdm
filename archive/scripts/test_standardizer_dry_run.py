#!/usr/bin/env python3
"""
Test Paper Standardizer - Dry Run
This version simulates the standardization process without calling the API
"""

import sys
import json
import csv
from pathlib import Path
from datetime import datetime
import re

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

class StandardizerDryRun:
    """Dry run test of paper standardizer"""
    
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self.csv_data = self.load_csv_data()
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "csv_file": str(self.csv_path),
            "dry_run": True,
            "papers": {}
        }
    
    def load_csv_data(self):
        """Load CSV data"""
        csv_data = {}
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cite_key = row.get('cite_key', '').strip()
                    if cite_key:
                        csv_data[cite_key] = row
            
            print(f"✓ Loaded {len(csv_data)} papers from CSV")
            return csv_data
        
        except Exception as e:
            print(f"❌ Failed to load CSV: {e}")
            return {}
    
    def extract_frontmatter(self, content):
        """Extract YAML frontmatter"""
        if not content.startswith('---'):
            return {}, content
        
        try:
            end_match = re.search(r'\n---\s*\n', content[3:])
            if not end_match:
                return {}, content
            
            yaml_text = content[3:end_match.start() + 3]
            remaining = content[end_match.end() + 3:]
            
            # Simple YAML parsing
            metadata = {}
            current_list = None
            
            for line in yaml_text.split('\n'):
                line = line.rstrip()
                
                if not line or line.startswith('#'):
                    continue
                
                # List item
                if line.startswith('  - ') or line.startswith('- '):
                    if current_list is not None:
                        item = line.replace('  - ', '').replace('- ', '').strip()
                        metadata[current_list].append(item)
                    continue
                
                # Key: value
                if ':' in line and not line.startswith(' '):
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if not value:  # Start of list
                        metadata[key] = []
                        current_list = key
                    else:
                        # Remove quotes
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        metadata[key] = value
                        current_list = None
            
            return metadata, remaining
        
        except Exception as e:
            print(f"⚠️  Failed to parse frontmatter: {e}")
            return {}, content
    
    def simulate_standardization(self, content, csv_row, cite_key):
        """Simulate what the standardization would do"""
        # Extract current metadata
        current_metadata, body = self.extract_frontmatter(content)
        
        # Parse tags from CSV
        tags = []
        if csv_row.get('Tags'):
            tags = [t.strip() for t in csv_row['Tags'].split(',') if t.strip()]
        
        # Count words and sections
        word_count = len(body.split())
        sections = len(re.findall(r'^#{1,3}\s+', body, re.MULTILINE))
        
        # Build standardized metadata
        standardized_metadata = {
            "cite_key": cite_key,
            "title": csv_row.get('title', current_metadata.get('title', 'N/A')),
            "authors": csv_row.get('authors', current_metadata.get('authors', 'N/A')),
            "year": csv_row.get('year', current_metadata.get('year', 'N/A')),
            "doi": csv_row.get('DOI', current_metadata.get('doi', 'N/A')),
            "url": csv_row.get('url', current_metadata.get('url', 'N/A')),
            "relevancy": csv_row.get('Relevancy', current_metadata.get('relevancy', 'N/A')),
            "relevancy_justification": csv_row.get('Relevancy Justification', 'N/A'),
            "tags": tags or current_metadata.get('tags', []),
            "date_processed": current_metadata.get('date_processed', 'N/A'),
            "phase2_processed": current_metadata.get('phase2_processed', False),
            "standardization_date": datetime.now().strftime('%Y-%m-%d'),
            "standardization_version": "1.0",
            "word_count": word_count,
            "sections_count": sections
        }
        
        return standardized_metadata
    
    def validate_paper(self, paper_path, metadata, csv_row):
        """Validate the paper would be correctly standardized"""
        warnings = []
        
        # Check required fields
        required = ['cite_key', 'title', 'authors', 'year']
        for field in required:
            if not metadata.get(field) or metadata[field] == 'N/A':
                warnings.append(f"Missing required field: {field}")
        
        # Check CSV alignment
        if csv_row:
            if metadata['title'] != csv_row.get('title', ''):
                warnings.append("Title mismatch with CSV")
            if metadata['year'] != csv_row.get('year', ''):
                warnings.append("Year mismatch with CSV")
        
        return warnings
    
    def process_paper(self, paper_path):
        """Process a single paper (dry run)"""
        cite_key = paper_path.parent.name
        print(f"\n📄 Processing: {cite_key}")
        
        result = {
            "cite_key": cite_key,
            "path": str(paper_path),
            "status": "simulated"
        }
        
        try:
            # Get CSV data
            csv_row = self.csv_data.get(cite_key, {})
            if not csv_row:
                print(f"  ⚠️  No CSV data found for {cite_key}")
            
            # Read content
            with open(paper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"  ✓ Read {len(content)} characters")
            
            # Extract current metadata
            current_metadata, _ = self.extract_frontmatter(content)
            print(f"  ✓ Current metadata fields: {list(current_metadata.keys())}")
            
            # Simulate standardization
            new_metadata = self.simulate_standardization(content, csv_row, cite_key)
            
            # Validate
            warnings = self.validate_paper(paper_path, new_metadata, csv_row)
            if warnings:
                result["warnings"] = warnings
                for w in warnings:
                    print(f"  ⚠️  {w}")
            
            # Show what would change
            print(f"  📊 Standardization preview:")
            print(f"     - Word count: {new_metadata['word_count']}")
            print(f"     - Sections: {new_metadata['sections_count']}")
            print(f"     - Tags: {len(new_metadata['tags'])}")
            
            # Check what would be added from CSV
            additions = []
            if csv_row:
                if csv_row.get('TL;DR'):
                    additions.append("TL;DR section")
                if csv_row.get('Insights'):
                    additions.append("Key Insights section")
                if csv_row.get('Research Question'):
                    additions.append("Metadata Summary section")
            
            if additions:
                print(f"  ➕ Would add: {', '.join(additions)}")
            
            result["status"] = "success"
            result["metadata"] = new_metadata
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            print(f"  ❌ Error: {e}")
        
        return result
    
    def run(self, papers):
        """Run dry run test on specified papers"""
        print(f"\n🚀 Starting dry run test")
        print(f"📊 CSV data loaded: {len(self.csv_data)} papers")
        
        # Find paper paths
        paper_paths = []
        for cite_key in papers:
            path = Path(f"markdown_papers/{cite_key}/paper.md")
            if path.exists():
                paper_paths.append(path)
            else:
                print(f"⚠️  Paper not found: {cite_key}")
        
        if not paper_paths:
            print("❌ No valid papers found")
            return
        
        print(f"📚 Found {len(paper_paths)} papers to test")
        
        # Process each paper
        successful = 0
        failed = 0
        warnings_count = 0
        
        for path in paper_paths:
            result = self.process_paper(path)
            self.report["papers"][result["cite_key"]] = result
            
            if result["status"] == "success":
                successful += 1
                if result.get("warnings"):
                    warnings_count += len(result["warnings"])
            else:
                failed += 1
        
        # Save report
        report_path = f"dry_run_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(self.report, f, indent=2)
        
        # Summary
        print(f"\n\n{'='*60}")
        print("DRY RUN SUMMARY")
        print(f"{'='*60}")
        print(f"✓ Papers analyzed: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Total warnings: {warnings_count}")
        print(f"📊 Report saved: {report_path}")
        print(f"\nThis was a dry run - no files were modified")
        print(f"{'='*60}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Test paper standardizer (dry run)")
    parser.add_argument("--papers", nargs="+", default=["abdallah_2021", "aburasheed_2023b", "ai_2025"], 
                       help="Paper cite_keys to test")
    parser.add_argument("--csv", default="hdm_research_papers_merged_20250710.csv", 
                       help="CSV file")
    
    args = parser.parse_args()
    
    tester = StandardizerDryRun(args.csv)
    tester.run(args.papers)


if __name__ == "__main__":
    main()
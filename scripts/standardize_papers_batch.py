#!/usr/bin/env python3
"""
Batch standardizer for all papers - processes papers sequentially with proper error handling
"""

import sys
import json
import csv
import urllib.request
import urllib.error
import ssl
import os
from pathlib import Path
from datetime import datetime
import time

# Add parent directory
sys.path.append(str(Path(__file__).parent.parent))

from lib.kilocode_config_simple import load_config, ConfigurationError


class BatchStandardizer:
    """Standardize all papers sequentially"""
    
    def __init__(self):
        # Load configuration
        try:
            self.config = load_config()
            print(f"✓ Kilocode configuration loaded")
        except ConfigurationError as e:
            print(f"❌ Failed to load configuration: {e}")
            sys.exit(1)
        
        # SSL context
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        # Load CSV data
        self.csv_data = self.load_csv_data()
        
        # Progress tracking
        self.progress_file = "standardization_progress.json"
        self.progress = self.load_progress()
    
    def load_progress(self):
        """Load progress from file"""
        if Path(self.progress_file).exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            "completed": [],
            "failed": {},
            "started": datetime.now().isoformat()
        }
    
    def save_progress(self):
        """Save progress to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def load_csv_data(self):
        """Load CSV data"""
        csv_data = {}
        csv_path = "hdm_research_papers_merged_20250710.csv"
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cite_key = row.get('cite_key', '').strip()
                if cite_key:
                    csv_data[cite_key] = row
        
        print(f"✓ Loaded {len(csv_data)} papers from CSV")
        return csv_data
    
    def call_gemini_api(self, prompt, max_retries=3):
        """Call Gemini API with retry logic"""
        url = self.config.openrouter_url + "/chat/completions"
        
        for attempt in range(max_retries):
            try:
                data = {
                    "model": "google/gemini-2.5-pro-preview",
                    "messages": [
                        {"role": "system", "content": "You are an expert academic paper formatter. Preserve ALL content."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 50000
                }
                
                headers = {
                    "Authorization": f"Bearer {self.config.token}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": self.config.http_referer,
                    "X-Title": self.config.x_title
                }
                
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode('utf-8'),
                    headers=headers,
                    method='POST'
                )
                
                with urllib.request.urlopen(req, context=self.ssl_context, timeout=90) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    return result['choices'][0]['message']['content']
            
            except Exception as e:
                print(f"  ⚠️  Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
        
        return None
    
    def create_standardization_prompt(self, content, csv_row, cite_key):
        """Create standardization prompt"""
        # Parse tags from DOI field
        tags = []
        if csv_row.get('DOI'):
            tags = [t.strip() for t in csv_row['DOI'].split(',') if t.strip()][:15]
        
        return f"""Standardize this academic paper while preserving ALL original content.

CSV DATA:
Title: {csv_row.get('title', '')}
Authors: {csv_row.get('authors', '')}
Year: {csv_row.get('year', '')}
Relevancy: {csv_row.get('Relevancy', 'HIGH')}
TL;DR: {csv_row.get('TL;DR', '')}
Insights: {csv_row.get('Insights', '')}

CURRENT PAPER:
{content}

INSTRUCTIONS:
1. Update YAML frontmatter:
   - Remove images_total, images_kept, images_removed fields
   - Add standardization_date: {datetime.now().strftime('%Y-%m-%d')}
   - Add standardization_version: 1.0
   
2. After Abstract, add:
   ## TL;DR
   {csv_row.get('TL;DR', '')}
   
   ## Key Insights
   {csv_row.get('Insights', '')}

3. At the very end, add:
   ## Metadata Summary
   ### Research Context
   - **Research Question**: {csv_row.get('Research Question', 'Not available')}
   - **Methodology**: {csv_row.get('Methodology', 'Not available')}
   - **Key Findings**: {csv_row.get('Key Findings', 'Not available')}
   - **Primary Outcomes**: {csv_row.get('Primary Outcomes', 'Not available')}
   
   ### Analysis
   - **Limitations**: {csv_row.get('Limitations', 'Not available')}
   - **Research Gaps**: {csv_row.get('Research Gaps', 'Not available')}
   - **Future Work**: {csv_row.get('Future Work', 'Not available')}
   - **Conclusion**: {csv_row.get('Conclusion', 'Not available')}
   
   ### Implementation Notes
   {csv_row.get('Implementation Insights', 'Not available')}

4. PRESERVE ALL OTHER CONTENT EXACTLY AS IS

Return the complete standardized paper."""
    
    def standardize_paper(self, cite_key):
        """Standardize a single paper"""
        paper_path = Path(f"markdown_papers/{cite_key}/paper.md")
        
        if not paper_path.exists():
            print(f"❌ Paper not found: {paper_path}")
            return False
        
        # Get CSV data
        csv_row = self.csv_data.get(cite_key, {})
        if not csv_row:
            print(f"⚠️  No CSV data for {cite_key}")
        
        # Read content
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"  📄 Read {len(content)} chars")
        
        # Skip very large papers for now
        if len(content) > 40000:
            print(f"  ⏭️  Skipping large paper (will process later)")
            return False
        
        # Create backup
        backup_dir = Path(f"paper_backups/{cite_key}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / f"paper_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Call API
        print(f"  🤖 Calling Gemini API...")
        prompt = self.create_standardization_prompt(content, csv_row, cite_key)
        standardized = self.call_gemini_api(prompt)
        
        if not standardized:
            print(f"  ❌ API call failed")
            return False
        
        # Clean response
        if standardized.startswith('```markdown'):
            standardized = standardized[11:]
        if standardized.endswith('```'):
            standardized = standardized[:-3]
        standardized = standardized.strip()
        
        # Save standardized version
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(standardized)
        
        print(f"  ✅ Standardized and replaced paper.md")
        return True
    
    def get_papers_to_process(self):
        """Get list of papers to process"""
        all_papers = []
        papers_dir = Path("markdown_papers")
        
        for paper_dir in papers_dir.iterdir():
            if paper_dir.is_dir() and (paper_dir / "paper.md").exists():
                cite_key = paper_dir.name
                if cite_key not in self.progress["completed"] and cite_key not in self.progress["failed"]:
                    all_papers.append(cite_key)
        
        # Sort by file size (process smaller papers first)
        papers_with_size = []
        for cite_key in all_papers:
            paper_path = papers_dir / cite_key / "paper.md"
            size = paper_path.stat().st_size
            papers_with_size.append((cite_key, size))
        
        papers_with_size.sort(key=lambda x: x[1])
        return [p[0] for p in papers_with_size]
    
    def run(self, limit=None):
        """Run batch standardization"""
        papers = self.get_papers_to_process()
        
        if limit:
            papers = papers[:limit]
        
        print(f"\n{'='*60}")
        print(f"Starting batch standardization")
        print(f"Papers to process: {len(papers)}")
        print(f"Already completed: {len(self.progress['completed'])}")
        print(f"Failed: {len(self.progress['failed'])}")
        print(f"{'='*60}\n")
        
        for i, cite_key in enumerate(papers, 1):
            print(f"\n[{i}/{len(papers)}] Processing {cite_key}")
            
            try:
                success = self.standardize_paper(cite_key)
                
                if success:
                    self.progress["completed"].append(cite_key)
                    self.save_progress()
                else:
                    self.progress["failed"][cite_key] = "Processing failed"
                    self.save_progress()
                
                # Brief pause between papers
                time.sleep(2)
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                self.progress["failed"][cite_key] = str(e)
                self.save_progress()
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"Batch standardization complete!")
        print(f"Total processed: {len(self.progress['completed'])}")
        print(f"Failed: {len(self.progress['failed'])}")
        print(f"{'='*60}")
        
        if self.progress["failed"]:
            print("\nFailed papers:")
            for cite_key, error in self.progress["failed"].items():
                print(f"  - {cite_key}: {error}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch standardize papers")
    parser.add_argument("--limit", type=int, help="Limit number of papers to process")
    parser.add_argument("--reset", action="store_true", help="Reset progress and start fresh")
    
    args = parser.parse_args()
    
    if args.reset and Path("standardization_progress.json").exists():
        os.remove("standardization_progress.json")
        print("Progress reset!")
    
    standardizer = BatchStandardizer()
    standardizer.run(limit=args.limit)


if __name__ == "__main__":
    main()
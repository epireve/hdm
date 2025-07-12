#!/usr/bin/env python3
"""
Minimal Paper.md Standardizer - No external dependencies
Uses Kilocode API with standard library only
"""

import sys
import json
import csv
import urllib.request
import urllib.error
import ssl
import argparse
from pathlib import Path
from datetime import datetime
import time
import re

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import Kilocode configuration
from lib.kilocode_config_simple import load_config, ConfigurationError


class MinimalStandardizer:
    """Minimal paper standardizer using only standard library"""
    
    def __init__(self, csv_path: str, dry_run: bool = False):
        self.csv_path = Path(csv_path)
        self.dry_run = dry_run
        self.backup_dir = Path(f"paper_backups_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # Load configuration
        try:
            self.config = load_config()
            print(f"✓ Kilocode configuration loaded")
        except ConfigurationError as e:
            print(f"❌ Failed to load configuration: {e}")
            sys.exit(1)
        
        # SSL context for API calls
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        # Load CSV data
        self.csv_data = self.load_csv_data()
        
        # Report
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "csv_file": str(self.csv_path),
            "dry_run": self.dry_run,
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
            sys.exit(1)
    
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
                if line.startswith('  - '):
                    if current_list is not None:
                        metadata[current_list].append(line[4:].strip())
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
    
    def call_gemini_api(self, prompt):
        """Call Gemini API using urllib"""
        url = self.config.openrouter_url + "/chat/completions"
        
        data = {
            "model": self.config.default_model,
            "messages": [
                {"role": "system", "content": "You are an expert academic paper formatter."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 32000
        }
        
        headers = {
            "Authorization": f"Bearer {self.config.token}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.config.http_referer,
            "X-Title": self.config.x_title
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req, context=self.ssl_context) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']
        
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ API error {e.code}: {error_body}")
            return None
        except Exception as e:
            print(f"❌ Error calling API: {e}")
            return None
    
    def create_prompt(self, content, csv_row):
        """Create standardization prompt"""
        # Truncate content if too long (keep beginning and end)
        max_content_length = 20000
        if len(content) > max_content_length:
            half = max_content_length // 2
            content = content[:half] + "\n\n[... CONTENT TRUNCATED FOR API LIMITS ...]\n\n" + content[-half:]
        
        prompt = f"""Standardize this academic paper while preserving ALL original content.

CSV METADATA:
Title: {csv_row.get('title', 'N/A')}
Authors: {csv_row.get('authors', 'N/A')}
Year: {csv_row.get('year', 'N/A')}
DOI: {csv_row.get('DOI', 'N/A')}
URL: {csv_row.get('url', 'N/A')}
Relevancy: {csv_row.get('Relevancy', 'N/A')}
Tags: {csv_row.get('Tags', 'N/A')}
TL;DR: {csv_row.get('TL;DR', 'N/A')}
Insights: {csv_row.get('Insights', 'N/A')}

CURRENT PAPER:
{content}

OUTPUT FORMAT:
---
cite_key: [preserve from original]
title: [from CSV]
authors: [from CSV]
year: [from CSV]
doi: [from CSV]
url: [from CSV]
relevancy: [from CSV]
relevancy_justification: [from CSV]
tags:
  - [parse CSV tags]
date_processed: [preserve if exists]
standardization_date: {datetime.now().strftime('%Y-%m-%d')}
---

# [Title]

## Authors
[formatted authors]

## Abstract
[original abstract]

## TL;DR
[from CSV]

## Key Insights
[from CSV Insights]

[Original sections numbered 1, 2, 3...]

## References
[original references]

## Metadata Summary
### Research Context
- **Research Question**: [from CSV]
- **Methodology**: [from CSV]
- **Key Findings**: [from CSV]

Return ONLY the standardized markdown."""
        
        return prompt
    
    def process_paper(self, paper_path):
        """Process a single paper"""
        cite_key = paper_path.parent.name
        print(f"\n📄 Processing: {cite_key}")
        
        result = {
            "cite_key": cite_key,
            "path": str(paper_path),
            "status": "pending"
        }
        
        try:
            # Get CSV data
            csv_row = self.csv_data.get(cite_key, {})
            if not csv_row:
                print(f"  ⚠️  No CSV data found")
            
            # Read content
            with open(paper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"  ✓ Read {len(content)} characters")
            
            # Create backup
            if not self.dry_run:
                backup_path = self.backup_dir / cite_key / "paper.md"
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                backup_path.write_text(content, encoding='utf-8')
                print(f"  ✓ Backup created")
            
            # Call API
            print(f"  🤖 Calling Gemini API...")
            prompt = self.create_prompt(content, csv_row)
            standardized = self.call_gemini_api(prompt)
            
            if not standardized:
                result["status"] = "failed"
                result["error"] = "API call failed"
                return result
            
            print(f"  ✓ Received {len(standardized)} characters")
            
            # Save if not dry run
            if not self.dry_run:
                with open(paper_path, 'w', encoding='utf-8') as f:
                    f.write(standardized)
                print(f"  ✓ Saved standardized version")
            else:
                print(f"  ✓ DRY RUN - would save {len(standardized)} characters")
            
            result["status"] = "success"
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            print(f"  ❌ Error: {e}")
        
        return result
    
    def run(self, papers):
        """Run standardization on specified papers"""
        print(f"\n🚀 Starting standardization (dry_run={self.dry_run})")
        
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
        
        print(f"📚 Found {len(paper_paths)} papers to process")
        
        # Process each paper
        for i, path in enumerate(paper_paths, 1):
            print(f"\n[{i}/{len(paper_paths)}]", end="")
            result = self.process_paper(path)
            self.report["papers"][result["cite_key"]] = result
            
            # Rate limiting
            if i < len(paper_paths):
                time.sleep(2)
        
        # Save report
        report_path = f"standardization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(self.report, f, indent=2)
        
        # Summary
        print(f"\n\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        successful = sum(1 for p in self.report["papers"].values() if p["status"] == "success")
        failed = sum(1 for p in self.report["papers"].values() if p["status"] == "failed")
        print(f"✓ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        if not self.dry_run:
            print(f"📁 Backups: {self.backup_dir}")
        print(f"📊 Report: {report_path}")
        print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Minimal paper standardizer")
    parser.add_argument("--papers", nargs="+", required=True, help="Paper cite_keys to process")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    parser.add_argument("--csv", default="hdm_research_papers_merged_20250710.csv", help="CSV file")
    
    args = parser.parse_args()
    
    standardizer = MinimalStandardizer(args.csv, args.dry_run)
    standardizer.run(args.papers)


if __name__ == "__main__":
    main()
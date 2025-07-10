#!/usr/bin/env python3
"""
Process a single paper and show the actual result
"""

import sys
import json
import csv
import urllib.request
import urllib.error
import ssl
from pathlib import Path
from datetime import datetime
import re
import time

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import Kilocode configuration
from lib.kilocode_config_simple import load_config, ConfigurationError


class SinglePaperProcessor:
    """Process a single paper with Gemini API"""
    
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
    
    def call_gemini_api(self, prompt):
        """Call Gemini API"""
        url = self.config.openrouter_url + "/chat/completions"
        
        data = {
            "model": "google/gemini-2.5-pro-preview",
            "messages": [
                {"role": "system", "content": "You are an expert academic paper formatter. Respond ONLY with the formatted markdown, no explanations."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 50000
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
            
            print("  🤖 Calling Gemini API...")
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result['choices'][0]['message']['content']
                
                # Show token usage
                if 'usage' in result:
                    usage = result['usage']
                    print(f"  📊 Tokens - Input: {usage.get('prompt_tokens', 0)}, Output: {usage.get('completion_tokens', 0)}")
                
                return content
        
        except Exception as e:
            print(f"❌ API error: {e}")
            return None
    
    def create_standardization_prompt(self, content, csv_row, cite_key):
        """Create a focused prompt for standardization"""
        
        # Parse tags properly
        tags = []
        # The DOI field seems to contain tags based on our discovery
        if csv_row.get('DOI'):
            tags = [t.strip() for t in csv_row['DOI'].split(',') if t.strip()]
        elif csv_row.get('Tags'):
            tags = [t.strip() for t in csv_row['Tags'].split(',') if t.strip()]
        
        # The URL field contains what looks like a DOI
        doi = csv_row.get('url', '')
        if doi.startswith('10.'):
            url = f"https://doi.org/{doi}"
        else:
            url = csv_row.get('url', '')
            doi = ''
        
        prompt = f"""Standardize this academic paper into the exact format below. Preserve ALL original content.

CSV DATA:
Title: {csv_row.get('title', '')}
Authors: {csv_row.get('authors', '')}
Year: {csv_row.get('year', '')}
DOI: {doi}
URL: {url}
Relevancy: {csv_row.get('Relevancy', '')}
Relevancy Justification: {csv_row.get('Relevancy Justification', '')}
TL;DR: {csv_row.get('TL;DR', '')}
Insights: {csv_row.get('Insights', '')}
Research Question: {csv_row.get('Research Question', '')}
Methodology: {csv_row.get('Methodology', '')}
Key Findings: {csv_row.get('Key Findings', '')}
Primary Outcomes: {csv_row.get('Primary Outcomes', '')}
Limitations: {csv_row.get('Limitations', '')}
Conclusion: {csv_row.get('Conclusion', '')}
Research Gaps: {csv_row.get('Research Gaps', '')}
Future Work: {csv_row.get('Future Work', '')}
Implementation Insights: {csv_row.get('Implementation Insights', '')}

CURRENT PAPER (first 5000 chars):
{content[:5000]}

[... rest of paper ...]

REQUIRED FORMAT:
---
cite_key: {cite_key}
title: [from CSV]
authors: [from CSV]
year: [from CSV]
doi: [from CSV or parse from URL]
url: [from CSV]
relevancy: [from CSV]
relevancy_justification: [from CSV]
tags:
{chr(10).join(f'  - {tag}' for tag in tags[:10])}
date_processed: [preserve if exists in original]
phase2_processed: [preserve if exists in original]
standardization_date: {datetime.now().strftime('%Y-%m-%d')}
standardization_version: 1.0
word_count: [estimate]
sections_count: [count ## headers]
---

# [Title from CSV]

## Authors
[Format authors from CSV nicely]

## Abstract
[PRESERVE ORIGINAL ABSTRACT EXACTLY]

## TL;DR
[From CSV]

## Key Insights
[From CSV Insights]

[PRESERVE ALL ORIGINAL SECTIONS WITH THEIR CONTENT]

## References
[PRESERVE ORIGINAL REFERENCES]

## Metadata Summary
### Research Context
- **Research Question**: [from CSV]
- **Methodology**: [from CSV]
- **Key Findings**: [from CSV]
- **Primary Outcomes**: [from CSV]

### Analysis
- **Limitations**: [from CSV]
- **Research Gaps**: [from CSV]
- **Future Work**: [from CSV]
- **Conclusion**: [from CSV]

### Implementation Notes
[From CSV Implementation Insights]

Return ONLY the formatted markdown."""
        
        return prompt
    
    def process_paper(self, cite_key):
        """Process a single paper"""
        print(f"\n{'='*60}")
        print(f"Processing: {cite_key}")
        print(f"{'='*60}")
        
        # Check if paper exists
        paper_path = Path(f"markdown_papers/{cite_key}/paper.md")
        if not paper_path.exists():
            print(f"❌ Paper not found: {paper_path}")
            return False
        
        # Get CSV data
        csv_row = self.csv_data.get(cite_key, {})
        if not csv_row:
            print(f"❌ No CSV data for {cite_key}")
            return False
        
        # Read original content
        with open(paper_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        print(f"✓ Read {len(original_content)} characters")
        
        # Create backup
        backup_path = Path(f"backup_{cite_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"✓ Backup saved to: {backup_path}")
        
        # Create prompt and call API
        prompt = self.create_standardization_prompt(original_content, csv_row, cite_key)
        standardized_content = self.call_gemini_api(prompt)
        
        if not standardized_content:
            print("❌ Failed to get response from API")
            return False
        
        # Save standardized version
        output_path = Path(f"standardized_{cite_key}.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(standardized_content)
        
        print(f"✓ Standardized version saved to: {output_path}")
        
        # Show preview of the result
        print(f"\n📄 Preview of standardized content (first 1000 chars):")
        print("-" * 60)
        print(standardized_content[:1000])
        print("-" * 60)
        
        return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Process and standardize a single paper")
    parser.add_argument("cite_key", help="Paper cite_key to process")
    
    args = parser.parse_args()
    
    processor = SinglePaperProcessor()
    success = processor.process_paper(args.cite_key)
    
    if success:
        print(f"\n✅ Successfully processed {args.cite_key}")
        print(f"Check the file: standardized_{args.cite_key}.md")
    else:
        print(f"\n❌ Failed to process {args.cite_key}")


if __name__ == "__main__":
    main()
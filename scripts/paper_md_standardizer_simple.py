#!/usr/bin/env python3
"""
Simplified Paper.md Standardizer using Gemini 2.5 Pro via Kilocode API
Version without external dependencies (no tqdm, uses basic yaml parsing)
"""

import os
import sys
import json
import csv
import logging
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time
import re

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import Kilocode configuration
from lib.kilocode_config_simple import load_config, ConfigurationError

# Try to import OpenAI client
try:
    from openai import OpenAI
except ImportError:
    print("Error: OpenAI library not installed. Please run: pip install openai")
    sys.exit(1)


class SimpleYAMLParser:
    """Simple YAML parser for frontmatter"""
    
    @staticmethod
    def parse(yaml_content: str) -> Dict:
        """Parse simple YAML frontmatter"""
        result = {}
        current_list = None
        current_list_key = None
        
        for line in yaml_content.split('\n'):
            line = line.rstrip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Handle list items
            if line.startswith('  - '):
                if current_list is not None:
                    current_list.append(line[4:].strip())
                continue
            
            # End list if we're back to regular key
            if current_list is not None and not line.startswith(' '):
                result[current_list_key] = current_list
                current_list = None
                current_list_key = None
            
            # Parse key: value
            if ':' in line and not line.startswith(' '):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Check if this starts a list
                if not value:
                    current_list = []
                    current_list_key = key
                else:
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    result[key] = value
        
        # Don't forget the last list
        if current_list is not None:
            result[current_list_key] = current_list
        
        return result


class PaperStandardizer:
    """Handles comprehensive standardization of paper.md files"""
    
    def __init__(self, csv_path: str, dry_run: bool = False, batch_size: int = 5):
        self.csv_path = Path(csv_path)
        self.dry_run = dry_run
        self.batch_size = batch_size
        self.backup_dir = Path(f"paper_backups_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # Setup logging
        self.setup_logging()
        
        # Load configuration
        try:
            self.config = load_config()
            self.logger.info("Kilocode configuration loaded successfully")
        except ConfigurationError as e:
            self.logger.error(f"Failed to load configuration: {e}")
            sys.exit(1)
        
        # Initialize OpenAI client with Kilocode
        self.client = OpenAI(
            base_url=self.config.openrouter_url,
            api_key=self.config.token,
            default_headers={
                "HTTP-Referer": self.config.http_referer,
                "X-Title": self.config.x_title,
            }
        )
        
        # Load CSV data
        self.csv_data = self.load_csv_data()
        
        # Statistics
        self.stats = {
            "total_papers": 0,
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "validation_warnings": 0
        }
        
        # Processing report
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "csv_file": str(self.csv_path),
            "dry_run": self.dry_run,
            "papers": {}
        }
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(log_format))
        
        # File handler
        file_handler = logging.FileHandler('standardization_errors.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(log_format))
        
        # Setup logger
        self.logger = logging.getLogger('PaperStandardizer')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def load_csv_data(self) -> Dict[str, Dict]:
        """Load CSV data into memory for validation"""
        csv_data = {}
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cite_key = row.get('cite_key', '').strip()
                    if cite_key:
                        csv_data[cite_key] = row
            
            self.logger.info(f"Loaded {len(csv_data)} papers from CSV")
            return csv_data
        
        except Exception as e:
            self.logger.error(f"Failed to load CSV: {e}")
            sys.exit(1)
    
    def find_all_papers(self) -> List[Path]:
        """Find all paper.md files in markdown_papers directory"""
        papers_dir = Path("markdown_papers")
        if not papers_dir.exists():
            self.logger.error("markdown_papers directory not found")
            return []
        
        papers = list(papers_dir.glob("*/paper.md"))
        self.logger.info(f"Found {len(papers)} paper.md files")
        return papers
    
    def extract_yaml_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Extract YAML frontmatter and remaining content"""
        if not content.startswith('---'):
            return {}, content
        
        try:
            # Find the closing ---
            end_match = re.search(r'\n---\s*\n', content[3:])
            if not end_match:
                return {}, content
            
            yaml_content = content[3:end_match.start() + 3]
            remaining_content = content[end_match.end() + 3:]
            
            # Parse YAML using simple parser
            metadata = SimpleYAMLParser.parse(yaml_content)
            return metadata, remaining_content
        
        except Exception as e:
            self.logger.warning(f"Failed to parse YAML frontmatter: {e}")
            return {}, content
    
    def create_backup(self, paper_path: Path) -> bool:
        """Create backup of original paper"""
        if self.dry_run:
            return True
        
        try:
            # Create backup directory structure
            relative_path = paper_path.parent.name
            backup_path = self.backup_dir / relative_path / "paper.md"
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(paper_path, backup_path)
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to backup {paper_path}: {e}")
            return False
    
    def create_standardization_prompt(self, content: str, csv_row: Dict) -> str:
        """Create prompt for Gemini to standardize the paper"""
        prompt = f"""You are a meticulous academic paper standardizer. Your task is to reorganize the given paper content into a standardized format while preserving ALL original content.

CRITICAL REQUIREMENTS:
1. Preserve ALL original text content - do not remove or summarize any information
2. Only reorganize and reformat the content
3. Maintain academic integrity and accuracy
4. Fix formatting issues (e.g., broken references, inconsistent headers)

CSV METADATA FOR THIS PAPER:
Title: {csv_row.get('title', 'N/A')}
Authors: {csv_row.get('authors', 'N/A')}
Year: {csv_row.get('year', 'N/A')}
DOI: {csv_row.get('DOI', 'N/A')}
URL: {csv_row.get('url', 'N/A')}
Relevancy: {csv_row.get('Relevancy', 'N/A')}
Relevancy Justification: {csv_row.get('Relevancy Justification', 'N/A')}
Tags: {csv_row.get('Tags', 'N/A')}
TL;DR: {csv_row.get('TL;DR', 'N/A')}
Insights: {csv_row.get('Insights', 'N/A')}
Summary: {csv_row.get('Summary', 'N/A')}
Research Question: {csv_row.get('Research Question', 'N/A')}
Methodology: {csv_row.get('Methodology', 'N/A')}
Key Findings: {csv_row.get('Key Findings', 'N/A')}
Primary Outcomes: {csv_row.get('Primary Outcomes', 'N/A')}
Limitations: {csv_row.get('Limitations', 'N/A')}
Conclusion: {csv_row.get('Conclusion', 'N/A')}
Research Gaps: {csv_row.get('Research Gaps', 'N/A')}
Future Work: {csv_row.get('Future Work', 'N/A')}
Implementation Insights: {csv_row.get('Implementation Insights', 'N/A')}

CURRENT PAPER CONTENT:
{content}

REQUIRED OUTPUT FORMAT:
```markdown
---
# Core Metadata (validate against CSV)
cite_key: [keep existing cite_key from frontmatter]
title: [from CSV or existing]
authors: [from CSV or existing]
year: [from CSV or existing]
doi: [from CSV or existing]
url: [from CSV or existing]

# Relevancy & Classification
relevancy: [from CSV]
relevancy_justification: [from CSV]
tags:
  - [parse from CSV Tags field, one per line]

# Processing Metadata
date_processed: [keep existing if present]
phase2_processed: [keep existing if present]
standardization_date: {datetime.now().strftime('%Y-%m-%d')}
standardization_version: 1.0

# Document Statistics
word_count: [calculate approximate word count]
sections_count: [count major sections]
---

# [Full Paper Title]

## Authors
[Format authors nicely with affiliations if available in the original content]

## Abstract
[Original abstract content - preserve exactly]

## TL;DR
[From CSV]

## Key Insights
[From CSV Implementation Insights]

## 1. Introduction
[Original introduction content - preserve exactly]

## 2. [Next Section Title]
[Original content - preserve exactly]

[... continue with all sections, maintaining original content ...]

## References
[Original references - fix formatting if needed]

## Metadata Summary
### Research Context
- **Research Question**: [From CSV]
- **Methodology**: [From CSV]
- **Key Findings**: [From CSV]
- **Primary Outcomes**: [From CSV]

### Analysis
- **Limitations**: [From CSV]
- **Research Gaps**: [From CSV]
- **Future Work**: [From CSV]
- **Conclusion**: [From CSV]

### Implementation Notes
[From CSV Implementation Insights, formatted nicely]
```

IMPORTANT NOTES:
1. Extract the existing cite_key from the current frontmatter and preserve it
2. Use CSV data to fill in or validate metadata fields
3. Parse the Tags field from CSV (comma-separated) into a YAML list
4. Count words and sections for statistics
5. Preserve ALL original paper content - just reorganize it
6. Fix any obvious formatting issues (e.g., malformed references, broken lists)
7. If a section doesn't exist in the original, note it as "Not available in original paper"
8. Ensure all YAML is valid and properly formatted

Return ONLY the standardized markdown content, no explanations."""
        
        return prompt
    
    def standardize_paper_with_gemini(self, content: str, csv_row: Dict) -> Optional[str]:
        """Use Gemini to standardize the paper content"""
        try:
            prompt = self.create_standardization_prompt(content, csv_row)
            
            response = self.client.chat.completions.create(
                model="google/gemini-2.5-pro-preview",
                messages=[
                    {"role": "system", "content": "You are an expert academic paper formatter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=32000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            return None
    
    def validate_standardized_content(self, content: str, cite_key: str) -> List[str]:
        """Validate the standardized content"""
        warnings = []
        
        # Check if content has YAML frontmatter
        if not content.startswith('---'):
            warnings.append("Missing YAML frontmatter")
        
        # Extract metadata
        metadata, _ = self.extract_yaml_frontmatter(content)
        
        # Validate required fields
        required_fields = ['cite_key', 'title', 'authors', 'year']
        for field in required_fields:
            if field not in metadata:
                warnings.append(f"Missing required field: {field}")
        
        # Check cite_key matches
        if metadata.get('cite_key') != cite_key:
            warnings.append(f"cite_key mismatch: {metadata.get('cite_key')} vs {cite_key}")
        
        # Check for required sections
        required_sections = ['Abstract', 'TL;DR', 'Key Insights', 'References', 'Metadata Summary']
        for section in required_sections:
            if f"## {section}" not in content:
                warnings.append(f"Missing section: {section}")
        
        return warnings
    
    def process_paper(self, paper_path: Path) -> Dict:
        """Process a single paper"""
        result = {
            "path": str(paper_path),
            "status": "pending",
            "warnings": [],
            "error": None
        }
        
        try:
            # Extract cite_key from folder name
            cite_key = paper_path.parent.name
            result["cite_key"] = cite_key
            
            # Get CSV data
            csv_row = self.csv_data.get(cite_key, {})
            if not csv_row:
                result["warnings"].append("No CSV data found for this paper")
                self.logger.warning(f"No CSV data for {cite_key}")
            
            # Read current content
            with open(paper_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            # Create backup
            if not self.create_backup(paper_path):
                result["status"] = "failed"
                result["error"] = "Backup creation failed"
                return result
            
            # Standardize with Gemini
            standardized_content = self.standardize_paper_with_gemini(current_content, csv_row)
            
            if not standardized_content:
                result["status"] = "failed"
                result["error"] = "Gemini standardization failed"
                return result
            
            # Validate
            warnings = self.validate_standardized_content(standardized_content, cite_key)
            result["warnings"].extend(warnings)
            
            if warnings:
                self.stats["validation_warnings"] += 1
            
            # Write standardized content
            if not self.dry_run:
                with open(paper_path, 'w', encoding='utf-8') as f:
                    f.write(standardized_content)
            
            result["status"] = "success"
            self.stats["successful"] += 1
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            self.stats["failed"] += 1
            self.logger.error(f"Failed to process {paper_path}: {e}")
        
        return result
    
    def process_batch(self, papers: List[Path]) -> List[Dict]:
        """Process a batch of papers"""
        results = []
        
        for paper in papers:
            self.logger.info(f"Processing {paper.parent.name}/paper.md")
            result = self.process_paper(paper)
            results.append(result)
            self.stats["processed"] += 1
            
            # Rate limiting
            time.sleep(1)  # Avoid hitting API rate limits
        
        return results
    
    def run(self, specific_papers: Optional[List[str]] = None):
        """Run the standardization process"""
        self.logger.info(f"Starting paper standardization (dry_run={self.dry_run})")
        
        # Find papers
        all_papers = self.find_all_papers()
        
        # Filter specific papers if requested
        if specific_papers:
            papers_to_process = [
                p for p in all_papers 
                if p.parent.name in specific_papers
            ]
        else:
            papers_to_process = all_papers
        
        self.stats["total_papers"] = len(papers_to_process)
        self.logger.info(f"Processing {len(papers_to_process)} papers")
        
        # Create backup directory
        if not self.dry_run:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Process in batches with simple progress display
        total = len(papers_to_process)
        for i in range(0, total, self.batch_size):
            batch = papers_to_process[i:i + self.batch_size]
            batch_end = min(i + self.batch_size, total)
            print(f"\nProcessing papers {i+1}-{batch_end} of {total}")
            
            results = self.process_batch(batch)
            
            # Update report
            for result in results:
                cite_key = result.get("cite_key", "unknown")
                self.report["papers"][cite_key] = result
        
        # Save report
        self.save_report()
        
        # Print summary
        self.print_summary()
    
    def save_report(self):
        """Save processing report"""
        report_path = f"standardization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        self.report["stats"] = self.stats
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2)
        
        self.logger.info(f"Report saved to {report_path}")
    
    def print_summary(self):
        """Print processing summary"""
        print("\n" + "="*60)
        print("STANDARDIZATION SUMMARY")
        print("="*60)
        print(f"Total papers found: {self.stats['total_papers']}")
        print(f"Papers processed: {self.stats['processed']}")
        print(f"Successful: {self.stats['successful']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Validation warnings: {self.stats['validation_warnings']}")
        
        if self.dry_run:
            print("\nDRY RUN - No files were modified")
        else:
            print(f"\nBackups saved to: {self.backup_dir}")
        
        print("="*60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Standardize paper.md files using Gemini 2.5 Pro"
    )
    
    parser.add_argument(
        "--csv",
        default="hdm_research_papers_merged_20250710.csv",
        help="Path to CSV file with paper metadata"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of papers to process in each batch"
    )
    
    parser.add_argument(
        "--papers",
        nargs="+",
        help="Specific paper cite_keys to process"
    )
    
    args = parser.parse_args()
    
    # Create standardizer
    standardizer = PaperStandardizer(
        csv_path=args.csv,
        dry_run=args.dry_run,
        batch_size=args.batch_size
    )
    
    # Run standardization
    standardizer.run(specific_papers=args.papers)


if __name__ == "__main__":
    main()
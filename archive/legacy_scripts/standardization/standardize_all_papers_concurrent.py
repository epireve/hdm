#!/usr/bin/env python3
"""
Concurrent Paper Standardizer with Logging and Resume Capability
Processes all paper.md files in parallel while preserving complete content
"""

import os
import sys
import json
import csv
import logging
import shutil
import argparse
import concurrent.futures
import threading
import time
import re
import urllib.request
import urllib.error
import ssl
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import Kilocode configuration
from lib.kilocode_config_simple import load_config, ConfigurationError

# Thread-safe lock for state updates
state_lock = threading.Lock()

# Global state file
STATE_FILE = "standardization_state.json"


class ConcurrentPaperStandardizer:
    """Handles concurrent standardization of all papers with resume capability"""
    
    def __init__(self, csv_path: str, max_workers: int = 20):
        self.csv_path = Path(csv_path)
        self.max_workers = max_workers
        self.backup_dir = Path(f"paper_backups_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # Setup logging
        self.setup_logging()
        self.logger = logging.getLogger('standardization')
        
        # Load configuration
        try:
            self.config = load_config()
            self.logger.info("Kilocode configuration loaded successfully")
        except ConfigurationError as e:
            self.logger.error(f"Failed to load configuration: {e}")
            sys.exit(1)
        
        # SSL context for API calls
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        # Load CSV data
        self.csv_data = self.load_csv_data()
        
        # Load or initialize state
        self.state = self.load_state()
        
        # Statistics
        self.stats = {
            "start_time": datetime.now().isoformat(),
            "total_papers": 0,
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "api_calls": 0,
            "total_chars_processed": 0
        }
    
    def setup_logging(self):
        """Setup comprehensive logging system"""
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configure different loggers
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Main logger
        main_logger = logging.getLogger('standardization')
        main_logger.setLevel(logging.INFO)
        main_handler = logging.FileHandler(log_dir / 'standardization_main.log')
        main_handler.setFormatter(logging.Formatter(log_format))
        main_logger.addHandler(main_handler)
        
        # Console handler for main logger
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        main_logger.addHandler(console_handler)
        
        # Worker logger
        worker_format = '%(asctime)s - [Worker-%(thread)d] - %(levelname)s - %(message)s'
        worker_logger = logging.getLogger('worker')
        worker_logger.setLevel(logging.DEBUG)
        worker_handler = logging.FileHandler(log_dir / 'standardization_workers.log')
        worker_handler.setFormatter(logging.Formatter(worker_format))
        worker_logger.addHandler(worker_handler)
        
        # Error logger
        error_logger = logging.getLogger('errors')
        error_logger.setLevel(logging.ERROR)
        error_handler = logging.FileHandler(log_dir / 'standardization_errors.log')
        error_handler.setFormatter(logging.Formatter(log_format))
        error_logger.addHandler(error_handler)
        
        # API logger
        api_logger = logging.getLogger('api')
        api_logger.setLevel(logging.DEBUG)
        api_handler = logging.FileHandler(log_dir / 'standardization_api_calls.log')
        api_handler.setFormatter(logging.Formatter(log_format))
        api_logger.addHandler(api_handler)
    
    def load_state(self) -> Dict:
        """Load or initialize processing state"""
        if Path(STATE_FILE).exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                self.logger.info(f"Loaded existing state: {len(state.get('completed', []))} completed")
                return state
            except Exception as e:
                self.logger.error(f"Failed to load state: {e}")
        
        # Initialize new state
        return {
            "start_time": datetime.now().isoformat(),
            "completed": [],
            "failed": {},
            "in_progress": [],
            "last_update": datetime.now().isoformat()
        }
    
    def save_state(self):
        """Save current processing state"""
        with state_lock:
            self.state["last_update"] = datetime.now().isoformat()
            with open(STATE_FILE, 'w') as f:
                json.dump(self.state, f, indent=2)
    
    def update_state_completed(self, cite_key: str):
        """Mark paper as completed"""
        with state_lock:
            if cite_key in self.state["in_progress"]:
                self.state["in_progress"].remove(cite_key)
            if cite_key not in self.state["completed"]:
                self.state["completed"].append(cite_key)
            if cite_key in self.state["failed"]:
                del self.state["failed"][cite_key]
            self.save_state()
    
    def update_state_failed(self, cite_key: str, error: str):
        """Mark paper as failed"""
        with state_lock:
            if cite_key in self.state["in_progress"]:
                self.state["in_progress"].remove(cite_key)
            self.state["failed"][cite_key] = error
            self.save_state()
    
    def update_state_in_progress(self, cite_key: str):
        """Mark paper as in progress"""
        with state_lock:
            if cite_key not in self.state["in_progress"]:
                self.state["in_progress"].append(cite_key)
            self.save_state()
    
    def load_csv_data(self) -> Dict[str, Dict]:
        """Load CSV data into memory"""
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
    
    def get_papers_to_process(self) -> List[str]:
        """Get list of papers that need processing"""
        all_papers = []
        papers_dir = Path("markdown_papers")
        
        if not papers_dir.exists():
            self.logger.error("markdown_papers directory not found")
            return []
        
        # Get all paper cite_keys
        for paper_dir in papers_dir.iterdir():
            if paper_dir.is_dir() and (paper_dir / "paper.md").exists():
                all_papers.append(paper_dir.name)
        
        # Filter out completed papers
        completed = set(self.state.get("completed", []))
        to_process = [p for p in all_papers if p not in completed]
        
        self.logger.info(f"Total papers: {len(all_papers)}, Completed: {len(completed)}, To process: {len(to_process)}")
        
        return to_process
    
    def call_gemini_api(self, prompt: str, worker_id: int) -> Optional[str]:
        """Call Gemini API with logging"""
        api_logger = logging.getLogger('api')
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
            api_logger.debug(f"Worker {worker_id} calling API, prompt length: {len(prompt)}")
            
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result['choices'][0]['message']['content']
                
                # Log token usage
                if 'usage' in result:
                    usage = result['usage']
                    api_logger.info(f"Worker {worker_id} - Tokens: {usage.get('total_tokens', 0)}")
                    self.stats["api_calls"] += 1
                
                return content
        
        except Exception as e:
            api_logger.error(f"Worker {worker_id} API error: {e}")
            return None
    
    def create_backup(self, cite_key: str, content: str) -> Path:
        """Create backup of paper"""
        backup_path = self.backup_dir / cite_key / "paper.md"
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        backup_path.write_text(content, encoding='utf-8')
        return backup_path
    
    def split_at_sections(self, content: str) -> List[Tuple[str, str]]:
        """Split long content at section boundaries"""
        # Find all section headers
        sections = []
        current_section = []
        current_title = "Frontmatter"
        
        lines = content.split('\n')
        for line in lines:
            if line.startswith('## '):
                # Save previous section
                if current_section:
                    sections.append((current_title, '\n'.join(current_section)))
                current_title = line
                current_section = [line]
            else:
                current_section.append(line)
        
        # Don't forget the last section
        if current_section:
            sections.append((current_title, '\n'.join(current_section)))
        
        return sections
    
    def process_long_paper(self, cite_key: str, content: str, csv_row: Dict, worker_id: int) -> Optional[str]:
        """Process a long paper in chunks"""
        worker_logger = logging.getLogger('worker')
        worker_logger.info(f"Processing long paper {cite_key} in chunks")
        
        # Extract frontmatter
        frontmatter_end = content.find('\n---\n', 3)
        if frontmatter_end > 0:
            frontmatter = content[:frontmatter_end + 5]
            body = content[frontmatter_end + 5:]
        else:
            frontmatter = ""
            body = content
        
        # Process in two parts
        mid_point = len(body) // 2
        # Find nearest section break
        section_break = body.rfind('\n## ', 0, mid_point)
        if section_break == -1:
            section_break = mid_point
        
        part1 = frontmatter + body[:section_break]
        part2 = body[section_break:]
        
        # Process first part
        prompt1 = self.create_standardization_prompt(part1, csv_row, cite_key, part=1, total_parts=2)
        result1 = self.call_gemini_api(prompt1, worker_id)
        
        if not result1:
            return None
        
        time.sleep(1)  # Brief pause between API calls
        
        # Process second part
        prompt2 = self.create_standardization_prompt(part2, csv_row, cite_key, part=2, total_parts=2, previous_result=result1)
        result2 = self.call_gemini_api(prompt2, worker_id)
        
        if not result2:
            return None
        
        # Merge results intelligently
        # Remove any markdown wrapper
        if result2.startswith('```markdown'):
            result2 = result2[11:]
        if result2.endswith('```'):
            result2 = result2[:-3]
        
        # Find where to merge (after References usually)
        merge_point = result1.rfind('\n## References')
        if merge_point > 0:
            final_content = result1[:merge_point] + '\n' + result2
        else:
            final_content = result1 + '\n' + result2
        
        return final_content.strip()
    
    def create_standardization_prompt(self, content: str, csv_row: Dict, cite_key: str, 
                                     part: int = 0, total_parts: int = 1, previous_result: str = "") -> str:
        """Create standardization prompt"""
        # Parse tags from DOI field (based on CSV issue discovered)
        tags = []
        if csv_row.get('DOI'):
            tags = [t.strip() for t in csv_row['DOI'].split(',') if t.strip()][:15]
        elif csv_row.get('Tags'):
            tags = [t.strip() for t in csv_row['Tags'].split(',') if t.strip()][:15]
        
        # Fix DOI/URL issue
        doi = csv_row.get('url', '')
        if doi.startswith('10.'):
            url = f"https://doi.org/{doi}"
        else:
            url = csv_row.get('url', '')
            doi = ''
        
        if part == 1 and total_parts > 1:
            prompt = f"""This is PART 1 of 2 of a long paper. Standardize this section and I'll give you the rest next.

CSV DATA:
Title: {csv_row.get('title', '')}
Authors: {csv_row.get('authors', '')}
Year: {csv_row.get('year', '')}
Tags: {', '.join(tags)}

PART 1 CONTENT:
{content}

Format with standard frontmatter and process all content. Return the formatted markdown."""
        
        elif part == 2 and total_parts > 1:
            prompt = f"""This is PART 2 of 2. Continue from where Part 1 ended.

PART 2 CONTENT:
{content}

ADD THESE SECTIONS AT THE END:

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

Return ONLY the content for Part 2 including the metadata sections."""
        
        else:
            # Standard single prompt
            prompt = f"""Standardize this academic paper preserving ALL original content.

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
Tags: {', '.join(tags)}
Research Question: {csv_row.get('Research Question', '')}
Methodology: {csv_row.get('Methodology', '')}
Key Findings: {csv_row.get('Key Findings', '')}
Primary Outcomes: {csv_row.get('Primary Outcomes', '')}
Limitations: {csv_row.get('Limitations', '')}
Conclusion: {csv_row.get('Conclusion', '')}
Research Gaps: {csv_row.get('Research Gaps', '')}
Future Work: {csv_row.get('Future Work', '')}
Implementation Insights: {csv_row.get('Implementation Insights', '')}

CURRENT PAPER:
{content[:50000]}  # Limit to prevent token overflow

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
{chr(10).join(f'  - {tag}' for tag in tags)}
date_processed: [preserve if exists]
phase2_processed: [preserve if exists]
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
    
    def process_paper_worker(self, cite_key: str, worker_id: int) -> Dict:
        """Worker function to process a single paper"""
        worker_logger = logging.getLogger('worker')
        error_logger = logging.getLogger('errors')
        
        worker_logger.info(f"Worker {worker_id} starting {cite_key}")
        self.update_state_in_progress(cite_key)
        
        result = {
            "cite_key": cite_key,
            "status": "pending",
            "worker_id": worker_id,
            "start_time": datetime.now().isoformat()
        }
        
        try:
            # Check if paper exists
            paper_path = Path(f"markdown_papers/{cite_key}/paper.md")
            if not paper_path.exists():
                raise FileNotFoundError(f"Paper not found: {paper_path}")
            
            # Get CSV data
            csv_row = self.csv_data.get(cite_key, {})
            if not csv_row:
                worker_logger.warning(f"No CSV data for {cite_key}")
            
            # Read content
            with open(paper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            worker_logger.info(f"Read {len(content)} chars for {cite_key}")
            self.stats["total_chars_processed"] += len(content)
            
            # Create backup
            backup_path = self.create_backup(cite_key, content)
            worker_logger.info(f"Backup created: {backup_path}")
            
            # Process based on length
            if len(content) > 40000:
                worker_logger.info(f"Long paper detected: {cite_key}")
                standardized = self.process_long_paper(cite_key, content, csv_row, worker_id)
            else:
                prompt = self.create_standardization_prompt(content, csv_row, cite_key)
                standardized = self.call_gemini_api(prompt, worker_id)
            
            if not standardized:
                raise Exception("Failed to get API response")
            
            # Clean response
            if standardized.startswith('```markdown'):
                standardized = standardized[11:]
            if standardized.endswith('```'):
                standardized = standardized[:-3]
            standardized = standardized.strip()
            
            # REPLACE THE ORIGINAL paper.md FILE
            with open(paper_path, 'w', encoding='utf-8') as f:
                f.write(standardized)
            
            worker_logger.info(f"Successfully standardized and replaced {cite_key}/paper.md")
            self.update_state_completed(cite_key)
            
            result["status"] = "success"
            result["end_time"] = datetime.now().isoformat()
            result["chars_processed"] = len(content)
            result["chars_output"] = len(standardized)
            
            self.stats["successful"] += 1
            
        except Exception as e:
            error_logger.error(f"Failed to process {cite_key}: {str(e)}", exc_info=True)
            self.update_state_failed(cite_key, str(e))
            
            result["status"] = "failed"
            result["error"] = str(e)
            result["end_time"] = datetime.now().isoformat()
            
            self.stats["failed"] += 1
        
        finally:
            self.stats["processed"] += 1
        
        return result
    
    def run(self, resume: bool = False):
        """Run the concurrent standardization process"""
        self.logger.info(f"{'Resuming' if resume else 'Starting'} concurrent paper standardization")
        self.logger.info(f"Max workers: {self.max_workers}")
        
        # Get papers to process
        papers_to_process = self.get_papers_to_process()
        self.stats["total_papers"] = len(papers_to_process)
        
        if not papers_to_process:
            self.logger.info("No papers to process!")
            return
        
        # Create backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Backups will be saved to: {self.backup_dir}")
        
        # Process papers concurrently
        self.logger.info(f"Processing {len(papers_to_process)} papers...")
        
        start_time = time.time()
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all papers
            future_to_paper = {}
            for i, cite_key in enumerate(papers_to_process):
                worker_id = i % self.max_workers
                future = executor.submit(self.process_paper_worker, cite_key, worker_id)
                future_to_paper[future] = cite_key
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_paper):
                cite_key = future_to_paper[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Progress update
                    processed = self.stats["processed"]
                    total = self.stats["total_papers"]
                    success = self.stats["successful"]
                    failed = self.stats["failed"]
                    
                    self.logger.info(
                        f"Progress: {processed}/{total} "
                        f"(Success: {success}, Failed: {failed}) "
                        f"- Latest: {cite_key} [{result['status']}]"
                    )
                    
                except Exception as e:
                    self.logger.error(f"Unexpected error for {cite_key}: {e}")
        
        # Calculate statistics
        elapsed_time = time.time() - start_time
        self.stats["elapsed_time"] = elapsed_time
        self.stats["avg_time_per_paper"] = elapsed_time / max(self.stats["processed"], 1)
        
        # Generate final report
        self.generate_final_report(results)
        
        # Clean up state file if all completed
        if self.stats["failed"] == 0:
            if Path(STATE_FILE).exists():
                Path(STATE_FILE).unlink()
                self.logger.info("Removed state file (all papers completed successfully)")
    
    def generate_final_report(self, results: List[Dict]):
        """Generate comprehensive final report"""
        report = {
            "execution_summary": {
                "start_time": self.stats["start_time"],
                "end_time": datetime.now().isoformat(),
                "elapsed_time": self.stats.get("elapsed_time", 0),
                "total_papers": self.stats["total_papers"],
                "processed": self.stats["processed"],
                "successful": self.stats["successful"],
                "failed": self.stats["failed"],
                "api_calls": self.stats["api_calls"],
                "total_chars_processed": self.stats["total_chars_processed"],
                "avg_time_per_paper": self.stats.get("avg_time_per_paper", 0)
            },
            "failed_papers": self.state.get("failed", {}),
            "results": results
        }
        
        # Save detailed report
        report_path = f"standardization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save failed papers list
        if self.state.get("failed"):
            with open("failed_papers.txt", 'w') as f:
                for cite_key, error in self.state["failed"].items():
                    f.write(f"{cite_key}: {error}\n")
        
        # Print summary
        self.logger.info("\n" + "="*60)
        self.logger.info("STANDARDIZATION COMPLETE!")
        self.logger.info("="*60)
        self.logger.info(f"Total papers: {self.stats['total_papers']}")
        self.logger.info(f"Successful: {self.stats['successful']}")
        self.logger.info(f"Failed: {self.stats['failed']}")
        self.logger.info(f"Time elapsed: {self.stats.get('elapsed_time', 0):.1f} seconds")
        self.logger.info(f"Average per paper: {self.stats.get('avg_time_per_paper', 0):.1f} seconds")
        self.logger.info(f"Total API calls: {self.stats['api_calls']}")
        self.logger.info(f"Total characters processed: {self.stats['total_chars_processed']:,}")
        
        if self.state.get("failed"):
            self.logger.info(f"\nFailed papers saved to: failed_papers.txt")
        
        self.logger.info(f"\nDetailed report saved to: {report_path}")
        self.logger.info(f"Backups saved to: {self.backup_dir}")
        self.logger.info(f"Logs saved to: logs/")
        self.logger.info("="*60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Standardize all paper.md files concurrently with resume capability"
    )
    
    parser.add_argument(
        "--csv",
        default="hdm_research_papers_merged_20250710.csv",
        help="Path to CSV file with paper metadata"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=20,
        help="Number of concurrent workers (default: 20)"
    )
    
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from previous state"
    )
    
    args = parser.parse_args()
    
    # Create standardizer
    standardizer = ConcurrentPaperStandardizer(
        csv_path=args.csv,
        max_workers=args.workers
    )
    
    # Run standardization
    standardizer.run(resume=args.resume)


if __name__ == "__main__":
    main()
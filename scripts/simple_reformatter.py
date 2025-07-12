#!/usr/bin/env python3
"""
Simple Paper Reformatter using KiloCode API via requests
Simplified version that doesn't require OpenAI library
"""

import os
import sys
import re
import json
import time
import requests
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Load environment variables manually
def load_env_file(env_path=".env"):
    """Simple .env file loader"""
    env_vars = {}
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"\'')
    except FileNotFoundError:
        pass
    
    # Set environment variables
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value

# Load environment variables
load_env_file("/Users/invoture/dev.local/hdm/.env")

class SimplePaperReformatter:
    """Simplified paper reformatter using KiloCode API via requests"""
    
    REFORMATTING_PROMPT = r"""You are reformatting an academic paper from mixed HTML/Markdown to pure Markdown.

CRITICAL REQUIREMENTS:
1. Convert ALL HTML tags to Markdown:
   - <sup>text</sup> → ^text^
   - <sub>text</sub> → ~text~
   - <span>text</span> → text (remove span tags)
   - <em>text</em> → *text*
   - <strong>text</strong> → **text**
   - <i>text</i> → *text*
   - <b>text</b> → **text**

2. Fix ALL broken references and make them clickable:
   - [[1]](#page-x-y) → [[1]](#ref-1)
   - [1](#page-x-y) → [[1]](#ref-1) 
   - [\[1\]](#page-x-y) → [[1]](#ref-1)
   - Make all citations clickable: [N] → [[N]](#ref-N)
   - Add anchors to references: "N. Author..." → "<a id="ref-N"></a>N. Author..."

3. Remove ANY logo references or descriptions completely
4. Clean up excessive whitespace (max 2 consecutive empty lines)
5. Ensure proper header formatting (# ## ### etc.)
6. Preserve all academic content, figures, tables, and equations
7. Keep all image references like ![image description](filename.jpg)
8. Maintain proper paragraph structure and formatting

OUTPUT REQUIREMENTS:
- Return ONLY the reformatted markdown content
- Do NOT include any frontmatter or metadata
- Do NOT include explanations or comments
- Ensure all references are properly clickable
- Make sure all HTML is converted to proper Markdown

PAPER CONTENT TO REFORMAT:
{paper_content}"""

    def __init__(self, output_dir: Path = None):
        self.base_dir = Path("/Users/invoture/dev.local/hdm")
        self.markdown_dir = self.base_dir / "markdown_papers"
        self.output_dir = output_dir or Path(f"simple_reformatted_papers_{datetime.now():%Y%m%d_%H%M%S}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # KiloCode configuration
        self.token = os.getenv("KILOCODE_TOKEN")
        self.base_url = os.getenv("KILOCODE_BASE_URL", "https://kilocode.ai")
        self.api_url = f"{self.base_url}/api/openrouter/chat/completions"
        self.model = "google/gemini-2.5-flash"
        
        if not self.token:
            raise ValueError("KILOCODE_TOKEN not found in environment variables")
        
        # Setup logging
        self.logger = self._setup_logger()
        self.progress_lock = Lock()
        
        self.logger.info(f"📁 Output directory: {self.output_dir}")
        self.logger.info(f"🤖 Using model: {self.model}")
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger("SimplePaperReformatter")
        logger.setLevel(logging.INFO)
        
        # Console handler
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    def needs_reformatting(self, paper_path: Path) -> Tuple[bool, List[str]]:
        """Check if a paper needs reformatting based on content analysis."""
        try:
            with open(paper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            
            # Check for HTML tags
            html_patterns = [
                r'<sup>.*?</sup>', r'<sub>.*?</sub>', r'<span[^>]*>.*?</span>',
                r'<em>.*?</em>', r'<strong>.*?</strong>', r'<i>.*?</i>', r'<b>.*?</b>'
            ]
            
            for pattern in html_patterns:
                if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                    issues.append("Contains HTML tags")
                    break
            
            # Check for broken references
            broken_ref_patterns = [
                r'\[\[(\d+)\]\]\(#page-\d+-\d+\)',
                r'\[(\d+)\]\(#page-\d+-\d+\)',
                r'\[\\\[(\d+)\\\]\]\(#page-\d+-\d+\)'
            ]
            
            for pattern in broken_ref_patterns:
                if re.search(pattern, content):
                    issues.append("Has broken references")
                    break
            
            # Check for non-clickable references
            citation_pattern = r'\[(\d+)\](?!\(#ref-\d+\))'
            if re.search(citation_pattern, content):
                issues.append("Has non-clickable references")
            
            return len(issues) > 0, issues
            
        except Exception as e:
            self.logger.error(f"Error checking {paper_path}: {e}")
            return False, ["Error reading file"]
    
    def extract_frontmatter_and_content(self, paper_path: Path) -> Tuple[Optional[Dict], str]:
        """Extract YAML frontmatter and content from a markdown file."""
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            return None, content
        
        try:
            # Find the ending ---
            end_match = re.search(r'\n---\n', content[3:])
            if end_match:
                yaml_content = content[3:end_match.start() + 3]
                # Simple frontmatter parsing
                frontmatter = {}
                if yaml_content.strip():
                    for line in yaml_content.strip().split('\n'):
                        if ':' in line and not line.strip().startswith('-'):
                            key, value = line.split(':', 1)
                            frontmatter[key.strip()] = value.strip().strip('"\'')
                
                main_content = content[end_match.end() + 3:]
                return frontmatter, main_content
        except Exception as e:
            self.logger.warning(f"Failed to parse frontmatter: {e}")
        
        return None, content
    
    def call_kilocode_api(self, content: str) -> str:
        """Call KiloCode API to reformat the content."""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://kilocode.ai",
            "X-Title": "HDM Paper Reformatter"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": self.REFORMATTING_PROMPT.format(paper_content=content)
                }
            ],
            "max_tokens": 500000,
            "temperature": 0.1,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=600
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                self.logger.error(f"API Error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"API call failed: {e}")
            return None
    
    def save_with_frontmatter(self, output_path: Path, frontmatter: Optional[Dict], content: str):
        """Save markdown file with YAML frontmatter."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if frontmatter:
                f.write('---\n')
                for key, value in frontmatter.items():
                    f.write(f'{key}: {value}\n')
                f.write('---\n\n')
            f.write(content)
    
    def reformat_paper(self, paper_path: Path) -> Dict[str, Any]:
        """Reformat a single paper."""
        start_time = time.time()
        cite_key = paper_path.parent.name
        
        try:
            # Check if reformatting is needed
            needs_reform, issues = self.needs_reformatting(paper_path)
            if not needs_reform:
                self.logger.info(f"✅ {cite_key}: Already properly formatted")
                return {"success": True, "skipped": True, "cite_key": cite_key}
            
            # Extract frontmatter and content
            frontmatter, content = self.extract_frontmatter_and_content(paper_path)
            
            self.logger.info(f"🔄 {cite_key}: Processing {len(content):,} chars - {', '.join(issues)}")
            
            # Call API for reformatting
            reformatted_content = self.call_kilocode_api(content)
            
            if reformatted_content is None:
                return {"success": False, "error": "API call failed", "cite_key": cite_key}
            
            # Save to output directory
            output_path = self.output_dir / cite_key / "paper.md"
            self.save_with_frontmatter(output_path, frontmatter, reformatted_content)
            
            # Copy images
            source_dir = paper_path.parent
            output_dir = self.output_dir / cite_key
            for image_file in source_dir.glob("*.jpeg"):
                shutil.copy2(image_file, output_dir)
            for image_file in source_dir.glob("*.jpg"):
                shutil.copy2(image_file, output_dir)
            for image_file in source_dir.glob("*.png"):
                shutil.copy2(image_file, output_dir)
            
            processing_time = time.time() - start_time
            chars_per_sec = len(content) / processing_time if processing_time > 0 else 0
            
            self.logger.info(f"✅ {cite_key}: Completed in {processing_time:.1f}s ({chars_per_sec:.0f} chars/sec)")
            
            return {
                "success": True,
                "cite_key": cite_key,
                "processing_time": processing_time,
                "chars_per_sec": chars_per_sec,
                "issues_fixed": issues
            }
            
        except Exception as e:
            self.logger.error(f"❌ {cite_key}: Error - {e}")
            return {"success": False, "error": str(e), "cite_key": cite_key}
    
    def process_papers(self, max_papers: int = None, max_workers: int = 3):
        """Process papers with concurrent workers."""
        # Find all papers
        paper_files = list(self.markdown_dir.glob("*/paper.md"))
        if max_papers:
            paper_files = paper_files[:max_papers]
        
        self.logger.info(f"📚 Found {len(paper_files)} papers to process")
        
        # Quick analysis to see how many need reformatting
        needs_reform_count = 0
        for paper_path in paper_files[:20]:  # Sample first 20
            needs_reform, _ = self.needs_reformatting(paper_path)
            if needs_reform:
                needs_reform_count += 1
        
        self.logger.info(f"🔍 Analysis: {needs_reform_count}/20 sampled papers need reformatting")
        
        # Process papers
        results = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_paper = {
                executor.submit(self.reformat_paper, paper_path): paper_path 
                for paper_path in paper_files
            }
            
            for future in as_completed(future_to_paper):
                result = future.result()
                results.append(result)
                
                if len(results) % 10 == 0:
                    elapsed = time.time() - start_time
                    self.logger.info(f"📊 Progress: {len(results)}/{len(paper_files)} papers processed in {elapsed:.1f}s")
        
        # Generate summary
        successful = sum(1 for r in results if r["success"])
        skipped = sum(1 for r in results if r.get("skipped", False))
        failed = len(results) - successful
        
        total_time = time.time() - start_time
        
        self.logger.info(f"🎉 Processing Complete!")
        self.logger.info(f"   ✅ Successful: {successful}")
        self.logger.info(f"   ⏭️  Skipped: {skipped}")
        self.logger.info(f"   ❌ Failed: {failed}")
        self.logger.info(f"   ⏱️  Total time: {total_time:.1f}s")
        self.logger.info(f"   📁 Output: {self.output_dir}")
        
        # Save results
        with open(self.output_dir / "processing_results.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Paper Reformatter using KiloCode API")
    parser.add_argument("--max-papers", type=int, help="Maximum number of papers to process")
    parser.add_argument("--max-workers", type=int, default=3, help="Number of concurrent workers")
    parser.add_argument("--output-dir", type=Path, help="Output directory")
    parser.add_argument("--test", action="store_true", help="Test mode - process only 3 papers")
    
    args = parser.parse_args()
    
    if args.test:
        args.max_papers = 3
        args.max_workers = 1
    
    reformatter = SimplePaperReformatter(output_dir=args.output_dir)
    reformatter.process_papers(max_papers=args.max_papers, max_workers=args.max_workers)

if __name__ == "__main__":
    main()
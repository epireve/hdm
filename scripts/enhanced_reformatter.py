#!/usr/bin/env python3
"""
Enhanced Paper Reformatter with Correct Author Extraction
Includes intelligent author extraction and cite key correction
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

class EnhancedPaperReformatter:
    """Enhanced paper reformatter with intelligent author extraction and cite key correction"""
    
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

AT THE END, provide author and year information in this exact format:
FIRST_AUTHOR_LASTNAME: [lastname]
YEAR: [year]

Where [lastname] is the last name of the first author and [year] is the publication year.

PAPER CONTENT TO REFORMAT:
{paper_content}"""

    def __init__(self, output_dir: Path = None):
        self.base_dir = Path("/Users/invoture/dev.local/hdm")
        self.markdown_dir = self.base_dir / "markdown_papers"
        self.output_dir = output_dir or Path(f"enhanced_reformatted_papers_{datetime.now():%Y%m%d_%H%M%S}")
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
        
        # Track cite key corrections and uniqueness
        self.cite_key_corrections = {}
        self.used_cite_keys = set()
        
        # Pre-populate used cite keys from existing output directory
        self._populate_existing_cite_keys()
        
        self.logger.info(f"📁 Output directory: {self.output_dir}")
        self.logger.info(f"🤖 Using model: {self.model}")
        self.logger.info(f"🔑 Pre-loaded {len(self.used_cite_keys)} existing cite keys")
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger("EnhancedPaperReformatter")
        logger.setLevel(logging.INFO)
        
        # Console handler
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    def _populate_existing_cite_keys(self):
        """Pre-populate used cite keys from existing output directory and markdown_papers"""
        # Check existing output directory
        if self.output_dir.exists():
            for folder in self.output_dir.iterdir():
                if folder.is_dir():
                    self.used_cite_keys.add(folder.name)
        
        # Also check original markdown_papers directory to avoid conflicts
        if self.markdown_dir.exists():
            for folder in self.markdown_dir.iterdir():
                if folder.is_dir():
                    self.used_cite_keys.add(folder.name)
    
    def extract_authors_from_content(self, content: str) -> List[str]:
        """Extract author names from paper content using multiple patterns"""
        
        # Remove YAML frontmatter first
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
        
        authors = []
        
        # Look for author patterns in the first 3000 characters
        search_content = content[:3000]
        
        # Pattern 1: Standard academic format with emails or affiliations
        # Carlo Humana1, Anton H Bassona2*, Karel Krugera3
        pattern1 = r'([A-Z][a-z]+ [A-Z]\.? ?[A-Z][a-z]+)[\d\*]*'
        matches1 = re.findall(pattern1, search_content)
        
        # Pattern 2: After title, look for author lines
        lines = search_content.split('\n')
        title_found = False
        for i, line in enumerate(lines[:30]):
            # Skip YAML and title
            if line.startswith('#') or 'author' in line.lower():
                title_found = True
                continue
            
            if title_found and line.strip():
                # Look for multiple names in line
                name_matches = re.findall(r'([A-Z][a-z]+ [A-Z]\.? ?[A-Z][a-z]+)', line)
                for match in name_matches:
                    if len(match.split()) >= 2:
                        authors.append(match.strip())
                
                # Stop after finding names or after reasonable number of lines
                if authors or i > 10:
                    break
        
        # Clean and deduplicate
        cleaned_authors = []
        seen = set()
        for author in authors:
            # Clean up
            author = re.sub(r'[\d\*]+$', '', author).strip()
            if len(author.split()) >= 2 and author not in seen and len(author) > 5:
                cleaned_authors.append(author)
                seen.add(author)
                if len(cleaned_authors) >= 5:  # Max 5 authors
                    break
        
        return cleaned_authors
    
    def extract_year_from_content(self, content: str) -> Optional[int]:
        """Extract publication year from paper content"""
        
        search_content = content[:3000]
        
        # Pattern 1: arXiv format
        arxiv_pattern = r'arXiv:\d+\.\d+v?\d*.*?(\d{4})'
        arxiv_match = re.search(arxiv_pattern, search_content)
        if arxiv_match:
            return int(arxiv_match.group(1))
        
        # Pattern 2: Copyright year
        copyright_pattern = r'©\s*(\d{4})'
        copyright_match = re.search(copyright_pattern, search_content)
        if copyright_match:
            return int(copyright_match.group(1))
        
        # Pattern 3: Recent years in content
        year_pattern = r'\b(20[01]\d|19[89]\d)\b'
        year_matches = re.findall(year_pattern, search_content)
        if year_matches:
            years = [int(y) for y in year_matches]
            current_year = datetime.now().year
            valid_years = [y for y in years if 1990 <= y <= current_year]
            if valid_years:
                return max(valid_years)
        
        return None
    
    def generate_cite_key(self, authors: List[str], year: int) -> str:
        """Generate proper cite key from authors and year with uniqueness handling"""
        if not authors:
            base_key = f"unknown_{year}"
        else:
            first_author = authors[0]
            name_parts = first_author.split()
            
            if len(name_parts) >= 2:
                last_name = name_parts[-1].lower()
            else:
                last_name = first_author.lower()
            
            # Clean last name
            last_name = re.sub(r'[^a-z]', '', last_name)
            base_key = f"{last_name}_{year}"
        
        # Ensure uniqueness by appending letters (a, b, c, etc.)
        cite_key = base_key
        suffix = ""
        counter = 0
        
        while cite_key in self.used_cite_keys:
            counter += 1
            suffix = chr(ord('a') + counter - 1)  # a, b, c, d, etc.
            cite_key = f"{base_key}{suffix}"
            
            # Safety check to prevent infinite loop
            if counter > 25:  # z is the 26th letter
                cite_key = f"{base_key}_{counter}"
                break
        
        # Add to used set
        self.used_cite_keys.add(cite_key)
        
        return cite_key
    
    def needs_reformatting(self, paper_path: Path) -> Tuple[bool, List[str]]:
        """Check if a paper needs reformatting"""
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
            "X-Title": "HDM Enhanced Paper Reformatter"
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
    
    def extract_author_info_from_response(self, response_text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract author lastname and year from model response."""
        lines = response_text.strip().split('\n')
        
        lastname = None
        year = None
        
        # Look for the metadata at the end
        for line in reversed(lines[-10:]):  # Check last 10 lines
            if line.startswith("FIRST_AUTHOR_LASTNAME:"):
                lastname = line.split(":", 1)[1].strip()
            elif line.startswith("YEAR:"):
                year = line.split(":", 1)[1].strip()
                
        return lastname, year
    
    def save_with_frontmatter(self, output_path: Path, frontmatter: Optional[Dict], content: str, cite_key: str):
        """Save markdown file with corrected YAML frontmatter."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Update frontmatter with correct cite_key
        if frontmatter:
            frontmatter['cite_key'] = cite_key
        else:
            frontmatter = {'cite_key': cite_key}
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            for key, value in frontmatter.items():
                f.write(f'{key}: {value}\n')
            f.write('---\n\n')
            f.write(content)
    
    def reformat_paper(self, paper_path: Path) -> Dict[str, Any]:
        """Reformat a single paper with enhanced author extraction."""
        start_time = time.time()
        original_cite_key = paper_path.parent.name
        
        try:
            # Check if reformatting is needed
            needs_reform, issues = self.needs_reformatting(paper_path)
            if not needs_reform:
                self.logger.info(f"✅ {original_cite_key}: Already properly formatted")
                return {"success": True, "skipped": True, "cite_key": original_cite_key}
            
            # Extract frontmatter and content
            frontmatter, content = self.extract_frontmatter_and_content(paper_path)
            
            self.logger.info(f"🔄 {original_cite_key}: Processing {len(content):,} chars - {', '.join(issues)}")
            
            # Call API for reformatting with author extraction
            reformatted_content = self.call_kilocode_api(content)
            
            if reformatted_content is None:
                return {"success": False, "error": "API call failed", "cite_key": original_cite_key}
            
            # Extract author info from response
            extracted_lastname, extracted_year = self.extract_author_info_from_response(reformatted_content)
            
            # Generate correct cite key
            if extracted_lastname and extracted_year:
                try:
                    year_int = int(extracted_year)
                    correct_cite_key = f"{extracted_lastname.lower()}_{year_int}"
                    
                    # Track correction if different
                    if correct_cite_key != original_cite_key:
                        self.cite_key_corrections[original_cite_key] = correct_cite_key
                        self.logger.info(f"🔑 {original_cite_key} → {correct_cite_key}")
                except:
                    correct_cite_key = original_cite_key
            else:
                correct_cite_key = original_cite_key
            
            # Clean the reformatted content (remove author extraction lines)
            lines = reformatted_content.split('\n')
            cleaned_lines = []
            for line in lines:
                if not (line.startswith("FIRST_AUTHOR_LASTNAME:") or line.startswith("YEAR:")):
                    cleaned_lines.append(line)
            
            final_content = '\n'.join(cleaned_lines).strip()
            
            # Save to output directory with correct cite key
            output_path = self.output_dir / correct_cite_key / "paper.md"
            self.save_with_frontmatter(output_path, frontmatter, final_content, correct_cite_key)
            
            # Copy images
            source_dir = paper_path.parent
            output_dir = self.output_dir / correct_cite_key
            for image_file in source_dir.glob("*.jpeg"):
                shutil.copy2(image_file, output_dir)
            for image_file in source_dir.glob("*.jpg"):
                shutil.copy2(image_file, output_dir)
            for image_file in source_dir.glob("*.png"):
                shutil.copy2(image_file, output_dir)
            
            processing_time = time.time() - start_time
            chars_per_sec = len(content) / processing_time if processing_time > 0 else 0
            
            self.logger.info(f"✅ {correct_cite_key}: Completed in {processing_time:.1f}s ({chars_per_sec:.0f} chars/sec)")
            
            return {
                "success": True,
                "original_cite_key": original_cite_key,
                "correct_cite_key": correct_cite_key,
                "processing_time": processing_time,
                "chars_per_sec": chars_per_sec,
                "issues_fixed": issues,
                "cite_key_corrected": correct_cite_key != original_cite_key
            }
            
        except Exception as e:
            self.logger.error(f"❌ {original_cite_key}: Error - {e}")
            return {"success": False, "error": str(e), "cite_key": original_cite_key}
    
    def process_papers(self, max_papers: int = None, max_workers: int = 2):
        """Process papers with concurrent workers and enhanced author extraction."""
        # Find all papers
        paper_files = list(self.markdown_dir.glob("*/paper.md"))
        if max_papers:
            paper_files = paper_files[:max_papers]
        
        self.logger.info(f"📚 Found {len(paper_files)} papers to process")
        
        # Process papers
        self._process_paper_list(paper_files, max_workers)
    
    def process_papers_from_list(self, paper_files: List[Path], max_workers: int = 1):
        """Process a specific list of paper files"""
        self.logger.info(f"📚 Processing {len(paper_files)} specific papers")
        self._process_paper_list(paper_files, max_workers)
    
    def _process_paper_list(self, paper_files: List[Path], max_workers: int):
        """Internal method to process a list of papers"""
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
        corrected_cite_keys = sum(1 for r in results if r.get("cite_key_corrected", False))
        failed = len(results) - successful
        
        total_time = time.time() - start_time
        
        self.logger.info(f"🎉 Processing Complete!")
        self.logger.info(f"   ✅ Successful: {successful}")
        self.logger.info(f"   ⏭️  Skipped: {skipped}")
        self.logger.info(f"   🔑 Cite keys corrected: {corrected_cite_keys}")
        self.logger.info(f"   ❌ Failed: {failed}")
        self.logger.info(f"   ⏱️  Total time: {total_time:.1f}s")
        self.logger.info(f"   📁 Output: {self.output_dir}")
        
        # Save results and corrections
        with open(self.output_dir / "processing_results.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        with open(self.output_dir / "cite_key_corrections.json", 'w') as f:
            json.dump(self.cite_key_corrections, f, indent=2)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Paper Reformatter with Author Extraction")
    parser.add_argument("--max-papers", type=int, help="Maximum number of papers to process")
    parser.add_argument("--max-workers", type=int, default=2, help="Number of concurrent workers")
    parser.add_argument("--output-dir", type=Path, help="Output directory")
    parser.add_argument("--test", action="store_true", help="Test mode - process only 3 papers")
    
    args = parser.parse_args()
    
    if args.test:
        args.max_papers = 3
        args.max_workers = 1
    
    reformatter = EnhancedPaperReformatter(output_dir=args.output_dir)
    reformatter.process_papers(max_papers=args.max_papers, max_workers=args.max_workers)

if __name__ == "__main__":
    main()
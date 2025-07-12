#!/usr/bin/env python3
"""
Paper Reformatter Script using KiloCode API
Reformats all paper.md files to fix formatting issues, convert HTML to Markdown,
fix references, and ensure proper cite_key conventions.
"""

import os
import sys
import re
import json
import time
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
try:
    import yaml
except ImportError:
    yaml = None
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import threading

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


@dataclass
class ReformattingResult:
    """Result of reformatting a single paper."""
    success: bool
    paper_path: Path
    original_cite_key: str
    new_cite_key: Optional[str] = None
    folder_renamed: bool = False
    errors: List[str] = None
    changes_made: List[str] = None


class PaperReformatter:
    """Enhanced Paper Reformatter with frontmatter awareness"""
    """Handles reformatting of academic papers using Gemini 2.5 Pro via KiloCode."""
    
    REFORMATTING_PROMPT = r"""You are reformatting an academic paper from mixed HTML/Markdown to pure Markdown.

REQUIREMENTS:
1. Convert ALL HTML tags to Markdown equivalents:
   - <sup>text</sup> → ^text^
   - <sub>text</sub> → ~text~
   - <span> tags → remove tags, keep content
   - <span id="page-x-y"> → remove entirely
   - &lt;, &gt;, &amp; → <, >, &

2. Fix ALL broken references and make them clickable:
   - [[1]](#page-x-y) → [[1]](#ref-1)
   - [\[1\]](#page-x-y) → [[1]](#ref-1)
   - [\\[1\\]](#page-x-y) → [[1]](#ref-1)
   - Remove all #page-x-y anchors
   - Make all citations clickable: [N] → [[N]](#ref-N)
   - Add anchors to references: "N. Author..." → "<a id="ref-N"></a>N. Author..."

3. Standardize formatting:
   - Use proper Markdown headers (# ## ###)
   - Fix broken italic/bold formatting (*italic*, **bold**)
   - Ensure consistent list formatting
   - Preserve mathematical notation
   - Clean up excessive line breaks (\\n\\n\\n → \\n\\n)
   - Ensure proper spacing around headers and sections
   - Format author affiliations consistently with superscripts

4. Remove logo references:
   - Remove any image descriptions mentioning logos
   - Remove "Publisher logo" or similar references
   - Keep actual research content images

5. Extract author information:
   - Find the FIRST AUTHOR's full name (usually appears after title)
   - Extract their LAST NAME only
   - Also note the publication year

IMPORTANT:
- Preserve ALL academic content
- Maintain paper structure
- Keep all citations and references
- Preserve tables and figures
- Do not add any new content
- Return ONLY the reformatted content, no explanations

REFERENCE LINKING:
- In the main text: Convert [1] to [[1]](#ref-1), [23] to [[23]](#ref-23), etc.
- In the References section: Add anchor before each reference
  Example: "1. Smith, J..." becomes "<a id="ref-1"></a>1. Smith, J..."
- This creates clickable links from citations to their references

ADDITIONAL IMPROVEMENTS:
- Format tables properly with markdown table syntax
- Add proper figure captions: **Figure N:** Caption text
- Add proper table captions: **Table N:** Caption text
- Ensure images have alt text in markdown: ![Description](image.jpg)
- Add horizontal rules (---) between major sections if appropriate
- Format equations properly (preserve LaTeX if present)

Paper content to reformat:
{paper_content}

ALSO, at the very end of your response, on a new line, provide:
FIRST_AUTHOR_LASTNAME: [lastname]
YEAR: [year]
"""

    def __init__(self, backup_dir: Path = None, model: str = None, output_dir: Path = None):
        """Initialize the reformatter with KiloCode API."""
        # Load KiloCode configuration
        try:
            self.config = load_config()
            self.logger = self._setup_logger()
            self.logger.info("KiloCode configuration loaded successfully")
        except ConfigurationError as e:
            print(f"Failed to load KiloCode configuration: {e}")
            sys.exit(1)
        
        # Use specified model or default to Gemini 2.5 Flash
        self.model = model or "google/gemini-2.5-flash"
        
        # Initialize OpenAI client with KiloCode
        self.client = OpenAI(
            base_url=self.config.openrouter_url,
            api_key=self.config.token,
            default_headers={
                "HTTP-Referer": self.config.http_referer,
                "X-Title": self.config.x_title,
            }
        )
        
        # Set up directories
        self.backup_dir = backup_dir or Path("backups/paper_reformatter")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Output directory for reformatted papers
        self.output_dir = output_dir or Path(f"reformatted_papers_{datetime.now():%Y%m%d_%H%M%S}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Checkpoint and report files
        self.checkpoint_file = self.output_dir / "reformatting_checkpoint.json"
        self.report_file = self.output_dir / f"reformatting_report_{datetime.now():%Y%m%d_%H%M%S}.json"
        self.progress_file = self.output_dir / "progress.json"
        
        # Thread safety for concurrent processing
        self.checkpoint_lock = Lock()
        self.cite_key_lock = Lock()
        
        self.logger.info(f"Using model: {self.model}")
        self.logger.info(f"API endpoint: {self.config.openrouter_url}")
        self.logger.info(f"📁 Output directory: {self.output_dir}")
        self.logger.info(f"💾 Checkpoint file: {self.checkpoint_file}")
        self.logger.info(f"📊 Progress tracking: {self.progress_file}")
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger("PaperReformatter")
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(f"paper_reformatter_{datetime.now():%Y%m%d_%H%M%S}.log")
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
        
    def load_checkpoint(self) -> Dict[str, Any]:
        """Load processing checkpoint."""
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return {"processed": [], "failed": [], "last_processed": None}
        
    def save_checkpoint(self, checkpoint: Dict[str, Any]):
        """Save processing checkpoint with thread safety."""
        with self.checkpoint_lock:
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint, f, indent=2)
                
    def save_progress(self, progress: Dict[str, Any]):
        """Save real-time progress tracking."""
        with self.checkpoint_lock:
            with open(self.progress_file, 'w') as f:
                json.dump(progress, f, indent=2)
            
    def extract_frontmatter_and_content(self, file_path: Path) -> Tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter and content from a markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for YAML frontmatter
        if content.startswith('---'):
            try:
                # Find the ending ---
                end_match = re.search(r'\n---\n', content[3:])
                if end_match:
                    yaml_content = content[3:end_match.start() + 3]
                    # Handle empty frontmatter
                    if yaml_content.strip():
                        if yaml:
                            frontmatter = yaml.safe_load(yaml_content)
                            if frontmatter is None:
                                frontmatter = {}
                        else:
                            # Simple YAML parsing fallback
                            frontmatter = {}
                            for line in yaml_content.strip().split('\n'):
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    frontmatter[key.strip()] = value.strip().strip('"\'')
                    else:
                        frontmatter = {}
                    main_content = content[end_match.end() + 3:]
                    return frontmatter, main_content
            except Exception as e:
                self.logger.warning(f"Failed to parse YAML frontmatter: {e}")
                
        return {}, content
        
    def save_with_frontmatter(self, file_path: Path, frontmatter: Dict[str, Any], content: str):
        """Save markdown file with YAML frontmatter - preserving all existing metadata."""
        # Build YAML frontmatter preserving ALL existing fields
        yaml_lines = ["---"]
        
        # Priority fields first (if they exist)
        priority_fields = ["cite_key", "title", "authors", "year"]
        
        for field in priority_fields:
            if field in frontmatter:
                value = frontmatter[field]
                # Convert datetime objects to string
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                    
                if isinstance(value, list):
                    yaml_lines.append(f"{field}:")
                    for item in value:
                        # Convert datetime in list items
                        if hasattr(item, 'isoformat'):
                            item = item.isoformat()
                        yaml_lines.append(f"  - {json.dumps(item)}")
                else:
                    yaml_lines.append(f"{field}: {json.dumps(value)}")
                    
        # Add all remaining fields in their original order
        for key, value in frontmatter.items():
            if key not in priority_fields:
                # Convert datetime objects to string
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                    
                if key == "tags" and isinstance(value, list):
                    yaml_lines.append(f"{key}:")
                    for tag in value:
                        if isinstance(tag, str):
                            yaml_lines.append(f'  - "{tag}"')
                        else:
                            yaml_lines.append(f"  - {json.dumps(tag)}")
                elif isinstance(value, list):
                    yaml_lines.append(f"{key}:")
                    for item in value:
                        # Convert datetime in list items
                        if hasattr(item, 'isoformat'):
                            item = item.isoformat()
                        yaml_lines.append(f"  - {json.dumps(item)}")
                else:
                    yaml_lines.append(f"{key}: {json.dumps(value)}")
                    
        yaml_lines.append("---")
        yaml_lines.append("")
        
        # Combine frontmatter and content
        full_content = '\n'.join(yaml_lines) + '\n' + content
        
        # Save file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
            
    def generate_cite_key(self, lastname: str, year: str, existing_keys: set) -> str:
        """Generate a unique cite_key in lastname_year format."""
        # Clean lastname
        lastname = re.sub(r'[^a-zA-Z]', '', lastname).lower()
        base_key = f"{lastname}_{year}"
        
        # Handle duplicates
        if base_key not in existing_keys:
            return base_key
            
        # Add suffix for duplicates
        suffix = 'a'
        while f"{base_key}{suffix}" in existing_keys:
            suffix = chr(ord(suffix) + 1)
            
        return f"{base_key}{suffix}"
    
    def needs_reformatting(self, paper_path: Path) -> Tuple[bool, List[str]]:
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
            # Look for citation patterns that aren't properly linked
            citation_pattern = r'\[(\d+)\](?!\(#ref-\d+\))'
            if re.search(citation_pattern, content):
                issues.append("Has non-clickable references")
            
            # Check for poor formatting (excessive spaces, inconsistent headers, etc.)
            if re.search(r'\n\s*\n\s*\n\s*\n', content):  # More than 2 consecutive empty lines
                issues.append("Has excessive whitespace")
            
            if re.search(r'#{5,}', content):  # Headers with 5+ hash marks
                issues.append("Has malformed headers")
            
            needs_reform = len(issues) > 0
            return needs_reform, issues
            
        except Exception as e:
            self.logger.error(f"Error checking {paper_path}: {e}")
            return False, ["Error reading file"]
        
    def extract_author_info_from_response(self, response_text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract author lastname and year from model response."""
        lines = response_text.strip().split('\n')
        
        lastname = None
        year = None
        
        # Look for the metadata at the end
        for line in reversed(lines[-5:]):  # Check last 5 lines
            if line.startswith("FIRST_AUTHOR_LASTNAME:"):
                lastname = line.split(":", 1)[1].strip()
            elif line.startswith("YEAR:"):
                year = line.split(":", 1)[1].strip()
                
        return lastname, year
        
    def reformat_paper(self, paper_path: Path, existing_keys: set) -> ReformattingResult:
        """Reformat a single paper using KiloCode API."""
        start_time = time.time()
        
        try:
            # Create backup
            backup_path = self.backup_dir / paper_path.parent.name / paper_path.name
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(paper_path, backup_path)
            
            # Extract frontmatter and content
            frontmatter, content = self.extract_frontmatter_and_content(paper_path)
            if frontmatter is None:
                frontmatter = {}
            original_cite_key = frontmatter.get('cite_key', '')
            
            # Send to KiloCode API for reformatting
            prompt = self.REFORMATTING_PROMPT.format(paper_content=content)
            
            # Log content size and estimated processing time
            self.logger.info(f"📄 {paper_path.parent.name}: {len(content):,} chars - Processing with {self.model}")
            
            api_start = time.time()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at reformatting academic papers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500000,  # Support very long papers
                timeout=600  # 10 minute timeout
            )
            api_time = time.time() - api_start
            
            if not response.choices[0].message.content:
                raise Exception("Empty response from API")
                
            response_text = response.choices[0].message.content
            
            # Extract reformatted content and author info
            response_lines = response_text.strip().split('\n')
            
            # Find where the metadata starts (look for FIRST_AUTHOR_LASTNAME)
            metadata_start = -1
            for i in range(len(response_lines) - 1, max(0, len(response_lines) - 10), -1):
                if response_lines[i].startswith("FIRST_AUTHOR_LASTNAME:"):
                    metadata_start = i
                    break
                    
            if metadata_start > 0:
                reformatted_content = '\n'.join(response_lines[:metadata_start])
                extracted_lastname, extracted_year = self.extract_author_info_from_response(
                    '\n'.join(response_lines[metadata_start:])
                )
            else:
                reformatted_content = response_text
                extracted_lastname, extracted_year = None, None
                
            changes_made = []
            
            # Check if HTML was converted
            if '<sup>' in content or '<sub>' in content or '<span' in content:
                changes_made.append("Converted HTML tags to Markdown")
                
            # Check if references were fixed
            if '[[' in content or '\\[' in content or '#page-' in content:
                changes_made.append("Fixed broken references")
                
            # Update cite_key if needed
            new_cite_key = original_cite_key
            folder_renamed = False
            
            if extracted_lastname and extracted_year:
                # Thread-safe cite key operations
                with self.cite_key_lock:
                    # Generate new cite_key
                    potential_key = self.generate_cite_key(extracted_lastname, extracted_year, existing_keys)
                    
                    if potential_key != original_cite_key:
                        new_cite_key = potential_key
                        frontmatter['cite_key'] = new_cite_key
                        changes_made.append(f"Updated cite_key: {original_cite_key} → {new_cite_key}")
                        existing_keys.add(new_cite_key)
                        
                        # Check if folder needs renaming
                        current_folder = paper_path.parent
                        new_folder = current_folder.parent / new_cite_key
                        
                        if current_folder.name != new_cite_key and not new_folder.exists():
                            # Rename folder
                            current_folder.rename(new_folder)
                            paper_path = new_folder / paper_path.name
                            folder_renamed = True
                            changes_made.append(f"Renamed folder: {current_folder.name} → {new_cite_key}")
                        
            # Save reformatted content to output directory
            output_folder = self.output_dir / (new_cite_key if new_cite_key != original_cite_key else paper_path.parent.name)
            output_folder.mkdir(parents=True, exist_ok=True)
            output_path = output_folder / paper_path.name
            
            self.save_with_frontmatter(output_path, frontmatter, reformatted_content)
            
            # Copy images to output directory
            if paper_path.parent.is_dir():
                for img_file in paper_path.parent.glob("*.jpeg"):
                    shutil.copy2(img_file, output_folder)
                for img_file in paper_path.parent.glob("*.jpg"):
                    shutil.copy2(img_file, output_folder)
                for img_file in paper_path.parent.glob("*.png"):
                    shutil.copy2(img_file, output_folder)
            
            # Calculate total processing time and speed
            total_time = time.time() - start_time
            chars_per_sec = len(content) / total_time if total_time > 0 else 0
            
            self.logger.info(f"✅ {paper_path.parent.name}: Completed in {total_time:.1f}s (API: {api_time:.1f}s) - {chars_per_sec:.0f} chars/sec")
            
            return ReformattingResult(
                success=True,
                paper_path=output_path,  # Return output path instead of input path
                original_cite_key=original_cite_key,
                new_cite_key=new_cite_key if new_cite_key != original_cite_key else None,
                folder_renamed=folder_renamed,
                changes_made=changes_made
            )
            
        except Exception as e:
            total_time = time.time() - start_time
            self.logger.error(f"❌ {paper_path.parent.name}: Failed after {total_time:.1f}s - {str(e)}")
            return ReformattingResult(
                success=False,
                paper_path=paper_path,
                original_cite_key=frontmatter.get('cite_key', 'unknown') if frontmatter else 'unknown',
                errors=[str(e)]
            )
            
    def process_paper_with_checkpoint(self, paper_path: Path, existing_keys: set, checkpoint: Dict[str, Any]) -> ReformattingResult:
        """Process a single paper and update checkpoint."""
        result = self.reformat_paper(paper_path, existing_keys)
        
        # Thread-safe checkpoint update
        with self.checkpoint_lock:
            if result.success:
                checkpoint["processed"].append(str(paper_path))
            else:
                checkpoint["failed"].append(str(paper_path))
            checkpoint["last_processed"] = str(paper_path)
            self.save_checkpoint(checkpoint)
            
        return result
    
    def process_all_papers(self, markdown_dir: Path, batch_size: int = 10, max_workers: int = 3, smart_processing: bool = True):
        """Process all papers in the markdown directory with concurrent processing."""
        # Find all paper.md files
        paper_files = list(markdown_dir.glob("*/paper.md"))
        self.logger.info(f"📚 Found {len(paper_files)} total papers")
        
        # Load checkpoint
        checkpoint = self.load_checkpoint()
        processed = set(checkpoint.get("processed", []))
        failed = set(checkpoint.get("failed", []))
        
        # Filter out already processed papers
        remaining_papers = [p for p in paper_files if str(p) not in processed and str(p) not in failed]
        
        # Check which papers actually need reformatting (if smart processing enabled)
        if smart_processing:
            papers_needing_reform = []
            skipped_count = 0
            
            self.logger.info("🔍 Analyzing papers for reformatting needs...")
            for paper_path in remaining_papers:
                needs_reform, issues = self.needs_reformatting(paper_path)
                if needs_reform:
                    papers_needing_reform.append(paper_path)
                    self.logger.debug(f"📄 {paper_path.parent.name}: Needs reformatting - {', '.join(issues)}")
                else:
                    skipped_count += 1
                    self.logger.debug(f"✅ {paper_path.parent.name}: No reformatting needed")
            
            remaining_papers = papers_needing_reform
            
            if skipped_count > 0:
                self.logger.info(f"⏭️  {skipped_count} papers skipped (already properly formatted)")
        else:
            self.logger.info("🔄 Force processing all papers")
        
        if not remaining_papers:
            self.logger.info("✅ All papers already properly formatted!")
            return
            
        self.logger.info(f"🔄 {len(remaining_papers)} papers need reformatting")
        self.logger.info(f"⏭️  {skipped_count} papers skipped (already properly formatted)")
        self.logger.info(f"⚡ Using {max_workers} concurrent workers")
        
        # Collect existing cite_keys
        existing_keys = set()
        for paper_path in paper_files:
            try:
                frontmatter, _ = self.extract_frontmatter_and_content(paper_path)
                if frontmatter and 'cite_key' in frontmatter:
                    existing_keys.add(frontmatter['cite_key'])
            except:
                pass
        
        # Initialize progress tracking
        progress = {
            "session_id": datetime.now().isoformat(),
            "total_papers": len(paper_files),
            "remaining_papers": len(remaining_papers),
            "processed_count": len(processed),
            "failed_count": len(failed),
            "current_batch": 0,
            "total_batches": (len(remaining_papers) + batch_size - 1) // batch_size,
            "status": "processing",
            "start_time": datetime.now().isoformat(),
            "papers_completed": [],
            "papers_failed": []
        }
        self.save_progress(progress)
        
        # Process in concurrent batches
        results = []
        start_time = time.time()
        
        for i in range(0, len(remaining_papers), batch_size):
            batch = remaining_papers[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            self.logger.info(f"🚀 Starting batch {batch_num}/{(len(remaining_papers) + batch_size - 1) // batch_size} ({len(batch)} papers)")
            
            # Process batch concurrently
            batch_start = time.time()
            with ThreadPoolExecutor(max_workers=min(max_workers, len(batch))) as executor:
                # Submit all papers in the batch
                future_to_paper = {
                    executor.submit(self.process_paper_with_checkpoint, paper_path, existing_keys, checkpoint): paper_path
                    for paper_path in batch
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_paper):
                    result = future.result()
                    results.append(result)
                    
            batch_time = time.time() - batch_start
            self.logger.info(f"✅ Batch {batch_num} completed in {batch_time:.1f}s")
            
            # Update progress tracking
            progress["current_batch"] = batch_num
            progress["processed_count"] = len(processed) + len([r for r in results if r.success])
            progress["failed_count"] = len(failed) + len([r for r in results if not r.success])
            
            for result in results[-len(batch):]:  # Only track this batch's results
                if result.success:
                    progress["papers_completed"].append({
                        "paper": str(result.paper_path),
                        "original_cite_key": result.original_cite_key,
                        "new_cite_key": result.new_cite_key,
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    progress["papers_failed"].append({
                        "paper": str(result.paper_path),
                        "errors": result.errors,
                        "timestamp": datetime.now().isoformat()
                    })
            
            self.save_progress(progress)
            
            # Brief pause between batches to avoid API rate limits
            if i + batch_size < len(remaining_papers):
                time.sleep(2)
                
        # Generate final report
        total_time = time.time() - start_time
        progress["status"] = "completed"
        progress["end_time"] = datetime.now().isoformat()
        progress["total_time_seconds"] = total_time
        self.save_progress(progress)
        
        self.logger.info(f"🎉 All processing completed in {total_time:.1f}s")
        self.generate_report(results)
        
    def generate_report(self, results: List[ReformattingResult]):
        """Generate a comprehensive report of the reformatting process."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_processed": len(results),
            "successful": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
            "cite_keys_updated": sum(1 for r in results if r.new_cite_key),
            "folders_renamed": sum(1 for r in results if r.folder_renamed),
            "model_used": self.model,
            "api_endpoint": self.config.openrouter_url,
            "details": []
        }
        
        for result in results:
            detail = {
                "paper": str(result.paper_path),
                "success": result.success,
                "original_cite_key": result.original_cite_key
            }
            
            if result.new_cite_key:
                detail["new_cite_key"] = result.new_cite_key
                
            if result.folder_renamed:
                detail["folder_renamed"] = True
                
            if result.changes_made:
                detail["changes"] = result.changes_made
                
            if result.errors:
                detail["errors"] = result.errors
                
            report["details"].append(detail)
            
        # Save report
        with open(self.report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        self.logger.info(f"Report saved to: {self.report_file}")
        self.logger.info(f"Summary: {report['successful']} successful, {report['failed']} failed")
        self.logger.info(f"Cite keys updated: {report['cite_keys_updated']}")
        self.logger.info(f"Folders renamed: {report['folders_renamed']}")


def main():
    """Main entry point for the paper reformatter."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Reformat academic papers using KiloCode API")
    parser.add_argument("--markdown-dir", type=Path, 
                       default=Path("markdown_papers"),
                       help="Directory containing markdown papers")
    parser.add_argument("--output-dir", type=Path,
                       help="Output directory for reformatted papers (default: auto-generated)")
    parser.add_argument("--batch-size", type=int, default=10,
                       help="Number of papers to process in each batch")
    parser.add_argument("--max-workers", type=int, default=3,
                       help="Number of concurrent workers (default: 3)")
    parser.add_argument("--test", action="store_true",
                       help="Test mode - process only first 3 papers")
    parser.add_argument("--model", type=str, 
                       default="google/gemini-2.5-flash",
                       help="Model to use (default: google/gemini-2.5-flash)")
    parser.add_argument("--smart-processing", action="store_true", 
                       help="Only process papers that need reformatting (default: True)")
    parser.add_argument("--force-all", action="store_true",
                       help="Force process all papers, even if they don't need reformatting")
    
    args = parser.parse_args()
    
    # Initialize reformatter
    reformatter = PaperReformatter(model=args.model, output_dir=args.output_dir)
    
    if args.test:
        # Test mode - process only a few papers
        test_papers = list(args.markdown_dir.glob("*/paper.md"))[:3]
        reformatter.logger.info(f"TEST MODE: Processing {len(test_papers)} papers")
        
        results = []
        existing_keys = set()
        
        for paper_path in test_papers:
            result = reformatter.reformat_paper(paper_path, existing_keys)
            results.append(result)
            time.sleep(1)
            
        reformatter.generate_report(results)
    else:
        # Process all papers with concurrent workers
        smart_processing = not args.force_all  # Use smart processing unless force_all is specified
        reformatter.process_all_papers(args.markdown_dir, args.batch_size, args.max_workers, smart_processing)
        
    return 0


if __name__ == "__main__":
    exit(main())
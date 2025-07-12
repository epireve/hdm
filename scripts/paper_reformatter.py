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
import yaml

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
    """Handles reformatting of academic papers using Gemini 2.5 Pro via KiloCode."""
    
    REFORMATTING_PROMPT = r"""You are reformatting an academic paper from mixed HTML/Markdown to pure Markdown.

REQUIREMENTS:
1. Convert ALL HTML tags to Markdown equivalents:
   - <sup>text</sup> → ^text^
   - <sub>text</sub> → ~text~
   - <span> tags → remove tags, keep content
   - <span id="page-x-y"> → remove entirely
   - &lt;, &gt;, &amp; → <, >, &

2. Fix ALL broken references:
   - [[1]](#page-x-y) → [1]
   - [\[1\]](#page-x-y) → [1]
   - [\\[1\\]](#page-x-y) → [1]
   - Remove all #page-x-y anchors
   - Ensure consistent [N] format for all citations

3. Standardize formatting:
   - Use proper Markdown headers (# ## ###)
   - Fix broken italic/bold formatting
   - Ensure consistent list formatting
   - Preserve mathematical notation
   - Clean up any \\n\\n\\n patterns to just \\n\\n

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

Paper content to reformat:
{paper_content}

ALSO, at the very end of your response, on a new line, provide:
FIRST_AUTHOR_LASTNAME: [lastname]
YEAR: [year]
"""

    def __init__(self, backup_dir: Path = None, model: str = None):
        """Initialize the reformatter with KiloCode API."""
        # Load KiloCode configuration
        try:
            self.config = load_config()
            self.logger = self._setup_logger()
            self.logger.info("KiloCode configuration loaded successfully")
        except ConfigurationError as e:
            print(f"Failed to load KiloCode configuration: {e}")
            sys.exit(1)
        
        # Use specified model or default to Gemini 2.5 Pro
        self.model = model or "google/gemini-2.5-pro-preview"
        
        # Initialize OpenAI client with KiloCode
        self.client = OpenAI(
            base_url=self.config.openrouter_url,
            api_key=self.config.token,
            default_headers={
                "HTTP-Referer": self.config.http_referer,
                "X-Title": self.config.x_title,
            }
        )
        
        self.backup_dir = backup_dir or Path("backups/paper_reformatter")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file = Path("paper_reformatter_checkpoint.json")
        self.report_file = Path(f"reformatting_report_{datetime.now():%Y%m%d_%H%M%S}.json")
        
        self.logger.info(f"Using model: {self.model}")
        self.logger.info(f"API endpoint: {self.config.openrouter_url}")
        
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
        """Save processing checkpoint."""
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)
            
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
                        frontmatter = yaml.safe_load(yaml_content)
                        if frontmatter is None:
                            frontmatter = {}
                    else:
                        frontmatter = {}
                    main_content = content[end_match.end() + 3:]
                    return frontmatter, main_content
            except Exception as e:
                self.logger.warning(f"Failed to parse YAML frontmatter: {e}")
                
        return {}, content
        
    def save_with_frontmatter(self, file_path: Path, frontmatter: Dict[str, Any], content: str):
        """Save markdown file with YAML frontmatter."""
        # Build YAML frontmatter
        yaml_lines = ["---"]
        
        # Preserve order of important fields
        ordered_fields = ["cite_key", "title", "authors", "year", "doi", "url", "relevancy", "tldr", "insights", "summary"]
        
        for field in ordered_fields:
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
                    
        # Add any remaining fields
        for key, value in frontmatter.items():
            if key not in ordered_fields:
                # Convert datetime objects to string
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                    
                if key == "tags" and isinstance(value, list):
                    yaml_lines.append(f"{key}:")
                    for tag in value:
                        yaml_lines.append(f'  - "{tag}"')
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
        self.logger.info(f"Processing: {paper_path}")
        
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
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at reformatting academic papers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=8192
            )
            
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
                        
            # Save reformatted content
            self.save_with_frontmatter(paper_path, frontmatter, reformatted_content)
            
            return ReformattingResult(
                success=True,
                paper_path=paper_path,
                original_cite_key=original_cite_key,
                new_cite_key=new_cite_key if new_cite_key != original_cite_key else None,
                folder_renamed=folder_renamed,
                changes_made=changes_made
            )
            
        except Exception as e:
            self.logger.error(f"Failed to process {paper_path}: {str(e)}")
            return ReformattingResult(
                success=False,
                paper_path=paper_path,
                original_cite_key=frontmatter.get('cite_key', 'unknown') if frontmatter else 'unknown',
                errors=[str(e)]
            )
            
    def process_all_papers(self, markdown_dir: Path, batch_size: int = 10):
        """Process all papers in the markdown directory."""
        # Find all paper.md files
        paper_files = list(markdown_dir.glob("*/paper.md"))
        self.logger.info(f"Found {len(paper_files)} papers to process")
        
        # Load checkpoint
        checkpoint = self.load_checkpoint()
        processed = set(checkpoint["processed"])
        failed = set(checkpoint["failed"])
        
        # Filter out already processed papers
        remaining_papers = [p for p in paper_files if str(p) not in processed and str(p) not in failed]
        self.logger.info(f"Remaining papers to process: {len(remaining_papers)}")
        
        # Collect existing cite_keys
        existing_keys = set()
        for paper_path in paper_files:
            try:
                frontmatter, _ = self.extract_frontmatter_and_content(paper_path)
                if 'cite_key' in frontmatter:
                    existing_keys.add(frontmatter['cite_key'])
            except:
                pass
                
        # Process in batches
        results = []
        
        for i in range(0, len(remaining_papers), batch_size):
            batch = remaining_papers[i:i + batch_size]
            self.logger.info(f"Processing batch {i//batch_size + 1} ({len(batch)} papers)")
            
            for paper_path in batch:
                # Rate limiting for KiloCode
                time.sleep(1)  # Wait 1 second between API calls
                
                result = self.reformat_paper(paper_path, existing_keys)
                results.append(result)
                
                # Update checkpoint
                if result.success:
                    processed.add(str(paper_path))
                else:
                    failed.add(str(paper_path))
                    
                checkpoint["processed"] = list(processed)
                checkpoint["failed"] = list(failed)
                checkpoint["last_processed"] = str(paper_path)
                self.save_checkpoint(checkpoint)
                
            self.logger.info(f"Completed batch {i//batch_size + 1}")
            
        # Generate report
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
    parser.add_argument("--batch-size", type=int, default=10,
                       help="Number of papers to process in each batch")
    parser.add_argument("--test", action="store_true",
                       help="Test mode - process only first 3 papers")
    parser.add_argument("--model", type=str, 
                       default="google/gemini-2.5-pro-preview",
                       help="Model to use (default: google/gemini-2.5-pro-preview)")
    
    args = parser.parse_args()
    
    # Initialize reformatter
    reformatter = PaperReformatter(model=args.model)
    
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
        # Process all papers
        reformatter.process_all_papers(args.markdown_dir, args.batch_size)
        
    return 0


if __name__ == "__main__":
    exit(main())
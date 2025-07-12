#!/usr/bin/env python3
"""
Test version of Paper Reformatter that saves to a test output directory
instead of modifying original files.
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
    output_path: Path
    original_cite_key: str
    new_cite_key: Optional[str] = None
    folder_renamed: bool = False
    errors: List[str] = None
    changes_made: List[str] = None


class PaperReformatterTest:
    """Test version that outputs to separate directory."""
    
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

    def __init__(self, output_dir: Path = None, backup_dir: Path = None, model: str = None):
        """Initialize the test reformatter with KiloCode API."""
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
        
        # Test output directory
        self.output_dir = output_dir or Path("test_reformatted_papers")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.backup_dir = backup_dir or Path("backups/paper_reformatter_test")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.checkpoint_file = Path("paper_reformatter_test_checkpoint.json")
        self.report_file = Path(f"test_reformatting_report_{datetime.now():%Y%m%d_%H%M%S}.json")
        
        self.logger.info(f"Using model: {self.model}")
        self.logger.info(f"API endpoint: {self.config.openrouter_url}")
        self.logger.info(f"Output directory: {self.output_dir}")
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger("PaperReformatterTest")
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(f"paper_reformatter_test_{datetime.now():%Y%m%d_%H%M%S}.log")
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
        
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
        """Reformat a single paper and save to test output directory."""
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
            
            # Log content length for debugging
            self.logger.info(f"Content length: {len(content)} characters")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at reformatting academic papers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=50000,  # More reasonable limit
                timeout=300  # 5 minute timeout
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
                    folder_renamed = True
                        
            # Create output path in test directory
            if folder_renamed and new_cite_key:
                output_folder = self.output_dir / new_cite_key
            else:
                output_folder = self.output_dir / paper_path.parent.name
                
            output_path = output_folder / paper_path.name
            output_folder.mkdir(parents=True, exist_ok=True)
            
            # Save reformatted content to test directory
            self.save_with_frontmatter(output_path, frontmatter, reformatted_content)
            
            # Copy images if folder exists
            if paper_path.parent.is_dir():
                for img_file in paper_path.parent.glob("*.jpeg"):
                    shutil.copy2(img_file, output_folder)
                for img_file in paper_path.parent.glob("*.jpg"):
                    shutil.copy2(img_file, output_folder)
                for img_file in paper_path.parent.glob("*.png"):
                    shutil.copy2(img_file, output_folder)
            
            return ReformattingResult(
                success=True,
                paper_path=paper_path,
                output_path=output_path,
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
                output_path=Path(""),
                original_cite_key=frontmatter.get('cite_key', 'unknown') if frontmatter else 'unknown',
                errors=[str(e)]
            )
            
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
            "output_directory": str(self.output_dir),
            "details": []
        }
        
        for result in results:
            detail = {
                "paper": str(result.paper_path),
                "output": str(result.output_path),
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
        self.logger.info(f"Output saved to: {self.output_dir}")


def main():
    """Main entry point for the test paper reformatter."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test reformatting papers to separate directory")
    parser.add_argument("papers", nargs="+", type=Path,
                       help="Specific paper paths to test")
    parser.add_argument("--output-dir", type=Path, 
                       default=Path("test_reformatted_papers"),
                       help="Output directory for test results")
    parser.add_argument("--model", type=str, 
                       default="google/gemini-2.5-pro-preview",
                       help="Model to use (default: google/gemini-2.5-pro-preview)")
    
    args = parser.parse_args()
    
    # Initialize test reformatter
    reformatter = PaperReformatterTest(output_dir=args.output_dir, model=args.model)
    
    reformatter.logger.info(f"Testing {len(args.papers)} papers")
    
    results = []
    existing_keys = set()
    
    for paper_path in args.papers:
        if not paper_path.exists():
            reformatter.logger.error(f"Paper not found: {paper_path}")
            continue
            
        result = reformatter.reformat_paper(paper_path, existing_keys)
        results.append(result)
        time.sleep(1)  # Rate limiting
        
    reformatter.generate_report(results)
    
    return 0


if __name__ == "__main__":
    exit(main())
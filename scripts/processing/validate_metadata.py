#!/Users/invoture/dev.local/hdm/.venv/bin/python
"""
Validate and correct metadata (title, authors, year, DOI) in research paper markdown files.
"""

import os
import re
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime
import requests
from time import sleep

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MetadataValidator:
    def __init__(self):
        self.stats = {
            'files_processed': 0,
            'titles_corrected': 0,
            'authors_corrected': 0,
            'years_corrected': 0,
            'dois_corrected': 0,
            'errors': 0,
            'error_details': []
        }
        
        # Patterns for extracting metadata from filenames
        self.arxiv_pattern = re.compile(r'arxiv_(\d{4})\.(\d{4,5})')
        self.arxiv_v2_pattern = re.compile(r'arxiv_arxiv_(\d{4})\.(\d{4,5})')
        self.year_from_filename = re.compile(r'(\d{4})')
        
    def extract_arxiv_info(self, filename: str) -> Optional[Tuple[str, int]]:
        """Extract arXiv ID and year from filename."""
        # Try different arxiv patterns
        match = self.arxiv_pattern.search(filename)
        if not match:
            match = self.arxiv_v2_pattern.search(filename)
        
        if match:
            year_part = match.group(1)
            number_part = match.group(2)
            arxiv_id = f"{year_part}.{number_part}"
            
            # Extract year from arxiv ID
            # Format: YYMM.NNNNN (since 2007)
            year_code = int(year_part[:2])
            if year_code >= 91:  # 91-99 = 1991-1999
                year = 1900 + year_code
            else:  # 00-90 = 2000-2090
                year = 2000 + year_code
            
            return arxiv_id, year
        
        return None
    
    def clean_doi(self, doi: str) -> str:
        """Clean up DOI string."""
        if not doi:
            return doi
            
        # Remove trailing parentheses or other artifacts
        doi = re.sub(r'[\)\]]+$', '', doi)
        
        # Ensure proper DOI format
        if not doi.startswith('10.'):
            # Try to extract DOI pattern
            doi_match = re.search(r'(10\.\d{4,}/[-._;()/:a-zA-Z0-9]+)', doi)
            if doi_match:
                doi = doi_match.group(1)
        
        return doi.strip()
    
    def clean_authors(self, authors: str) -> str:
        """Clean up author names."""
        if not authors:
            return authors
            
        # Remove escaped characters
        authors = authors.replace('\\,', ',')
        authors = authors.replace('\\', '')
        
        # Remove HTML entities and artifacts
        authors = re.sub(r'&[a-zA-Z]+;', '', authors)
        authors = re.sub(r'<[^>]+>', '', authors)
        
        # Ensure proper comma separation
        authors = re.sub(r'\s*,\s*', ', ', authors)
        
        # Remove trailing artifacts
        authors = re.sub(r'["\']$', '', authors)
        
        return authors.strip()
    
    def extract_title_from_content(self, content: str) -> Optional[str]:
        """Extract title from markdown content."""
        # Look for main heading
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            # Clean up the title
            title = re.sub(r'\*\*(.+?)\*\*', r'\1', title)  # Remove bold
            title = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', title)  # Remove links
            return title
        return None
    
    def validate_year(self, year: int, filename: str) -> int:
        """Validate and potentially correct the year."""
        current_year = datetime.now().year
        
        # Check if year is reasonable
        if year < 1990 or year > current_year + 1:
            # Try to extract from filename
            arxiv_info = self.extract_arxiv_info(filename)
            if arxiv_info:
                return arxiv_info[1]
            
            # Try to extract any 4-digit year from filename
            year_matches = self.year_from_filename.findall(filename)
            for y in year_matches:
                y_int = int(y)
                if 1990 <= y_int <= current_year + 1:
                    return y_int
        
        return year
    
    def extract_metadata_from_paper(self, content: str) -> Dict[str, any]:
        """Extract metadata directly from paper content."""
        metadata = {}
        
        # Extract title
        title = self.extract_title_from_content(content)
        if title:
            metadata['title'] = title
        
        # Extract authors (usually after title)
        # Look for author patterns
        author_patterns = [
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+ [A-Z][a-z]+)*)',
            r'^(.+?)\n\n(?:Abstract|ABSTRACT|1\s+Introduction)',
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
            if match:
                authors = match.group(1).strip()
                # Clean up
                authors = re.sub(r'\d+', '', authors)  # Remove numbers
                authors = re.sub(r'\*', '', authors)  # Remove asterisks
                authors = re.sub(r'\s+', ' ', authors)  # Normalize spaces
                if len(authors) > 10 and len(authors) < 500:
                    metadata['authors'] = authors
                    break
        
        return metadata
    
    def process_file(self, filepath: Path) -> Tuple[bool, str]:
        """Process a single markdown file."""
        try:
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split frontmatter and body
            if not content.startswith('---'):
                return False, "No frontmatter found"
            
            parts = content.split('---', 2)
            if len(parts) < 3:
                return False, "Invalid frontmatter structure"
            
            yaml_content = parts[1]
            body = parts[2]
            
            # Parse YAML (with error handling)
            try:
                # Fix common YAML issues first
                yaml_lines = yaml_content.split('\n')
                fixed_lines = []
                for line in yaml_lines:
                    # Fix escaped quotes in values
                    if ':' in line:
                        key, value = line.split(':', 1)
                        value = value.strip()
                        if value.startswith('"') and value.endswith('"'):
                            # Remove quotes and unescape
                            value = value[1:-1].replace('\\"', '"').replace('\\\\', '\\')
                            line = f"{key}: {value}"
                    fixed_lines.append(line)
                
                yaml_content = '\n'.join(fixed_lines)
                metadata = yaml.safe_load(yaml_content)
                
                if not metadata:
                    metadata = {}
            except yaml.YAMLError as e:
                return False, f"YAML parsing error: {e}"
            
            # Track if any changes were made
            changes_made = False
            
            # Extract metadata from paper content
            paper_metadata = self.extract_metadata_from_paper(body)
            
            # Validate and correct title
            current_title = metadata.get('title', '')
            if not current_title or len(current_title) < 10:
                if 'title' in paper_metadata:
                    metadata['title'] = paper_metadata['title']
                    self.stats['titles_corrected'] += 1
                    changes_made = True
                    logger.info(f"  Fixed title: {paper_metadata['title'][:50]}...")
            
            # Validate and correct authors
            current_authors = metadata.get('authors', '')
            cleaned_authors = self.clean_authors(current_authors)
            if cleaned_authors != current_authors:
                metadata['authors'] = cleaned_authors
                self.stats['authors_corrected'] += 1
                changes_made = True
                logger.info(f"  Fixed authors: {cleaned_authors[:50]}...")
            elif not current_authors and 'authors' in paper_metadata:
                metadata['authors'] = paper_metadata['authors']
                self.stats['authors_corrected'] += 1
                changes_made = True
                logger.info(f"  Added authors: {paper_metadata['authors'][:50]}...")
            
            # Validate and correct year
            current_year = metadata.get('year', 0)
            if isinstance(current_year, str):
                try:
                    current_year = int(current_year)
                except:
                    current_year = 0
            
            validated_year = self.validate_year(current_year, filepath.name)
            if validated_year != current_year:
                metadata['year'] = validated_year
                self.stats['years_corrected'] += 1
                changes_made = True
                logger.info(f"  Fixed year: {current_year} -> {validated_year}")
            
            # Validate and correct DOI
            current_doi = metadata.get('doi', '')
            cleaned_doi = self.clean_doi(current_doi)
            if cleaned_doi != current_doi:
                metadata['doi'] = cleaned_doi
                self.stats['dois_corrected'] += 1
                changes_made = True
                logger.info(f"  Fixed DOI: {cleaned_doi}")
            
            # If changes were made, write back
            if changes_made:
                # Reconstruct file
                new_yaml = yaml.dump(metadata, default_flow_style=False, sort_keys=False, allow_unicode=True)
                new_content = f"---\n{new_yaml}---\n{body}"
                
                # Write back
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True, f"Updated: {self.stats['titles_corrected']} titles, {self.stats['authors_corrected']} authors, {self.stats['years_corrected']} years, {self.stats['dois_corrected']} DOIs"
            
            return False, "No changes needed"
            
        except Exception as e:
            return False, f"Error: {e}"
    
    def validate_all_files(self):
        """Validate all markdown files."""
        base_dir = Path('/Users/invoture/dev.local/hdm/markdown_papers')
        
        # Find all markdown files
        md_files = list(base_dir.rglob('*.md'))
        logger.info(f"Found {len(md_files)} markdown files to validate")
        
        # Process each file
        for i, filepath in enumerate(md_files, 1):
            logger.info(f"Processing {i}/{len(md_files)}: {filepath.name}")
            
            success, message = self.process_file(filepath)
            
            if success:
                logger.info(f"  ✓ {message}")
            else:
                if "No changes needed" in message:
                    logger.debug(f"  - {message}")
                else:
                    self.stats['errors'] += 1
                    self.stats['error_details'].append({
                        'file': filepath.name,
                        'error': message
                    })
                    logger.error(f"  ✗ {message}")
            
            self.stats['files_processed'] += 1
            
            # Progress report
            if i % 50 == 0:
                logger.info(f"\nProgress: {i}/{len(md_files)}")
                logger.info(f"Corrections - Titles: {self.stats['titles_corrected']}, Authors: {self.stats['authors_corrected']}, Years: {self.stats['years_corrected']}, DOIs: {self.stats['dois_corrected']}")
        
        # Final report
        print("\n" + "="*60)
        print("METADATA VALIDATION SUMMARY")
        print("="*60)
        print(f"Total files processed: {self.stats['files_processed']}")
        print(f"Titles corrected: {self.stats['titles_corrected']}")
        print(f"Authors corrected: {self.stats['authors_corrected']}")
        print(f"Years corrected: {self.stats['years_corrected']}")
        print(f"DOIs corrected: {self.stats['dois_corrected']}")
        print(f"Errors: {self.stats['errors']}")
        print("="*60)
        
        # Save error details
        if self.stats['error_details']:
            error_file = Path('metadata_validation_errors.json')
            with open(error_file, 'w') as f:
                json.dump(self.stats['error_details'], f, indent=2)
            print(f"\nError details saved to: {error_file}")

def main():
    """Main function."""
    validator = MetadataValidator()
    validator.validate_all_files()

if __name__ == '__main__':
    main()
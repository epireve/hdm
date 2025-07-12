#!/usr/bin/env python3
"""
Create a clean CSV file listing all research papers with cite_key, title, authors, and year.
Handles YAML parsing errors more robustly.
"""

import os
import re
import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CleanPapersCSVGenerator:
    def __init__(self):
        self.papers = []
        self.errors = []
        
    def parse_yaml_safely(self, yaml_content: str) -> Dict:
        """Parse YAML content safely, handling common issues."""
        metadata = {}
        lines = yaml_content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if ':' in line:
                # Split on first colon
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    
                    # Clean up the value
                    # Remove quotes if they wrap the entire value
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # Handle multiline values (for now, just take first line)
                    if '\n' in value:
                        value = value.split('\n')[0].strip()
                    
                    metadata[key] = value
        
        return metadata
    
    def extract_title_from_content(self, content: str) -> str:
        """Extract title from markdown content if not in frontmatter."""
        # Look for first major heading
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# ') and len(line) > 3:
                title = line[2:].strip()
                # Clean up common artifacts
                title = re.sub(r'\*\*(.+?)\*\*', r'\1', title)  # Remove bold
                title = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', title)  # Remove links
                return title
        return ""
    
    def extract_metadata(self, filepath: Path) -> Optional[Dict]:
        """Extract metadata from a markdown file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Initialize with defaults
            paper_info = {
                'cite_key': '',
                'title': '',
                'authors': '',
                'year': ''
            }
            
            # Check if file has frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    body_content = parts[2]
                    
                    # Parse YAML safely
                    metadata = self.parse_yaml_safely(yaml_content)
                    
                    # Extract fields
                    paper_info['cite_key'] = metadata.get('cite_key', '')
                    paper_info['title'] = metadata.get('title', '')
                    paper_info['authors'] = metadata.get('authors', '')
                    paper_info['year'] = str(metadata.get('year', ''))
                else:
                    body_content = content
            else:
                body_content = content
            
            # If we don't have a title, try to extract from content
            if not paper_info['title']:
                paper_info['title'] = self.extract_title_from_content(body_content)
            
            # If we still don't have basic info, generate from filename
            if not paper_info['cite_key']:
                # Generate cite_key from filename
                filename = filepath.stem
                # Look for year in filename
                year_match = re.search(r'(19|20)\d{2}', filename)
                year = year_match.group(0) if year_match else '2024'
                
                # Extract first meaningful part for author
                clean_name = re.sub(r'[_-]+', '_', filename)
                parts = clean_name.split('_')
                author_part = 'unknown'
                for part in parts:
                    if len(part) > 3 and not part.isdigit() and part not in ['arxiv', 'paper', 'pdf']:
                        author_part = part.lower()
                        break
                
                paper_info['cite_key'] = f"{author_part}_{year}"
            
            # If we don't have a year, try to extract from cite_key or filename
            if not paper_info['year']:
                if '_' in paper_info['cite_key']:
                    year_part = paper_info['cite_key'].split('_')[-1]
                    if year_part.isdigit() and len(year_part) == 4:
                        paper_info['year'] = year_part
                else:
                    paper_info['year'] = '2024'  # Default
            
            # Clean up fields
            # Remove extra whitespace and clean title
            paper_info['title'] = re.sub(r'\s+', ' ', paper_info['title']).strip()
            paper_info['authors'] = re.sub(r'\s+', ' ', paper_info['authors']).strip()
            
            # Remove common artifacts from title
            if paper_info['title']:
                # Remove leading numbers and dots
                paper_info['title'] = re.sub(r'^[\d\.\s]+', '', paper_info['title'])
                # Remove markdown artifacts
                paper_info['title'] = re.sub(r'[#*`]', '', paper_info['title'])
                # Clean up
                paper_info['title'] = paper_info['title'].strip()
            
            # If title is still empty or too short, use filename
            if len(paper_info['title']) < 5:
                paper_info['title'] = filepath.stem.replace('_', ' ').replace('-', ' ')
            
            return paper_info
                
        except Exception as e:
            self.errors.append(f"Error reading {filepath.name}: {str(e)[:100]}")
            return None
    
    def generate_csv(self, output_file: str = 'research_papers_clean.csv'):
        """Generate clean CSV file with all papers."""
        base_dir = Path('/Users/invoture/dev.local/hdm/markdown_papers')
        
        # Find all markdown files
        logger.info("Scanning for markdown files...")
        md_files = []
        for folder in base_dir.iterdir():
            if folder.is_dir():
                for md_file in folder.glob("*.md"):
                    # Skip meta files
                    if not md_file.name.endswith('_meta.json') and not 'meta' in md_file.name:
                        md_files.append(md_file)
        
        logger.info(f"Found {len(md_files)} markdown files")
        
        # Process each file
        for i, filepath in enumerate(md_files, 1):
            if i % 50 == 0:
                logger.info(f"Processing {i}/{len(md_files)}...")
            
            paper_info = self.extract_metadata(filepath)
            if paper_info:
                self.papers.append(paper_info)
        
        # Sort papers by cite_key
        self.papers.sort(key=lambda x: x['cite_key'].lower())
        
        # Remove duplicates based on cite_key
        seen_keys = set()
        unique_papers = []
        for paper in self.papers:
            if paper['cite_key'] not in seen_keys:
                seen_keys.add(paper['cite_key'])
                unique_papers.append(paper)
            else:
                logger.warning(f"Duplicate cite_key found: {paper['cite_key']}")
        
        self.papers = unique_papers
        
        # Write to CSV
        output_path = Path(output_file)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['cite_key', 'title', 'authors', 'year']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write papers
            for paper in self.papers:
                writer.writerow(paper)
        
        # Print summary
        print("\n" + "="*60)
        print("CLEAN CSV GENERATION SUMMARY")
        print("="*60)
        print(f"Total markdown files found: {len(md_files)}")
        print(f"Papers successfully extracted: {len(self.papers)}")
        print(f"Errors encountered: {len(self.errors)}")
        print(f"Output file: {output_path.absolute()}")
        print("="*60)
        
        # Save errors if any
        if self.errors:
            error_file = Path('clean_csv_generation_errors.txt')
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.errors))
            print(f"\nError details saved to: {error_file}")
        
        # Show sample of the CSV
        print("\nFirst 10 entries in the CSV:")
        print("-"*80)
        for i, paper in enumerate(self.papers[:10]):
            print(f"{i+1:2d}. {paper['cite_key']:<20} | {paper['year']} | {paper['title'][:45]}...")

def main():
    """Main function."""
    generator = CleanPapersCSVGenerator()
    generator.generate_csv()

if __name__ == '__main__':
    main()
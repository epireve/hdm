#!/usr/bin/env python3
"""
Create a CSV file listing all research papers with cite_key, title, authors, and year.
"""

import os
import re
import yaml
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

class PapersCSVGenerator:
    def __init__(self):
        self.papers = []
        self.errors = []
        
    def extract_metadata(self, filepath: Path) -> Optional[Dict]:
        """Extract metadata from a markdown file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has frontmatter
            if not content.startswith('---'):
                self.errors.append(f"No frontmatter in {filepath.name}")
                return None
            
            # Split frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.errors.append(f"Invalid frontmatter in {filepath.name}")
                return None
            
            yaml_content = parts[1]
            
            # Parse YAML
            try:
                metadata = yaml.safe_load(yaml_content)
                if not metadata:
                    self.errors.append(f"Empty metadata in {filepath.name}")
                    return None
                
                # Extract required fields
                paper_info = {
                    'cite_key': metadata.get('cite_key', ''),
                    'title': metadata.get('title', ''),
                    'authors': metadata.get('authors', ''),
                    'year': metadata.get('year', '')
                }
                
                # Clean up the fields
                # Remove quotes from title if present
                if paper_info['title'].startswith('"') and paper_info['title'].endswith('"'):
                    paper_info['title'] = paper_info['title'][1:-1]
                
                # Ensure year is string
                paper_info['year'] = str(paper_info['year'])
                
                # Clean authors - remove extra whitespace
                paper_info['authors'] = ' '.join(paper_info['authors'].split())
                
                return paper_info
                
            except yaml.YAMLError as e:
                self.errors.append(f"YAML error in {filepath.name}: {str(e)[:100]}")
                return None
                
        except Exception as e:
            self.errors.append(f"Error reading {filepath.name}: {str(e)[:100]}")
            return None
    
    def generate_csv(self, output_file: str = 'research_papers.csv'):
        """Generate CSV file with all papers."""
        base_dir = Path('/Users/invoture/dev.local/hdm/markdown_papers')
        
        # Find all markdown files
        logger.info("Scanning for markdown files...")
        md_files = []
        for folder in base_dir.iterdir():
            if folder.is_dir():
                for md_file in folder.glob("*.md"):
                    # Skip meta.json files
                    if not md_file.name.endswith('_meta.json'):
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
        print("CSV GENERATION SUMMARY")
        print("="*60)
        print(f"Total markdown files found: {len(md_files)}")
        print(f"Papers successfully extracted: {len(self.papers)}")
        print(f"Errors encountered: {len(self.errors)}")
        print(f"Output file: {output_path.absolute()}")
        print("="*60)
        
        # Save errors if any
        if self.errors:
            error_file = Path('csv_generation_errors.txt')
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.errors))
            print(f"\nError details saved to: {error_file}")
        
        # Show sample of the CSV
        print("\nFirst 5 entries in the CSV:")
        print("-"*60)
        for i, paper in enumerate(self.papers[:5]):
            print(f"{i+1}. {paper['cite_key']} | {paper['year']} | {paper['title'][:50]}...")

def main():
    """Main function."""
    generator = PapersCSVGenerator()
    generator.generate_csv()

if __name__ == '__main__':
    main()
#!/Users/invoture/dev.local/hdm/.venv/bin/python
"""
Fix remaining YAML parsing issues in markdown files.
"""

import os
import re
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class YAMLFixer:
    def __init__(self):
        self.stats = {
            'files_processed': 0,
            'files_fixed': 0,
            'errors': 0
        }
        
        # Files with known issues from the error log
        self.problem_files = [
            "arxiv_arxiv_2406.14191_Temporal_Knowledge_Graph_Question_Answering_A_Survey.md",
            "arxiv_2004.06809_Issues_and_challenges_in_Cloud_Storage_Architecture_A_Survey.md",
            "arxiv_2302.03593_A_Systematic_Review_on_Human_Modeling_Digging_int.md",
            "ISJv23p119-145Schmitt6471.md",
            "arxiv_2019_deep_learning_sequential_recommendation_survey.md",
            "arxiv_arxiv_2505.14629_KERL_Knowledge-Enhanced_Personalized_Recipe_Recommendation_using_Large_Language_.md",
            "arxiv_2211.10904_Temporal_Knowledge_Graph_Reasoning_with_Historical_Contrastive_Learning.md"
        ]
    
    def fix_yaml_content(self, yaml_content: str) -> str:
        """Fix common YAML issues."""
        lines = yaml_content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                fixed_lines.append(line)
                continue
            
            # Check if line has a key-value pair
            if ':' in line:
                # Split only on first colon
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    
                    # Fix title, authors, and other text fields with colons
                    if key in ['title', 'authors', 'tldr']:
                        # If value contains colon and not already quoted
                        if ':' in value and not (value.startswith('"') and value.endswith('"')):
                            # Escape internal quotes
                            value = value.replace('"', '\\"')
                            # Quote the entire value
                            value = f'"{value}"'
                        elif value and not value.startswith('"'):
                            # Quote values that might have special characters
                            if any(char in value for char in [':', '|', '>', '<', '&', '*', '!', '%', '@', '#']):
                                value = value.replace('"', '\\"')
                                value = f'"{value}"'
                    
                    # Fix cite_key if it's empty or has issues
                    if key == 'cite_key':
                        if not value or value == "'":
                            value = 'unknown_2024'
                        # Remove quotes from cite_key
                        value = value.strip('"\'')
                    
                    # Fix year
                    if key == 'year':
                        # Remove quotes and ensure it's a number
                        value = value.strip('"\'')
                        try:
                            int(value)
                        except:
                            value = '2024'
                    
                    # Fix DOI
                    if key == 'doi':
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        # Remove trailing periods
                        value = value.rstrip('.')
                    
                    # Reconstruct the line
                    line = f"{key}: {value}"
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def process_file(self, filepath: Path) -> Tuple[bool, str]:
        """Process a single markdown file."""
        try:
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has frontmatter
            if not content.startswith('---'):
                # Add basic frontmatter if missing
                filename = filepath.stem
                # Extract info from filename
                year = 2024
                year_match = re.search(r'(19|20)\d{2}', filename)
                if year_match:
                    year = int(year_match.group(0))
                
                cite_key = f"unknown_{year}"
                title = filename.replace('_', ' ').replace('-', ' ')
                
                frontmatter = f"""---
cite_key: {cite_key}
title: "{title}"
authors: ""
year: {year}
date_processed: "2025-07-02"
---
"""
                content = frontmatter + content
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.stats['files_fixed'] += 1
                return True, "Added missing frontmatter"
            
            # Split frontmatter and body
            parts = content.split('---', 2)
            if len(parts) < 3:
                return False, "Invalid frontmatter structure"
            
            yaml_content = parts[1]
            body = parts[2]
            
            # Fix YAML content
            fixed_yaml = self.fix_yaml_content(yaml_content)
            
            # Try to parse the fixed YAML
            try:
                metadata = yaml.safe_load(fixed_yaml)
                if not metadata:
                    metadata = {}
            except yaml.YAMLError as e:
                # If still failing, try more aggressive fixes
                logger.warning(f"First fix attempt failed for {filepath.name}, trying aggressive fix")
                
                # Create a minimal valid YAML
                lines = fixed_yaml.split('\n')
                new_metadata = {}
                
                for line in lines:
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip().strip('"\'')
                            if key and value:
                                new_metadata[key] = value
                
                # Ensure required fields
                if 'cite_key' not in new_metadata or not new_metadata['cite_key']:
                    new_metadata['cite_key'] = 'unknown_2024'
                if 'year' not in new_metadata:
                    new_metadata['year'] = 2024
                
                fixed_yaml = yaml.dump(new_metadata, default_flow_style=False, sort_keys=False)
            
            # Write back
            new_content = f"---\n{fixed_yaml}---\n{body}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.stats['files_fixed'] += 1
            return True, "Fixed YAML issues"
            
        except Exception as e:
            return False, f"Error: {e}"
    
    def fix_problem_files(self):
        """Fix known problem files."""
        base_dir = Path('/Users/invoture/dev.local/hdm/markdown_papers')
        
        logger.info(f"Fixing {len(self.problem_files)} problem files")
        
        for filename in self.problem_files:
            # Find the file
            file_path = None
            for path in base_dir.rglob(filename):
                file_path = path
                break
            
            if not file_path:
                logger.error(f"File not found: {filename}")
                self.stats['errors'] += 1
                continue
            
            logger.info(f"Processing: {filename}")
            success, message = self.process_file(file_path)
            
            if success:
                logger.info(f"  ✓ {message}")
            else:
                logger.error(f"  ✗ {message}")
                self.stats['errors'] += 1
            
            self.stats['files_processed'] += 1
        
        # Summary
        print("\n" + "="*60)
        print("YAML FIX SUMMARY")
        print("="*60)
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Files fixed: {self.stats['files_fixed']}")
        print(f"Errors: {self.stats['errors']}")
        print("="*60)

def main():
    """Main function."""
    fixer = YAMLFixer()
    fixer.fix_problem_files()

if __name__ == '__main__':
    main()
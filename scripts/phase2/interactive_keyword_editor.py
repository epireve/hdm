#!/usr/bin/env python3
"""
Interactive script to help manually edit keywords in markdown files
Shows abstract and current keywords before opening each file
"""
import sys
import re
import os
from pathlib import Path
import yaml
from typing import Optional, List
import textwrap

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import MARKDOWN_DIR
from utils import setup_logging


class InteractiveKeywordEditor:
    """Interactive editor for keywords in research papers"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "edited": 0,
            "skipped": 0,
            "no_abstract": 0,
            "errors": 0
        }
    
    def extract_abstract(self, content: str) -> Optional[str]:
        """Extract abstract section from markdown content"""
        # Try different abstract patterns
        patterns = [
            # ## Abstract
            r'#{1,3}\s*Abstract\s*\n+(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
            # **Abstract**
            r'\*\*Abstract\*\*\s*\n+(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
            # Abstract: ...
            r'Abstract:\s*\n?(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
            # ABSTRACT (all caps)
            r'ABSTRACT\s*\n+(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                abstract_text = match.group(1).strip()
                # Clean up the abstract text
                abstract_text = re.sub(r'\n+', ' ', abstract_text)
                abstract_text = re.sub(r'\s+', ' ', abstract_text)
                # Remove markdown formatting
                abstract_text = re.sub(r'\*\*(.*?)\*\*', r'\1', abstract_text)
                abstract_text = re.sub(r'\*(.*?)\*', r'\1', abstract_text)
                abstract_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', abstract_text)
                return abstract_text
        
        return None
    
    def get_current_keywords(self, file_path: Path) -> Optional[List[str]]:
        """Extract current keywords from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter
            yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if not yaml_match:
                return None
            
            yaml_content = yaml_match.group(1)
            
            # Parse YAML
            try:
                metadata = yaml.safe_load(yaml_content)
                return metadata.get('keywords', [])
            except yaml.YAMLError:
                return None
                
        except Exception:
            return None
    
    def display_file_info(self, file_path: Path, abstract: Optional[str], keywords: Optional[List[str]]) -> None:
        """Display file information in a formatted way"""
        print("\n" + "="*80)
        print(f"FILE: {file_path.parent.name}/{file_path.name}")
        print("="*80)
        
        if abstract:
            print("\nABSTRACT:")
            print("-"*80)
            # Wrap abstract text for better readability
            wrapped = textwrap.fill(abstract, width=78)
            print(wrapped)
            print("-"*80)
        else:
            print("\nABSTRACT: Not found")
            
        if keywords:
            print(f"\nCURRENT KEYWORDS ({len(keywords)}):")
            print("-"*80)
            # Display keywords in columns
            for i in range(0, len(keywords), 3):
                row = keywords[i:i+3]
                print("  " + "  |  ".join(f"{kw:<25}" for kw in row))
        else:
            print("\nCURRENT KEYWORDS: None")
        
        print("\n" + "="*80)
    
    def suggest_keywords_from_abstract(self, abstract: str) -> List[str]:
        """Suggest keywords based on abstract content"""
        suggestions = []
        
        # Technical terms to look for
        technical_patterns = [
            r'\b(federated learning)\b',
            r'\b(machine learning)\b',
            r'\b(deep learning)\b',
            r'\b(neural network[s]?)\b',
            r'\b(knowledge graph[s]?)\b',
            r'\b(homomorphic encryption)\b',
            r'\b(differential privacy)\b',
            r'\b(secret sharing)\b',
            r'\b(secure aggregation)\b',
            r'\b(privacy[- ]preserving)\b',
            r'\b(temporal reasoning)\b',
            r'\b(graph embedding[s]?)\b',
            r'\b(multi-task learning)\b',
            r'\b(transfer learning)\b',
            r'\b(reinforcement learning)\b',
            r'\b(natural language processing)\b',
            r'\b(computer vision)\b',
            r'\b(data mining)\b',
            r'\b(blockchain)\b',
            r'\b(edge computing)\b',
            r'\b(IoT|internet of things)\b',
            r'\b(cloud computing)\b',
            r'\b(distributed system[s]?)\b',
            r'\b(optimization)\b',
            r'\b(algorithm[s]?)\b',
            r'\b(framework[s]?)\b',
            r'\b(protocol[s]?)\b',
            r'\b(architecture[s]?)\b',
        ]
        
        abstract_lower = abstract.lower()
        for pattern in technical_patterns:
            matches = re.findall(pattern, abstract_lower, re.IGNORECASE)
            suggestions.extend(matches)
        
        # Remove duplicates and sort
        suggestions = sorted(list(set(suggestions)))
        
        return suggestions[:10]  # Return top 10 suggestions
    
    def process_file(self, file_path: Path) -> bool:
        """Process a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter
            yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if not yaml_match:
                print(f"\nWarning: No YAML frontmatter found")
                self.stats["errors"] += 1
                return False
            
            markdown_content = content[yaml_match.end():]
            
            # Extract abstract
            abstract = self.extract_abstract(markdown_content)
            if not abstract:
                self.stats["no_abstract"] += 1
            
            # Get current keywords
            keywords = self.get_current_keywords(file_path)
            
            # Display file information
            self.display_file_info(file_path, abstract, keywords)
            
            # Suggest keywords if abstract exists
            if abstract:
                suggestions = self.suggest_keywords_from_abstract(abstract)
                if suggestions:
                    print("\nSUGGESTED KEYWORDS (from abstract):")
                    print("-"*80)
                    for i, kw in enumerate(suggestions, 1):
                        print(f"  {i:2d}. {kw}")
                    print("-"*80)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            self.stats["errors"] += 1
            return False
    
    def run(self):
        """Run the interactive editor"""
        # Find all markdown files
        markdown_files = []
        for folder in MARKDOWN_DIR.iterdir():
            if folder.is_dir():
                for md_file in folder.glob("*.md"):
                    markdown_files.append(md_file)
        
        total_files = len(markdown_files)
        self.logger.info(f"Found {total_files} markdown files")
        
        print("\n" + "="*80)
        print("INTERACTIVE KEYWORD EDITOR FOR RESEARCH PAPERS")
        print("="*80)
        print(f"Total files to process: {total_files}")
        print("\nInstructions:")
        print("1. Review the abstract and current keywords")
        print("2. Note the suggested keywords (if any)")
        print("3. Edit the keywords in the YAML frontmatter to include relevant terms")
        print("4. Keywords should be technical terms from the abstract, not fragments")
        print("\nCommands:")
        print("  [Enter] - Process this file")
        print("  s/skip  - Skip this file")
        print("  q/quit  - Exit the program")
        print("="*80)
        
        input("\nPress Enter to start...")
        
        for i, md_file in enumerate(markdown_files, 1):
            print(f"\n\n[FILE {i}/{total_files}]")
            
            # Process and display file info
            if not self.process_file(md_file):
                continue
            
            # Get user action
            while True:
                action = input("\nAction ([Enter]/s/q): ").strip().lower()
                
                if action == "" or action == "enter":
                    print(f"\nPlease edit the keywords in: {md_file}")
                    print("Focus on the abstract and use technical terms, not fragments.")
                    print("Example good keywords: 'federated learning', 'homomorphic encryption', 'secret sharing'")
                    print("Example bad keywords: 'a notable limitation', 'achieves the balance'")
                    input("\nPress Enter when you've finished editing the file...")
                    self.stats["edited"] += 1
                    self.logger.info(f"Edited {md_file.name}")
                    break
                    
                elif action in ["s", "skip"]:
                    self.stats["skipped"] += 1
                    self.logger.info(f"Skipped {md_file.name}")
                    break
                    
                elif action in ["q", "quit"]:
                    self.print_summary()
                    self.logger.info("User requested exit")
                    return
                    
                else:
                    print("Invalid action. Use Enter, 's' for skip, or 'q' for quit.")
        
        self.print_summary()
    
    def print_summary(self):
        """Print processing summary"""
        print("\n" + "="*80)
        print("PROCESSING SUMMARY")
        print("="*80)
        print(f"Files edited: {self.stats['edited']}")
        print(f"Files skipped: {self.stats['skipped']}")
        print(f"Files without abstract: {self.stats['no_abstract']}")
        print(f"Errors: {self.stats['errors']}")
        print("="*80)


def main():
    """Main function"""
    logger = setup_logging("interactive_keyword_editor")
    logger.info("Starting interactive keyword editor")
    
    editor = InteractiveKeywordEditor(logger)
    editor.run()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
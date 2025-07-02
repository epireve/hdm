#!/usr/bin/env python3
"""
Test the cite key update on a single file
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from update_cite_keys_and_tags import CitationUpdater
from utils import setup_logging


def test_single_file():
    """Test on a single file"""
    logger = setup_logging("test_cite_key")
    updater = CitationUpdater(logger)
    
    # Test files
    test_files = [
        Path("markdown_papers/jmir_e50210/jmir_e50210.md"),
        Path("markdown_papers/Callahan-2024-An-open-source-knowledge-graph-ecos/Callahan-2024-An-open-source-knowledge-graph-ecos.md"),
        Path("markdown_papers/1-s2.0-S0378778821011129-am/1-s2.0-S0378778821011129-am.md")
    ]
    
    for test_file in test_files:
        if test_file.exists():
            print(f"\n{'='*60}")
            print(f"Testing: {test_file}")
            print('='*60)
            
            # Read current metadata
            with open(test_file, 'r') as f:
                content = f.read()
                
            import re
            import yaml
            
            yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if yaml_match:
                metadata = yaml.safe_load(yaml_match.group(1))
                print(f"Current cite_key: {metadata.get('cite_key')}")
                print(f"Authors: {metadata.get('authors')}")
                print(f"Year: {metadata.get('year')}")
                print(f"Tags: {metadata.get('tags', 'None')}")
                
                # Test author cleaning
                clean_authors = updater.clean_authors(metadata.get('authors', ''))
                print(f"\nCleaned authors: {clean_authors}")
                
                # Test cite key generation
                if metadata.get('year'):
                    new_cite_key = updater.generate_cite_key(clean_authors, metadata['year'])
                    print(f"New cite_key would be: {new_cite_key}")
                
                # Test tag extraction
                title = metadata.get('title', '')
                tags = updater.extract_tags_from_content(content, title)
                print(f"Suggested tags: {tags}")


if __name__ == "__main__":
    test_single_file()
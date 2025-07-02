#!/usr/bin/env python3
"""
Final cite_key update and validation
Ensures all papers have proper cite_keys and renames folders accordingly
"""

import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

MARKDOWN_PAPERS = Path("markdown_papers")
CITE_KEY_UPDATE_LOG = Path("cite_key_update_log.json")

def extract_yaml_data(content: str) -> Optional[Dict]:
    """Extract data from YAML frontmatter"""
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    
    if not yaml_match:
        return None
    
    yaml_str = yaml_match.group(1)
    yaml_data = {}
    
    for line in yaml_str.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('-'):
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip().strip('"').strip("'")
                yaml_data[key] = value
    
    return yaml_data

def generate_cite_key(authors: str, year: str) -> str:
    """Generate cite key from authors and year"""
    if not authors or not year:
        return ""
    
    # Get first author's last name
    first_author = authors.split(',')[0].strip()
    
    # Extract last name
    words = first_author.split()
    if words:
        last_name = words[-1]
    else:
        last_name = "unknown"
    
    # Clean last name
    last_name = re.sub(r'[^a-zA-Z]', '', last_name).lower()
    
    return f"{last_name}_{year}"

def ensure_unique_cite_keys(papers: List[Dict]) -> Dict[str, str]:
    """Ensure all cite keys are unique"""
    # Count occurrences
    cite_key_counts = defaultdict(list)
    
    for paper in papers:
        base_key = paper['base_cite_key']
        cite_key_counts[base_key].append(paper)
    
    # Generate unique keys
    cite_key_mapping = {}
    
    for base_key, paper_list in cite_key_counts.items():
        if len(paper_list) == 1:
            paper = paper_list[0]
            cite_key_mapping[paper['folder']] = base_key
        else:
            # Sort by folder name for consistency
            paper_list.sort(key=lambda p: p['folder'])
            
            for i, paper in enumerate(paper_list):
                suffix = chr(ord('a') + i)
                unique_key = f"{base_key}{suffix}"
                cite_key_mapping[paper['folder']] = unique_key
    
    return cite_key_mapping

def update_yaml_cite_key(content: str, new_cite_key: str) -> str:
    """Update cite_key in YAML frontmatter"""
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    
    if not yaml_match:
        return content
    
    yaml_str = yaml_match.group(1)
    rest_content = content[yaml_match.end():]
    
    # Update cite_key line
    new_yaml_lines = []
    cite_key_found = False
    
    for line in yaml_str.split('\n'):
        if line.strip().startswith('cite_key:'):
            new_yaml_lines.append(f'cite_key: "{new_cite_key}"')
            cite_key_found = True
        else:
            new_yaml_lines.append(line)
    
    # Add cite_key if not found
    if not cite_key_found:
        new_yaml_lines.insert(0, f'cite_key: "{new_cite_key}"')
    
    new_yaml = '\n'.join(new_yaml_lines)
    return f"---\n{new_yaml}\n---\n{rest_content}"

def main():
    """Update all cite_keys and rename folders"""
    print("Analyzing all papers for cite_key updates...")
    
    papers = []
    issues = []
    
    # Collect all paper data
    for folder in MARKDOWN_PAPERS.iterdir():
        if folder.is_dir():
            md_path = folder / "paper.md"
            if md_path.exists():
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    yaml_data = extract_yaml_data(content)
                    
                    if yaml_data:
                        authors = yaml_data.get('authors', '')
                        year = yaml_data.get('year', '')
                        current_cite_key = yaml_data.get('cite_key', '')
                        
                        if authors and year:
                            base_cite_key = generate_cite_key(authors, str(year))
                            
                            papers.append({
                                'folder': folder.name,
                                'path': md_path,
                                'current_cite_key': current_cite_key,
                                'base_cite_key': base_cite_key,
                                'authors': authors,
                                'year': year
                            })
                        else:
                            issues.append({
                                'folder': folder.name,
                                'issue': 'Missing authors or year'
                            })
                    else:
                        issues.append({
                            'folder': folder.name,
                            'issue': 'No YAML frontmatter'
                        })
                        
                except Exception as e:
                    issues.append({
                        'folder': folder.name,
                        'issue': f'Error: {str(e)}'
                    })
    
    print(f"Found {len(papers)} papers to process")
    print(f"Found {len(issues)} papers with issues")
    
    # Generate unique cite keys
    cite_key_mapping = ensure_unique_cite_keys(papers)
    
    # Update papers and rename folders
    updates = []
    renames = []
    
    for paper in papers:
        folder_name = paper['folder']
        new_cite_key = cite_key_mapping[folder_name]
        current_cite_key = paper['current_cite_key']
        
        # Update YAML if cite_key changed
        if current_cite_key != new_cite_key:
            try:
                with open(paper['path'], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = update_yaml_cite_key(content, new_cite_key)
                
                with open(paper['path'], 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                updates.append({
                    'folder': folder_name,
                    'old_cite_key': current_cite_key,
                    'new_cite_key': new_cite_key
                })
                print(f"✓ Updated cite_key: {folder_name} -> {new_cite_key}")
                
            except Exception as e:
                print(f"✗ Error updating {folder_name}: {e}")
        
        # Rename folder if needed
        if folder_name != new_cite_key:
            old_path = MARKDOWN_PAPERS / folder_name
            new_path = MARKDOWN_PAPERS / new_cite_key
            
            if not new_path.exists():
                try:
                    shutil.move(str(old_path), str(new_path))
                    renames.append({
                        'old_name': folder_name,
                        'new_name': new_cite_key
                    })
                    print(f"✓ Renamed folder: {folder_name} -> {new_cite_key}")
                except Exception as e:
                    print(f"✗ Error renaming {folder_name}: {e}")
    
    # Save log
    log = {
        'total_papers': len(papers),
        'cite_key_updates': len(updates),
        'folder_renames': len(renames),
        'issues': issues,
        'updates': updates,
        'renames': renames
    }
    
    with open(CITE_KEY_UPDATE_LOG, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("Cite Key Update Summary:")
    print(f"Total papers processed: {len(papers)}")
    print(f"Cite keys updated: {len(updates)}")
    print(f"Folders renamed: {len(renames)}")
    print(f"Papers with issues: {len(issues)}")
    print(f"\nLog saved to: {CITE_KEY_UPDATE_LOG}")

if __name__ == "__main__":
    main()
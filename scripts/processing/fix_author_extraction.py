#!/usr/bin/env python3
"""
Fix author extraction issues in YAML frontmatter
- Replace email prefixes with actual author names
- Extract authors from the paper content
"""

import re
import json
from pathlib import Path
from typing import Dict, Optional, Tuple

# Manual corrections for known papers
AUTHOR_CORRECTIONS = {
    "BUILD-KG: Integrating Heterogeneous Data Into Analytics-Enabling Knowledge Graphs": 
        "Kara Schatz, Pei-Yu Hou, Alexey V. Gulyuk, Yaroslava G. Yingling, Rada Chirkova",
    
    "Log Anomaly Detection by Adversarial Autoencoders With Graph Feature Fusion":
        "Yuxia Xie, Kai Yang",
    
    "Privacy‐preserving graph publishing with disentangled variational information bottleneck": 
        "Jiahao Ma, Yijian Liu, Jinbao Wang, Yiyun Huang, Li-Ping Wang",
}

def extract_authors_from_content(content: str) -> Optional[str]:
    """Extract author names from paper content"""
    lines = content.split('\n')[:100]  # Check first 100 lines
    
    # Look for author patterns
    authors = []
    author_section_found = False
    
    for i, line in enumerate(lines):
        # Skip YAML frontmatter
        if i < 10 and line.startswith('---'):
            continue
            
        # Look for author names after title
        if re.match(r'^#\s+', line):  # Title line
            # Check next few lines for authors
            for j in range(i+1, min(i+10, len(lines))):
                next_line = lines[j].strip()
                
                # Pattern: Full names with affiliations
                if re.match(r'^[A-Z][a-z]+\s+[A-Z]\.?\s*[A-Z]?\.?\s*[A-Z][a-z]+', next_line):
                    # Extract names before commas, numbers, or affiliations
                    name_match = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z]\.?)*\s+[A-Z][a-z]+)', next_line)
                    authors.extend(name_match)
                
                # Pattern: Names with "and"
                if ' and ' in next_line and re.search(r'[A-Z][a-z]+', next_line):
                    parts = next_line.split(' and ')
                    for part in parts:
                        name_match = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z]\.?)*\s+[A-Z][a-z]+)', part)
                        authors.extend(name_match)
                
                # Stop at abstract or introduction
                if re.match(r'^\*?(Abstract|Introduction|Keywords)', next_line, re.IGNORECASE):
                    break
    
    # Clean and deduplicate authors
    cleaned_authors = []
    for author in authors:
        # Remove trailing punctuation and numbers
        author = re.sub(r'[,\d\*]+$', '', author).strip()
        if author and len(author) > 5 and author not in cleaned_authors:
            cleaned_authors.append(author)
    
    if cleaned_authors:
        return ', '.join(cleaned_authors)
    
    return None

def fix_paper_authors(md_path: Path) -> Tuple[bool, str]:
    """Fix authors in a single paper"""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if YAML frontmatter exists
        yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not yaml_match:
            return False, "No YAML frontmatter found"
        
        yaml_content = yaml_match.group(1)
        rest_content = content[yaml_match.end():]
        
        # Extract current authors
        authors_match = re.search(r'^authors: "([^"]+)"', yaml_content, re.MULTILINE)
        if not authors_match:
            return False, "No authors field found"
        
        current_authors = authors_match.group(1)
        
        # Check if authors look like email prefixes
        if re.match(r'^[a-z]+(?:,\s*[a-z]+)*$', current_authors):
            # Get title for manual lookup
            title_match = re.search(r'^title: "([^"]+)"', yaml_content, re.MULTILINE)
            title = title_match.group(1) if title_match else ""
            
            # Check manual corrections first
            new_authors = None
            for pattern, correct_authors in AUTHOR_CORRECTIONS.items():
                if pattern.lower() in title.lower():
                    new_authors = correct_authors
                    break
            
            # If no manual correction, try to extract from content
            if not new_authors:
                new_authors = extract_authors_from_content(rest_content)
            
            if new_authors:
                # Replace authors in YAML
                new_yaml = re.sub(
                    r'^authors: "[^"]+"',
                    f'authors: "{new_authors}"',
                    yaml_content,
                    flags=re.MULTILINE
                )
                
                # Write back
                new_content = f"---\n{new_yaml}\n---\n{rest_content}"
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True, f"{current_authors} -> {new_authors}"
        
        return False, "Authors look correct"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Fix author extraction issues in all papers"""
    markdown_papers = Path("markdown_papers")
    
    # Find papers with potential author issues
    papers_to_fix = []
    
    print("Scanning for papers with author extraction issues...")
    for folder in markdown_papers.iterdir():
        if folder.is_dir():
            md_path = folder / "paper.md"
            if md_path.exists():
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read(500)
                    
                    # Check for email-like authors
                    if re.search(r'^authors: "[a-z]+(?:,\s*[a-z]+)*"', content, re.MULTILINE):
                        papers_to_fix.append(md_path)
                except:
                    continue
    
    print(f"Found {len(papers_to_fix)} papers with potential author issues")
    
    # Fix each paper
    fixed_count = 0
    results = []
    
    for md_path in papers_to_fix:
        success, message = fix_paper_authors(md_path)
        if success:
            fixed_count += 1
            print(f"✓ Fixed: {md_path.parent.name}")
            print(f"  {message}")
        else:
            print(f"✗ Skipped: {md_path.parent.name} - {message}")
        
        results.append({
            'path': str(md_path),
            'folder': md_path.parent.name,
            'success': success,
            'message': message
        })
    
    # Save results
    with open('author_fix_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_papers': len(papers_to_fix),
            'fixed': fixed_count,
            'results': results
        }, f, indent=2)
    
    print(f"\nFixed {fixed_count} out of {len(papers_to_fix)} papers")
    print("Results saved to: author_fix_results.json")

if __name__ == "__main__":
    main()
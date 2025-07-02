"""
Improved author extraction from markdown papers
Cleans up HTML, superscripts, and extracts all author names
"""
import re
from pathlib import Path
from typing import List, Optional, Tuple


def extract_clean_authors(markdown_path: Path, lines_to_scan: int = 50) -> Optional[str]:
    """
    Extract clean author names from the first N lines of a markdown file.
    
    Args:
        markdown_path: Path to markdown file
        lines_to_scan: Number of lines to scan from the beginning (default: 50)
    
    Returns:
        Clean author string or None if not found
    """
    try:
        with open(markdown_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:lines_to_scan]
        
        content = '\n'.join(lines)
        
        # Skip YAML frontmatter if present
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
        
        # Look for author patterns
        authors = find_authors_in_content(content)
        
        if authors:
            # Clean and format authors
            cleaned_authors = clean_author_list(authors)
            return ', '.join(cleaned_authors)
        
        return None
        
    except Exception as e:
        print(f"Error reading {markdown_path}: {e}")
        return None


def find_authors_in_content(content: str) -> List[str]:
    """Find author names in content using various patterns."""
    authors = []
    
    # Pattern 1: Authors after title, before affiliations
    # Look for lines that contain author-like names with commas or "and"
    lines = content.split('\n')
    
    # Skip empty lines and find potential author lines
    found_title = False
    author_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Identify title (usually starts with # or is in all caps)
        if line.startswith('#') and not found_title:
            found_title = True
            continue
        
        # After title, look for author patterns
        if found_title and not line.startswith('#'):
            # Check if line contains affiliation indicators - if so, we're past authors
            if any(indicator in line.lower() for indicator in ['university', 'institute', 'department', 
                                                               'school', 'college', 'laboratory', 
                                                               'abstract', 'keywords', 'introduction',
                                                               'article info', '©', 'copyright', 
                                                               'a r t i c l e', 'received', 'revised']):
                # But don't break if it's an author line with superscripts
                if not re.search(r'[A-Z][a-z]+.*<sup>', line):
                    break
            
            # Check if line looks like authors
            if re.search(r'[A-Z][a-z]+', line) and not line.startswith('![]'):
                # This line likely contains authors
                author_lines.append(line)
    
    # Parse author lines
    for line in author_lines:
        # First, check if this is a complex author line with superscripts
        # Pattern: Name<sup>x</sup>, Name<sup>y</sup>, etc.
        if '<sup>' in line or '*<sup>' in line:
            # Extract names before superscripts - more flexible pattern
            # This handles: Name Name*<sup>x</sup>*, Name Name <sup>y</sup>, etc.
            name_pattern = r'([A-Z][a-z]+(?:\s+[A-Z]\.?)*(?:\s+[A-Z][a-z]+)+)\s*\*?\s*(?:<sup>|,)'
            matches = re.findall(name_pattern, line)
            for match in matches:
                if is_valid_author_name(match):
                    authors.append(match)
        
        # If no superscripts found, try regular parsing
        if not authors:
            # Remove HTML tags and markdown
            clean_line = remove_html_and_markdown(line)
            
            # Split by common separators
            if ' and ' in clean_line.lower():
                parts = re.split(r'\s+and\s+', clean_line, flags=re.IGNORECASE)
            elif ' & ' in clean_line:
                parts = clean_line.split(' & ')
            elif ';' in clean_line:
                parts = clean_line.split(';')
            else:
                parts = clean_line.split(',')
            
            for part in parts:
                part = part.strip()
                if is_valid_author_name(part):
                    authors.append(part)
    
    # If no authors found with above method, try alternative patterns
    if not authors:
        # Pattern 2: Look for author pattern with asterisk (Nathan Leroy \*, Steve Majerus, etc)
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            # Look for lines with author pattern and asterisk/backslash
            if re.search(r'[A-Z][a-z]+.*\\?\*', line):
                # Clean the line and extract names
                clean_line = re.sub(r'\\?\*+', '', line)
                clean_line = remove_html_and_markdown(clean_line)
                
                # Split by comma or and
                if ' and ' in clean_line.lower():
                    parts = re.split(r'\s+and\s+', clean_line, flags=re.IGNORECASE)
                else:
                    parts = clean_line.split(',')
                
                for part in parts:
                    part = part.strip()
                    if is_valid_author_name(part):
                        authors.append(part)
                
                if authors:
                    break
        
        # Pattern 3: Look for lines starting with author names
        if not authors:
            author_pattern = r'^([A-Z][a-z]+(?:\s+[A-Z]\.?)?(?:\s+[A-Z][a-z]+)+)'
            for line in lines:
                if not line.strip():
                    continue
                match = re.match(author_pattern, line.strip())
                if match:
                    name = match.group(1)
                    if is_valid_author_name(name):
                        authors.append(name)
    
    return authors


def remove_html_and_markdown(text: str) -> str:
    """Remove HTML tags, markdown links, and clean up text."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove markdown links [text](url)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove superscripts *<sup>x</sup>*
    text = re.sub(r'\*?<sup>[^<]+</sup>\*?', '', text)
    text = re.sub(r'\*\*?sup\*\*?[a-z0-9,]+\*\*?', '', text)
    
    # Remove asterisks
    text = re.sub(r'\*+', '', text)
    
    # Remove reference numbers in brackets
    text = re.sub(r'\[[0-9,\s]+\]', '', text)
    
    # Remove et al.
    text = re.sub(r'\s+et\s+al\.?', '', text, flags=re.IGNORECASE)
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def clean_author_list(authors: List[str]) -> List[str]:
    """Clean and validate author names."""
    cleaned = []
    
    for author in authors:
        # Remove any remaining HTML/markdown
        author = remove_html_and_markdown(author)
        
        # Remove email addresses
        author = re.sub(r'\S+@\S+', '', author)
        
        # Remove numbers and special characters at the end
        author = re.sub(r'[0-9,\*\†\‡\§\¶\#]+$', '', author).strip()
        
        # Remove trailing commas
        author = author.rstrip(',').strip()
        
        # Validate and add
        if is_valid_author_name(author):
            cleaned.append(author)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_authors = []
    for author in cleaned:
        if author.lower() not in seen:
            seen.add(author.lower())
            unique_authors.append(author)
    
    return unique_authors


def is_valid_author_name(name: str) -> bool:
    """Check if a string is likely an author name."""
    if not name or len(name) < 3:
        return False
    
    # Should have at least one space (first and last name) or initial
    if ' ' not in name and '.' not in name:
        return False
    
    # Should start with capital letter
    if not re.match(r'^[A-Z]', name):
        return False
    
    # Should not be too long
    if len(name) > 50:
        return False
    
    # Should not contain certain keywords
    exclude_keywords = ['abstract', 'keywords', 'introduction', 'article', 
                       'university', 'department', 'institute', 'school',
                       'email', 'corresponding', 'author', 'address',
                       'received', 'revised', 'accepted', 'available',
                       'elsevier', 'copyright', 'reserved', 'published',
                       'technology', 'information', 'science', 'college']
    if any(keyword in name.lower() for keyword in exclude_keywords):
        return False
    
    # Should not contain numbers at the beginning
    if re.match(r'^\d', name):
        return False
    
    # Should contain mostly letters
    letter_ratio = sum(1 for c in name if c.isalpha()) / len(name)
    if letter_ratio < 0.5:
        return False
    
    return True


def extract_title_from_markdown(markdown_path: Path, lines_to_scan: int = 50) -> Optional[str]:
    """Extract clean title from markdown file."""
    try:
        with open(markdown_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:lines_to_scan]
        
        content = '\n'.join(lines)
        
        # Skip YAML frontmatter if present
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
        
        # Look for title patterns
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and images
            if not line or line.startswith('!['):
                continue
            
            # Pattern 1: Markdown header
            if line.startswith('#'):
                title = line.lstrip('#').strip()
                # Clean title
                title = remove_html_and_markdown(title)
                if len(title) > 10:  # Reasonable title length
                    return title
            
            # Pattern 2: Line that looks like a title (all caps or title case)
            if len(line) > 10 and not any(char in line for char in ['@', 'http', 'www']):
                # Check if it's mostly uppercase or title case
                if line.isupper() or (sum(1 for c in line if c.isupper()) / len(line) > 0.3):
                    return remove_html_and_markdown(line)
        
        return None
        
    except Exception as e:
        print(f"Error extracting title from {markdown_path}: {e}")
        return None


# Test the functions
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_file = Path(sys.argv[1])
        if test_file.exists():
            print(f"Testing on: {test_file}")
            authors = extract_clean_authors(test_file)
            title = extract_title_from_markdown(test_file)
            print(f"Title: {title}")
            print(f"Authors: {authors}")
        else:
            print(f"File not found: {test_file}")
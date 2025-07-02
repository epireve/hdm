"""
Shared utilities for Phase 2 scripts
"""
import os
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re

from config import LOG_DIR, LOG_FORMAT, LOG_LEVEL, BACKUP_DIR


def setup_logging(script_name: str) -> logging.Logger:
    """Setup logging for a script"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"{script_name}_{timestamp}.log"
    
    logger = logging.getLogger(script_name)
    logger.setLevel(LOG_LEVEL)
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(LOG_LEVEL)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


def create_backup(source_dir: Path, backup_name: str) -> Path:
    """Create a backup of a directory"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"{backup_name}_{timestamp}"
    
    shutil.copytree(source_dir, backup_path)
    return backup_path


def save_json(data: dict, file_path: Path) -> None:
    """Save data to JSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(file_path: Path) -> dict:
    """Load data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_author_year(authors_str: str, year_str: str) -> Tuple[str, str]:
    """Extract first author's last name and year"""
    # Clean up authors string
    authors_str = authors_str.strip()
    
    # Handle "et al." cases
    if "et al." in authors_str:
        authors_str = authors_str.split("et al.")[0].strip()
    
    # Split by comma or semicolon
    if "," in authors_str:
        first_author = authors_str.split(",")[0].strip()
    elif ";" in authors_str:
        first_author = authors_str.split(";")[0].strip()
    else:
        first_author = authors_str.strip()
    
    # Extract last name (handle various formats)
    # Remove any numbers or special characters
    first_author = re.sub(r'[0-9\*\†\‡\§\¶\#]', '', first_author).strip()
    
    # Split by spaces and get the last part as last name
    name_parts = first_author.split()
    if name_parts:
        last_name = name_parts[-1]
    else:
        last_name = "unknown"
    
    # Clean up last name
    last_name = re.sub(r'[^a-zA-Z\-]', '', last_name).lower()
    
    # Clean up year
    year = re.sub(r'[^0-9]', '', str(year_str))
    if not year:
        year = "nd"  # no date
    
    return last_name, year


def generate_cite_key(last_name: str, year: str, existing_keys: set) -> str:
    """Generate a unique cite key"""
    base_key = f"{last_name}{year}"
    
    # If base key is unique, use it
    if base_key not in existing_keys:
        return base_key
    
    # Otherwise, add suffix
    suffix = 'b'
    while True:
        new_key = f"{base_key}{suffix}"
        if new_key not in existing_keys:
            return new_key
        # Increment suffix
        suffix = chr(ord(suffix) + 1)


def parse_markdown_table(file_path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    """Parse a markdown table and return headers and rows"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    headers = []
    rows = []
    in_table = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if it's a table row
        if line.startswith("|") and line.endswith("|"):
            if not in_table:
                # First table row is headers
                headers = [h.strip() for h in line.split("|")[1:-1]]
                in_table = True
            elif line.startswith("| :---") or line.startswith("|:---") or line.startswith("| ---"):
                # Skip separator row
                continue
            else:
                # Data row
                values = [v.strip() for v in line.split("|")[1:-1]]
                if len(values) == len(headers):
                    row_dict = dict(zip(headers, values))
                    rows.append(row_dict)
    
    return headers, rows


def write_markdown_table(headers: List[str], rows: List[Dict[str, str]], file_path: Path) -> None:
    """Write a markdown table to file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        # Write headers
        f.write("| " + " | ".join(headers) + " |\n")
        
        # Write separator
        f.write("| " + " | ".join([":---" for _ in headers]) + " |\n")
        
        # Write rows
        for row in rows:
            values = [row.get(h, "") for h in headers]
            f.write("| " + " | ".join(values) + " |\n")


def extract_title_from_markdown(file_path: Path) -> Optional[str]:
    """Extract title from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Look for first H1 header
    for line in lines[:20]:  # Check first 20 lines
        if line.startswith("# "):
            return line[2:].strip()
    
    return None


def extract_metadata_from_markdown(file_path: Path) -> Dict[str, any]:
    """Extract metadata from markdown file"""
    metadata = {
        'title': None,
        'authors': None,
        'year': None,
        'journal': None,
        'doi': None
    }
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    
    # Extract authors (look for common patterns)
    authors_patterns = [
        r'^([^#\n]+)\n+[^#\n]*(?:University|Institute|Department|School)',
        r'^Authors?:\s*(.+)$',
        r'^By\s+(.+)$'
    ]
    
    for pattern in authors_patterns:
        match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
        if match:
            metadata['authors'] = match.group(1).strip()
            break
    
    # Extract year
    year_match = re.search(r'\b(20\d{2})\b', content)
    if year_match:
        metadata['year'] = year_match.group(1)
    
    # Extract DOI
    doi_match = re.search(r'10\.\d{4,}/[-._;()/:\w]+', content)
    if doi_match:
        metadata['doi'] = doi_match.group(0)
    
    return metadata


class ProgressTracker:
    """Track processing progress"""
    def __init__(self, total: int, logger: logging.Logger):
        self.total = total
        self.current = 0
        self.logger = logger
        self.start_time = datetime.now()
    
    def update(self, message: str = ""):
        """Update progress"""
        self.current += 1
        percent = (self.current / self.total) * 100
        elapsed = datetime.now() - self.start_time
        
        if self.current > 0:
            rate = self.current / elapsed.total_seconds()
            eta = (self.total - self.current) / rate if rate > 0 else 0
            eta_str = str(datetime.fromtimestamp(eta).strftime('%M:%S'))
        else:
            eta_str = "N/A"
        
        self.logger.info(f"Progress: {self.current}/{self.total} ({percent:.1f}%) - ETA: {eta_str} - {message}")


def read_json(file_path: Path) -> dict:
    """Read data from JSON file"""
    return load_json(file_path)


def write_json(data: dict, file_path: Path) -> None:
    """Write data to JSON file"""
    save_json(data, file_path)


def parse_markdown_content(content: str) -> Dict[str, any]:
    """Parse markdown content and extract structure"""
    lines = content.split('\n')
    result = {
        "headers": [],
        "images": [],
        "code_blocks": [],
        "links": []
    }
    
    for i, line in enumerate(lines):
        # Extract headers
        if line.startswith('#'):
            level = len(line.split()[0])
            title = line[level:].strip()
            result["headers"].append({
                "level": level,
                "title": title,
                "line": i
            })
        
        # Extract images
        import re
        images = re.findall(r'!\[([^\]]*)\]\(([^\)]+)\)', line)
        for alt_text, url in images:
            result["images"].append({
                "alt_text": alt_text,
                "url": url,
                "line": i
            })
    
    return result


def should_remove_image(image_path: str, remove_patterns: List[str]) -> bool:
    """Check if an image should be removed based on patterns"""
    from fnmatch import fnmatch
    
    for pattern in remove_patterns:
        if fnmatch(image_path.lower(), pattern.lower()):
            return True
    
    return False
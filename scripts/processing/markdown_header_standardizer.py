#!/usr/bin/env python3
"""
Comprehensive Markdown Header Standardizer
Standardizes header hierarchy and formatting across all papers in markdown_papers/
"""

import re
from pathlib import Path
from datetime import datetime
import json

def extract_yaml_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if yaml_match:
        yaml_content = yaml_match.group(1)
        remaining_content = content[yaml_match.end():]
        return yaml_content, remaining_content
    return None, content

def standardize_headers(content):
    """Standardize header hierarchy and formatting"""
    lines = content.split('\n')
    standardized_lines = []
    
    # Track header levels for proper hierarchy
    title_found = False
    
    for i, line in enumerate(lines):
        # Skip empty lines at the start
        if not line.strip() and not standardized_lines:
            continue
            
        # Detect headers
        header_match = re.match(r'^(#{1,6})\s*(.*)', line.strip())
        
        if header_match:
            level = len(header_match.group(1))
            header_text = header_match.group(2).strip()
            
            # Skip if header text is empty
            if not header_text:
                continue
            
            # First non-empty header should be the main title (H1)
            if not title_found and header_text:
                # Main paper title - always H1
                standardized_lines.append(f"# {header_text}")
                title_found = True
            else:
                # Handle other headers with proper hierarchy
                if level == 1:
                    # Secondary titles should be H2
                    standardized_lines.append(f"## {header_text}")
                elif level == 2:
                    # Keep as H2 for main sections
                    standardized_lines.append(f"## {header_text}")
                elif level >= 3:
                    # Subsections as H3
                    standardized_lines.append(f"### {header_text}")
        else:
            # Non-header line - process for formatting
            processed_line = clean_line_formatting(line)
            standardized_lines.append(processed_line)
    
    return '\n'.join(standardized_lines)

def clean_line_formatting(line):
    """Clean up line formatting issues"""
    # Remove excessive whitespace
    line = re.sub(r'\s+', ' ', line.strip())
    
    # Fix common formatting issues
    # Remove asterisks around abstracts, conclusions etc.
    line = re.sub(r'^\*([A-Z][a-zA-Z\s]+)\*—', r'**\1:** ', line)
    line = re.sub(r'^\*([A-Z][a-zA-Z\s]+)\*\s*[:—-]?', r'**\1:** ', line)
    
    # Standardize bold text formatting
    line = re.sub(r'\*\*([^*]+)\*\*', r'**\1**', line)
    
    # Clean up author affiliations and email formatting
    line = re.sub(r'\*([^*]+)\*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r'*\1* \2', line)
    
    # Standardize figure references
    line = re.sub(r'Fig\.\s*(\d+)', r'Figure \1', line)
    line = re.sub(r'Figure\s*(\d+):', r'**Figure \1:**', line)
    
    # Standardize table references
    line = re.sub(r'Table\s*(\d+):', r'**Table \1:**', line)
    
    return line

def remove_redundant_elements(content):
    """Remove redundant or problematic elements"""
    lines = content.split('\n')
    cleaned_lines = []
    
    # Patterns to remove
    remove_patterns = [
        r'^<span id="page-\d+-\d+"></span>$',  # Page span tags
        r'^\s*\*\*?prefix\s+[^:]+:\s*<[^>]+>\s*\*\*?',  # SPARQL prefixes
        r'^\s*Received:.*?Accepted:.*$',  # Publication dates
        r'^\s*V?C?\s*The Author\(s\).*Published by.*$',  # Copyright notices
        r'^\s*This is an Open Access.*properly cited\.$',  # License text
    ]
    
    skip_next = False
    
    for i, line in enumerate(lines):
        # Skip if marked
        if skip_next:
            skip_next = False
            continue
            
        # Check if line should be removed
        should_remove = False
        for pattern in remove_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                should_remove = True
                break
        
        if should_remove:
            continue
            
        # Special handling for author lines that appear after titles
        if line.strip() and not line.startswith('#'):
            # Check if this looks like a misplaced author line after a title
            if (i > 0 and lines[i-1].startswith('#') and 
                re.match(r'^[A-Z][a-zA-Z\s,]+(\d+)?[,\s]*[a-zA-Z\s]*(@|\*|$)', line.strip())):
                # This is likely an author line that should be cleaned up
                line = clean_author_line(line)
        
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def clean_author_line(line):
    """Clean up author and affiliation lines"""
    # Standardize author formatting
    line = re.sub(r'\s*\*([^*]+)\*\s*', r' *\1* ', line)
    line = re.sub(r'\s+', ' ', line.strip())
    
    # Ensure proper spacing around affiliations
    line = re.sub(r'([a-zA-Z])\s*\*([^*]+)\*', r'\1 *\2*', line)
    
    return line

def add_proper_spacing(content):
    """Add proper spacing between sections"""
    lines = content.split('\n')
    spaced_lines = []
    
    for i, line in enumerate(lines):
        # Add line
        spaced_lines.append(line)
        
        # Add spacing after headers (except before other headers)
        if line.startswith('#') and i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            if next_line and not next_line.startswith('#'):
                spaced_lines.append('')
        
        # Add spacing before headers (except at the start)
        elif (i < len(lines) - 1 and lines[i + 1].startswith('#') and 
              line.strip() and i > 0):
            spaced_lines.append('')
    
    return '\n'.join(spaced_lines)

def standardize_paper(paper_path):
    """Standardize a single paper's markdown"""
    try:
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract YAML frontmatter
        yaml_content, markdown_content = extract_yaml_frontmatter(content)
        
        if not yaml_content:
            print(f"Warning: No YAML frontmatter found in {paper_path}")
            return False
        
        # Standardize the markdown content
        standardized_content = standardize_headers(markdown_content)
        standardized_content = remove_redundant_elements(standardized_content)
        standardized_content = add_proper_spacing(standardized_content)
        
        # Reconstruct the file
        final_content = f"---\n{yaml_content}\n---\n\n{standardized_content}"
        
        # Write back to file
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        return True
        
    except Exception as e:
        print(f"Error processing {paper_path}: {e}")
        return False

def main():
    """Main standardization function"""
    print("🔧 Starting Markdown Header Standardization")
    print("=" * 60)
    
    markdown_papers_dir = Path('markdown_papers')
    
    if not markdown_papers_dir.exists():
        print("Error: markdown_papers directory not found")
        return
    
    # Get all paper directories
    paper_folders = [f for f in markdown_papers_dir.iterdir() if f.is_dir()]
    
    print(f"Found {len(paper_folders)} paper folders")
    
    # Process each paper
    processed_count = 0
    error_count = 0
    
    for folder in sorted(paper_folders):
        paper_file = folder / 'paper.md'
        
        if not paper_file.exists():
            print(f"Warning: No paper.md found in {folder.name}")
            continue
        
        print(f"Processing: {folder.name}")
        
        if standardize_paper(paper_file):
            processed_count += 1
        else:
            error_count += 1
    
    # Generate report
    print("\n" + "=" * 60)
    print("📊 Standardization Summary:")
    print(f"  Total folders: {len(paper_folders)}")
    print(f"  Successfully processed: {processed_count}")
    print(f"  Errors: {error_count}")
    print(f"  Success rate: {processed_count/(processed_count+error_count)*100:.1f}%")
    
    # Create report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_folders': len(paper_folders),
        'processed': processed_count,
        'errors': error_count,
        'success_rate': processed_count/(processed_count+error_count)*100 if (processed_count+error_count) > 0 else 0
    }
    
    report_path = Path('reports/current/markdown_standardization_report.json')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📋 Report saved to: {report_path}")
    
    print("\n✅ Header standardization completed!")
    print("\n🎯 Key Improvements Made:")
    print("  - Proper header hierarchy (H1 for title, H2 for sections, H3 for subsections)")
    print("  - Removed redundant elements (page spans, copyright notices)")
    print("  - Standardized figure and table references")
    print("  - Improved author and affiliation formatting")
    print("  - Added proper spacing between sections")
    print("  - Cleaned up bold text formatting")

if __name__ == '__main__':
    main()
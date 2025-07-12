#!/usr/bin/env python3
"""
Comprehensive markdown standardizer
- Removes quotes from frontmatter
- Removes logos and non-research images
- Standardizes formatting
- Makes content professional and readable
"""
import re
import os
from pathlib import Path
from datetime import datetime
import shutil

def parse_yaml_frontmatter(content):
    """Parse YAML frontmatter and return it with the rest of content"""
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not yaml_match:
        return None, content
    
    yaml_str = yaml_match.group(1)
    rest_content = content[yaml_match.end():]
    
    return yaml_str, rest_content

def clean_yaml_value(value):
    """Remove unnecessary quotes from YAML values"""
    # Remove surrounding quotes
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    
    # Only add quotes back if necessary (contains special characters)
    if ':' in value or '|' in value or value.startswith('@') or value.startswith('*'):
        return f'"{value}"'
    
    return value

def standardize_yaml_frontmatter(yaml_str):
    """Standardize YAML frontmatter formatting"""
    lines = yaml_str.split('\n')
    standardized_lines = []
    
    in_tags = False
    in_keywords = False
    
    for line in lines:
        if line.strip() == 'tags:':
            in_tags = True
            in_keywords = False
            standardized_lines.append(line)
        elif line.strip() == 'keywords:':
            in_keywords = True
            in_tags = False
            standardized_lines.append(line)
        elif line.startswith('  -'):
            # Handle list items (tags/keywords)
            item = line.replace('  -', '').strip()
            item = clean_yaml_value(item)
            standardized_lines.append(f'  - {item}')
        elif ':' in line and not line.startswith(' '):
            # Handle key-value pairs
            in_tags = False
            in_keywords = False
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ''
            
            # Special handling for certain fields
            if key in ['title', 'authors', 'cite_key', 'doi', 'url']:
                value = clean_yaml_value(value)
            
            standardized_lines.append(f'{key}: {value}')
        else:
            standardized_lines.append(line)
    
    return '\n'.join(standardized_lines)

def is_logo_or_brand_image(image_file, content_around):
    """Detect if an image is likely a logo or brand image"""
    image_file_lower = image_file.lower()
    content_lower = content_around.lower()
    
    # Check filename patterns
    logo_patterns = [
        'logo', 'brand', 'sponsor', 'partner', 'copyright', 
        'publisher', 'journal', 'elsevier', 'springer', 'wiley',
        'ieee', 'acm', 'footer', 'header', 'banner', 'watermark'
    ]
    
    for pattern in logo_patterns:
        if pattern in image_file_lower:
            return True
    
    # Check surrounding text
    if any(word in content_lower for word in ['copyright', 'all rights reserved', 'published by']):
        return True
    
    # Check if it's a very small figure number (often logos)
    if re.search(r'Figure_[0-9]\.jpeg$', image_file) and '_page_1_' in image_file:
        # First page single digit figures are often logos
        return True
    
    return False

def clean_markdown_content(content):
    """Clean and standardize markdown content"""
    # Remove HTML comments that are not image descriptions
    content = re.sub(r'<!--(?!.*Image Description:).*?-->', '', content, flags=re.DOTALL)
    
    # Remove excessive blank lines (more than 2 consecutive)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Remove trailing spaces
    lines = content.split('\n')
    cleaned_lines = [line.rstrip() for line in lines]
    content = '\n'.join(cleaned_lines)
    
    # Standardize headers (ensure space after #)
    content = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', content, flags=re.MULTILINE)
    
    # Remove fancy Unicode characters (keeping standard ones)
    replacements = {
        '"': '"', '"': '"',  # Smart quotes to regular
        ''': "'", ''': "'",  # Smart single quotes
        '…': '...',          # Ellipsis
        '–': '-', '—': '-',  # Em and en dashes
        '\u200b': '',        # Zero-width space
        '\xa0': ' ',         # Non-breaking space
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Standardize list formatting
    content = re.sub(r'^(\s*)[*•·]\s+', r'\1- ', content, flags=re.MULTILINE)
    
    # Remove page span tags if they're empty
    content = re.sub(r'<span[^>]*></span>\s*\n', '', content)
    
    return content

def process_paper(paper_path, remove_images=True):
    """Process a single paper to standardize it"""
    print(f"Processing: {paper_path.parent.name}")
    
    try:
        # Read content
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Backup original
        backup_path = paper_path.parent / f"{paper_path.stem}_original{paper_path.suffix}"
        if not backup_path.exists():
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Parse frontmatter
        yaml_str, rest_content = parse_yaml_frontmatter(content)
        
        if yaml_str:
            # Standardize frontmatter
            standardized_yaml = standardize_yaml_frontmatter(yaml_str)
            
            # Process content
            processed_content = rest_content
            
            # Find and handle images
            if remove_images:
                images_to_remove = []
                image_pattern = r'(!\[\]\(([^)]+)\)(?:\s*\n\s*<!-- Image Description:.*?-->)?)'
                
                for match in re.finditer(image_pattern, processed_content, re.DOTALL):
                    full_match = match.group(0)
                    image_file = match.group(2)
                    
                    # Get context around image (100 chars before and after)
                    start_pos = max(0, match.start() - 100)
                    end_pos = min(len(processed_content), match.end() + 100)
                    context = processed_content[start_pos:end_pos]
                    
                    if is_logo_or_brand_image(image_file, context):
                        images_to_remove.append((full_match, image_file))
                
                # Remove logo images
                for full_match, image_file in images_to_remove:
                    processed_content = processed_content.replace(full_match, '')
                    
                    # Try to delete the actual image file
                    image_path = paper_path.parent / image_file
                    if image_path.exists():
                        print(f"  - Removing logo/brand image: {image_file}")
                        os.remove(image_path)
            
            # Clean content
            processed_content = clean_markdown_content(processed_content)
            
            # Reconstruct full content
            new_content = f"---\n{standardized_yaml}\n---\n{processed_content}"
            
            # Write back
            with open(paper_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✓ Standardized successfully")
            return True
            
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False

def main():
    """Main function"""
    import sys
    
    print("Markdown Standardizer")
    print("=" * 60)
    print("Features:")
    print("- Remove quotes from frontmatter")
    print("- Remove logos and brand images")
    print("- Standardize formatting")
    print("- Clean up content")
    print("=" * 60)
    
    markdown_papers = Path('markdown_papers')
    
    # Get papers to process
    if len(sys.argv) > 1:
        # Specific papers provided
        papers_to_process = []
        for arg in sys.argv[1:]:
            paper_path = markdown_papers / arg / 'paper.md'
            if paper_path.exists():
                papers_to_process.append(paper_path)
    else:
        # Process all papers
        papers_to_process = []
        for folder in sorted(markdown_papers.iterdir()):
            if folder.is_dir():
                paper_path = folder / 'paper.md'
                if paper_path.exists():
                    papers_to_process.append(paper_path)
    
    print(f"Papers to process: {len(papers_to_process)}")
    
    # Process each paper
    processed = 0
    for paper_path in papers_to_process:
        if process_paper(paper_path):
            processed += 1
    
    print("\n" + "=" * 60)
    print(f"Processing complete: {processed}/{len(papers_to_process)} papers standardized")
    
    # Create report
    report_file = Path(f'markdown_standardization_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
    with open(report_file, 'w') as f:
        f.write(f"Markdown Standardization Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"="*60 + "\n")
        f.write(f"Total papers processed: {processed}/{len(papers_to_process)}\n")
    
    print(f"Report saved to: {report_file}")

if __name__ == '__main__':
    main()
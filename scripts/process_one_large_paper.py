#!/usr/bin/env python3
"""
Process a single large paper efficiently with chunk-based processing
"""

import sys
import json
import csv
import urllib.request
import urllib.error
import ssl
import os
from pathlib import Path
from datetime import datetime
import time

# Add parent directory
sys.path.append(str(Path(__file__).parent.parent))

from lib.kilocode_config_simple import load_config, ConfigurationError


def load_csv_data():
    """Load CSV data"""
    csv_data = {}
    csv_path = "hdm_research_papers_merged_20250710.csv"
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cite_key = row.get('cite_key', '').strip()
            if cite_key:
                csv_data[cite_key] = row
    
    return csv_data


def call_gemini_api(config, ssl_context, prompt):
    """Call Gemini API"""
    url = config.openrouter_url + "/chat/completions"
    
    data = {
        "model": "google/gemini-2.5-pro-preview",
        "messages": [
            {"role": "system", "content": "You are an expert academic paper formatter. Preserve ALL content."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 100000
    }
    
    headers = {
        "Authorization": f"Bearer {config.token}",
        "Content-Type": "application/json",
        "HTTP-Referer": config.http_referer,
        "X-Title": config.x_title
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, context=ssl_context, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            
            # Show token usage
            if 'usage' in result:
                usage = result['usage']
                print(f"📊 Tokens - Input: {usage.get('prompt_tokens', 0)}, Output: {usage.get('completion_tokens', 0)}")
            
            return content
    except Exception as e:
        print(f"❌ API error: {e}")
        return None


def create_simple_standardization_prompt(content, csv_row, cite_key):
    """Create a simple standardization prompt"""
    return f"""Standardize this academic paper by adding these sections while preserving ALL original content:

1. After the Abstract section, add:
## TL;DR
{csv_row.get('TL;DR', 'Not available')}

## Key Insights  
{csv_row.get('Insights', 'Not available')}

2. At the very end, add:
## Metadata Summary
### Research Context
- **Research Question**: {csv_row.get('Research Question', 'Not available')}
- **Methodology**: {csv_row.get('Methodology', 'Not available')}
- **Key Findings**: {csv_row.get('Key Findings', 'Not available')}

### Analysis
- **Limitations**: {csv_row.get('Limitations', 'Not available')}
- **Future Work**: {csv_row.get('Future Work', 'Not available')}

PAPER TO PROCESS:
{content}

CRITICAL: Preserve every single line of the original paper. Only add the new sections as specified above.
Return the complete paper with the new sections added."""


def process_large_paper(cite_key):
    """Process a single large paper"""
    print(f"Processing {cite_key}...")
    
    # Load config
    try:
        config = load_config()
    except ConfigurationError as e:
        print(f"❌ Config error: {e}")
        return False
    
    # SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Load CSV data
    csv_data = load_csv_data()
    
    # Check paper exists
    paper_path = Path(f"markdown_papers/{cite_key}/paper.md")
    if not paper_path.exists():
        print(f"❌ Paper not found: {paper_path}")
        return False
    
    # Get CSV data
    csv_row = csv_data.get(cite_key, {})
    
    # Read content
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📄 Read {len(content)} chars, {content.count(chr(10))} lines")
    
    # Create backup
    backup_dir = Path(f"paper_backups/{cite_key}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_file = backup_dir / f"paper_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Backup saved")
    
    # For very large papers, split into sections
    if len(content) > 60000:
        print("📄 Large paper detected - using section-based processing")
        
        # Split by major sections
        sections = content.split('\n## ')
        
        if len(sections) > 1:
            # Process first part (includes frontmatter + abstract)
            first_part = sections[0]
            
            # Find where to insert TL;DR (after abstract)
            abstract_end = -1
            lines = first_part.split('\n')
            for i, line in enumerate(lines):
                if line.strip().lower().startswith('## ') and 'abstract' in line.lower():
                    # Find next section or end
                    for j in range(i+1, len(lines)):
                        if lines[j].strip().startswith('## ') or j == len(lines)-1:
                            abstract_end = j
                            break
                    break
            
            if abstract_end > 0:
                # Insert TL;DR and Key Insights after abstract
                new_sections = [
                    f"\n## TL;DR\n{csv_row.get('TL;DR', 'Not available')}",
                    f"\n## Key Insights\n{csv_row.get('Insights', 'Not available')}"
                ]
                
                lines.insert(abstract_end, '\n'.join(new_sections))
                processed_content = '\n'.join(lines)
                
                # Add remaining sections
                for i, section in enumerate(sections[1:], 1):
                    processed_content += '\n## ' + section
                
                # Add metadata at the end
                metadata = f"""
## Metadata Summary
### Research Context
- **Research Question**: {csv_row.get('Research Question', 'Not available')}
- **Methodology**: {csv_row.get('Methodology', 'Not available')}
- **Key Findings**: {csv_row.get('Key Findings', 'Not available')}

### Analysis
- **Limitations**: {csv_row.get('Limitations', 'Not available')}
- **Future Work**: {csv_row.get('Future Work', 'Not available')}"""
                
                processed_content += metadata
                
            else:
                # Fallback: just add at the end
                processed_content = content + f"""

## TL;DR
{csv_row.get('TL;DR', 'Not available')}

## Key Insights
{csv_row.get('Insights', 'Not available')}

## Metadata Summary
### Research Context
- **Research Question**: {csv_row.get('Research Question', 'Not available')}
- **Methodology**: {csv_row.get('Methodology', 'Not available')}
- **Key Findings**: {csv_row.get('Key Findings', 'Not available')}

### Analysis
- **Limitations**: {csv_row.get('Limitations', 'Not available')}
- **Future Work**: {csv_row.get('Future Work', 'Not available')}"""
        else:
            # Single section paper
            processed_content = content + f"""

## TL;DR
{csv_row.get('TL;DR', 'Not available')}

## Key Insights
{csv_row.get('Insights', 'Not available')}

## Metadata Summary
### Research Context
- **Research Question**: {csv_row.get('Research Question', 'Not available')}"""
        
        standardized_content = processed_content
        
    else:
        # Regular processing for medium papers
        prompt = create_simple_standardization_prompt(content, csv_row, cite_key)
        standardized_content = call_gemini_api(config, ssl_context, prompt)
        
        if not standardized_content:
            return False
        
        # Clean response
        if standardized_content.startswith('```markdown'):
            standardized_content = standardized_content[11:]
        if standardized_content.endswith('```'):
            standardized_content = standardized_content[:-3]
        standardized_content = standardized_content.strip()
    
    if not standardized_content:
        print("❌ No standardized content generated")
        return False
    
    # Save standardized version
    with open(paper_path, 'w', encoding='utf-8') as f:
        f.write(standardized_content)
    
    original_lines = content.count('\n')
    new_lines = standardized_content.count('\n')
    
    print(f"✅ Standardized and replaced paper.md")
    print(f"   Lines: {original_lines} → {new_lines}")
    
    return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Process a single large paper")
    parser.add_argument("cite_key", help="Paper cite_key to process")
    
    args = parser.parse_args()
    
    success = process_large_paper(args.cite_key)
    
    if success:
        print(f"\n✅ Successfully processed {args.cite_key}")
        
        # Update progress file
        progress_file = "standardization_progress.json"
        progress = {"completed": [], "failed": {}}
        
        if Path(progress_file).exists():
            with open(progress_file, 'r') as f:
                progress = json.load(f)
        
        if args.cite_key not in progress["completed"]:
            progress["completed"].append(args.cite_key)
        
        # Remove from failed if it was there
        if args.cite_key in progress["failed"]:
            del progress["failed"][args.cite_key]
        
        with open(progress_file, 'w') as f:
            json.dump(progress, f, indent=2)
        
        print(f"✅ Updated progress file")
    else:
        print(f"\n❌ Failed to process {args.cite_key}")


if __name__ == "__main__":
    main()
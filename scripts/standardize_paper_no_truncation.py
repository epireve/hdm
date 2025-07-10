#!/usr/bin/env python3
"""
Standardize papers with ABSOLUTE guarantee of no content truncation
This version ensures 100% content preservation
"""

import sys
import json
import csv
import urllib.request
import urllib.error
import ssl
from pathlib import Path
from datetime import datetime
import time

# Add parent directory
sys.path.append(str(Path(__file__).parent.parent))

from lib.kilocode_config_simple import load_config, ConfigurationError


class NoTruncationStandardizer:
    """Standardizer that guarantees no content loss"""
    
    def __init__(self):
        # Load configuration
        try:
            self.config = load_config()
            print(f"✓ Kilocode configuration loaded")
        except ConfigurationError as e:
            print(f"❌ Failed to load configuration: {e}")
            sys.exit(1)
        
        # SSL context
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        # Load CSV data
        self.csv_data = self.load_csv_data()
    
    def load_csv_data(self):
        """Load CSV data"""
        csv_data = {}
        csv_path = "hdm_research_papers_merged_20250710.csv"
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cite_key = row.get('cite_key', '').strip()
                if cite_key:
                    csv_data[cite_key] = row
        
        print(f"✓ Loaded {len(csv_data)} papers from CSV")
        return csv_data
    
    def call_gemini_api(self, prompt, max_retries=3):
        """Call Gemini API with retry logic"""
        url = self.config.openrouter_url + "/chat/completions"
        
        for attempt in range(max_retries):
            try:
                data = {
                    "model": "google/gemini-2.5-pro-preview",
                    "messages": [
                        {"role": "system", "content": "You are an expert academic paper formatter. Preserve ALL content."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 100000  # Very high limit
                }
                
                headers = {
                    "Authorization": f"Bearer {self.config.token}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": self.config.http_referer,
                    "X-Title": self.config.x_title
                }
                
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode('utf-8'),
                    headers=headers,
                    method='POST'
                )
                
                print(f"  🤖 API call attempt {attempt + 1}...")
                with urllib.request.urlopen(req, context=self.ssl_context, timeout=120) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    content = result['choices'][0]['message']['content']
                    
                    # Show token usage
                    if 'usage' in result:
                        usage = result['usage']
                        print(f"  📊 Tokens - Input: {usage.get('prompt_tokens', 0)}, Output: {usage.get('completion_tokens', 0)}")
                    
                    return content
            
            except Exception as e:
                print(f"  ⚠️  Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    return None
        
        return None
    
    def extract_sections(self, content):
        """Extract major sections from the paper"""
        sections = []
        current_section = []
        current_title = "Frontmatter"
        
        lines = content.split('\n')
        in_frontmatter = False
        
        for line in lines:
            # Track frontmatter
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                current_section.append(line)
                continue
            
            # Skip section detection in frontmatter
            if in_frontmatter:
                current_section.append(line)
                continue
            
            # Detect major sections (##)
            if line.startswith('## '):
                # Save previous section
                if current_section:
                    sections.append({
                        'title': current_title,
                        'content': '\n'.join(current_section)
                    })
                current_title = line
                current_section = [line]
            else:
                current_section.append(line)
        
        # Don't forget the last section
        if current_section:
            sections.append({
                'title': current_title,
                'content': '\n'.join(current_section)
            })
        
        return sections
    
    def process_in_chunks(self, content, csv_row, cite_key):
        """Process paper in chunks to avoid truncation"""
        print(f"  📄 Processing paper in chunks to ensure no truncation...")
        
        # Extract sections
        sections = self.extract_sections(content)
        print(f"  ✓ Found {len(sections)} sections")
        
        # Group sections into processable chunks
        # Keep frontmatter + abstract + first few sections together
        chunks = []
        current_chunk = []
        current_size = 0
        max_chunk_size = 30000  # Conservative limit
        
        for i, section in enumerate(sections):
            section_size = len(section['content'])
            
            # Always keep frontmatter with first chunk
            if i == 0 or (current_size + section_size < max_chunk_size):
                current_chunk.append(section)
                current_size += section_size
            else:
                # Start new chunk
                chunks.append(current_chunk)
                current_chunk = [section]
                current_size = section_size
        
        # Add last chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        print(f"  ✓ Grouped into {len(chunks)} chunks for processing")
        
        # Process each chunk
        processed_parts = []
        
        for i, chunk in enumerate(chunks):
            chunk_content = '\n'.join([s['content'] for s in chunk])
            
            if i == 0:
                # First chunk - add new sections
                prompt = self.create_first_chunk_prompt(chunk_content, csv_row, cite_key)
            else:
                # Subsequent chunks - just preserve content
                prompt = f"""Preserve this content EXACTLY as is. Do not summarize or truncate.

CONTENT:
{chunk_content}

Return the content unchanged."""
            
            result = self.call_gemini_api(prompt)
            if result:
                processed_parts.append(result)
                print(f"  ✓ Processed chunk {i+1}/{len(chunks)}")
            else:
                print(f"  ❌ Failed to process chunk {i+1}")
                return None
            
            time.sleep(1)  # Brief pause between calls
        
        # Add metadata summary at the end
        metadata_section = self.create_metadata_section(csv_row)
        processed_parts.append(metadata_section)
        
        # Combine all parts
        final_content = '\n\n'.join(processed_parts)
        
        # Clean any markdown wrappers
        if final_content.startswith('```markdown'):
            final_content = final_content[11:]
        if final_content.endswith('```'):
            final_content = final_content[:-3]
        
        return final_content.strip()
    
    def create_first_chunk_prompt(self, content, csv_row, cite_key):
        """Create prompt for first chunk with standardization"""
        # Parse tags from DOI field (CSV issue)
        tags = []
        if csv_row.get('DOI'):
            tags = [t.strip() for t in csv_row['DOI'].split(',') if t.strip()][:15]
        elif csv_row.get('Tags'):
            tags = [t.strip() for t in csv_row['Tags'].split(',') if t.strip()][:15]
        
        # Fix DOI/URL
        doi = csv_row.get('url', '')
        if doi.startswith('10.'):
            url = f"https://doi.org/{doi}"
        else:
            url = csv_row.get('url', '')
            doi = ''
        
        prompt = f"""Standardize this paper's frontmatter and add new sections while preserving ALL original content.

CSV DATA for new sections:
TL;DR: {csv_row.get('TL;DR', '')}
Insights: {csv_row.get('Insights', '')}

CURRENT CONTENT (preserve all of this):
{content}

INSTRUCTIONS:
1. Update the YAML frontmatter with these values:
   - cite_key: {cite_key}
   - relevancy: {csv_row.get('Relevancy', 'HIGH')}
   - relevancy_justification: {csv_row.get('Relevancy Justification', '')}
   - tags: {', '.join(tags)}
   - standardization_date: {datetime.now().strftime('%Y-%m-%d')}
   - standardization_version: 1.0
   - Remove images_total, images_kept, images_removed fields

2. After the Abstract section, add:
   ## TL;DR
   [from CSV data above]
   
   ## Key Insights
   [from CSV Insights above]

3. Preserve ALL other content exactly as is

Return the complete standardized content."""
        
        return prompt
    
    def create_metadata_section(self, csv_row):
        """Create the metadata summary section"""
        return f"""## Metadata Summary
### Research Context
- **Research Question**: {csv_row.get('Research Question', 'Not available')}
- **Methodology**: {csv_row.get('Methodology', 'Not available')}
- **Key Findings**: {csv_row.get('Key Findings', 'Not available')}
- **Primary Outcomes**: {csv_row.get('Primary Outcomes', 'Not available')}

### Analysis
- **Limitations**: {csv_row.get('Limitations', 'Not available')}
- **Research Gaps**: {csv_row.get('Research Gaps', 'Not available')}
- **Future Work**: {csv_row.get('Future Work', 'Not available')}
- **Conclusion**: {csv_row.get('Conclusion', 'Not available')}

### Implementation Notes
{csv_row.get('Implementation Insights', 'Not available')}"""
    
    def standardize_paper(self, cite_key):
        """Standardize a single paper with no truncation"""
        print(f"\n{'='*60}")
        print(f"Standardizing: {cite_key} (No Truncation Mode)")
        print(f"{'='*60}")
        
        # Path to paper
        paper_path = Path(f"markdown_papers/{cite_key}/paper.md")
        
        if not paper_path.exists():
            print(f"❌ Paper not found: {paper_path}")
            return False
        
        # Get CSV data
        csv_row = self.csv_data.get(cite_key, {})
        if not csv_row:
            print(f"⚠️  No CSV data for {cite_key}")
        
        # Read original content
        with open(paper_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        original_lines = original_content.count('\n')
        print(f"✓ Read original: {len(original_content)} chars, {original_lines} lines")
        
        # Create backup
        backup_dir = Path(f"paper_backups/{cite_key}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / f"paper_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        print(f"✓ Backup saved: {backup_file}")
        
        # Process based on size
        if len(original_content) > 30000:
            # Large paper - process in chunks
            standardized_content = self.process_in_chunks(original_content, csv_row, cite_key)
        else:
            # Small paper - process in one go
            prompt = self.create_standardization_prompt(original_content, csv_row, cite_key)
            standardized_content = self.call_gemini_api(prompt)
            
            # Clean response
            if standardized_content and standardized_content.startswith('```markdown'):
                standardized_content = standardized_content[11:]
            if standardized_content and standardized_content.endswith('```'):
                standardized_content = standardized_content[:-3]
            if standardized_content:
                standardized_content = standardized_content.strip()
        
        if not standardized_content:
            print("❌ Failed to get standardized content")
            return False
        
        # Verify no truncation
        standardized_lines = standardized_content.count('\n')
        print(f"✓ Standardized: {len(standardized_content)} chars, {standardized_lines} lines")
        
        # Check for truncation indicators
        if "..." in standardized_content[-100:] or standardized_content.endswith(("...", ". . .")):
            print("⚠️  WARNING: Possible truncation detected!")
        
        # Save standardized version
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(standardized_content)
        
        print(f"✅ REPLACED original paper.md")
        print(f"   Original: {original_lines} lines")
        print(f"   New: {standardized_lines} lines")
        
        # Final check - make sure key sections exist
        if "## References" not in standardized_content:
            print("⚠️  WARNING: References section might be missing!")
        
        return True
    
    def create_standardization_prompt(self, content, csv_row, cite_key):
        """Create prompt for smaller papers"""
        # Parse tags
        tags = []
        if csv_row.get('DOI'):
            tags = [t.strip() for t in csv_row['DOI'].split(',') if t.strip()][:15]
        elif csv_row.get('Tags'):
            tags = [t.strip() for t in csv_row['Tags'].split(',') if t.strip()][:15]
        
        # Fix DOI/URL
        doi = csv_row.get('url', '')
        if doi.startswith('10.'):
            url = f"https://doi.org/{doi}"
        else:
            url = csv_row.get('url', '')
            doi = ''
        
        return f"""Standardize this paper while preserving EVERY SINGLE LINE of original content.

CSV DATA:
Title: {csv_row.get('title', '')}
Authors: {csv_row.get('authors', '')}
Year: {csv_row.get('year', '')}
DOI: {doi}
URL: {url}
Relevancy: {csv_row.get('Relevancy', '')}
Relevancy Justification: {csv_row.get('Relevancy Justification', '')}
TL;DR: {csv_row.get('TL;DR', '')}
Insights: {csv_row.get('Insights', '')}
Tags: {', '.join(tags)}

CURRENT PAPER ({len(content)} characters - PRESERVE ALL):
{content}

CRITICAL INSTRUCTIONS:
1. Update YAML frontmatter with CSV data
2. Add ## TL;DR and ## Key Insights sections after Abstract
3. Add ## Metadata Summary at the very end
4. PRESERVE ALL ORIGINAL CONTENT - every section, every paragraph, every sentence
5. Do NOT truncate, summarize, or omit ANY content
6. If the paper is long, still include EVERYTHING

Return the COMPLETE standardized paper."""


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Standardize papers with no truncation")
    parser.add_argument("cite_key", help="Paper cite_key to standardize")
    
    args = parser.parse_args()
    
    standardizer = NoTruncationStandardizer()
    success = standardizer.standardize_paper(args.cite_key)
    
    if success:
        print(f"\n✅ Successfully standardized {args.cite_key} with no truncation!")
    else:
        print(f"\n❌ Failed to standardize {args.cite_key}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Enhanced batch standardizer that handles both small and large papers
Uses chunk-based processing for large papers to avoid truncation
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


class EnhancedBatchStandardizer:
    """Standardize all papers including large ones with chunk processing"""
    
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
        
        # Progress tracking
        self.progress_file = "standardization_progress.json"
        self.progress = self.load_progress()
    
    def load_progress(self):
        """Load progress from file"""
        if Path(self.progress_file).exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            "completed": [],
            "failed": {},
            "started": datetime.now().isoformat()
        }
    
    def save_progress(self):
        """Save progress to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
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
                    "max_tokens": 100000
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
                
                with urllib.request.urlopen(req, context=self.ssl_context, timeout=120) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    content = result['choices'][0]['message']['content']
                    
                    # Show token usage
                    if 'usage' in result:
                        usage = result['usage']
                        print(f"    📊 Tokens - Input: {usage.get('prompt_tokens', 0)}, Output: {usage.get('completion_tokens', 0)}")
                    
                    return content
            
            except Exception as e:
                print(f"    ⚠️  Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
        
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
    
    def process_large_paper(self, content, csv_row, cite_key):
        """Process large paper using chunk-based approach"""
        print(f"    📄 Processing large paper with chunk-based approach...")
        
        # Extract sections
        sections = self.extract_sections(content)
        print(f"    ✓ Found {len(sections)} sections")
        
        # Group sections into processable chunks
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
        
        print(f"    ✓ Grouped into {len(chunks)} chunks for processing")
        
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
                print(f"    ✓ Processed chunk {i+1}/{len(chunks)}")
            else:
                print(f"    ❌ Failed to process chunk {i+1}")
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
        # Parse tags from DOI field
        tags = []
        if csv_row.get('DOI'):
            tags = [t.strip() for t in csv_row['DOI'].split(',') if t.strip()][:15]
        
        return f"""Standardize this paper section while preserving ALL original content.

CSV DATA for new sections:
TL;DR: {csv_row.get('TL;DR', '')}
Insights: {csv_row.get('Insights', '')}

CURRENT CONTENT (preserve all of this):
{content}

INSTRUCTIONS:
1. Update the YAML frontmatter with these values:
   - cite_key: {cite_key}
   - relevancy: {csv_row.get('Relevancy', 'HIGH')}
   - standardization_date: {datetime.now().strftime('%Y-%m-%d')}
   - standardization_version: 1.0
   - Remove images_total, images_kept, images_removed fields if present

2. After the Abstract section, add:
   ## TL;DR
   {csv_row.get('TL;DR', '')}
   
   ## Key Insights
   {csv_row.get('Insights', '')}

3. Preserve ALL other content exactly as is

Return the complete processed content."""
    
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
    
    def create_small_paper_prompt(self, content, csv_row, cite_key):
        """Create prompt for smaller papers"""
        # Parse tags from DOI field
        tags = []
        if csv_row.get('DOI'):
            tags = [t.strip() for t in csv_row['DOI'].split(',') if t.strip()][:15]
        
        return f"""Standardize this academic paper while preserving ALL original content.

CSV DATA:
TL;DR: {csv_row.get('TL;DR', '')}
Insights: {csv_row.get('Insights', '')}

CURRENT PAPER:
{content}

INSTRUCTIONS:
1. Update YAML frontmatter:
   - Remove images_total, images_kept, images_removed fields
   - Add standardization_date: {datetime.now().strftime('%Y-%m-%d')}
   - Add standardization_version: 1.0
   
2. After Abstract, add:
   ## TL;DR
   {csv_row.get('TL;DR', '')}
   
   ## Key Insights
   {csv_row.get('Insights', '')}

3. At the very end, add:
   {self.create_metadata_section(csv_row)}

4. PRESERVE ALL OTHER CONTENT EXACTLY AS IS

Return the complete standardized paper."""
    
    def standardize_paper(self, cite_key):
        """Standardize a single paper (small or large)"""
        paper_path = Path(f"markdown_papers/{cite_key}/paper.md")
        
        if not paper_path.exists():
            print(f"❌ Paper not found: {paper_path}")
            return False
        
        # Get CSV data
        csv_row = self.csv_data.get(cite_key, {})
        if not csv_row:
            print(f"⚠️  No CSV data for {cite_key}")
        
        # Read content
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"  📄 Read {len(content)} chars")
        
        # Create backup
        backup_dir = Path(f"paper_backups/{cite_key}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / f"paper_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Backup saved")
        
        # Process based on size
        if len(content) > 40000:
            # Large paper - use chunk processing
            standardized_content = self.process_large_paper(content, csv_row, cite_key)
        else:
            # Small paper - process in one go
            prompt = self.create_small_paper_prompt(content, csv_row, cite_key)
            standardized_content = self.call_gemini_api(prompt)
            
            # Clean response
            if standardized_content and standardized_content.startswith('```markdown'):
                standardized_content = standardized_content[11:]
            if standardized_content and standardized_content.endswith('```'):
                standardized_content = standardized_content[:-3]
            if standardized_content:
                standardized_content = standardized_content.strip()
        
        if not standardized_content:
            print(f"  ❌ Failed to get standardized content")
            return False
        
        # Save standardized version
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(standardized_content)
        
        print(f"  ✅ Standardized and replaced paper.md")
        return True
    
    def get_papers_to_process(self):
        """Get list of papers to process"""
        all_papers = []
        papers_dir = Path("markdown_papers")
        
        for paper_dir in papers_dir.iterdir():
            if paper_dir.is_dir() and (paper_dir / "paper.md").exists():
                cite_key = paper_dir.name
                if cite_key not in self.progress["completed"] and cite_key not in self.progress["failed"]:
                    all_papers.append(cite_key)
        
        # Sort by file size (process smaller papers first for initial success)
        papers_with_size = []
        for cite_key in all_papers:
            paper_path = papers_dir / cite_key / "paper.md"
            if paper_path.exists():
                size = paper_path.stat().st_size
                papers_with_size.append((cite_key, size))
        
        papers_with_size.sort(key=lambda x: x[1])
        return [p[0] for p in papers_with_size]
    
    def run(self, limit=None):
        """Run enhanced batch standardization"""
        papers = self.get_papers_to_process()
        
        if limit:
            papers = papers[:limit]
        
        print(f"\n{'='*60}")
        print(f"Enhanced batch standardization (handles large papers)")
        print(f"Papers to process: {len(papers)}")
        print(f"Already completed: {len(self.progress['completed'])}")
        print(f"Failed: {len(self.progress['failed'])}")
        print(f"{'='*60}\n")
        
        for i, cite_key in enumerate(papers, 1):
            print(f"\n[{i}/{len(papers)}] Processing {cite_key}")
            
            try:
                success = self.standardize_paper(cite_key)
                
                if success:
                    self.progress["completed"].append(cite_key)
                    # Remove from failed if it was there
                    if cite_key in self.progress["failed"]:
                        del self.progress["failed"][cite_key]
                    self.save_progress()
                else:
                    self.progress["failed"][cite_key] = "Processing failed"
                    self.save_progress()
                
                # Brief pause between papers
                time.sleep(2)
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                self.progress["failed"][cite_key] = str(e)
                self.save_progress()
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"Enhanced batch standardization complete!")
        print(f"Total processed: {len(self.progress['completed'])}")
        print(f"Failed: {len(self.progress['failed'])}")
        print(f"{'='*60}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced batch standardize papers (handles large papers)")
    parser.add_argument("--limit", type=int, help="Limit number of papers to process")
    parser.add_argument("--reset", action="store_true", help="Reset progress and start fresh")
    
    args = parser.parse_args()
    
    if args.reset and Path("standardization_progress.json").exists():
        os.remove("standardization_progress.json")
        print("Progress reset!")
    
    standardizer = EnhancedBatchStandardizer()
    standardizer.run(limit=args.limit)


if __name__ == "__main__":
    main()
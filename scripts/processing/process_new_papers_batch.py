#!/usr/bin/env python3
"""
Comprehensive script to process newly converted papers and missing papers
- Adds YAML frontmatter to markdown files
- Processes missing papers from JSON
- Ensures unique cite keys
- Updates CSV with all papers
"""

import os
import json
import csv
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Configuration
MARKDOWN_PAPERS = Path("markdown_papers")
MISSING_PAPERS_JSON = Path("missing_papers.json")
MERGED_CSV = Path("research_papers_merged_final.csv")
OUTPUT_CSV = Path("research_papers_complete.csv")
NEW_PAPERS_CHECKPOINT = Path("new_papers_checkpoint.json")
CITE_KEY_MAPPING = Path("cite_key_mapping_complete.json")

def clean_title(title: str) -> str:
    """Clean title by removing quotes, brackets, and normalizing case"""
    if not title:
        return ""
    
    # Remove quotes and brackets
    title = title.replace('"', '').replace("'", '')
    title = title.replace('(', '').replace(')', '')
    title = title.replace('[', '').replace(']', '')
    
    # Remove "Article" prefix if present
    if title.startswith("Article"):
        title = title[7:].strip()
    
    # Normalize whitespace
    title = ' '.join(title.split())
    
    # Don't convert to all lowercase - keep proper case
    return title.strip()

def clean_authors(authors: str) -> str:
    """Clean authors list - ensure no 'et al.' and use commas only"""
    if not authors:
        return ""
    
    # Remove et al.
    authors = authors.replace(' et al.', '')
    authors = authors.replace(' et al', '')
    
    # Replace semicolons with commas
    authors = authors.replace(';', ',')
    
    # Replace 'and' with comma
    authors = re.sub(r'\s+and\s+', ', ', authors)
    
    # Replace ampersand with comma
    authors = authors.replace(' & ', ', ')
    authors = authors.replace('&', ', ')
    
    # Clean up multiple commas and spaces
    authors = re.sub(r',\s*,', ',', authors)
    authors = re.sub(r'\s+', ' ', authors)
    authors = authors.strip()
    
    # Remove trailing comma
    if authors.endswith(','):
        authors = authors[:-1].strip()
    
    return authors

def generate_cite_key(authors: str, year: str) -> str:
    """Generate cite key from first author's last name and year"""
    if not authors or not year:
        return ""
    
    # Get first author
    first_author = authors.split(',')[0].strip()
    
    # Extract last name (assume last word is last name)
    last_name = first_author.split()[-1] if first_author else "unknown"
    
    # Clean last name
    last_name = re.sub(r'[^a-zA-Z]', '', last_name).lower()
    
    # Generate cite key
    cite_key = f"{last_name}_{year}"
    
    return cite_key

def load_missing_papers():
    """Load missing papers from JSON"""
    if not MISSING_PAPERS_JSON.exists():
        print(f"Warning: {MISSING_PAPERS_JSON} not found")
        return []
    
    with open(MISSING_PAPERS_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_existing_csv():
    """Load existing CSV data"""
    papers = []
    if MERGED_CSV.exists():
        with open(MERGED_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            papers = list(reader)
    return papers

def extract_authors_from_markdown(md_path: Path) -> Optional[str]:
    """Try to extract full author list from markdown file"""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for author patterns in first 100 lines
        lines = content.split('\n')[:100]
        
        # Common patterns
        patterns = [
            r'^##?\s*Authors?:?\s*(.+)$',
            r'^\*?Authors?:?\*?\s*(.+)$',
            r'^by\s+(.+)$',
        ]
        
        for line in lines:
            for pattern in patterns:
                match = re.match(pattern, line.strip(), re.IGNORECASE)
                if match:
                    authors = match.group(1).strip()
                    # Check if it looks like a complete author list
                    if ',' in authors or ' and ' in authors:
                        return clean_authors(authors)
        
        # Look for email patterns to find authors
        email_pattern = r'([A-Za-z\s\.-]+)\s*[<\(]?\s*[\w\.-]+@[\w\.-]+[\w]\s*[>\)]?'
        emails = re.findall(email_pattern, content[:5000])
        if emails:
            authors = ', '.join([name.strip() for name in emails[:10]])  # Limit to 10
            return clean_authors(authors)
    
    except Exception as e:
        print(f"Error extracting authors from {md_path}: {e}")
    
    return None

def build_yaml_frontmatter(paper_data: Dict) -> str:
    """Build YAML frontmatter from paper data"""
    yaml_lines = ['---']
    
    # Core metadata
    if paper_data.get('cite_key'):
        yaml_lines.append(f'cite_key: "{paper_data["cite_key"]}"')
    
    if paper_data.get('title'):
        title = clean_title(paper_data['title'])
        yaml_lines.append(f'title: "{title}"')
    
    if paper_data.get('authors'):
        authors = clean_authors(paper_data['authors'])
        yaml_lines.append(f'authors: "{authors}"')
    
    if paper_data.get('year'):
        yaml_lines.append(f'year: {paper_data["year"]}')
    
    # Additional metadata
    if paper_data.get('doi'):
        yaml_lines.append(f'doi: "{paper_data["doi"]}"')
    
    if paper_data.get('url'):
        yaml_lines.append(f'url: "{paper_data["url"]}"')
    
    if paper_data.get('relevancy'):
        yaml_lines.append(f'relevancy: "{paper_data["relevancy"]}"')
    
    if paper_data.get('tldr'):
        tldr = paper_data['tldr'].replace('"', '\\"')
        yaml_lines.append(f'tldr: "{tldr}"')
    
    if paper_data.get('insights'):
        insights = paper_data['insights'].replace('"', '\\"')
        yaml_lines.append(f'insights: "{insights}"')
    
    if paper_data.get('summary'):
        summary = paper_data['summary'].replace('"', '\\"').replace('\n', ' ')
        yaml_lines.append(f'summary: "{summary}"')
    
    if paper_data.get('research_question'):
        rq = paper_data['research_question'].replace('"', '\\"')
        yaml_lines.append(f'research_question: "{rq}"')
    
    if paper_data.get('methodology'):
        method = paper_data['methodology'].replace('"', '\\"')
        yaml_lines.append(f'methodology: "{method}"')
    
    if paper_data.get('key_findings'):
        findings = paper_data['key_findings'].replace('"', '\\"')
        yaml_lines.append(f'key_findings: "{findings}"')
    
    if paper_data.get('limitations'):
        limitations = paper_data['limitations'].replace('"', '\\"')
        yaml_lines.append(f'limitations: "{limitations}"')
    
    if paper_data.get('conclusion'):
        conclusion = paper_data['conclusion'].replace('"', '\\"')
        yaml_lines.append(f'conclusion: "{conclusion}"')
    
    if paper_data.get('future_work'):
        future = paper_data['future_work'].replace('"', '\\"')
        yaml_lines.append(f'future_work: "{future}"')
    
    if paper_data.get('implementation_insights'):
        impl = paper_data['implementation_insights'].replace('"', '\\"')
        yaml_lines.append(f'implementation_insights: "{impl}"')
    
    # Tags
    if paper_data.get('tags'):
        tags = [tag.strip() for tag in paper_data['tags'].split(',') if tag.strip()]
        if tags:
            yaml_lines.append('tags:')
            for tag in tags:
                yaml_lines.append(f'  - "{tag}"')
    
    yaml_lines.append('---')
    return '\n'.join(yaml_lines)

def add_yaml_to_markdown(md_path: Path, paper_data: Dict):
    """Add or update YAML frontmatter in markdown file"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if YAML frontmatter exists
    yaml_pattern = r'^---\n(.*?)\n---\n'
    yaml_match = re.match(yaml_pattern, content, re.DOTALL)
    
    # Build YAML frontmatter
    yaml_content = build_yaml_frontmatter(paper_data)
    
    if yaml_match:
        # Replace existing frontmatter
        new_content = re.sub(yaml_pattern, yaml_content + '\n', content, count=1, flags=re.DOTALL)
    else:
        # Add new frontmatter
        new_content = yaml_content + '\n\n' + content
    
    # Write back
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def process_newly_converted_papers(missing_papers_lookup: Dict):
    """Process newly converted papers from new_papers folder"""
    processed_papers = []
    
    # Load checkpoint to get list of converted papers
    if NEW_PAPERS_CHECKPOINT.exists():
        with open(NEW_PAPERS_CHECKPOINT, 'r') as f:
            checkpoint = json.load(f)
        
        completed_pdfs = checkpoint.get('completed', [])
        
        for pdf_path in completed_pdfs:
            # Extract folder name from PDF name
            pdf_name = Path(pdf_path).stem
            folder_path = MARKDOWN_PAPERS / pdf_name
            
            if folder_path.exists():
                md_path = folder_path / "paper.md"
                if md_path.exists():
                    # Try to extract metadata from markdown
                    paper_data = extract_metadata_from_markdown(md_path, pdf_name, missing_papers_lookup)
                    
                    # Add YAML frontmatter
                    add_yaml_to_markdown(md_path, paper_data)
                    
                    processed_papers.append(paper_data)
                    print(f"Processed: {paper_data['cite_key']} - {paper_data['title'][:50]}...")
    
    return processed_papers

def extract_metadata_from_markdown(md_path: Path, folder_name: str, missing_papers_lookup: Dict) -> Dict:
    """Extract metadata from markdown file"""
    paper_data = {
        'folder_name': folder_name,
        'markdown_file': md_path.name
    }
    
    # Check if this paper is in missing papers lookup
    # Try to match by various fields
    for missing_paper in missing_papers_lookup.values():
        # Match by title similarity or URL
        if (folder_name in str(missing_paper.get('url', '')) or 
            folder_name in str(missing_paper.get('Paper Title', ''))):
            
            # Found a match - use the metadata
            paper_data.update({
                'title': clean_title(missing_paper.get('Paper Title', '')),
                'authors': clean_authors(missing_paper.get('Authors', '')),
                'year': missing_paper.get('Year', ''),
                'doi': missing_paper.get('DOI', ''),
                'url': missing_paper.get('url', ''),
                'relevancy': missing_paper.get('Relevancy', ''),
                'tldr': missing_paper.get('TL;DR', ''),
                'insights': missing_paper.get('Insights', ''),
                'summary': missing_paper.get('Summary', ''),
                'research_question': missing_paper.get('Research Question', ''),
                'methodology': missing_paper.get('Methodology', ''),
                'key_findings': missing_paper.get('Key Findings', ''),
                'limitations': missing_paper.get('Limitations', ''),
                'conclusion': missing_paper.get('Conclusion', ''),
                'future_work': missing_paper.get('Future Work', ''),
                'implementation_insights': missing_paper.get('Implementation Insights', ''),
                'tags': missing_paper.get('Tags', '')
            })
            break
    
    # If no match found, try to extract from markdown
    if not paper_data.get('title'):
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:20]
            
            # Extract title (usually first # heading)
            for line in lines:
                if line.startswith('# '):
                    paper_data['title'] = clean_title(line[2:].strip())
                    break
            
            # Try to extract authors
            authors = extract_authors_from_markdown(md_path)
            if authors:
                paper_data['authors'] = authors
            
            # Extract year from folder name or content
            year_match = re.search(r'20\d{2}', folder_name)
            if year_match:
                paper_data['year'] = year_match.group()
        
        except Exception as e:
            print(f"Error extracting metadata from {md_path}: {e}")
    
    # Generate cite key if we have authors and year
    if paper_data.get('authors') and paper_data.get('year'):
        paper_data['cite_key'] = generate_cite_key(paper_data['authors'], paper_data['year'])
    else:
        # Fallback cite key from folder name
        paper_data['cite_key'] = re.sub(r'[^a-zA-Z0-9_]', '_', folder_name).lower()
    
    return paper_data

def ensure_unique_cite_keys(all_papers: List[Dict]) -> List[Dict]:
    """Ensure all cite keys are unique by adding a/b/c suffixes"""
    cite_key_counts = {}
    
    # First pass - count occurrences
    for paper in all_papers:
        base_key = paper.get('cite_key', '')
        if base_key:
            # Remove existing suffix if present
            if re.match(r'.+_\d{4}[a-z]$', base_key):
                base_key = base_key[:-1]
            
            if base_key not in cite_key_counts:
                cite_key_counts[base_key] = []
            cite_key_counts[base_key].append(paper)
    
    # Second pass - add suffixes where needed
    for base_key, papers in cite_key_counts.items():
        if len(papers) > 1:
            # Sort by year, then title to ensure consistent ordering
            papers.sort(key=lambda p: (p.get('year', ''), p.get('title', '')))
            
            for i, paper in enumerate(papers):
                suffix = chr(ord('a') + i)  # a, b, c, ...
                paper['cite_key'] = f"{base_key}{suffix}"
    
    return all_papers

def save_to_csv(papers: List[Dict], output_path: Path):
    """Save papers to CSV with all columns"""
    if not papers:
        print("No papers to save")
        return
    
    # Define all columns
    columns = [
        'cite_key', 'title', 'authors', 'year', 
        'Downloaded', 'Relevancy', 'Relevancy Justification',
        'Insights', 'TL;DR', 'Summary', 'Research Question',
        'Methodology', 'Key Findings', 'Primary Outcomes',
        'Limitations', 'Conclusion', 'Research Gaps',
        'Future Work', 'Implementation Insights', 'url', 'DOI', 'Tags'
    ]
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        
        for paper in papers:
            row = {col: '' for col in columns}  # Initialize with empty strings
            
            # Map our keys to CSV columns
            row['cite_key'] = paper.get('cite_key', '')
            row['title'] = paper.get('title', '')
            row['authors'] = paper.get('authors', '')
            row['year'] = paper.get('year', '')
            row['Downloaded'] = paper.get('Downloaded', 'Yes')  # Assume downloaded if processed
            row['Relevancy'] = paper.get('relevancy', paper.get('Relevancy', ''))
            row['Relevancy Justification'] = paper.get('Relevancy Justification', '')
            row['Insights'] = paper.get('insights', paper.get('Insights', ''))
            row['TL;DR'] = paper.get('tldr', paper.get('TL;DR', ''))
            row['Summary'] = paper.get('summary', paper.get('Summary', ''))
            row['Research Question'] = paper.get('research_question', paper.get('Research Question', ''))
            row['Methodology'] = paper.get('methodology', paper.get('Methodology', ''))
            row['Key Findings'] = paper.get('key_findings', paper.get('Key Findings', ''))
            row['Primary Outcomes'] = paper.get('Primary Outcomes', '')
            row['Limitations'] = paper.get('limitations', paper.get('Limitations', ''))
            row['Conclusion'] = paper.get('conclusion', paper.get('Conclusion', ''))
            row['Research Gaps'] = paper.get('Research Gaps', '')
            row['Future Work'] = paper.get('future_work', paper.get('Future Work', ''))
            row['Implementation Insights'] = paper.get('implementation_insights', paper.get('Implementation Insights', ''))
            row['url'] = paper.get('url', '')
            row['DOI'] = paper.get('doi', paper.get('DOI', ''))
            row['Tags'] = paper.get('tags', paper.get('Tags', ''))
            
            writer.writerow(row)

def main():
    print("Starting comprehensive paper processing...")
    print("=" * 60)
    
    # Load missing papers
    missing_papers = load_missing_papers()
    missing_papers_lookup = {p.get('Paper Title', ''): p for p in missing_papers if p.get('Paper Title')}
    print(f"Loaded {len(missing_papers)} missing papers")
    
    # Load existing CSV
    existing_papers = load_existing_csv()
    print(f"Loaded {len(existing_papers)} existing papers from CSV")
    
    # Process newly converted papers
    print("\nProcessing newly converted papers...")
    new_papers = process_newly_converted_papers(missing_papers_lookup)
    print(f"Processed {len(new_papers)} new papers")
    
    # Add missing papers that weren't found in converted papers
    print("\nAdding remaining missing papers...")
    processed_titles = {p.get('title', '') for p in new_papers}
    
    for missing_paper in missing_papers:
        title = clean_title(missing_paper.get('Paper Title', ''))
        if title and title not in processed_titles:
            # Add this missing paper
            paper_data = {
                'title': title,
                'authors': clean_authors(missing_paper.get('Authors', '')),
                'year': missing_paper.get('Year', ''),
                'doi': missing_paper.get('DOI', ''),
                'url': missing_paper.get('url', ''),
                'relevancy': missing_paper.get('Relevancy', ''),
                'tldr': missing_paper.get('TL;DR', ''),
                'insights': missing_paper.get('Insights', ''),
                'summary': missing_paper.get('Summary', ''),
                'research_question': missing_paper.get('Research Question', ''),
                'methodology': missing_paper.get('Methodology', ''),
                'key_findings': missing_paper.get('Key Findings', ''),
                'limitations': missing_paper.get('Limitations', ''),
                'conclusion': missing_paper.get('Conclusion', ''),
                'future_work': missing_paper.get('Future Work', ''),
                'implementation_insights': missing_paper.get('Implementation Insights', ''),
                'tags': missing_paper.get('Tags', ''),
                'Downloaded': 'No'  # These are missing papers
            }
            
            # Generate cite key
            if paper_data.get('authors') and paper_data.get('year'):
                paper_data['cite_key'] = generate_cite_key(paper_data['authors'], paper_data['year'])
            
            new_papers.append(paper_data)
    
    # Combine all papers
    all_papers = existing_papers + new_papers
    
    # Ensure unique cite keys
    print("\nEnsuring unique cite keys...")
    all_papers = ensure_unique_cite_keys(all_papers)
    
    # Remove duplicates based on title
    seen_titles = set()
    unique_papers = []
    for paper in all_papers:
        title = paper.get('title', '').lower().strip()
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_papers.append(paper)
    
    # Save to CSV
    print(f"\nSaving {len(unique_papers)} papers to CSV...")
    save_to_csv(unique_papers, OUTPUT_CSV)
    
    # Save cite key mapping
    cite_key_mapping = {
        'total_papers': len(unique_papers),
        'papers': {p['cite_key']: {
            'title': p.get('title', ''),
            'authors': p.get('authors', ''),
            'year': p.get('year', ''),
            'folder_name': p.get('folder_name', '')
        } for p in unique_papers if p.get('cite_key')}
    }
    
    with open(CITE_KEY_MAPPING, 'w', encoding='utf-8') as f:
        json.dump(cite_key_mapping, f, indent=2)
    
    print("\n" + "=" * 60)
    print("Processing complete!")
    print(f"Total papers: {len(unique_papers)}")
    print(f"Output CSV: {OUTPUT_CSV}")
    print(f"Cite key mapping: {CITE_KEY_MAPPING}")
    
    # Move PDFs from new_papers to papers folder
    print("\nMoving PDFs from new_papers to papers folder...")
    move_processed_pdfs()

def move_processed_pdfs():
    """Move PDFs from new_papers to papers folder after processing"""
    new_papers_dir = Path("new_papers")
    papers_dir = Path("papers")
    
    # Create papers directory if it doesn't exist
    papers_dir.mkdir(exist_ok=True)
    
    # Load checkpoint to get list of processed PDFs
    if NEW_PAPERS_CHECKPOINT.exists():
        with open(NEW_PAPERS_CHECKPOINT, 'r') as f:
            checkpoint = json.load(f)
        
        completed_pdfs = checkpoint.get('completed', [])
        moved_count = 0
        
        for pdf_path in completed_pdfs:
            source_path = Path(pdf_path)
            if source_path.exists():
                dest_path = papers_dir / source_path.name
                try:
                    shutil.move(str(source_path), str(dest_path))
                    moved_count += 1
                    print(f"Moved: {source_path.name}")
                except Exception as e:
                    print(f"Error moving {source_path.name}: {e}")
        
        print(f"Moved {moved_count} PDFs to papers folder")
    else:
        print("No checkpoint file found - no PDFs to move")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Extract author names from paper.md files using Gemini Flash model for papers with missing authors.
"""

import sqlite3
import os
import json
import logging
import time
from typing import List, Dict, Optional
from pathlib import Path
import google.generativeai as genai
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaperAuthorsExtractor:
    """Extract authors from paper.md files using Gemini Flash."""
    
    def __init__(self):
        # Configure Gemini
        self.setup_gemini()
        self.papers_dir = Path("markdown_papers")
        
    def setup_gemini(self):
        """Setup Gemini API."""
        try:
            # Try to get API key from environment
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                # You'll need to set this
                logger.error("Please set GOOGLE_API_KEY environment variable")
                return False
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("✅ Gemini Flash model initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to setup Gemini: {e}")
            return False
    
    def get_papers_missing_authors(self) -> List[Dict]:
        """Get papers with missing or problematic authors."""
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Find papers with missing, empty, or clearly wrong authors
        cursor.execute("""
            SELECT cite_key, title, authors, csv_original_authors, corrected_cite_key
            FROM papers 
            WHERE 
                -- Missing or empty authors
                (authors IS NULL OR authors = '' OR authors = 'N/A' OR authors = 'unavailable') OR
                -- Clearly wrong extractions
                authors LIKE '%check for updates%' OR
                authors LIKE '%additional key words%' OR
                authors LIKE '%.edu.%' OR
                authors LIKE '%@%' OR
                authors LIKE '%university%' OR
                authors LIKE '%institute%' OR
                authors LIKE '%systems group%' OR
                authors LIKE '%digital humanities%' OR
                authors LIKE '%mechatronic engineering%' OR
                authors LIKE '%his majesty%' OR
                authors LIKE '%.surnam%' OR
                LENGTH(authors) > 200 OR
                -- Very short/suspicious authors
                LENGTH(TRIM(authors)) < 3
            ORDER BY cite_key
        """)
        
        papers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        logger.info(f"Found {len(papers)} papers needing author extraction")
        return papers
    
    def find_paper_md_file(self, cite_key: str) -> Optional[Path]:
        """Find the paper.md file for a given cite_key."""
        # Try different possible folder structures
        possible_paths = [
            self.papers_dir / cite_key / "paper.md",
            self.papers_dir / cite_key.replace('_', '-') / "paper.md",
            self.papers_dir / cite_key.lower() / "paper.md",
        ]
        
        # Also try corrected_cite_key if different
        # We'll handle this in the main function
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def extract_authors_with_gemini(self, paper_content: str, cite_key: str, title: str) -> Optional[str]:
        """Extract authors from paper content using Gemini Flash."""
        
        # Create a focused prompt for author extraction
        prompt = f"""
You are an expert at extracting author information from academic papers. 

Given the following paper content, extract ONLY the author names in a clean, standardized format.

Paper Title: {title}
Cite Key: {cite_key}

Paper Content (first 2000 characters):
{paper_content[:2000]}

Instructions:
1. Find the author names from the paper (usually near the beginning)
2. Return ONLY the author names in this format: "FirstName LastName, FirstName LastName, FirstName LastName"
3. Do NOT include affiliations, emails, or institutional information
4. Do NOT include titles like "Dr.", "Prof.", etc.
5. If you find "et al.", try to find the full author list
6. If no clear authors are found, return "AUTHORS_NOT_FOUND"

Examples of good output:
- "John Smith, Mary Johnson, Robert Davis"
- "Li Wei, Chen Zhang"
- "Maria Garcia-Rodriguez, Jean-Pierre Dubois"

Extract the authors:
"""

        try:
            response = self.model.generate_content(prompt)
            extracted_authors = response.text.strip()
            
            # Clean up the response
            extracted_authors = re.sub(r'^["\']|["\']$', '', extracted_authors)
            extracted_authors = extracted_authors.replace('\n', ' ').strip()
            
            # Validate the extraction
            if "AUTHORS_NOT_FOUND" in extracted_authors:
                return None
            
            # Basic validation - should look like names
            if len(extracted_authors) < 3 or '@' in extracted_authors or 'http' in extracted_authors.lower():
                return None
            
            logger.info(f"Extracted authors for {cite_key}: {extracted_authors}")
            return extracted_authors
            
        except Exception as e:
            logger.error(f"Gemini extraction failed for {cite_key}: {e}")
            return None
    
    def process_papers_batch(self, papers: List[Dict], batch_size: int = 10) -> Dict:
        """Process papers in batches to extract authors."""
        results = {
            'successful_extractions': [],
            'failed_extractions': [],
            'no_paper_file': [],
            'total_processed': 0
        }
        
        for i, paper in enumerate(papers):
            cite_key = paper['cite_key']
            title = paper['title'] or 'Unknown Title'
            current_authors = paper['authors']
            
            logger.info(f"Processing {i+1}/{len(papers)}: {cite_key}")
            
            # Find the paper.md file
            paper_file = self.find_paper_md_file(cite_key)
            
            if not paper_file:
                # Try with corrected_cite_key if different
                corrected_key = paper['corrected_cite_key']
                if corrected_key and corrected_key != cite_key:
                    paper_file = self.find_paper_md_file(corrected_key)
            
            if not paper_file:
                logger.warning(f"No paper.md file found for {cite_key}")
                results['no_paper_file'].append({
                    'cite_key': cite_key,
                    'title': title,
                    'current_authors': current_authors
                })
                continue
            
            try:
                # Read the paper content
                with open(paper_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract authors using Gemini
                extracted_authors = self.extract_authors_with_gemini(content, cite_key, title)
                
                if extracted_authors:
                    results['successful_extractions'].append({
                        'cite_key': cite_key,
                        'title': title,
                        'current_authors': current_authors,
                        'extracted_authors': extracted_authors,
                        'paper_file': str(paper_file)
                    })
                else:
                    results['failed_extractions'].append({
                        'cite_key': cite_key,
                        'title': title,
                        'current_authors': current_authors,
                        'paper_file': str(paper_file)
                    })
                
                results['total_processed'] += 1
                
                # Rate limiting - be nice to Gemini API
                if (i + 1) % batch_size == 0:
                    logger.info(f"Completed batch {(i + 1) // batch_size}, sleeping 2 seconds...")
                    time.sleep(2)
                else:
                    time.sleep(0.5)  # Small delay between requests
                    
            except Exception as e:
                logger.error(f"Error processing {cite_key}: {e}")
                results['failed_extractions'].append({
                    'cite_key': cite_key,
                    'title': title,
                    'error': str(e)
                })
        
        return results
    
    def update_database_with_extractions(self, extractions: List[Dict], commit_changes: bool = False) -> int:
        """Update database with extracted authors."""
        conn = sqlite3.connect('hdm_papers.db')
        cursor = conn.cursor()
        
        updated_count = 0
        
        for extraction in extractions:
            cite_key = extraction['cite_key']
            extracted_authors = extraction['extracted_authors']
            
            # Update both authors and add a note about the extraction method
            cursor.execute("""
                UPDATE papers 
                SET authors = ?,
                    yaml_authors = ?
                WHERE cite_key = ?
            """, (extracted_authors, extracted_authors, cite_key))
            
            if cursor.rowcount > 0:
                updated_count += 1
                logger.info(f"Updated {cite_key} with authors: {extracted_authors}")
        
        if commit_changes:
            conn.commit()
            logger.info(f"✅ Committed {updated_count} author updates to database")
        else:
            logger.info(f"📝 Prepared {updated_count} author updates (not committed)")
        
        conn.close()
        return updated_count
    
    def generate_extraction_report(self, results: Dict) -> None:
        """Generate a detailed report of the extraction process."""
        successful = results['successful_extractions']
        failed = results['failed_extractions']
        no_file = results['no_paper_file']
        
        print(f"\n📊 AUTHOR EXTRACTION REPORT")
        print(f"=" * 80)
        print(f"Total papers processed: {results['total_processed']}")
        print(f"Successful extractions: {len(successful)}")
        print(f"Failed extractions: {len(failed)}")
        print(f"No paper.md file found: {len(no_file)}")
        
        if successful:
            print(f"\n✅ SUCCESSFUL EXTRACTIONS:")
            print("-" * 60)
            for extraction in successful[:10]:  # Show first 10
                cite_key = extraction['cite_key']
                extracted = extraction['extracted_authors']
                current = extraction['current_authors'] or 'NO AUTHORS'
                
                print(f"\n🔑 {cite_key}")
                print(f"   Before: {current}")
                print(f"   After:  {extracted}")
            
            if len(successful) > 10:
                print(f"\n   ... and {len(successful) - 10} more successful extractions")
        
        if failed:
            print(f"\n❌ FAILED EXTRACTIONS:")
            print("-" * 60)
            for failure in failed[:5]:  # Show first 5
                cite_key = failure['cite_key']
                title = failure['title'][:50] + "..." if failure['title'] else "NO TITLE"
                print(f"   {cite_key}: {title}")
        
        if no_file:
            print(f"\n📁 NO PAPER.MD FILE FOUND:")
            print("-" * 60)
            for missing in no_file[:5]:  # Show first 5
                cite_key = missing['cite_key']
                title = missing['title'][:50] + "..." if missing['title'] else "NO TITLE"
                print(f"   {cite_key}: {title}")
        
        # Save detailed report
        with open('author_extraction_report.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Detailed report saved to: author_extraction_report.json")

def main():
    """Execute author extraction from paper.md files."""
    logger.info("Starting author extraction from paper.md files using Gemini Flash...")
    
    extractor = PaperAuthorsExtractor()
    
    # Check if Gemini is properly configured
    if not hasattr(extractor, 'model'):
        print("❌ Gemini not properly configured. Please set GOOGLE_API_KEY environment variable.")
        return
    
    # Get papers needing author extraction
    papers_to_process = extractor.get_papers_missing_authors()
    
    if not papers_to_process:
        print("✅ No papers found needing author extraction!")
        return
    
    print(f"🔍 Found {len(papers_to_process)} papers needing author extraction")
    print(f"⚠️  This will make API calls to Gemini Flash")
    
    # Process papers
    results = extractor.process_papers_batch(papers_to_process, batch_size=5)
    
    # Generate report
    extractor.generate_extraction_report(results)
    
    # Ask about database update
    if results['successful_extractions']:
        print(f"\n🔧 Found {len(results['successful_extractions'])} successful extractions")
        print(f"   Run update_database_with_extractions(commit_changes=True) to apply them")
        
        # For now, just prepare the updates
        updated_count = extractor.update_database_with_extractions(
            results['successful_extractions'], 
            commit_changes=False
        )
        
        print(f"📝 Prepared {updated_count} database updates")
    
    print(f"\n✅ Author extraction process completed")

if __name__ == "__main__":
    main()
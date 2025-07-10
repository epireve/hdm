#!/usr/bin/env python3
"""
Complete ALL missing data in research papers CSV using KiloCode API
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
import ssl
from datetime import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
from lib.kilocode_config_simple import load_config, ConfigurationError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("complete_missing_data.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

# Research context
RESEARCH_FOCUS = """
Research Focus: Heterogeneous Data Integration in Personal Knowledge Graph (PKG) Architectures
Our research focuses on developing bespoke PKG systems that seamlessly integrate diverse upstream data sources through temporal-first architecture and advanced schema design.
"""

RELEVANCY_CRITERIA = """
SUPER: Directly addresses heterogeneous data integration in PKG/knowledge graphs
HIGH: Strongly relates to PKG construction with data integration focus  
MEDIUM: Provides supporting technologies or concepts
LOW: Minimal relevance to heterogeneous data focus
"""

class ComprehensiveDataCompleter:
    def __init__(self, config):
        self.config = config
        self.base_url = f"{config.openrouter_url}/chat/completions"
        self.model = "anthropic/claude-3.5-sonnet"
        self.headers = config.headers
        self.checkpoint_file = "comprehensive_checkpoint.json"
        self.checkpoint_data = self.load_checkpoint()
        
    def load_checkpoint(self) -> Dict:
        """Load checkpoint data"""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return {"processed": {}, "last_index": 0}
    
    def save_checkpoint(self):
        """Save checkpoint data"""
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.checkpoint_data, f, indent=2)
    
    def make_api_request(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """Make API request using urllib"""
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": max_tokens
        }
        
        req = urllib.request.Request(
            self.base_url,
            data=json.dumps(data).encode('utf-8'),
            headers=self.headers
        )
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        try:
            with urllib.request.urlopen(req, context=ssl_context) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content'].strip()
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limit
                logging.warning("Rate limited, waiting 60 seconds...")
                time.sleep(60)
                return self.make_api_request(prompt, max_tokens)
            logging.error(f"HTTP Error: {e.code} - {e.reason}")
            return None
        except Exception as e:
            logging.error(f"Error making API request: {str(e)}")
            return None
    
    def generate_comprehensive_analysis(self, paper: Dict) -> Dict:
        """Generate all missing fields for a paper"""
        cite_key = paper.get('cite_key', 'unknown')
        title = paper.get('title', 'Unknown Title')
        authors = paper.get('authors', 'Unknown Authors')
        year = paper.get('year', 'Unknown')
        
        # Build a comprehensive prompt
        prompt = f"""Analyze this research paper and provide comprehensive information for a research database on heterogeneous data integration in Personal Knowledge Graphs.

Paper Information:
Title: {title}
Authors: {authors}
Year: {year}

{RESEARCH_FOCUS}

Based on the paper title and context, provide the following information in a structured format:

1. RELEVANCY: Assess relevancy (SUPER/HIGH/MEDIUM/LOW) based on these criteria:
{RELEVANCY_CRITERIA}

2. RELEVANCY JUSTIFICATION: 2-3 sentences explaining the relevancy rating

3. INSIGHTS: Key insights this paper provides for HDM/PKG implementation (2-3 sentences)

4. TL;DR: One-sentence summary capturing the main contribution

5. SUMMARY: Comprehensive 2-3 paragraph abstract describing the paper's approach, methods, and contributions

6. RESEARCH QUESTION: The primary research question addressed (1-2 sentences)

7. METHODOLOGY: Research methods employed (2-3 sentences)

8. KEY FINDINGS: Main discoveries and results (2-3 bullet points)

9. PRIMARY OUTCOMES: Concrete deliverables or frameworks (2-3 sentences)

10. LIMITATIONS: Acknowledged constraints or gaps (2-3 sentences)

11. CONCLUSION: Paper's final assessment (2-3 sentences)

12. RESEARCH GAPS: Areas needing further research (2-3 bullet points)

13. FUTURE WORK: Suggested next steps (2-3 sentences)

14. IMPLEMENTATION INSIGHTS: Practical takeaways for HDM development (2-3 sentences)

15. TAGS: 5-8 comma-separated keywords relevant to the paper

Format your response as a JSON object with these exact keys."""

        try:
            response = self.make_api_request(prompt, max_tokens=1500)
            if response:
                # Try to parse as JSON
                try:
                    # Clean up response if needed
                    if response.startswith('```json'):
                        response = response[7:]
                    if response.endswith('```'):
                        response = response[:-3]
                    
                    data = json.loads(response)
                    return data
                except json.JSONDecodeError:
                    # If not valid JSON, try to extract key-value pairs
                    logging.warning(f"Failed to parse JSON for {cite_key}, using fallback")
                    return self.parse_text_response(response)
            return {}
        except Exception as e:
            logging.error(f"Error generating analysis for {cite_key}: {str(e)}")
            return {}
    
    def parse_text_response(self, text: str) -> Dict:
        """Fallback parser for non-JSON responses"""
        result = {}
        
        # Simple pattern matching for common fields
        patterns = {
            'RELEVANCY': r'RELEVANCY[:\s]*(SUPER|HIGH|MEDIUM|LOW)',
            'RELEVANCY JUSTIFICATION': r'RELEVANCY JUSTIFICATION[:\s]*(.+?)(?=\d+\.|$)',
            'INSIGHTS': r'INSIGHTS[:\s]*(.+?)(?=\d+\.|TL;DR|$)',
            'TL;DR': r'TL;DR[:\s]*(.+?)(?=\d+\.|SUMMARY|$)',
            'TAGS': r'TAGS[:\s]*(.+?)(?=\d+\.|$)',
        }
        
        import re
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                result[key] = match.group(1).strip()
        
        return result
    
    def process_papers(self, input_file: str, output_file: str, limit: Optional[int] = None):
        """Process papers to complete all missing data"""
        # Read all papers
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            papers = list(reader)
            fieldnames = reader.fieldnames
        
        # Clean fieldnames
        fieldnames = [f for f in fieldnames if f is not None]
        
        total_papers = len(papers)
        processed_count = 0
        skipped_count = 0
        error_count = 0
        
        # Start from checkpoint
        start_index = self.checkpoint_data.get('last_index', 0)
        
        logging.info(f"Starting from index {start_index}")
        logging.info(f"Total papers: {total_papers}")
        
        # Process papers
        for i, paper in enumerate(papers):
            if i < start_index:
                continue
                
            if limit and processed_count >= limit:
                logging.info(f"Reached limit of {limit} papers")
                break
            
            cite_key = paper.get('cite_key', f'paper_{i}')
            
            # Check what's missing
            missing_fields = []
            critical_fields = ['Relevancy', 'Relevancy Justification', 'Insights', 'TL;DR', 
                             'Summary', 'Research Question', 'Tags']
            
            for field in critical_fields:
                value = paper.get(field, '').strip()
                if not value or value.lower() in ['', 'none', 'null', 'not available', 'n/a']:
                    missing_fields.append(field)
            
            if not missing_fields:
                logging.info(f"Paper {cite_key} already complete")
                skipped_count += 1
                continue
            
            logging.info(f"Processing paper {i+1}/{total_papers}: {cite_key} (missing {len(missing_fields)} fields)")
            
            try:
                # Generate comprehensive analysis
                analysis = self.generate_comprehensive_analysis(paper)
                
                if analysis:
                    # Update paper with generated data
                    field_mapping = {
                        'RELEVANCY': 'Relevancy',
                        'RELEVANCY JUSTIFICATION': 'Relevancy Justification',
                        'INSIGHTS': 'Insights',
                        'TL;DR': 'TL;DR',
                        'SUMMARY': 'Summary',
                        'RESEARCH QUESTION': 'Research Question',
                        'METHODOLOGY': 'Methodology',
                        'KEY FINDINGS': 'Key Findings',
                        'PRIMARY OUTCOMES': 'Primary Outcomes',
                        'LIMITATIONS': 'Limitations',
                        'CONCLUSION': 'Conclusion',
                        'RESEARCH GAPS': 'Research Gaps',
                        'FUTURE WORK': 'Future Work',
                        'IMPLEMENTATION INSIGHTS': 'Implementation Insights',
                        'TAGS': 'Tags'
                    }
                    
                    updated_fields = 0
                    for api_key, csv_field in field_mapping.items():
                        if api_key in analysis:
                            current_value = paper.get(csv_field, '').strip()
                            if not current_value or current_value.lower() in ['', 'none', 'null', 'not available']:
                                paper[csv_field] = analysis[api_key]
                                updated_fields += 1
                    
                    logging.info(f"  Updated {updated_fields} fields for {cite_key}")
                    processed_count += 1
                else:
                    logging.error(f"  Failed to generate analysis for {cite_key}")
                    error_count += 1
                
                # Save checkpoint
                self.checkpoint_data['processed'][cite_key] = True
                self.checkpoint_data['last_index'] = i + 1
                
                if processed_count % 5 == 0:
                    self.save_checkpoint()
                    # Write intermediate results
                    with open(output_file, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(papers)
                    logging.info(f"Checkpoint saved. Processed: {processed_count}")
                
                # Rate limiting
                time.sleep(3)
                
            except Exception as e:
                logging.error(f"Error processing {cite_key}: {str(e)}")
                error_count += 1
                continue
        
        # Final save
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(papers)
        
        self.save_checkpoint()
        
        # Summary
        logging.info("\n=== Processing Complete ===")
        logging.info(f"Total papers: {total_papers}")
        logging.info(f"Processed: {processed_count}")
        logging.info(f"Skipped (already complete): {skipped_count}")
        logging.info(f"Errors: {error_count}")
        logging.info(f"Output saved to: {output_file}")


def main():
    try:
        # Load config
        config = load_config()
        logging.info("KiloCode configuration loaded")
    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description='Complete missing data in research papers CSV')
    parser.add_argument('--limit', type=int, help='Limit number of papers to process')
    parser.add_argument('--test', action='store_true', help='Test mode (process 3 papers)')
    args = parser.parse_args()
    
    # File paths
    input_file = project_root / "research_papers_complete_with_relevancy.csv"
    output_file = project_root / "research_papers_complete_filled.csv"
    
    # Create processor and run
    processor = ComprehensiveDataCompleter(config)
    
    limit = 3 if args.test else args.limit
    processor.process_papers(str(input_file), str(output_file), limit=limit)


if __name__ == "__main__":
    main()
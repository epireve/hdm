#!/usr/bin/env python3
"""
Script to complete Relevancy and Relevancy Justification columns in research_papers_complete.csv
using KiloCode API (OpenRouter proxy) with Claude Sonnet 3.5 model.
"""

import csv
import json
import os
import sys
import time
from typing import Dict, List, Optional
import requests
from datetime import datetime
import logging
from pathlib import Path

# Add project root to path to import from lib
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
from lib.kilocode_config import load_config, ConfigurationError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('relevancy_analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Research focus context for relevancy assessment
RESEARCH_FOCUS = """
Current Research Focus: Heterogeneous Data Integration in Personal Knowledge Graph (PKG) Architectures

Our research focuses on developing bespoke PKG systems that seamlessly integrate diverse upstream data sources through temporal-first architecture and advanced schema design.

Primary Research Pillars:

1. Heterogeneous Data Integration & Schema Architecture
   - Multi-Modal Data Fusion: Integration patterns for structured (databases, APIs), semi-structured (JSON, XML), and unstructured (text, multimedia) data sources
   - Schema Harmonization: Dynamic schema mapping and transformation techniques for disparate data formats and ontologies
   - Upstream Data Source Orchestration: Early-stage data ingestion pipelines with real-time validation and quality assessment
   - Entity Resolution Across Domains: Cross-source entity linking with 78% accuracy improvements through advanced schema integration

2. Temporal-First Architecture Design
   - Time-Centric Data Modeling: Moving from traditional entity-centric to temporal-first PKG architectures achieving 94.8% performance with 90% latency reduction
   - Temporal Schema Evolution: Dynamic schema adaptation over time to accommodate changing data source structures
   - Versioned Knowledge Representation: Temporal versioning of entities, relationships, and schema definitions
   - Chronological Query Optimization: Query engines optimized for temporal range operations and historical data analysis

3. Bespoke System Design Patterns
   - Domain-Specific PKG Architectures: Customized designs for healthcare, education, enterprise, and personal productivity domains
   - Modular Integration Frameworks: Pluggable components for different data source types and integration patterns
   - Adaptive Schema Management: Self-evolving schemas that learn from data patterns and user interactions
   - Performance-Optimized Pipelines: Custom data processing workflows tailored to specific heterogeneous data combinations
"""

# Relevancy criteria
RELEVANCY_CRITERIA = """
Relevancy Assessment Criteria:

SUPER - Papers that directly address:
- Heterogeneous data integration methodologies in PKG/knowledge graphs
- Temporal-first PKG architectures or time-centric knowledge modeling
- Schema harmonization techniques for multi-source data fusion
- Upstream data orchestration and early-stage integration pipelines
- Bespoke PKG system designs for specific domains
- Multi-modal data fusion approaches in knowledge graphs

HIGH - Papers that strongly relate to:
- PKG/knowledge graph construction with emphasis on data integration
- Dynamic schema mapping and transformation
- Entity resolution across heterogeneous sources
- Temporal aspects of knowledge graphs
- Domain-specific knowledge graph implementations (healthcare, education, etc.)

MEDIUM - Papers that provide supporting technologies or concepts:
- General knowledge graph construction techniques
- Graph databases and storage solutions
- ETL frameworks and data quality tools
- Schema evolution strategies
- Query optimization for graph data

LOW - Papers that have minimal relevance:
- General knowledge graphs without heterogeneous data focus
- Static schema approaches
- Downstream-only processing systems
- Traditional database systems without graph focus
"""


class RelevancyAnalyzer:
    def __init__(self, config):
        self.config = config
        self.base_url = f"{config.openrouter_url}/chat/completions"
        self.model = "anthropic/claude-3.5-sonnet"  # Using Claude Sonnet 3.5
        self.headers = config.headers
        self.checkpoint_file = "relevancy_checkpoint.json"
        self.checkpoint_data = self.load_checkpoint()
        
    def load_checkpoint(self) -> Dict:
        """Load checkpoint data if exists"""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return {"processed": [], "last_index": 0}
    
    def save_checkpoint(self):
        """Save checkpoint data"""
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.checkpoint_data, f, indent=2)
    
    def assess_relevancy(self, paper_data: Dict) -> str:
        """Assess relevancy of a paper based on research focus"""
        prompt = f"""Based on the following research focus and paper information, assess the relevancy level.

{RESEARCH_FOCUS}

{RELEVANCY_CRITERIA}

Paper Information:
- Title: {paper_data.get('title', 'N/A')}
- Summary: {paper_data.get('Summary', 'N/A')}
- Research Question: {paper_data.get('Research Question', 'N/A')}
- Key Findings: {paper_data.get('Key Findings', 'N/A')}
- Tags: {paper_data.get('Tags', 'N/A')}

Provide ONLY the relevancy level (SUPER, HIGH, MEDIUM, or LOW) as a single word response."""
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 50
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                relevancy = result['choices'][0]['message']['content'].strip().upper()
                if relevancy in ['SUPER', 'HIGH', 'MEDIUM', 'LOW']:
                    return relevancy
                else:
                    logging.warning(f"Invalid relevancy response: {relevancy}")
                    return "MEDIUM"  # Default fallback
            else:
                logging.error(f"API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"Error assessing relevancy: {str(e)}")
            return None
    
    def generate_justification(self, paper_data: Dict, relevancy: str) -> str:
        """Generate relevancy justification based on paper content"""
        prompt = f"""Based on the following research focus and paper information, provide a detailed justification for why this paper has been rated as {relevancy} relevancy.

{RESEARCH_FOCUS}

Paper Information:
- Title: {paper_data.get('title', 'N/A')}
- Summary: {paper_data.get('Summary', 'N/A')}
- Research Question: {paper_data.get('Research Question', 'N/A')}
- Methodology: {paper_data.get('Methodology', 'N/A')}
- Key Findings: {paper_data.get('Key Findings', 'N/A')}
- Primary Outcomes: {paper_data.get('Primary Outcomes', 'N/A')}
- Implementation Insights: {paper_data.get('Implementation Insights', 'N/A')}
- Tags: {paper_data.get('Tags', 'N/A')}

Relevancy Level: {relevancy}

Provide a 2-3 sentence justification explaining why this paper received this relevancy rating. Focus on specific aspects of the paper that align or don't align with our research focus on heterogeneous data integration in PKG architectures. Be specific and reference actual content from the paper."""
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.5,
                    "max_tokens": 300
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                justification = result['choices'][0]['message']['content'].strip()
                return justification
            else:
                logging.error(f"API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"Error generating justification: {str(e)}")
            return None
    
    def process_papers(self, input_file: str, output_file: str, test_mode: bool = False):
        """Process papers to complete relevancy and justification"""
        # Read all papers
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            papers = list(reader)
            fieldnames = reader.fieldnames
        
        # Statistics
        total_papers = len(papers)
        processed_count = 0
        skipped_count = 0
        error_count = 0
        
        # Start processing from checkpoint
        start_index = self.checkpoint_data.get('last_index', 0)
        
        # Test mode - only process first 5 papers
        if test_mode:
            papers = papers[:5]
            logging.info("TEST MODE: Processing only first 5 papers")
        
        logging.info(f"Starting processing from index {start_index}")
        logging.info(f"Total papers to process: {len(papers)}")
        
        for i, paper in enumerate(papers):
            if i < start_index:
                continue
                
            cite_key = paper.get('cite_key', f'paper_{i}')
            
            # Check if already processed
            if cite_key in self.checkpoint_data['processed']:
                logging.info(f"Skipping already processed paper: {cite_key}")
                skipped_count += 1
                continue
            
            # Check if relevancy needs to be filled
            relevancy = paper.get('Relevancy', '').strip()
            needs_relevancy = not relevancy or relevancy.lower() in ['', 'none', 'null']
            
            # Check if justification needs to be filled
            justification = paper.get('Relevancy Justification', '').strip()
            needs_justification = not justification or justification.lower() in ['', 'none', 'null', 'not available']
            
            if not needs_relevancy and not needs_justification:
                logging.info(f"Paper {cite_key} already has both relevancy and justification")
                skipped_count += 1
                continue
            
            logging.info(f"Processing paper {i+1}/{total_papers}: {cite_key}")
            
            try:
                # Assess relevancy if needed
                if needs_relevancy:
                    logging.info(f"  - Assessing relevancy for {cite_key}")
                    new_relevancy = self.assess_relevancy(paper)
                    if new_relevancy:
                        paper['Relevancy'] = new_relevancy
                        relevancy = new_relevancy
                        logging.info(f"  - Relevancy: {new_relevancy}")
                    else:
                        logging.error(f"  - Failed to assess relevancy for {cite_key}")
                        error_count += 1
                        continue
                
                # Generate justification if needed
                if needs_justification and relevancy:
                    logging.info(f"  - Generating justification for {cite_key}")
                    new_justification = self.generate_justification(paper, relevancy)
                    if new_justification:
                        paper['Relevancy Justification'] = new_justification
                        logging.info(f"  - Generated justification")
                    else:
                        logging.error(f"  - Failed to generate justification for {cite_key}")
                        error_count += 1
                        continue
                
                processed_count += 1
                self.checkpoint_data['processed'].append(cite_key)
                self.checkpoint_data['last_index'] = i + 1
                
                # Save checkpoint every 10 papers
                if processed_count % 10 == 0:
                    self.save_checkpoint()
                    logging.info(f"Checkpoint saved. Processed: {processed_count}")
                
                # Rate limiting - wait 1 second between API calls
                time.sleep(1)
                
            except Exception as e:
                logging.error(f"Error processing paper {cite_key}: {str(e)}")
                error_count += 1
                continue
        
        # Write updated data
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(papers)
        
        # Final checkpoint save
        self.save_checkpoint()
        
        # Summary statistics
        logging.info("\n=== Processing Complete ===")
        logging.info(f"Total papers: {total_papers}")
        logging.info(f"Processed: {processed_count}")
        logging.info(f"Skipped: {skipped_count}")
        logging.info(f"Errors: {error_count}")
        logging.info(f"Output saved to: {output_file}")


def main():
    try:
        # Load KiloCode configuration
        config = load_config()
        logging.info("KiloCode configuration loaded successfully")
        
    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
        print("\nTo set up KiloCode:")
        print("1. Create a .env file in the project root")
        print("2. Add: KILOCODE_TOKEN='your-token-here'")
        print("3. Get your token from: https://kilocode.ai/auth/signin")
        sys.exit(1)
    
    # Parse command line arguments
    test_mode = '--test' in sys.argv
    
    # File paths
    input_file = 'research_papers_complete.csv'
    output_file = 'research_papers_complete_updated.csv' if not test_mode else 'research_papers_test_output.csv'
    
    # Create analyzer and process papers
    analyzer = RelevancyAnalyzer(config)
    analyzer.process_papers(input_file, output_file, test_mode)


if __name__ == "__main__":
    main()
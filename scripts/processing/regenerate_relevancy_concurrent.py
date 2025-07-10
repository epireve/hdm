#!/usr/bin/env python3
"""
Regenerate relevancy data concurrently using existing checkpoint
"""

import csv
import json
import os
import sys
import time
from typing import Dict, List, Optional
import urllib.request
import urllib.error
import urllib.parse
import ssl
from datetime import datetime
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Add project root to path to import from lib
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
from lib.kilocode_config_simple import load_config, ConfigurationError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(threadName)s] - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("relevancy_regeneration.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

# Research focus context (same as before)
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

# Thread-safe progress tracking
progress_lock = threading.Lock()
progress_data = {
    'processed': 0,
    'errors': 0,
    'total': 0
}

def make_api_request(config, prompt: str, max_tokens: int = 300) -> Optional[str]:
    """Make API request using urllib"""
    base_url = f"{config.openrouter_url}/chat/completions"
    model = "anthropic/claude-3.5-sonnet"
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3 if max_tokens == 50 else 0.5,
        "max_tokens": max_tokens
    }
    
    req = urllib.request.Request(
        base_url,
        data=json.dumps(data).encode('utf-8'),
        headers=config.headers
    )
    
    # Create SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, context=ssl_context) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        logging.error(f"API request error: {str(e)}")
        return None

def process_single_paper(config, paper: Dict) -> Dict:
    """Process a single paper and return updated data"""
    cite_key = paper.get('cite_key', 'unknown')
    thread_name = threading.current_thread().name
    
    try:
        # Check what needs processing
        relevancy = paper.get('Relevancy', '').strip()
        needs_relevancy = not relevancy or relevancy.lower() in ['', 'none', 'null']
        
        justification = paper.get('Relevancy Justification', '').strip()
        needs_justification = not justification or justification.lower() in ['', 'none', 'null', 'not available']
        
        # Process relevancy if needed
        if needs_relevancy:
            logging.info(f"[{thread_name}] Assessing relevancy for {cite_key}")
            
            prompt = f"""Based on the following research focus and paper information, assess the relevancy level.

{RESEARCH_FOCUS}

{RELEVANCY_CRITERIA}

Paper Information:
- Title: {paper.get('title', 'N/A')}
- Summary: {paper.get('Summary', 'N/A')}
- Research Question: {paper.get('Research Question', 'N/A')}
- Key Findings: {paper.get('Key Findings', 'N/A')}
- Tags: {paper.get('Tags', 'N/A')}

Provide ONLY the relevancy level (SUPER, HIGH, MEDIUM, or LOW) as a single word response."""
            
            result = make_api_request(config, prompt, max_tokens=50)
            if result:
                relevancy = result.upper()
                if relevancy in ["SUPER", "HIGH", "MEDIUM", "LOW"]:
                    paper['Relevancy'] = relevancy
                else:
                    paper['Relevancy'] = "MEDIUM"
            else:
                raise Exception("Failed to get relevancy")
        
        # Process justification if needed
        if needs_justification and paper.get('Relevancy'):
            logging.info(f"[{thread_name}] Generating justification for {cite_key}")
            
            prompt = f"""Based on the following research focus and paper information, provide a detailed justification for why this paper has been rated as {paper['Relevancy']} relevancy.

{RESEARCH_FOCUS}

Paper Information:
- Title: {paper.get('title', 'N/A')}
- Summary: {paper.get('Summary', 'N/A')}
- Research Question: {paper.get('Research Question', 'N/A')}
- Methodology: {paper.get('Methodology', 'N/A')}
- Key Findings: {paper.get('Key Findings', 'N/A')}
- Primary Outcomes: {paper.get('Primary Outcomes', 'N/A')}
- Implementation Insights: {paper.get('Implementation Insights', 'N/A')}
- Tags: {paper.get('Tags', 'N/A')}

Relevancy Level: {paper['Relevancy']}

Provide a 2-3 sentence justification explaining why this paper received this relevancy rating. Focus on specific aspects of the paper that align or don't align with our research focus on heterogeneous data integration in PKG architectures. Be specific and reference actual content from the paper."""
            
            result = make_api_request(config, prompt, max_tokens=300)
            if result:
                paper['Relevancy Justification'] = result
            else:
                raise Exception("Failed to get justification")
        
        # Update progress
        with progress_lock:
            progress_data['processed'] += 1
            current = progress_data['processed']
            total = progress_data['total']
            pct = (current / total * 100) if total > 0 else 0
            logging.info(f"Progress: {current}/{total} ({pct:.1f}%)")
        
        return paper
        
    except Exception as e:
        logging.error(f"Error processing {cite_key}: {str(e)}")
        with progress_lock:
            progress_data['errors'] += 1
        return paper

def main():
    try:
        # Load KiloCode configuration
        config = load_config()
        logging.info("KiloCode configuration loaded successfully")
        
    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    
    # File paths
    input_file = project_root / "research_papers_complete.csv"
    output_file = project_root / "research_papers_complete_regenerated.csv"
    checkpoint_file = Path(__file__).parent / "relevancy_checkpoint.json"
    
    # Load checkpoint
    with open(checkpoint_file, 'r') as f:
        checkpoint = json.load(f)
    processed_keys = set(checkpoint['processed'])
    logging.info(f"Checkpoint shows {len(processed_keys)} papers to regenerate")
    
    # Read all papers
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_papers = list(reader)
        fieldnames = reader.fieldnames
    
    # Filter papers that need processing
    papers_to_process = []
    for paper in all_papers:
        cite_key = paper.get('cite_key')
        if cite_key in processed_keys:
            # Check if it needs regeneration
            rel = paper.get('Relevancy', '').strip()
            just = paper.get('Relevancy Justification', '').strip()
            if not rel or not just or just.lower() in ['', 'none', 'null', 'not available']:
                papers_to_process.append(paper)
    
    logging.info(f"Found {len(papers_to_process)} papers needing regeneration")
    progress_data['total'] = len(papers_to_process)
    
    # Process concurrently with fewer workers to avoid rate limits
    max_workers = 3  # Reduced to avoid rate limits
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="Worker") as executor:
        # Submit all tasks
        future_to_paper = {
            executor.submit(process_single_paper, config, paper): paper
            for paper in papers_to_process
        }
        
        # Process results as they complete
        for future in as_completed(future_to_paper):
            original_paper = future_to_paper[future]
            cite_key = original_paper.get('cite_key')
            
            try:
                updated_paper = future.result()
                results[cite_key] = updated_paper
                
                # Delay to respect rate limits
                time.sleep(2)  # Increased delay between requests
                
            except Exception as e:
                logging.error(f"Failed to process {cite_key}: {str(e)}")
    
    # Update all papers with results
    for paper in all_papers:
        cite_key = paper.get('cite_key')
        if cite_key in results:
            paper['Relevancy'] = results[cite_key].get('Relevancy', paper.get('Relevancy', ''))
            paper['Relevancy Justification'] = results[cite_key].get('Relevancy Justification', paper.get('Relevancy Justification', ''))
    
    # Write complete dataset
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_papers)
    
    logging.info(f"\nProcessing complete!")
    logging.info(f"Output saved to: {output_file}")
    logging.info(f"Processed: {progress_data['processed']}")
    logging.info(f"Errors: {progress_data['errors']}")
    
    # Final statistics
    stats = {'SUPER': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'Missing': 0}
    has_justification = 0
    
    for paper in all_papers:
        rel = paper.get('Relevancy', '').strip().upper()
        if rel in stats:
            stats[rel] += 1
        else:
            stats['Missing'] += 1
        
        just = paper.get('Relevancy Justification', '').strip()
        if just and just.lower() not in ['', 'none', 'null', 'not available']:
            has_justification += 1
    
    print("\n=== Final Statistics ===")
    print(f"Total papers: {len(all_papers)}")
    for level, count in stats.items():
        if count > 0:
            print(f"  {level}: {count}")
    print(f"Papers with justifications: {has_justification}")

if __name__ == "__main__":
    main()
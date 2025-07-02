#!/usr/bin/env python3
"""
Batch update keywords in markdown files based on abstract content
"""
import sys
import re
import os
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import yaml
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import MARKDOWN_DIR, BACKUP_DIR, LOG_DIR
from utils import setup_logging


class BatchKeywordUpdater:
    """Update keywords in research papers based on abstracts"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "files_processed": 0,
            "keywords_updated": 0,
            "no_abstract": 0,
            "errors": 0,
            "skipped": 0
        }
        
        # Technical term patterns for different domains
        self.domain_keywords = {
            'ml_ai': [
                'machine learning', 'deep learning', 'neural network', 'artificial intelligence',
                'supervised learning', 'unsupervised learning', 'reinforcement learning',
                'classification', 'regression', 'clustering', 'prediction',
                'convolutional neural network', 'recurrent neural network', 'transformer',
                'lstm', 'gru', 'cnn', 'rnn', 'gan', 'vae', 'bert', 'gpt',
                'gradient descent', 'backpropagation', 'optimization', 'regularization',
                'overfitting', 'underfitting', 'cross-validation', 'hyperparameter',
                'feature extraction', 'feature engineering', 'dimensionality reduction',
                'transfer learning', 'meta-learning', 'few-shot learning',
                'computer vision', 'natural language processing', 'nlp'
            ],
            'kg': [
                'knowledge graph', 'ontology', 'semantic web', 'entity linking',
                'relation extraction', 'graph embedding', 'knowledge representation',
                'reasoning', 'inference', 'triple', 'rdf', 'sparql', 'owl',
                'entity resolution', 'knowledge base', 'semantic similarity',
                'graph neural network', 'node embedding', 'link prediction',
                'knowledge graph completion', 'knowledge graph embedding',
                'temporal knowledge graph', 'dynamic knowledge graph',
                'heterogeneous graph', 'multi-relational graph'
            ],
            'security_privacy': [
                'cryptography', 'encryption', 'decryption', 'authentication',
                'authorization', 'access control', 'security', 'privacy',
                'homomorphic encryption', 'differential privacy', 'secure computation',
                'zero-knowledge proof', 'digital signature', 'hash function',
                'public key', 'private key', 'symmetric encryption', 'asymmetric encryption',
                'blockchain', 'distributed ledger', 'consensus', 'smart contract',
                'secure multiparty computation', 'secret sharing', 'threshold cryptography',
                'privacy-preserving', 'data privacy', 'model privacy'
            ],
            'fl': [
                'federated learning', 'distributed learning', 'edge computing',
                'model aggregation', 'client selection', 'communication efficiency',
                'gradient compression', 'model compression', 'secure aggregation',
                'parameter server', 'decentralized learning', 'collaborative learning',
                'local training', 'global model', 'model update', 'heterogeneous data',
                'non-iid data', 'client drift', 'system heterogeneity'
            ],
            'temporal': [
                'temporal', 'time series', 'temporal dynamics', 'temporal reasoning',
                'time-aware', 'temporal evolution', 'temporal pattern',
                'sequence modeling', 'temporal embedding', 'time prediction',
                'temporal consistency', 'temporal relation', 'temporal validity',
                'event prediction', 'time-stamped', 'chronological'
            ],
            'healthcare': [
                'electronic health records', 'ehr', 'clinical data', 'patient data',
                'medical diagnosis', 'treatment prediction', 'personalized medicine',
                'clinical decision support', 'biomarker', 'drug discovery',
                'medical imaging', 'healthcare analytics', 'disease prediction',
                'patient monitoring', 'health informatics', 'medical knowledge graph'
            ],
            'iot': [
                'internet of things', 'iot', 'sensor network', 'edge device',
                'smart home', 'smart city', 'wearable device', 'embedded system',
                'sensor data', 'real-time processing', 'data streaming',
                'device management', 'connectivity', 'mqtt', 'coap'
            ]
        }
    
    def extract_abstract(self, content: str) -> Optional[str]:
        """Extract abstract section from markdown content"""
        patterns = [
            r'#{1,3}\s*Abstract\s*\n+(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
            r'\*\*Abstract\*\*\s*\n+(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
            r'Abstract:\s*\n?(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
            r'ABSTRACT\s*\n+(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                abstract_text = match.group(1).strip()
                # Clean up
                abstract_text = re.sub(r'\n+', ' ', abstract_text)
                abstract_text = re.sub(r'\s+', ' ', abstract_text)
                abstract_text = re.sub(r'\*\*(.*?)\*\*', r'\1', abstract_text)
                abstract_text = re.sub(r'\*(.*?)\*', r'\1', abstract_text)
                abstract_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', abstract_text)
                return abstract_text
        
        return None
    
    def extract_keywords_from_abstract(self, abstract: str, title: str = "") -> List[str]:
        """Extract technical keywords from abstract"""
        keywords = set()
        
        # Combine title and abstract for analysis
        text = (title + " " + abstract).lower()
        
        # 1. Check for known domain keywords
        for domain, terms in self.domain_keywords.items():
            for term in terms:
                if term in text:
                    keywords.add(term)
        
        # 2. Extract compound technical terms
        compound_patterns = [
            r'\b([a-z]+(?:-[a-z]+)+)\b',  # hyphenated terms
            r'\b(\w+\s+(?:learning|network|graph|system|model|algorithm|method|framework|protocol|architecture)s?)\b',
            r'\b((?:deep|machine|reinforcement|supervised|unsupervised|transfer|meta|federated)\s+learning)\b',
            r'\b(\w+\s+(?:encryption|privacy|security|authentication))\b',
            r'\b(knowledge\s+\w+)\b',
            r'\b(graph\s+\w+)\b',
            r'\b(temporal\s+\w+)\b',
            r'\b(\w+\s+embedding)\b',
        ]
        
        for pattern in compound_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) > 3 and not self.is_fragment(match):
                    keywords.add(match)
        
        # 3. Extract acronyms and their expansions
        acronym_pattern = r'\b([A-Z]{2,})\b'
        for match in re.finditer(acronym_pattern, abstract):
            acronym = match.group(1)
            if len(acronym) <= 6:  # Reasonable acronym length
                keywords.add(acronym.lower())
        
        # 4. Extract technical terms with specific patterns
        # Terms ending with technical suffixes
        tech_suffixes = ['ation', 'ization', 'isation', 'ology', 'ometry', 'ography']
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            for suffix in tech_suffixes:
                if word.endswith(suffix) and len(word) > len(suffix) + 3:
                    keywords.add(word)
        
        # 5. Remove fragments and clean
        cleaned_keywords = []
        for kw in keywords:
            kw = kw.strip()
            if self.is_valid_keyword(kw) and not self.is_fragment(kw):
                cleaned_keywords.append(kw)
        
        # Sort and limit
        cleaned_keywords = sorted(list(set(cleaned_keywords)))
        
        # Prioritize multi-word technical terms
        multi_word = [k for k in cleaned_keywords if ' ' in k or '-' in k]
        single_word = [k for k in cleaned_keywords if ' ' not in k and '-' not in k]
        
        # Return up to 20 keywords
        final_keywords = multi_word[:12] + single_word[:8]
        return sorted(final_keywords[:20])
    
    def is_fragment(self, text: str) -> bool:
        """Check if text is a sentence fragment"""
        fragment_patterns = [
            r'^(a|an|the|this|that|these|those|we|our|us)\s+',
            r'^(and|or|but|with|for|from|to|in|on|at)\s+',
            r'^(is|are|was|were|be|been|being|have|has|had)\s+',
            r'^(can|could|will|would|should|may|might|must)\s+',
            r'^(achieves?|proposes?|presents?|introduces?|develops?)\s+',
            r'^(based|using|through|via|between|among)\s+',
            r'\s+(the|and|or|but|with|for|from|to)$',
        ]
        
        for pattern in fragment_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def is_valid_keyword(self, keyword: str) -> bool:
        """Check if keyword is valid"""
        # Length check
        if len(keyword) < 2 or len(keyword) > 50:
            return False
        
        # Not just numbers
        if keyword.isdigit():
            return False
        
        # Not just punctuation
        if all(c in '.-_()[]{}' for c in keyword):
            return False
        
        # Common words to exclude
        stopwords = {
            'abstract', 'introduction', 'conclusion', 'related', 'work',
            'paper', 'article', 'study', 'research', 'approach', 'method',
            'results', 'discussion', 'future', 'references', 'keywords',
            'however', 'therefore', 'moreover', 'furthermore', 'additionally'
        }
        
        if keyword.lower() in stopwords:
            return False
        
        return True
    
    def update_file(self, file_path: Path) -> bool:
        """Update keywords in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter
            yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if not yaml_match:
                self.logger.warning(f"No YAML frontmatter in {file_path.name}")
                self.stats["skipped"] += 1
                return False
            
            yaml_content = yaml_match.group(1)
            markdown_content = content[yaml_match.end():]
            
            # Parse YAML
            try:
                metadata = yaml.safe_load(yaml_content)
            except yaml.YAMLError as e:
                self.logger.error(f"YAML error in {file_path}: {e}")
                self.stats["errors"] += 1
                return False
            
            # Check if keywords need updating (if they look like fragments)
            current_keywords = metadata.get('keywords', [])
            needs_update = False
            
            if not current_keywords:
                needs_update = True
            else:
                # Check if current keywords are fragments
                fragment_count = sum(1 for kw in current_keywords if self.is_fragment(str(kw)))
                if fragment_count > len(current_keywords) * 0.3:  # More than 30% fragments
                    needs_update = True
            
            if not needs_update:
                self.logger.debug(f"Keywords look good in {file_path.name}")
                return False
            
            # Extract abstract
            abstract = self.extract_abstract(markdown_content)
            if not abstract:
                self.logger.warning(f"No abstract in {file_path.name}")
                self.stats["no_abstract"] += 1
                return False
            
            # Extract new keywords
            title = metadata.get('title', '')
            new_keywords = self.extract_keywords_from_abstract(abstract, title)
            
            if not new_keywords:
                self.logger.debug(f"No keywords extracted for {file_path.name}")
                return False
            
            # Update metadata
            metadata['keywords'] = new_keywords
            
            # Create backup
            backup_dir = BACKUP_DIR / "keyword_updates" / datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_file = backup_dir / file_path.name
            shutil.copy2(file_path, backup_file)
            
            # Write updated content
            new_yaml = yaml.dump(metadata, default_flow_style=False, sort_keys=False, allow_unicode=True)
            new_content = f"---\n{new_yaml}---\n{markdown_content}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"Updated keywords in {file_path.name} ({len(new_keywords)} keywords)")
            self.stats["keywords_updated"] += 1
            self.stats["files_processed"] += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            self.stats["errors"] += 1
            return False
    
    def process_all_files(self):
        """Process all markdown files"""
        # Find all markdown files
        markdown_files = []
        for folder in MARKDOWN_DIR.iterdir():
            if folder.is_dir():
                for md_file in folder.glob("*.md"):
                    markdown_files.append(md_file)
        
        self.logger.info(f"Found {len(markdown_files)} markdown files")
        
        # Process each file
        for i, md_file in enumerate(markdown_files, 1):
            self.logger.info(f"Processing {i}/{len(markdown_files)}: {md_file.name}")
            self.update_file(md_file)
            
            # Log progress
            if i % 10 == 0:
                self.logger.info(f"Progress: {i}/{len(markdown_files)} files")
                self.logger.info(f"Updated: {self.stats['keywords_updated']}")
    
    def print_summary(self):
        """Print processing summary"""
        print("\n" + "="*60)
        print("KEYWORD UPDATE SUMMARY")
        print("="*60)
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Keywords updated: {self.stats['keywords_updated']}")
        print(f"Files without abstract: {self.stats['no_abstract']}")
        print(f"Files skipped: {self.stats['skipped']}")
        print(f"Errors: {self.stats['errors']}")
        print("="*60)


def main():
    """Main function"""
    logger = setup_logging("batch_keyword_updater")
    logger.info("Starting batch keyword update")
    
    updater = BatchKeywordUpdater(logger)
    updater.process_all_files()
    updater.print_summary()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Add keywords to all markdown files by extracting from content
"""
import sys
import re
import os
from pathlib import Path
from typing import Dict, List, Set, Optional
import yaml
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import MARKDOWN_DIR, BACKUP_DIR, LOG_DIR
from utils import setup_logging


class KeywordExtractor:
    """Extracts keywords from markdown files"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "files_processed": 0,
            "keywords_added": 0,
            "keywords_updated": 0,
            "errors": 0,
            "skipped": 0
        }
        
        # Common technical terms to look for (lowercase)
        self.technical_terms = {
            # ML/AI terms
            "neural network", "deep learning", "machine learning", "artificial intelligence",
            "reinforcement learning", "supervised learning", "unsupervised learning",
            "semi-supervised learning", "transfer learning", "meta-learning",
            "gradient descent", "backpropagation", "optimization", "regularization",
            "overfitting", "underfitting", "cross-validation", "hyperparameter",
            
            # Model types
            "lstm", "rnn", "cnn", "gnn", "transformer", "bert", "gpt",
            "autoencoder", "gan", "vae", "resnet", "vgg", "alexnet",
            "random forest", "svm", "decision tree", "ensemble",
            
            # Federated Learning
            "federated learning", "federated averaging", "fedavg", "secure aggregation",
            "local model", "global model", "model aggregation", "client selection",
            "non-iid", "data heterogeneity", "communication efficiency",
            
            # Privacy & Security
            "differential privacy", "homomorphic encryption", "secure multiparty computation",
            "privacy preservation", "data privacy", "model privacy", "gradient leakage",
            "membership inference", "model inversion", "backdoor attack",
            "poisoning attack", "byzantine attack", "adversarial attack",
            
            # Cryptography
            "encryption", "decryption", "public key", "private key", "secret sharing",
            "threshold cryptography", "zero-knowledge proof", "commitment scheme",
            "hash function", "digital signature", "authentication",
            
            # Knowledge Graphs
            "knowledge graph", "ontology", "semantic web", "rdf", "sparql",
            "entity linking", "relation extraction", "knowledge embedding",
            "graph embedding", "node embedding", "link prediction",
            "knowledge base", "triple", "entity", "relation",
            
            # Healthcare/Medical
            "ehr", "electronic health record", "clinical data", "patient data",
            "medical imaging", "diagnosis", "prognosis", "treatment",
            "personalized medicine", "precision medicine", "clinical decision support",
            "biomarker", "genomics", "proteomics", "drug discovery",
            
            # Data Science
            "data preprocessing", "feature extraction", "feature engineering",
            "dimensionality reduction", "clustering", "classification", "regression",
            "time series", "anomaly detection", "outlier detection",
            "data augmentation", "data synthesis", "data generation",
            
            # Distributed Systems
            "distributed computing", "parallel computing", "edge computing",
            "cloud computing", "fog computing", "iot", "blockchain",
            "consensus", "synchronization", "asynchronous", "latency",
            
            # Evaluation Metrics
            "accuracy", "precision", "recall", "f1-score", "auc", "roc",
            "mse", "rmse", "mae", "loss function", "perplexity",
            "convergence", "performance", "efficiency", "scalability"
        }
        
        # Common abbreviations and their expansions
        self.abbreviations = {
            "ml": "machine learning",
            "dl": "deep learning",
            "ai": "artificial intelligence",
            "fl": "federated learning",
            "he": "homomorphic encryption",
            "mpc": "multiparty computation",
            "dp": "differential privacy",
            "kg": "knowledge graph",
            "nlp": "natural language processing",
            "cv": "computer vision",
            "rl": "reinforcement learning",
            "gan": "generative adversarial network",
            "vae": "variational autoencoder",
            "cnn": "convolutional neural network",
            "rnn": "recurrent neural network",
            "lstm": "long short-term memory",
            "gru": "gated recurrent unit",
            "bert": "bidirectional encoder representations from transformers",
            "gpt": "generative pre-trained transformer",
            "ehr": "electronic health record",
            "emr": "electronic medical record",
            "phr": "personal health record",
            "iot": "internet of things",
            "api": "application programming interface",
            "sdk": "software development kit",
            "http": "hypertext transfer protocol",
            "tcp": "transmission control protocol",
            "ip": "internet protocol",
            "ssl": "secure sockets layer",
            "tls": "transport layer security",
            "sgd": "stochastic gradient descent",
            "adam": "adaptive moment estimation",
            "bce": "binary cross entropy",
            "mse": "mean squared error",
            "mae": "mean absolute error",
            "rmse": "root mean squared error",
            "auc": "area under curve",
            "roc": "receiver operating characteristic",
            "kl": "kullback-leibler",
            "gan": "generative adversarial network",
            "dcgan": "deep convolutional gan",
            "wgan": "wasserstein gan",
            "ddpm": "denoising diffusion probabilistic model",
            "clip": "contrastive language-image pre-training"
        }
    
    def extract_keywords_from_content(self, content: str, title: str = "") -> List[str]:
        """Extract keywords from markdown content"""
        keywords = set()
        
        # Convert content to lowercase for matching
        search_text = (title + " " + content).lower()
        
        # Remove code blocks to avoid matching code
        search_text = re.sub(r'```[\s\S]*?```', '', search_text)
        search_text = re.sub(r'`[^`]+`', '', search_text)
        
        # Extract section headers as potential keywords
        headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        for header in headers:
            # Clean header
            header_clean = header.lower().strip()
            header_clean = re.sub(r'[^\w\s-]', '', header_clean)
            if 3 <= len(header_clean) <= 50 and header_clean not in ['introduction', 'conclusion', 'abstract', 'references', 'acknowledgments']:
                keywords.add(header_clean)
        
        # Look for technical terms
        for term in self.technical_terms:
            # Use word boundaries for more accurate matching
            if re.search(r'\b' + re.escape(term) + r'\b', search_text):
                keywords.add(term)
        
        # Look for abbreviations in parentheses
        abbrev_pattern = r'\b([A-Z]{2,})\b'
        for match in re.finditer(abbrev_pattern, content):
            abbrev = match.group(1).lower()
            if abbrev in self.abbreviations:
                keywords.add(self.abbreviations[abbrev])
                keywords.add(abbrev.upper())
        
        # Extract terms in quotes or emphasis
        quoted_terms = re.findall(r'"([^"]{3,30})"', content)
        for term in quoted_terms:
            term_clean = term.lower().strip()
            if re.match(r'^[a-z\s-]+$', term_clean) and ' ' in term_clean:
                keywords.add(term_clean)
        
        # Extract italicized terms
        italic_terms = re.findall(r'\*([^*]{3,30})\*', content)
        for term in italic_terms:
            term_clean = term.lower().strip()
            if re.match(r'^[a-z\s-]+$', term_clean):
                keywords.add(term_clean)
        
        # Extract method/algorithm names (often capitalized)
        method_pattern = r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b'
        for match in re.finditer(method_pattern, content):
            method = match.group(1)
            if len(method) > 4:  # Avoid short acronyms
                keywords.add(method)
        
        # Extract compound terms with hyphens
        hyphen_terms = re.findall(r'\b([a-z]+-[a-z]+(?:-[a-z]+)*)\b', search_text)
        for term in hyphen_terms:
            if len(term) > 5 and term.count('-') <= 3:
                keywords.add(term)
        
        # Look for specific patterns
        # "X-based Y" pattern
        based_pattern = r'(\w+)-based\s+(\w+)'
        for match in re.finditer(based_pattern, search_text):
            keywords.add(f"{match.group(1)}-based {match.group(2)}")
        
        # "X learning" pattern
        learning_pattern = r'(\w+)\s+learning\b'
        for match in re.finditer(learning_pattern, search_text):
            if match.group(1) not in ['machine', 'deep']:
                keywords.add(f"{match.group(1)} learning")
        
        # Remove too common or too short keywords
        keywords = {k for k in keywords if len(k) > 2 and k not in ['the', 'and', 'for', 'with', 'from', 'this', 'that']}
        
        # Sort and limit to reasonable number
        keywords_list = sorted(list(keywords))
        if len(keywords_list) > 30:
            # Prioritize multi-word terms and technical terms
            multi_word = [k for k in keywords_list if ' ' in k or '-' in k]
            single_word = [k for k in keywords_list if ' ' not in k and '-' not in k]
            keywords_list = multi_word[:20] + single_word[:10]
        
        return sorted(keywords_list)
    
    def update_markdown_file(self, file_path: Path) -> bool:
        """Update a single markdown file with keywords"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter
            yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if not yaml_match:
                self.logger.warning(f"No YAML frontmatter found in {file_path}")
                self.stats["skipped"] += 1
                return False
            
            yaml_content = yaml_match.group(1)
            markdown_content = content[yaml_match.end():]
            
            # Parse YAML
            try:
                metadata = yaml.safe_load(yaml_content)
            except yaml.YAMLError as e:
                self.logger.error(f"YAML parse error in {file_path}: {e}")
                self.stats["errors"] += 1
                return False
            
            # Extract keywords
            title = metadata.get('title', '')
            keywords = self.extract_keywords_from_content(markdown_content, title)
            
            if not keywords:
                self.logger.debug(f"No keywords extracted for {file_path.name}")
                return False
            
            # Update or add keywords
            if 'keywords' in metadata:
                # Merge with existing keywords
                existing = set(metadata['keywords']) if isinstance(metadata['keywords'], list) else set()
                new_keywords = sorted(list(existing.union(set(keywords))))
                if new_keywords != metadata['keywords']:
                    metadata['keywords'] = new_keywords
                    self.stats["keywords_updated"] += 1
                    changes_made = True
                else:
                    changes_made = False
            else:
                metadata['keywords'] = keywords
                self.stats["keywords_added"] += 1
                changes_made = True
            
            if changes_made:
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
                
                self.logger.info(f"Added {len(keywords)} keywords to {file_path.name}")
                self.stats["files_processed"] += 1
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            self.stats["errors"] += 1
            return False
    
    def process_all_files(self) -> None:
        """Process all markdown files in the directory"""
        # Find all markdown files
        markdown_files = []
        for folder in MARKDOWN_DIR.iterdir():
            if folder.is_dir():
                for md_file in folder.glob("*.md"):
                    markdown_files.append(md_file)
        
        self.logger.info(f"Found {len(markdown_files)} markdown files to process")
        
        # Process each file
        for i, md_file in enumerate(markdown_files, 1):
            self.logger.info(f"Processing {i}/{len(markdown_files)}: {md_file.parent.name}/{md_file.name}")
            self.update_markdown_file(md_file)
            
            # Log progress every 10 files
            if i % 10 == 0:
                self.logger.info(f"Progress: {i}/{len(markdown_files)} files processed")
    
    def print_summary(self):
        """Print processing summary"""
        self.logger.info("\n" + "="*50)
        self.logger.info("KEYWORD EXTRACTION SUMMARY")
        self.logger.info("="*50)
        self.logger.info(f"Files processed: {self.stats['files_processed']}")
        self.logger.info(f"Files skipped: {self.stats['skipped']}")
        self.logger.info(f"Keywords added (new): {self.stats['keywords_added']}")
        self.logger.info(f"Keywords updated (existing): {self.stats['keywords_updated']}")
        self.logger.info(f"Errors: {self.stats['errors']}")
        self.logger.info("="*50)


def main():
    """Main function"""
    logger = setup_logging("keyword_extractor")
    logger.info("Starting keyword extraction for all markdown files")
    
    extractor = KeywordExtractor(logger)
    extractor.process_all_files()
    extractor.print_summary()
    
    return 0 if extractor.stats["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
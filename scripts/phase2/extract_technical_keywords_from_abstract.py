#!/usr/bin/env python3
"""
Extract technical keywords from the abstract section of research papers
Focuses on complete terms and technical concepts, not fragments
"""
import sys
import re
import os
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import yaml
from datetime import datetime
import shutil
import nltk
from collections import Counter

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import MARKDOWN_DIR, BACKUP_DIR, LOG_DIR
from utils import setup_logging

# Try to download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except:
        pass

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    try:
        nltk.download('averaged_perceptron_tagger', quiet=True)
    except:
        pass


class TechnicalKeywordExtractor:
    """Extracts technical keywords from abstract sections of research papers"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "files_processed": 0,
            "keywords_added": 0,
            "keywords_updated": 0,
            "errors": 0,
            "skipped": 0,
            "no_abstract": 0
        }
        
        # Technical term patterns
        self.technical_patterns = [
            # Compound terms with hyphens
            r'\b([a-z]+(?:-[a-z]+)+)\b',
            # Acronyms
            r'\b([A-Z]{2,})\b',
            # Camel case terms
            r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b',
            # Terms with numbers (e.g., "3D", "IPv6")
            r'\b([A-Za-z]+\d+[A-Za-z]*|\d+[A-Za-z]+)\b',
        ]
        
        # Common technical term endings
        self.technical_endings = [
            'ation', 'ization', 'isation', 'ology', 'ometry', 'ography',
            'analysis', 'synthesis', 'algorithm', 'method', 'technique',
            'system', 'model', 'framework', 'approach', 'scheme', 'protocol',
            'network', 'graph', 'tree', 'structure', 'architecture',
            'learning', 'training', 'inference', 'prediction', 'classification',
            'encryption', 'decryption', 'security', 'privacy', 'authentication'
        ]
        
        # Domain-specific technical terms
        self.domain_terms = {
            'ml': {
                'machine learning', 'deep learning', 'neural network', 'artificial intelligence',
                'supervised learning', 'unsupervised learning', 'reinforcement learning',
                'classification', 'regression', 'clustering', 'prediction', 'training',
                'validation', 'optimization', 'algorithm', 'model', 'dataset',
                'feature extraction', 'feature engineering', 'dimensionality reduction',
                'cross-validation', 'hyperparameter tuning', 'gradient descent',
                'backpropagation', 'activation function', 'loss function',
                'convolutional neural network', 'recurrent neural network', 'transformer',
                'lstm', 'gru', 'cnn', 'rnn', 'gan', 'vae', 'bert', 'gpt'
            },
            'kg': {
                'knowledge graph', 'ontology', 'semantic web', 'entity linking',
                'relation extraction', 'graph embedding', 'knowledge representation',
                'reasoning', 'inference', 'triple', 'rdf', 'sparql', 'owl',
                'entity resolution', 'knowledge base', 'semantic similarity',
                'graph neural network', 'node embedding', 'link prediction',
                'knowledge graph completion', 'knowledge graph embedding'
            },
            'security': {
                'cryptography', 'encryption', 'decryption', 'authentication',
                'authorization', 'access control', 'security', 'privacy',
                'homomorphic encryption', 'differential privacy', 'secure computation',
                'zero-knowledge proof', 'digital signature', 'hash function',
                'public key', 'private key', 'symmetric encryption', 'asymmetric encryption',
                'blockchain', 'distributed ledger', 'consensus', 'smart contract'
            },
            'fl': {
                'federated learning', 'distributed learning', 'edge computing',
                'privacy-preserving', 'model aggregation', 'client selection',
                'communication efficiency', 'gradient compression', 'model compression',
                'secure aggregation', 'differential privacy', 'homomorphic encryption',
                'parameter server', 'decentralized learning', 'collaborative learning'
            },
            'temporal': {
                'temporal', 'time series', 'temporal dynamics', 'temporal knowledge graph',
                'temporal reasoning', 'time-aware', 'temporal evolution', 'temporal pattern',
                'sequence modeling', 'temporal embedding', 'time prediction',
                'temporal consistency', 'temporal relation', 'temporal validity'
            }
        }
    
    def extract_abstract(self, content: str) -> Optional[str]:
        """Extract abstract section from markdown content"""
        # Try different abstract patterns
        patterns = [
            # ## Abstract
            r'#{1,3}\s*Abstract\s*\n+(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
            # **Abstract**
            r'\*\*Abstract\*\*\s*\n+(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
            # Abstract: ...
            r'Abstract:\s*\n?(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
            # ABSTRACT (all caps)
            r'ABSTRACT\s*\n+(.*?)(?=\n#{1,3}\s+|\n\n#{1,3}\s+|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                abstract_text = match.group(1).strip()
                # Clean up the abstract text
                abstract_text = re.sub(r'\n+', ' ', abstract_text)  # Replace multiple newlines with space
                abstract_text = re.sub(r'\s+', ' ', abstract_text)  # Replace multiple spaces with single space
                # Remove markdown formatting
                abstract_text = re.sub(r'\*\*(.*?)\*\*', r'\1', abstract_text)  # Bold
                abstract_text = re.sub(r'\*(.*?)\*', r'\1', abstract_text)  # Italic
                abstract_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', abstract_text)  # Links
                return abstract_text
        
        return None
    
    def extract_noun_phrases(self, text: str) -> List[str]:
        """Extract noun phrases that are likely technical terms"""
        noun_phrases = []
        
        try:
            # Tokenize and POS tag
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            
            # Simple noun phrase pattern: (Adjective|Noun)* Noun
            i = 0
            while i < len(pos_tags):
                # Look for sequences that end with a noun
                if pos_tags[i][1] in ['NN', 'NNS', 'NNP', 'NNPS']:
                    phrase = [pos_tags[i][0]]
                    j = i - 1
                    # Look backwards for adjectives and other nouns
                    while j >= 0 and pos_tags[j][1] in ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS', 'VBG']:
                        phrase.insert(0, pos_tags[j][0])
                        j -= 1
                    
                    # Join the phrase
                    phrase_str = ' '.join(phrase)
                    
                    # Filter phrases
                    if (len(phrase) > 1 and len(phrase_str) > 5 and 
                        len(phrase_str) < 50 and not phrase_str.lower() in self.get_stopwords()):
                        noun_phrases.append(phrase_str.lower())
                
                i += 1
                
        except Exception as e:
            self.logger.debug(f"Error in noun phrase extraction: {e}")
        
        return noun_phrases
    
    def extract_technical_keywords(self, abstract: str) -> List[str]:
        """Extract technical keywords from abstract text"""
        keywords = set()
        abstract_lower = abstract.lower()
        
        # 1. Extract known domain terms
        for domain, terms in self.domain_terms.items():
            for term in terms:
                if term in abstract_lower:
                    keywords.add(term)
        
        # 2. Extract technical patterns
        for pattern in self.technical_patterns:
            matches = re.findall(pattern, abstract, re.IGNORECASE)
            for match in matches:
                if len(match) > 2:
                    keywords.add(match.lower())
        
        # 3. Extract terms ending with technical suffixes
        words = re.findall(r'\b\w+\b', abstract_lower)
        for word in words:
            for ending in self.technical_endings:
                if word.endswith(ending) and len(word) > len(ending) + 2:
                    keywords.add(word)
                    break
        
        # 4. Extract noun phrases
        noun_phrases = self.extract_noun_phrases(abstract)
        
        # Filter noun phrases to keep only technical ones
        for phrase in noun_phrases:
            # Check if phrase contains technical terms
            phrase_words = phrase.split()
            is_technical = False
            
            # Check if any word in phrase is already a keyword
            for word in phrase_words:
                if word in keywords:
                    is_technical = True
                    break
            
            # Check if phrase contains technical patterns
            if not is_technical:
                for pattern in self.technical_patterns:
                    if re.search(pattern, phrase):
                        is_technical = True
                        break
            
            # Check if phrase ends with technical term
            if not is_technical:
                last_word = phrase_words[-1] if phrase_words else ''
                for ending in self.technical_endings[:10]:  # Check common endings
                    if last_word.endswith(ending):
                        is_technical = True
                        break
            
            if is_technical:
                keywords.add(phrase)
        
        # 5. Extract capitalized technical terms (but not regular sentence starts)
        sentences = re.split(r'[.!?]\s+', abstract)
        for sentence in sentences:
            # Skip first word of sentence
            words = sentence.split()
            for i, word in enumerate(words[1:], 1):
                if word[0].isupper() and word.lower() not in self.get_stopwords():
                    # Check if it's a technical term (appears elsewhere in lowercase)
                    if word.lower() in abstract_lower:
                        keywords.add(word.lower())
        
        # 6. Clean and filter keywords
        filtered_keywords = set()
        for kw in keywords:
            # Clean the keyword
            kw = kw.strip()
            kw = re.sub(r'^[^\w]+|[^\w]+$', '', kw)  # Remove non-word chars from ends
            
            # Filter
            if (3 <= len(kw) <= 50 and 
                not kw.isdigit() and
                not all(c in '.-_' for c in kw) and
                kw not in self.get_stopwords()):
                filtered_keywords.add(kw)
        
        # 7. Prioritize multi-word technical terms
        final_keywords = []
        multi_word = sorted([k for k in filtered_keywords if ' ' in k or '-' in k])
        single_word = sorted([k for k in filtered_keywords if ' ' not in k and '-' not in k])
        
        # Add multi-word terms first
        final_keywords.extend(multi_word[:12])
        
        # Add single-word terms
        remaining_slots = 20 - len(final_keywords)
        if remaining_slots > 0:
            final_keywords.extend(single_word[:remaining_slots])
        
        return sorted(final_keywords)
    
    def get_stopwords(self) -> Set[str]:
        """Get common stopwords to filter out"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'under', 'again',
            'further', 'then', 'once', 'that', 'this', 'these', 'those', 'is',
            'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'must', 'can', 'cannot', 'it', 'its', 'itself', 'they',
            'them', 'their', 'what', 'which', 'who', 'whom', 'whose', 'when',
            'where', 'why', 'how', 'all', 'each', 'few', 'more', 'some', 'such',
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also',
            'we', 'our', 'us', 'he', 'she', 'him', 'her', 'his', 'hers',
            'however', 'therefore', 'thus', 'hence', 'moreover', 'furthermore',
            'additionally', 'specifically', 'particularly', 'especially',
            'namely', 'notably', 'significantly', 'consequently', 'subsequently',
            'previously', 'finally', 'ultimately', 'basically', 'essentially'
        }
    
    def update_markdown_file(self, file_path: Path) -> bool:
        """Update a single markdown file with keywords from abstract"""
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
            
            # Extract abstract
            abstract = self.extract_abstract(markdown_content)
            if not abstract:
                self.logger.warning(f"No abstract found in {file_path.name}")
                self.stats["no_abstract"] += 1
                return False
            
            # Extract keywords from abstract
            keywords = self.extract_technical_keywords(abstract)
            
            if not keywords:
                self.logger.debug(f"No keywords extracted from abstract in {file_path.name}")
                return False
            
            # Update or add keywords
            changes_made = False
            if 'keywords' in metadata:
                metadata['keywords'] = keywords
                self.stats["keywords_updated"] += 1
                changes_made = True
            else:
                metadata['keywords'] = keywords
                self.stats["keywords_added"] += 1
                changes_made = True
            
            if changes_made:
                # Create backup
                backup_dir = BACKUP_DIR / "technical_keywords" / datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_dir.mkdir(parents=True, exist_ok=True)
                backup_file = backup_dir / file_path.name
                shutil.copy2(file_path, backup_file)
                
                # Write updated content
                new_yaml = yaml.dump(metadata, default_flow_style=False, sort_keys=False, allow_unicode=True)
                new_content = f"---\n{new_yaml}---\n{markdown_content}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                self.logger.info(f"Added {len(keywords)} technical keywords from abstract to {file_path.name}")
                self.logger.debug(f"Keywords: {', '.join(keywords[:10])}...")
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
        self.logger.info("TECHNICAL KEYWORD EXTRACTION SUMMARY")
        self.logger.info("="*50)
        self.logger.info(f"Files processed: {self.stats['files_processed']}")
        self.logger.info(f"Files skipped: {self.stats['skipped']}")
        self.logger.info(f"Files without abstract: {self.stats['no_abstract']}")
        self.logger.info(f"Keywords added (new): {self.stats['keywords_added']}")
        self.logger.info(f"Keywords updated (existing): {self.stats['keywords_updated']}")
        self.logger.info(f"Errors: {self.stats['errors']}")
        self.logger.info("="*50)


def main():
    """Main function"""
    logger = setup_logging("technical_keyword_extractor")
    logger.info("Starting technical keyword extraction from abstracts")
    
    extractor = TechnicalKeywordExtractor(logger)
    extractor.process_all_files()
    extractor.print_summary()
    
    return 0 if extractor.stats["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
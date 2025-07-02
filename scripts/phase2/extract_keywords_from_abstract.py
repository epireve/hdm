#!/usr/bin/env python3
"""
Extract keywords from the abstract section of research papers
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


class AbstractKeywordExtractor:
    """Extracts keywords from abstract sections of research papers"""
    
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
                return abstract_text
        
        return None
    
    def extract_keywords_from_abstract(self, abstract: str) -> List[str]:
        """Extract keywords from abstract text"""
        keywords = set()
        
        # Convert to lowercase for processing
        abstract_lower = abstract.lower()
        
        # 1. Extract technical terms and phrases
        # Look for noun phrases (simplified pattern)
        noun_phrase_pattern = r'\b((?:[a-z]+\s+)?(?:[a-z]+\s+)?[a-z]+(?:\s+[a-z]+)?)\b'
        
        # Common important terms in abstracts
        important_patterns = [
            r'\b(\w+ing\s+\w+)\b',  # gerund phrases (e.g., "machine learning")
            r'\b(\w+\s+\w+ing)\b',  # noun + gerund (e.g., "data mining")
            r'\b(\w+\s+\w+\s+\w+)\b',  # three-word phrases
            r'\b(\w+-\w+)\b',  # hyphenated terms
            r'\b([A-Z]{2,})\b',  # acronyms in original case
        ]
        
        # Extract from original abstract (preserving case for acronyms)
        for pattern in important_patterns:
            matches = re.findall(pattern, abstract)
            for match in matches:
                if len(match) > 3 and match.lower() not in self.get_stopwords():
                    keywords.add(match.lower())
        
        # 2. Extract key concepts mentioned after specific phrases
        key_phrase_patterns = [
            r'(?:we propose|we present|we introduce|this paper presents?|this work presents?)\s+(?:a\s+)?(?:new\s+)?(?:novel\s+)?(\w+(?:\s+\w+){0,2})',
            r'(?:based on|using|through|via)\s+(\w+(?:\s+\w+){0,2})',
            r'(?:approach|method|technique|algorithm|framework|system|model)\s+(?:for|of)\s+(\w+(?:\s+\w+){0,2})',
        ]
        
        for pattern in key_phrase_patterns:
            matches = re.findall(pattern, abstract_lower, re.IGNORECASE)
            for match in matches:
                cleaned = match.strip()
                if len(cleaned) > 3 and cleaned not in self.get_stopwords():
                    keywords.add(cleaned)
        
        # 3. Extract domain-specific terms
        domain_terms = self.extract_domain_terms(abstract_lower)
        keywords.update(domain_terms)
        
        # 4. Extract compound terms
        compound_pattern = r'\b(\w+[-–]\w+(?:[-–]\w+)*)\b'
        compounds = re.findall(compound_pattern, abstract)
        for compound in compounds:
            if len(compound) > 3:
                keywords.add(compound.lower())
        
        # 5. Extract capitalized terms (likely important concepts)
        cap_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        cap_terms = re.findall(cap_pattern, abstract)
        for term in cap_terms:
            if len(term) > 4 and term.lower() not in self.get_stopwords():
                keywords.add(term.lower())
        
        # Clean and filter keywords
        cleaned_keywords = []
        for kw in keywords:
            # Remove extra spaces
            kw = ' '.join(kw.split())
            # Skip if too short or too long
            if 3 <= len(kw) <= 50:
                # Skip if all stopwords
                words = kw.split()
                if not all(w in self.get_stopwords() for w in words):
                    cleaned_keywords.append(kw)
        
        # Sort and limit
        cleaned_keywords = sorted(list(set(cleaned_keywords)))
        
        # Limit to 15-20 keywords (typical for research papers)
        if len(cleaned_keywords) > 20:
            # Prioritize multi-word terms and technical terms
            multi_word = [k for k in cleaned_keywords if ' ' in k or '-' in k]
            single_word = [k for k in cleaned_keywords if ' ' not in k and '-' not in k]
            cleaned_keywords = multi_word[:15] + single_word[:5]
        
        return sorted(cleaned_keywords)
    
    def extract_domain_terms(self, text: str) -> Set[str]:
        """Extract domain-specific technical terms"""
        domain_terms = set()
        
        # Common research domains and their key terms
        ml_terms = [
            'machine learning', 'deep learning', 'neural network', 'artificial intelligence',
            'supervised learning', 'unsupervised learning', 'reinforcement learning',
            'classification', 'regression', 'clustering', 'prediction',
            'training', 'validation', 'optimization', 'algorithm'
        ]
        
        kg_terms = [
            'knowledge graph', 'ontology', 'semantic web', 'entity linking',
            'relation extraction', 'graph embedding', 'knowledge representation',
            'reasoning', 'inference', 'triple', 'rdf', 'sparql'
        ]
        
        fl_terms = [
            'federated learning', 'privacy preservation', 'differential privacy',
            'secure aggregation', 'distributed learning', 'edge computing',
            'model aggregation', 'client selection', 'communication efficiency'
        ]
        
        data_terms = [
            'data analysis', 'data mining', 'big data', 'data science',
            'data processing', 'data integration', 'data quality',
            'database', 'information retrieval', 'data visualization'
        ]
        
        all_terms = ml_terms + kg_terms + fl_terms + data_terms
        
        for term in all_terms:
            if term in text:
                domain_terms.add(term)
        
        return domain_terms
    
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
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also'
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
            keywords = self.extract_keywords_from_abstract(abstract)
            
            if not keywords:
                self.logger.debug(f"No keywords extracted from abstract in {file_path.name}")
                return False
            
            # Update or add keywords
            if 'keywords' in metadata:
                # Keep existing keywords if they're manually curated
                existing = set(metadata['keywords']) if isinstance(metadata['keywords'], list) else set()
                # Only update if current keywords look auto-generated
                if existing and not any('abstract' in str(k).lower() for k in existing):
                    self.logger.info(f"Keeping existing keywords for {file_path.name}")
                    return False
                metadata['keywords'] = keywords
                self.stats["keywords_updated"] += 1
                changes_made = True
            else:
                metadata['keywords'] = keywords
                self.stats["keywords_added"] += 1
                changes_made = True
            
            if changes_made:
                # Create backup
                backup_dir = BACKUP_DIR / "abstract_keywords" / datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_dir.mkdir(parents=True, exist_ok=True)
                backup_file = backup_dir / file_path.name
                shutil.copy2(file_path, backup_file)
                
                # Write updated content
                new_yaml = yaml.dump(metadata, default_flow_style=False, sort_keys=False, allow_unicode=True)
                new_content = f"---\n{new_yaml}---\n{markdown_content}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                self.logger.info(f"Added {len(keywords)} keywords from abstract to {file_path.name}")
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
        self.logger.info("ABSTRACT KEYWORD EXTRACTION SUMMARY")
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
    logger = setup_logging("abstract_keyword_extractor")
    logger.info("Starting keyword extraction from abstracts for all markdown files")
    
    extractor = AbstractKeywordExtractor(logger)
    extractor.process_all_files()
    extractor.print_summary()
    
    return 0 if extractor.stats["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
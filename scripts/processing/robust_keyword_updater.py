#!/Users/invoture/dev.local/hdm/.venv/bin/python
"""
Robust keyword updater that handles YAML parsing errors and focuses on fixing fragment keywords.
"""

import os
import re
import yaml
import logging
from pathlib import Path
from typing import List, Set, Dict, Optional, Tuple
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RobustKeywordUpdater:
    def __init__(self):
        # Technical patterns for different domains
        self.technical_patterns = [
            # Machine Learning / AI
            r'\b(?:machine|deep|reinforcement|federated|transfer|supervised|unsupervised|semi-supervised)\s+learning\b',
            r'\b(?:neural|convolutional|recurrent|transformer|attention)\s+(?:network|networks|model|models)\b',
            r'\b(?:large|small)\s+language\s+model(?:s)?\b',
            r'\b(?:generative|discriminative)\s+(?:model|models|ai)\b',
            
            # Knowledge Graphs
            r'\b(?:knowledge|scene|social|temporal|spatial|heterogeneous|personal)\s+(?:graph|graphs)\b',
            r'\b(?:graph|knowledge graph)\s+(?:embedding|completion|reasoning|construction)\b',
            r'\b(?:entity|relation)\s+(?:extraction|recognition|resolution|linking)\b',
            r'\b(?:link|node)\s+(?:prediction|classification)\b',
            r'\b(?:temporal|dynamic)\s+knowledge\s+graph\b',
            
            # Privacy & Security
            r'\b(?:differential|data|information)\s+privacy\b',
            r'\b(?:homomorphic|symmetric|asymmetric|single-key|multi-key)\s+encryption\b',
            r'\b(?:privacy-preserving|privacy preserving)\s+(?:learning|computation|analytics)\b',
            r'\b(?:secure|secret)\s+(?:sharing|aggregation|computation)\b',
            r'\b(?:zero-knowledge|zero knowledge)\s+(?:proof|protocol)\b',
            r'\b(?:blockchain|distributed ledger)\b',
            
            # Temporal/Time-related
            r'\b(?:temporal|spatial|spatio-temporal)\s+(?:reasoning|modeling|analysis)\b',
            r'\b(?:time|event)\s+(?:series|sequence)\s+(?:analysis|forecasting)\b',
            r'\b(?:temporal|time-aware|time aware)\s+(?:embedding|representation)\b',
            
            # Healthcare/Medical
            r'\b(?:electronic|personal)\s+(?:health|medical)\s+(?:record|records|data)\b',
            r'\b(?:clinical|medical|health)\s+(?:data|analytics|informatics)\b',
            r'\b(?:digital|human)\s+(?:twin|twins)\b',
            
            # NLP
            r'\b(?:natural|computer)\s+language\s+(?:processing|understanding|generation)\b',
            r'\b(?:question|query)\s+answering\b',
            r'\b(?:sentiment|emotion)\s+analysis\b',
            r'\b(?:named|temporal)\s+entity\s+recognition\b',
            
            # Computing
            r'\b(?:edge|cloud|fog)\s+computing\b',
            r'\b(?:internet|web)\s+of\s+things\b',
            r'\b(?:distributed|decentralized)\s+(?:system|systems|computing|learning)\b',
            
            # Data Management
            r'\b(?:data|information)\s+(?:integration|fusion|harmonization)\b',
            r'\b(?:heterogeneous|multimodal|multi-modal)\s+(?:data|fusion|learning)\b',
            
            # Recommendation Systems
            r'\b(?:recommendation|recommender)\s+system(?:s)?\b',
            r'\b(?:collaborative|content-based|hybrid)\s+filtering\b',
            
            # Other Technical Terms
            r'\b(?:semantic|knowledge)\s+(?:web|search|retrieval)\b',
            r'\b(?:anomaly|outlier|fraud)\s+detection\b',
            r'\b(?:multi-agent|single-agent)\s+(?:system|framework)\b',
        ]
        
        # Compile patterns
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.technical_patterns]
        
        # Common technical acronyms
        self.technical_acronyms = {
            'LLM', 'NLP', 'ML', 'DL', 'AI', 'GAN', 'CNN', 'RNN', 'LSTM', 'GRU', 
            'BERT', 'GPT', 'KG', 'PKG', 'HDT', 'DT', 'IoT', 'EHR', 'EMR', 'PHR',
            'API', 'REST', 'SPARQL', 'SQL', 'GNN', 'GCN', 'GAT', 'VAE', 'RL', 'DRL',
            'FL', 'HE', 'FHE', 'PHE', 'MPC', 'SMC', 'ZKP', 'DP', 'TKG', 'TKGQA',
            'KBQA', 'RAG', 'RLHF', 'CoT', 'ToT', 'PEFT', 'LoRA', 'QLoRA'
        }
        
        # Fragment patterns to avoid
        self.fragment_indicators = [
            r'^\d+\s+',  # Starts with number
            r'^(a|an|the|this|that|these|those|we|our|us)\s+',
            r'^(and|or|but|with|for|from|to|in|on|at|by)\s+',
            r'^(is|are|was|were|be|been|being|have|has|had)\s+',
            r'^(can|could|will|would|should|may|might|must)\s+',
            r'^(achieves?|proposes?|presents?|introduces?|develops?)\s+',
            r'^(based|using|through|via|between|among)\s+',
            r'\s+(the|and|or|but|with|for|from|to)$',
            r'^(significant|novel|comprehensive|extensive|efficient)\s+',
            r'^(challenging|important|crucial|essential)\s+',
            r'^(compared|evaluation|experimental|empirical)\s+',
        ]
        
        # Words to exclude from keywords
        self.exclude_words = {
            'abstract', 'introduction', 'conclusion', 'related', 'work',
            'paper', 'article', 'study', 'research', 'approach', 'method',
            'results', 'discussion', 'future', 'references', 'keywords',
            'however', 'therefore', 'moreover', 'furthermore', 'additionally',
            'python', 'java', 'javascript', 'code', 'table', 'figure',
            'page', 'pages', 'chapter', 'section', 'appendix',
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            '2020', '2021', '2022', '2023', '2024', '2025',
            'university', 'institute', 'department', 'conference', 'journal'
        }
    
    def is_fragment(self, text: str) -> bool:
        """Check if text is a sentence fragment."""
        text_lower = text.lower().strip()
        
        # Check fragment patterns
        for pattern in self.fragment_indicators:
            if re.match(pattern, text_lower):
                return True
        
        # Check if it's just numbers or very short
        if text_lower.isdigit() or len(text_lower) < 3:
            return True
        
        # Check if it's in exclude words
        if text_lower in self.exclude_words:
            return True
        
        return False
    
    def extract_abstract(self, content: str) -> Optional[str]:
        """Extract abstract section from markdown content."""
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
    
    def extract_keywords_from_text(self, text: str, title: str = "") -> List[str]:
        """Extract technical keywords from text."""
        keywords = set()
        
        # Combine title and text
        full_text = (title + " " + text).lower()
        
        # Extract using technical patterns
        for pattern in self.compiled_patterns:
            matches = pattern.findall(full_text)
            for match in matches:
                if match and not self.is_fragment(match):
                    keywords.add(match.strip())
        
        # Extract acronyms
        words = re.findall(r'\b[A-Z]{2,}\b', text)  # Use original case for acronyms
        for word in words:
            if word in self.technical_acronyms:
                keywords.add(word.lower())
        
        # Extract hyphenated technical terms
        hyphenated = re.findall(r'\b[a-z]+(?:-[a-z]+)+\b', full_text)
        for term in hyphenated:
            if len(term) > 5 and not self.is_fragment(term):
                keywords.add(term)
        
        # Clean and filter
        final_keywords = []
        for kw in keywords:
            kw = kw.strip()
            if len(kw) >= 3 and len(kw) <= 50 and not self.is_fragment(kw):
                final_keywords.append(kw)
        
        # Remove duplicates and sort
        final_keywords = sorted(list(set(final_keywords)))
        
        return final_keywords[:25]  # Limit to 25 keywords
    
    def fix_yaml_issues(self, yaml_content: str) -> str:
        """Fix common YAML parsing issues."""
        # Fix escaped quotes in authors
        yaml_content = re.sub(r'\\[,"]', '', yaml_content)
        
        # Fix quotes around values that don't need them
        lines = yaml_content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Fix cite_key quotes
            if line.strip().startswith('cite_key:'):
                match = re.match(r'(\s*cite_key:\s*)"?([^"]+)"?\s*$', line)
                if match:
                    line = f"{match.group(1)}{match.group(2)}"
            
            # Fix year quotes
            if line.strip().startswith('year:'):
                match = re.match(r'(\s*year:\s*)"?(\d+)"?\s*$', line)
                if match:
                    line = f"{match.group(1)}{match.group(2)}"
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def process_file(self, filepath: Path) -> Tuple[bool, str]:
        """Process a single markdown file. Returns (success, message)."""
        try:
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split frontmatter and body
            if not content.startswith('---'):
                return False, "No frontmatter found"
            
            parts = content.split('---', 2)
            if len(parts) < 3:
                return False, "Invalid frontmatter structure"
            
            yaml_content = parts[1]
            body = parts[2]
            
            # Fix YAML issues
            yaml_content = self.fix_yaml_issues(yaml_content)
            
            # Parse YAML
            try:
                metadata = yaml.safe_load(yaml_content)
                if not metadata:
                    metadata = {}
            except yaml.YAMLError as e:
                return False, f"YAML parsing error: {e}"
            
            # Check current keywords
            current_keywords = metadata.get('keywords', [])
            
            # Check if keywords need updating
            needs_update = False
            if not current_keywords:
                needs_update = True
            else:
                # Check if keywords are fragments
                fragment_count = sum(1 for kw in current_keywords if self.is_fragment(str(kw)))
                if fragment_count > len(current_keywords) * 0.3:  # More than 30% fragments
                    needs_update = True
            
            if not needs_update:
                return False, "Keywords already good quality"
            
            # Extract abstract
            abstract = self.extract_abstract(body)
            if not abstract:
                # Try first few paragraphs
                paragraphs = body.strip().split('\n\n')
                non_empty = [p for p in paragraphs if p.strip() and not p.strip().startswith('#')]
                if non_empty:
                    abstract = ' '.join(non_empty[:3])
                else:
                    return False, "No abstract found"
            
            # Extract keywords
            title = metadata.get('title', '')
            new_keywords = self.extract_keywords_from_text(abstract, title)
            
            if not new_keywords:
                return False, "No keywords extracted"
            
            # Update metadata
            metadata['keywords'] = new_keywords
            
            # Reconstruct file
            new_yaml = yaml.dump(metadata, default_flow_style=False, sort_keys=False, allow_unicode=True)
            new_content = f"---\n{new_yaml}---\n{body}"
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True, f"Updated with {len(new_keywords)} keywords"
            
        except Exception as e:
            return False, f"Error: {e}"
    
    def process_all_files(self):
        """Process all markdown files."""
        base_dir = Path('/Users/invoture/dev.local/hdm/markdown_papers')
        
        # Find all markdown files
        md_files = list(base_dir.rglob('*.md'))
        logger.info(f"Found {len(md_files)} markdown files")
        
        # Track statistics
        stats = {
            'processed': 0,
            'updated': 0,
            'skipped': 0,
            'errors': 0,
            'error_details': []
        }
        
        # Process files
        for i, filepath in enumerate(md_files, 1):
            logger.info(f"Processing {i}/{len(md_files)}: {filepath.name}")
            
            success, message = self.process_file(filepath)
            
            if success:
                stats['updated'] += 1
                logger.info(f"  ✓ {message}")
            else:
                if "already good quality" in message:
                    stats['skipped'] += 1
                    logger.debug(f"  - {message}")
                else:
                    stats['errors'] += 1
                    stats['error_details'].append({
                        'file': filepath.name,
                        'error': message
                    })
                    logger.error(f"  ✗ {message}")
            
            stats['processed'] += 1
            
            # Progress report every 50 files
            if i % 50 == 0:
                logger.info(f"\nProgress: {i}/{len(md_files)}")
                logger.info(f"Updated: {stats['updated']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")
        
        # Final report
        print("\n" + "="*60)
        print("KEYWORD UPDATE SUMMARY")
        print("="*60)
        print(f"Total files: {len(md_files)}")
        print(f"Processed: {stats['processed']}")
        print(f"Updated: {stats['updated']}")
        print(f"Skipped (already good): {stats['skipped']}")
        print(f"Errors: {stats['errors']}")
        print("="*60)
        
        # Save error details
        if stats['error_details']:
            error_file = Path('keyword_update_errors.json')
            with open(error_file, 'w') as f:
                json.dump(stats['error_details'], f, indent=2)
            print(f"\nError details saved to: {error_file}")

def main():
    """Main function."""
    updater = RobustKeywordUpdater()
    updater.process_all_files()

if __name__ == '__main__':
    main()
#!/Users/invoture/dev.local/hdm/.venv/bin/python
"""
Update keywords in markdown files based on abstract content.
Focus on extracting technical terms rather than sentence fragments.
"""

import os
import re
import yaml
import logging
from pathlib import Path
from typing import List, Set, Dict, Optional
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.tree import Tree

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
except:
    logger.warning("Could not download NLTK data")

class KeywordExtractor:
    def __init__(self):
        # Common technical phrases patterns
        self.technical_patterns = [
            r'\b(?:machine|deep|reinforcement|federated|transfer|supervised|unsupervised|semi-supervised)\s+learning\b',
            r'\b(?:neural|convolutional|recurrent|transformer|attention)\s+(?:network|networks|model|models)\b',
            r'\b(?:knowledge|scene|social|temporal|spatial|heterogeneous)\s+(?:graph|graphs)\b',
            r'\b(?:natural|computer)\s+language\s+(?:processing|understanding|generation)\b',
            r'\b(?:differential|data|information)\s+privacy\b',
            r'\b(?:homomorphic|symmetric|asymmetric)\s+encryption\b',
            r'\b(?:temporal|spatial|spatio-temporal)\s+(?:reasoning|modeling|analysis)\b',
            r'\b(?:multi-modal|cross-modal|uni-modal)\s+(?:fusion|learning|representation)\b',
            r'\b(?:graph|knowledge graph)\s+(?:embedding|completion|reasoning|construction)\b',
            r'\b(?:digital|human digital)\s+twin(?:s)?\b',
            r'\b(?:personal|electronic)\s+(?:health|medical)\s+(?:record|records|data)\b',
            r'\b(?:blockchain|distributed|decentralized)\s+(?:ledger|system|network)\b',
            r'\b(?:secret|secure)\s+sharing\b',
            r'\b(?:zero-knowledge|zero-trust)\s+(?:proof|protocol|architecture)\b',
            r'\b(?:edge|cloud|fog)\s+computing\b',
            r'\b(?:internet|web)\s+of\s+things\b',
            r'\b(?:artificial|general|narrow)\s+intelligence\b',
            r'\b(?:large|small)\s+language\s+model(?:s)?\b',
            r'\b(?:pre-trained|fine-tuned)\s+model(?:s)?\b',
            r'\b(?:multi-agent|single-agent)\s+(?:system|framework)\b',
            r'\b(?:semantic|knowledge)\s+(?:web|search|retrieval)\b',
            r'\b(?:data|information)\s+(?:integration|fusion|harmonization)\b',
            r'\b(?:entity|relation)\s+(?:extraction|recognition|resolution)\b',
            r'\b(?:link|node)\s+(?:prediction|classification)\b',
            r'\b(?:time|event)\s+(?:series|sequence)\s+(?:analysis|forecasting)\b',
            r'\b(?:anomaly|outlier|fraud)\s+detection\b',
            r'\b(?:recommendation|recommender)\s+system(?:s)?\b',
            r'\b(?:question|query)\s+answering\b',
            r'\b(?:information|document)\s+retrieval\b',
            r'\b(?:sentiment|emotion)\s+analysis\b',
            r'\b(?:named|temporal)\s+entity\s+recognition\b',
            r'\b(?:part-of-speech|dependency)\s+(?:tagging|parsing)\b',
            r'\b(?:word|sentence|document)\s+embedding(?:s)?\b',
            r'\b(?:attention|self-attention)\s+mechanism(?:s)?\b',
            r'\b(?:gradient|stochastic gradient)\s+descent\b',
            r'\b(?:back|forward)\s+propagation\b',
            r'\b(?:activation|loss|objective)\s+function(?:s)?\b',
            r'\b(?:hyper|meta)\s+parameter(?:s)?\b',
            r'\b(?:cross|k-fold)\s+validation\b',
            r'\b(?:precision|recall|f1)\s+(?:score|metric)\b',
            r'\b(?:accuracy|performance)\s+(?:metric|measure|evaluation)\b',
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.technical_patterns]
        
        # Common stopwords and fragments to avoid
        self.avoid_phrases = {
            'we propose', 'we present', 'we introduce', 'we develop', 'we show',
            'this paper', 'this work', 'this study', 'our approach', 'our method',
            'a novel', 'a new', 'an efficient', 'a comprehensive', 'a systematic',
            'achieves the', 'outperforms the', 'demonstrates that', 'shows that',
            'results show', 'experiments show', 'evaluation shows', 'analysis shows',
            'significant improvement', 'significant performance', 'better performance',
            'state of the art', 'state-of-the-art', 'baseline methods', 'existing methods',
            'compared with', 'compared to', 'in comparison', 'evaluation on',
            'experimental results', 'empirical results', 'comprehensive evaluation',
            'extensive experiments', 'extensive evaluation', 'extensive analysis',
            'challenging due', 'challenging task', 'difficult problem', 'complex problem',
            'essential for', 'important for', 'crucial for', 'necessary for',
            'can be used', 'can be applied', 'can be extended', 'can be adapted',
            'future work', 'future research', 'further research', 'additional research',
            'limitation of', 'limitations of', 'drawback of', 'drawbacks of',
            'advantage of', 'advantages of', 'benefit of', 'benefits of',
            'in this paper', 'in this work', 'in this study', 'in our work',
            'to the best', 'best of our', 'our knowledge', 'knowledge about',
            'for the first', 'first time', 'for the most', 'most part',
            'has been', 'have been', 'has shown', 'have shown',
            'based on', 'based upon', 'built on', 'built upon',
            'in order to', 'in order for', 'so as to', 'so that',
            'as well as', 'as well', 'as such', 'such as',
            'due to', 'because of', 'owing to', 'thanks to',
            'with respect to', 'with regard to', 'in terms of', 'in relation to',
            'it is', 'it has', 'there is', 'there are',
            'that is', 'that are', 'which is', 'which are',
            'however', 'therefore', 'moreover', 'furthermore',
            'in addition', 'additionally', 'besides', 'also',
            'first', 'second', 'third', 'finally', 'lastly',
            'for example', 'for instance', 'such as', 'like',
            'in particular', 'particularly', 'especially', 'specifically',
            'on the other hand', 'on one hand', 'in contrast', 'by contrast',
            'as a result', 'consequently', 'thus', 'hence',
            'in conclusion', 'to conclude', 'in summary', 'to summarize',
            'python', 'java', 'c++', 'javascript', 'code',
            'table', 'figure', 'equation', 'section', 'appendix',
            'et al', 'al.', 'i.e.', 'e.g.', 'cf.',
            'page', 'pages', 'chapter', 'chapters', 'volume',
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            '2020', '2021', '2022', '2023', '2024', '2025',
            'university', 'institute', 'department', 'laboratory', 'center',
            'conference', 'workshop', 'symposium', 'journal', 'proceedings',
            'abstract', 'introduction', 'methodology', 'results', 'conclusion',
            'acknowledgments', 'references', 'bibliography', 'appendix',
        }
        
        # Technical acronyms and abbreviations
        self.technical_acronyms = {
            'LLM', 'LLMs', 'NLP', 'ML', 'DL', 'AI', 'GAN', 'GANs', 'CNN', 'CNNs',
            'RNN', 'RNNs', 'LSTM', 'LSTMs', 'GRU', 'GRUs', 'BERT', 'GPT', 'GPT-2',
            'GPT-3', 'GPT-4', 'T5', 'BART', 'RoBERTa', 'XLNet', 'ALBERT', 'DeBERTa',
            'KG', 'KGs', 'PKG', 'PKGs', 'HDT', 'HDTs', 'DT', 'DTs', 'IoT', 'IoMT',
            'EHR', 'EHRs', 'EMR', 'EMRs', 'PHR', 'PHRs', 'HIE', 'FHIR', 'HL7',
            'API', 'APIs', 'REST', 'RESTful', 'GraphQL', 'SPARQL', 'SQL', 'NoSQL',
            'HTTP', 'HTTPS', 'TCP', 'UDP', 'IP', 'DNS', 'VPN', 'SSL', 'TLS',
            'CPU', 'GPU', 'TPU', 'RAM', 'ROM', 'SSD', 'HDD', 'FPGA', 'ASIC',
            'GNN', 'GNNs', 'GCN', 'GCNs', 'GAT', 'GATs', 'GraphSAGE', 'GIN',
            'VAE', 'VAEs', 'AE', 'AEs', 'DAE', 'DAEs', 'SAE', 'SAEs',
            'RL', 'DRL', 'DQN', 'A3C', 'PPO', 'TRPO', 'SAC', 'TD3', 'DDPG',
            'SVM', 'SVMs', 'RF', 'RFs', 'DT', 'DTs', 'KNN', 'K-NN', 'LDA',
            'PCA', 'ICA', 'NMF', 'SVD', 'PLS', 'CCA', 'LLE', 'MDS', 't-SNE',
            'FL', 'FedAvg', 'FedProx', 'FedMA', 'HE', 'FHE', 'PHE', 'MPC', 'SMC',
            'ZKP', 'ZKPs', 'DP', 'LDP', 'CDP', 'RDP', 'PIR', 'PSI', 'OT',
            'CKKS', 'BFV', 'BGV', 'TFHE', 'RSA', 'ECC', 'AES', 'DES', '3DES',
            'SHA', 'SHA-256', 'SHA-512', 'MD5', 'HMAC', 'PBKDF2', 'bcrypt',
            'JSON', 'XML', 'YAML', 'CSV', 'TSV', 'HDF5', 'Parquet', 'Avro',
            'BERT', 'GPT', 'T5', 'CLIP', 'DALL-E', 'Stable Diffusion', 'Midjourney',
            'RAG', 'RLHF', 'DPO', 'PPO', 'PEFT', 'LoRA', 'QLoRA', 'DoRA',
            'CoT', 'ToT', 'GoT', 'NoT', 'ReAct', 'HuggingFace', 'OpenAI',
            'MIMIC', 'MIMIC-III', 'MIMIC-IV', 'eICU', 'OMOP', 'OHDSI',
            'DICOM', 'PACS', 'RIS', 'LIS', 'CIS', 'CDSS', 'CPOE', 'MAR',
            'ICD', 'ICD-10', 'ICD-11', 'CPT', 'SNOMED', 'LOINC', 'RxNorm',
            'UMLS', 'MeSH', 'GO', 'HPO', 'DOID', 'MONDO', 'Orphanet',
            'FDA', 'EMA', 'WHO', 'CDC', 'NIH', 'NHS', 'CMS', 'ONC',
            'HIPAA', 'GDPR', 'CCPA', 'PIPEDA', 'LGPD', 'DPA', 'COPPA',
            'SOC2', 'ISO27001', 'HITRUST', 'NIST', 'PCI-DSS', 'FISMA',
            'B2B', 'B2C', 'SaaS', 'PaaS', 'IaaS', 'DaaS', 'XaaS', 'MLaaS',
            'CI/CD', 'DevOps', 'MLOps', 'DataOps', 'AIOps', 'GitOps',
            'k-means', 'DBSCAN', 'HDBSCAN', 'OPTICS', 'Mean Shift', 'GMM',
            'EM', 'MLE', 'MAP', 'MCMC', 'VI', 'ELBO', 'KL', 'JS', 'WS'
        }

    def extract_abstract(self, content: str) -> Optional[str]:
        """Extract abstract from markdown content."""
        # Look for Abstract section
        abstract_pattern = r'##?\s*Abstract\s*\n+(.*?)(?=\n#|$)'
        match = re.search(abstract_pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # If no abstract section, try to find content between frontmatter and first major heading
        frontmatter_end = content.find('---', 3)
        if frontmatter_end > 0:
            after_frontmatter = content[frontmatter_end + 3:].strip()
            # Find first major heading
            first_heading = re.search(r'\n#\s+', after_frontmatter)
            if first_heading:
                # Get content between frontmatter and first heading
                potential_abstract = after_frontmatter[:first_heading.start()].strip()
                if len(potential_abstract) > 100:  # Reasonable abstract length
                    return potential_abstract
        
        return None

    def extract_technical_terms(self, text: str) -> Set[str]:
        """Extract technical terms from text."""
        terms = set()
        
        # Convert to lowercase for pattern matching
        text_lower = text.lower()
        
        # Extract using technical patterns
        for pattern in self.compiled_patterns:
            matches = pattern.findall(text_lower)
            for match in matches:
                if match and len(match) > 2:  # Avoid very short terms
                    terms.add(match.strip())
        
        # Extract acronyms (preserve original case)
        words = text.split()
        for word in words:
            clean_word = re.sub(r'[^\w-]', '', word)
            if clean_word.upper() in self.technical_acronyms:
                terms.add(clean_word.upper())
        
        # Extract noun phrases using NLTK
        try:
            sentences = sent_tokenize(text)
            for sentence in sentences[:10]:  # Limit to first 10 sentences for efficiency
                tokens = word_tokenize(sentence)
                pos_tags = pos_tag(tokens)
                
                # Extract compound nouns
                i = 0
                while i < len(pos_tags):
                    if pos_tags[i][1].startswith('NN'):  # Noun
                        phrase = [pos_tags[i][0]]
                        j = i + 1
                        # Look for consecutive nouns or adjectives
                        while j < len(pos_tags) and (pos_tags[j][1].startswith('NN') or 
                                                     pos_tags[j][1].startswith('JJ')):
                            phrase.append(pos_tags[j][0])
                            j += 1
                        
                        if len(phrase) >= 2:
                            compound = ' '.join(phrase).lower()
                            # Check if it's a valid technical term
                            if (len(compound) > 5 and 
                                compound not in self.avoid_phrases and
                                not any(avoid in compound for avoid in self.avoid_phrases)):
                                terms.add(compound)
                        i = j
                    else:
                        i += 1
        except Exception as e:
            logger.warning(f"NLTK processing failed: {e}")
        
        # Filter out unwanted phrases
        filtered_terms = set()
        for term in terms:
            term_lower = term.lower()
            # Skip if it's a fragment or contains avoid phrases
            if (term_lower not in self.avoid_phrases and
                not any(avoid in term_lower for avoid in self.avoid_phrases) and
                len(term.split()) <= 4 and  # Avoid very long phrases
                not term_lower.startswith(('a ', 'an ', 'the ', 'to ', 'for ', 'of ', 'in ', 'on ', 'at ', 'by ', 'with '))):
                filtered_terms.add(term)
        
        return filtered_terms

    def process_file(self, filepath: Path) -> bool:
        """Process a single markdown file and update its keywords."""
        try:
            # Read the file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split frontmatter and content
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter_str = parts[1]
                    body = parts[2]
                else:
                    logger.warning(f"Invalid frontmatter in {filepath}")
                    return False
            else:
                logger.info(f"No frontmatter found in {filepath}")
                return False
            
            # Parse frontmatter
            try:
                frontmatter = yaml.safe_load(frontmatter_str)
                if not frontmatter:
                    frontmatter = {}
            except yaml.YAMLError as e:
                logger.error(f"YAML parsing error in {filepath}: {e}")
                return False
            
            # Check current keywords
            current_keywords = frontmatter.get('keywords', [])
            if isinstance(current_keywords, list) and current_keywords:
                # Check if keywords are fragments
                fragments_count = sum(1 for kw in current_keywords 
                                    if any(fragment in str(kw).lower() for fragment in [
                                        'a ', 'an ', 'the ', 'we ', 'our ', 'this ',
                                        'for ', 'to ', 'of ', 'in ', 'on ', 'at ',
                                        'significant', 'novel', 'approach', 'method',
                                        'extensive', 'comprehensive', 'efficient',
                                        'challenging', 'important', 'crucial',
                                        'achieves', 'outperforms', 'demonstrates',
                                        'compared', 'evaluation', 'experimental'
                                    ]))
                
                # If most keywords are good quality, skip
                if fragments_count < len(current_keywords) * 0.3:  # Less than 30% fragments
                    logger.info(f"Keywords already good quality in {filepath}")
                    return False
            
            # Extract abstract
            abstract = self.extract_abstract(body)
            if not abstract:
                # Try to use first few paragraphs of body
                paragraphs = body.strip().split('\n\n')
                non_empty_paragraphs = [p for p in paragraphs if p.strip() and not p.strip().startswith('#')]
                if non_empty_paragraphs:
                    abstract = ' '.join(non_empty_paragraphs[:3])
                else:
                    logger.warning(f"No abstract found in {filepath}")
                    return False
            
            # Extract technical terms
            technical_terms = self.extract_technical_terms(abstract)
            
            # Also check the title for technical terms
            title = frontmatter.get('title', '')
            if title:
                title_terms = self.extract_technical_terms(title)
                technical_terms.update(title_terms)
            
            # Sort and limit keywords
            keywords = sorted(list(technical_terms))[:30]  # Limit to 30 keywords
            
            if not keywords:
                logger.warning(f"No keywords extracted from {filepath}")
                return False
            
            # Update frontmatter
            frontmatter['keywords'] = keywords
            
            # Reconstruct the file
            new_content = '---\n' + yaml.dump(frontmatter, default_flow_style=False, sort_keys=False) + '---\n' + body
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            logger.info(f"Updated keywords in {filepath}: {len(keywords)} keywords")
            return True
            
        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}")
            return False

def main():
    """Main function to process markdown files."""
    base_dir = Path('/Users/invoture/dev.local/hdm/markdown_papers')
    
    if not base_dir.exists():
        logger.error(f"Directory not found: {base_dir}")
        return
    
    # Find all markdown files
    md_files = list(base_dir.rglob('*.md'))
    logger.info(f"Found {len(md_files)} markdown files")
    
    # Initialize extractor
    extractor = KeywordExtractor()
    
    # Process files
    updated_count = 0
    for i, filepath in enumerate(md_files, 1):
        logger.info(f"Processing {i}/{len(md_files)}: {filepath.name}")
        if extractor.process_file(filepath):
            updated_count += 1
        
        # Break after processing a batch for testing
        if updated_count >= 50:  # Process up to 50 files in this run
            logger.info("Reached batch limit of 50 files")
            break
    
    logger.info(f"Updated keywords in {updated_count} files")

if __name__ == '__main__':
    main()
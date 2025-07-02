#!/usr/bin/env python3
"""
Update cite keys to LastName_Year format and add relevant tags to markdown files
"""
import sys
import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import MARKDOWN_DIR, BACKUP_DIR, LOG_DIR
from utils import setup_logging


class CitationUpdater:
    """Updates citations and tags in markdown files"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stats = {
            "files_processed": 0,
            "cite_keys_updated": 0,
            "tags_added": 0,
            "authors_fixed": 0,
            "errors": 0,
            "skipped": 0
        }
        
        # Common tags based on keywords
        self.tag_keywords = {
            "Knowledge Graph": ["knowledge graph", "knowledge-graph", "kg", "knowledge graphs", "knowledge-based"],
            "Personal Health": ["personal health", "phr", "personal health record", "health record", "patient data"],
            "Digital Health": ["digital health", "mhealth", "mobile health", "health technology", "health app"],
            "Machine Learning": ["machine learning", "deep learning", "neural network", "lstm", "rnn", "cnn", "ai", "artificial intelligence"],
            "Privacy": ["privacy", "privacy-preserving", "differential privacy", "secure", "security", "confidential"],
            "Federated Learning": ["federated learning", "federated", "distributed learning", "decentralized"],
            "Healthcare": ["healthcare", "medical", "clinical", "hospital", "patient", "diagnosis", "treatment"],
            "Data Integration": ["data integration", "data fusion", "heterogeneous data", "data harmonization"],
            "Temporal": ["temporal", "time-aware", "time series", "temporal knowledge", "temporal data"],
            "Semantic Web": ["semantic web", "rdf", "owl", "sparql", "ontology", "linked data"],
            "Personalized Medicine": ["personalized medicine", "precision medicine", "personalized health", "precision health"],
            "Recommendation System": ["recommendation", "recommender system", "personalized recommendation"],
            "Natural Language Processing": ["nlp", "natural language", "text mining", "information extraction"],
            "Electronic Health Records": ["ehr", "electronic health record", "emr", "electronic medical record"],
            "COVID-19": ["covid", "covid-19", "coronavirus", "pandemic", "sars-cov-2"],
            "Cancer": ["cancer", "oncology", "tumor", "malignant", "carcinoma"],
            "Vaccine": ["vaccine", "vaccination", "immunization", "hpv vaccine"],
            "Mental Health": ["mental health", "depression", "anxiety", "psychiatric", "psychological"],
            "IoT": ["iot", "internet of things", "sensor", "wearable", "smart device"],
            "Blockchain": ["blockchain", "distributed ledger", "decentralized"],
            "Cloud Computing": ["cloud", "cloud computing", "cloud-based", "saas"],
            "Biomedical": ["biomedical", "bioinformatics", "genomics", "proteomics", "multi-omics"],
            "Decision Support": ["decision support", "clinical decision", "cdss", "expert system"],
            "Patient Engagement": ["patient engagement", "patient empowerment", "self-management"],
            "Telemedicine": ["telemedicine", "telehealth", "remote health", "virtual care"]
        }
    
    def extract_last_name(self, author_string: str) -> Optional[str]:
        """Extract the last name from an author string"""
        # Remove special characters and clean up
        author = re.sub(r'[✉✓×]', '', author_string).strip()
        author = re.sub(r'\s+', ' ', author)
        
        # Remove email indicators
        author = re.sub(r'\s*\([^)]*@[^)]*\)', '', author)
        
        # Remove superscript numbers and asterisks
        author = re.sub(r'[*†‡§¶#]', '', author)
        author = re.sub(r'\d+', '', author)
        
        # Split by comma if present (Last, First format)
        if ',' in author:
            parts = author.split(',')
            return parts[0].strip()
        
        # Otherwise assume last word is last name
        parts = author.strip().split()
        if parts:
            # Handle names with particles (von, van, de, etc.)
            particles = ['von', 'van', 'de', 'del', 'della', 'di', 'da', 'la', 'le']
            
            # Check if second-to-last word is a particle
            if len(parts) >= 2 and parts[-2].lower() in particles:
                return f"{parts[-2]} {parts[-1]}"
            
            return parts[-1]
        
        return None
    
    def clean_authors(self, authors_string: str) -> str:
        """Clean author string: remove HTML, fix separators, etc."""
        # Remove HTML tags
        authors_string = re.sub(r'<[^>]+>', '', authors_string)
        
        # Remove superscripts and special markers
        authors_string = re.sub(r'<sup>[^<]+</sup>', '', authors_string)
        authors_string = re.sub(r'[*†‡§¶#]\d*', '', authors_string)
        
        # Replace ampersands with commas
        authors_string = authors_string.replace(' & ', ', ').replace(' and ', ', ')
        
        # Clean up multiple spaces and commas
        authors_string = re.sub(r'\s+', ' ', authors_string)
        authors_string = re.sub(r',\s*,', ',', authors_string)
        authors_string = re.sub(r',\s*$', '', authors_string)
        
        return authors_string.strip()
    
    def generate_cite_key(self, authors: str, year: int) -> str:
        """Generate cite key in format lastname_year (all lowercase)"""
        # Get first author's last name
        first_author = authors.split(',')[0].strip()
        last_name = self.extract_last_name(first_author)
        
        if last_name:
            # Clean the last name
            last_name = re.sub(r'[^a-zA-Z\s-]', '', last_name)
            last_name = last_name.replace(' ', '')
            
            # Convert to lowercase
            return f"{last_name.lower()}_{year}"
        
        # Fallback
        return f"unknown_{year}"
    
    def extract_tags_from_content(self, content: str, title: str) -> List[str]:
        """Extract relevant tags based on content and title"""
        tags = set()
        
        # Convert to lowercase for matching
        search_text = (title + " " + content[:5000]).lower()  # Check first 5000 chars
        
        # Check each keyword category
        for tag, keywords in self.tag_keywords.items():
            for keyword in keywords:
                if keyword in search_text:
                    tags.add(tag)
                    break
        
        # Always add at least one general tag
        if not tags:
            if "health" in search_text or "medical" in search_text:
                tags.add("Healthcare")
            else:
                tags.add("Research")
        
        return sorted(list(tags))
    
    def update_markdown_file(self, file_path: Path) -> bool:
        """Update a single markdown file"""
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
            
            # Track changes
            changes_made = False
            
            # 1. Update cite_key
            old_cite_key = metadata.get('cite_key', '')
            if metadata.get('authors') and metadata.get('year'):
                # Clean authors first
                clean_authors = self.clean_authors(metadata['authors'])
                if clean_authors != metadata['authors']:
                    metadata['authors'] = clean_authors
                    self.stats["authors_fixed"] += 1
                    changes_made = True
                
                # Generate new cite key
                new_cite_key = self.generate_cite_key(clean_authors, metadata['year'])
                
                if new_cite_key != old_cite_key:
                    metadata['cite_key'] = new_cite_key
                    self.stats["cite_keys_updated"] += 1
                    changes_made = True
                    self.logger.info(f"Updated cite_key: {old_cite_key} -> {new_cite_key}")
            
            # 2. Add tags if not present
            if 'tags' not in metadata:
                title = metadata.get('title', '')
                tags = self.extract_tags_from_content(markdown_content, title)
                if tags:
                    metadata['tags'] = tags
                    self.stats["tags_added"] += 1
                    changes_made = True
                    self.logger.info(f"Added tags to {file_path.name}: {tags}")
            
            # 3. Write back if changes were made
            if changes_made:
                # Create backup
                backup_dir = BACKUP_DIR / "cite_key_updates" / datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_dir.mkdir(parents=True, exist_ok=True)
                backup_file = backup_dir / file_path.name
                shutil.copy2(file_path, backup_file)
                
                # Write updated content
                new_yaml = yaml.dump(metadata, default_flow_style=False, sort_keys=False, allow_unicode=True)
                new_content = f"---\n{new_yaml}---\n{markdown_content}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                self.stats["files_processed"] += 1
                return True
            else:
                self.logger.debug(f"No changes needed for {file_path.name}")
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
        self.logger.info("CITATION UPDATE SUMMARY")
        self.logger.info("="*50)
        self.logger.info(f"Files processed: {self.stats['files_processed']}")
        self.logger.info(f"Files skipped: {self.stats['skipped']}")
        self.logger.info(f"Cite keys updated: {self.stats['cite_keys_updated']}")
        self.logger.info(f"Tags added: {self.stats['tags_added']}")
        self.logger.info(f"Authors fixed: {self.stats['authors_fixed']}")
        self.logger.info(f"Errors: {self.stats['errors']}")
        self.logger.info("="*50)


def main():
    """Main function"""
    logger = setup_logging("cite_key_updater")
    logger.info("Starting cite key and tag update process")
    
    updater = CitationUpdater(logger)
    updater.process_all_files()
    updater.print_summary()
    
    return 0 if updater.stats["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
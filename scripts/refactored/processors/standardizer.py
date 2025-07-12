"""
Data standardization processor for ensuring consistent formats and naming.
"""

import re
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass

from ..core import BaseProcessor, ProcessingResult, ProcessingStatus
from ..core.config import Config
from ..core.exceptions import ValidationError


@dataclass
class StandardizationRule:
    """Definition of a standardization rule."""
    field_name: str
    rule_type: str  # 'format', 'value_mapping', 'validation'
    pattern: Optional[str] = None
    replacement: Optional[str] = None
    mapping: Optional[Dict[str, str]] = None
    validation_regex: Optional[str] = None
    required: bool = False


class DataStandardizerProcessor(BaseProcessor):
    """Standardizes data formats, naming conventions, and values."""
    
    def __init__(self, config: Config, rules_file: Optional[Path] = None):
        super().__init__(config, "DataStandardizer")
        self.rules = self._load_standardization_rules(rules_file)
        self.known_authors: Set[str] = set()
        self.known_venues: Set[str] = set()
        self._load_reference_data()
    
    def _load_standardization_rules(self, rules_file: Optional[Path] = None) -> List[StandardizationRule]:
        """Load standardization rules from file or use defaults."""
        if rules_file and rules_file.exists():
            try:
                with open(rules_file) as f:
                    rules_data = json.load(f)
                return [StandardizationRule(**rule) for rule in rules_data]
            except Exception as e:
                self.logger.warning(f"Failed to load rules from {rules_file}: {e}")
        
        return self._get_default_rules()
    
    def _get_default_rules(self) -> List[StandardizationRule]:
        """Get default standardization rules."""
        return [
            # Title standardization
            StandardizationRule(
                field_name="title",
                rule_type="format",
                pattern=r'^["\'\[\]]+|["\'\[\]]+$',
                replacement=""
            ),
            StandardizationRule(
                field_name="title",
                rule_type="format",
                pattern=r'\s+',
                replacement=" "
            ),
            
            # Author standardization
            StandardizationRule(
                field_name="authors",
                rule_type="format",
                pattern=r'\s*&\s*|\s+and\s+',
                replacement=", "
            ),
            StandardizationRule(
                field_name="authors",
                rule_type="format",
                pattern=r',?\s*et al\.?',
                replacement=""
            ),
            
            # Year validation
            StandardizationRule(
                field_name="year",
                rule_type="validation",
                validation_regex=r'^(19|20)\d{2}$',
                required=True
            ),
            
            # DOI standardization
            StandardizationRule(
                field_name="doi",
                rule_type="format",
                pattern=r'^(doi:)?',
                replacement=""
            ),
            
            # URL validation
            StandardizationRule(
                field_name="url",
                rule_type="validation",
                validation_regex=r'^https?://.+',
                required=False
            ),
            
            # Relevancy standardization
            StandardizationRule(
                field_name="relevancy",
                rule_type="value_mapping",
                mapping={
                    "high": "High",
                    "medium": "Medium", 
                    "low": "Low",
                    "very high": "High",
                    "very low": "Low"
                }
            )
        ]
    
    def _load_reference_data(self):
        """Load reference data for consistency checking."""
        # Load known authors and venues from existing data
        data_files = [
            self.config.paths.base_dir / "research_papers_complete.csv",
            self.config.paths.base_dir / "missing_papers.json"
        ]
        
        for data_file in data_files:
            if data_file.exists():
                try:
                    if data_file.suffix == '.csv':
                        self._load_csv_reference_data(data_file)
                    elif data_file.suffix == '.json':
                        self._load_json_reference_data(data_file)
                except Exception as e:
                    self.logger.warning(f"Failed to load reference data from {data_file}: {e}")
    
    def _load_csv_reference_data(self, csv_file: Path):
        """Load reference data from CSV file."""
        import pandas as pd
        try:
            df = pd.read_csv(csv_file)
            
            # Extract authors
            if 'authors' in df.columns:
                for authors_str in df['authors'].dropna():
                    authors = [a.strip() for a in str(authors_str).split(',')]
                    self.known_authors.update(authors)
            
            # Extract venues/journals
            for col in ['venue', 'journal', 'publisher']:
                if col in df.columns:
                    venues = df[col].dropna().unique()
                    self.known_venues.update(venues)
                    
        except Exception as e:
            self.logger.warning(f"Failed to process CSV reference data: {e}")
    
    def _load_json_reference_data(self, json_file: Path):
        """Load reference data from JSON file."""
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            for paper_data in data.values():
                if isinstance(paper_data, dict):
                    # Extract authors
                    authors_str = paper_data.get('authors', '')
                    if authors_str:
                        authors = [a.strip() for a in str(authors_str).split(',')]
                        self.known_authors.update(authors)
                        
        except Exception as e:
            self.logger.warning(f"Failed to process JSON reference data: {e}")
    
    def process_item(self, data: Dict[str, Any], **kwargs) -> ProcessingResult:
        """Standardize a data record."""
        try:
            original_data = data.copy()
            standardized_data = self._apply_standardization_rules(data)
            
            # Validate required fields
            validation_errors = self._validate_data(standardized_data)
            if validation_errors:
                return ProcessingResult(
                    status=ProcessingStatus.FAILED,
                    message=f"Validation errors: {'; '.join(validation_errors)}",
                    data={'validation_errors': validation_errors}
                )
            
            # Check for changes
            changes = self._detect_changes(original_data, standardized_data)
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message=f"Standardized data with {len(changes)} changes",
                data={
                    'standardized_data': standardized_data,
                    'changes': changes
                }
            )
            
        except Exception as e:
            self.logger.error(f"Failed to standardize data: {str(e)}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=str(e),
                error=e
            )
    
    def _apply_standardization_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply all standardization rules to data."""
        standardized = data.copy()
        
        for rule in self.rules:
            if rule.field_name in standardized:
                value = standardized[rule.field_name]
                if value is not None and str(value).strip():
                    standardized[rule.field_name] = self._apply_rule(value, rule)
        
        # Apply additional standardizations
        standardized = self._standardize_cite_key(standardized)
        standardized = self._standardize_tags(standardized)
        
        return standardized
    
    def _apply_rule(self, value: Any, rule: StandardizationRule) -> Any:
        """Apply a single standardization rule."""
        str_value = str(value)
        
        if rule.rule_type == "format":
            if rule.pattern and rule.replacement is not None:
                return re.sub(rule.pattern, rule.replacement, str_value).strip()
        
        elif rule.rule_type == "value_mapping":
            if rule.mapping and str_value.lower() in rule.mapping:
                return rule.mapping[str_value.lower()]
        
        elif rule.rule_type == "validation":
            if rule.validation_regex:
                if not re.match(rule.validation_regex, str_value):
                    self.logger.warning(f"Invalid {rule.field_name}: {str_value}")
        
        return value
    
    def _standardize_cite_key(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize cite_key generation."""
        if 'cite_key' not in data or not data['cite_key']:
            # Generate cite_key from first author and year
            authors = str(data.get('authors', '')).strip()
            year = str(data.get('year', '')).strip()
            
            if authors and year:
                first_author = authors.split(',')[0].strip()
                # Extract lastname
                name_parts = first_author.split()
                lastname = name_parts[-1] if name_parts else first_author
                
                # Clean lastname
                lastname = re.sub(r'[^\w]', '', lastname).lower()
                cite_key = f"{lastname}_{year}"
                data['cite_key'] = cite_key
        
        return data
    
    def _standardize_tags(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize tags format."""
        if 'tags' in data:
            tags = data['tags']
            if isinstance(tags, str):
                # Split string tags
                tag_list = [tag.strip() for tag in re.split(r'[,;|]', tags) if tag.strip()]
                data['tags'] = tag_list
            elif isinstance(tags, list):
                # Clean list tags
                data['tags'] = [str(tag).strip() for tag in tags if str(tag).strip()]
        
        return data
    
    def _validate_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate standardized data."""
        errors = []
        
        # Check required fields
        required_fields = ['title', 'authors', 'year']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                errors.append(f"Missing required field: {field}")
        
        # Validate year
        if 'year' in data:
            try:
                year = int(data['year'])
                if year < 1900 or year > 2030:
                    errors.append(f"Invalid year: {year}")
            except (ValueError, TypeError):
                errors.append(f"Invalid year format: {data['year']}")
        
        # Validate DOI format
        if 'doi' in data and data['doi']:
            doi = str(data['doi']).strip()
            if doi and not re.match(r'^10\.\d+/.+', doi):
                errors.append(f"Invalid DOI format: {doi}")
        
        # Validate URL format
        if 'url' in data and data['url']:
            url = str(data['url']).strip()
            if url and not re.match(r'^https?://.+', url):
                errors.append(f"Invalid URL format: {url}")
        
        return errors
    
    def _detect_changes(self, original: Dict[str, Any], standardized: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect changes made during standardization."""
        changes = []
        
        for key in set(original.keys()) | set(standardized.keys()):
            orig_val = original.get(key)
            std_val = standardized.get(key)
            
            if orig_val != std_val:
                changes.append({
                    'field': key,
                    'original': orig_val,
                    'standardized': std_val
                })
        
        return changes
    
    def standardize_csv_file(self, input_file: Path, output_file: Optional[Path] = None) -> ProcessingResult:
        """Standardize data in a CSV file."""
        try:
            import pandas as pd
            
            df = pd.read_csv(input_file)
            results = []
            
            for idx, row in df.iterrows():
                result = self.process_item(row.to_dict())
                if result.status == ProcessingStatus.COMPLETED:
                    standardized_data = result.data['standardized_data']
                    for key, value in standardized_data.items():
                        df.at[idx, key] = value
                results.append(result)
            
            # Save standardized CSV
            if output_file is None:
                output_file = input_file.parent / f"standardized_{input_file.name}"
            
            df.to_csv(output_file, index=False)
            
            successful = sum(1 for r in results if r.status == ProcessingStatus.COMPLETED)
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message=f"Standardized {successful}/{len(results)} records",
                data={
                    'output_file': str(output_file),
                    'total_records': len(results),
                    'successful': successful
                }
            )
            
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Failed to standardize CSV: {str(e)}",
                error=e
            )
    
    def generate_cite_key_mapping(self, data_list: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate unique cite_keys for a list of papers."""
        cite_key_counts: Dict[str, int] = {}
        cite_key_mapping = {}
        
        for i, data in enumerate(data_list):
            base_cite_key = self._generate_base_cite_key(data)
            
            # Handle duplicates
            if base_cite_key in cite_key_counts:
                cite_key_counts[base_cite_key] += 1
                suffix = chr(ord('a') + cite_key_counts[base_cite_key] - 1)
                unique_cite_key = f"{base_cite_key}{suffix}"
            else:
                cite_key_counts[base_cite_key] = 1
                unique_cite_key = base_cite_key
            
            cite_key_mapping[str(i)] = unique_cite_key
        
        return cite_key_mapping
    
    def _generate_base_cite_key(self, data: Dict[str, Any]) -> str:
        """Generate base cite_key from paper data."""
        authors = str(data.get('authors', '')).strip()
        year = str(data.get('year', '')).strip()
        
        if authors and year:
            first_author = authors.split(',')[0].strip()
            name_parts = first_author.split()
            lastname = name_parts[-1] if name_parts else first_author
            lastname = re.sub(r'[^\w]', '', lastname).lower()
            return f"{lastname}_{year}"
        
        # Fallback to hash-based key
        title = str(data.get('title', '')).strip()
        if title:
            title_hash = abs(hash(title)) % 10000
            return f"paper_{title_hash}"
        
        return f"unknown_{abs(hash(str(data))) % 10000}"
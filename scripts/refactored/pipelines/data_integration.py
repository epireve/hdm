"""
Data integration pipeline for merging, validating, and harmonizing data sources.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import threading

from ..core import BaseProcessor, ProcessingResult, ProcessingStatus, Config
from ..core.exceptions import ValidationError, FileProcessingError
from ..processors import DataStandardizerProcessor, DataValidatorProcessor


@dataclass
class DataSource:
    """Configuration for a data source."""
    name: str
    file_path: Path
    file_type: str  # csv, json, yaml
    key_field: str  # Field to use for matching/merging
    priority: int = 1  # Higher number = higher priority for conflicts
    transformations: Dict[str, Any] = None
    validation_rules: Dict[str, Any] = None


@dataclass
class MergeStrategy:
    """Strategy for merging data sources."""
    strategy_type: str  # exact_match, fuzzy_match, append_only
    match_threshold: float = 0.8  # For fuzzy matching
    conflict_resolution: str = "priority"  # priority, merge, manual
    duplicate_handling: str = "keep_first"  # keep_first, keep_last, merge


class DataIntegrationPipeline(BaseProcessor):
    """Pipeline for integrating multiple data sources with validation and harmonization."""
    
    def __init__(self, config: Config, sources: List[DataSource] = None):
        super().__init__(config, "DataIntegrationPipeline")
        self.sources = sources or []
        self.standardizer = DataStandardizerProcessor(config)
        self.validator = DataValidatorProcessor(config)
        self._data_cache = {}
        self._lock = threading.Lock()
        
    def add_data_source(self, source: DataSource):
        """Add a data source to the pipeline."""
        self.sources.append(source)
        self.logger.info(f"Added data source: {source.name}")
    
    def process_item(self, merge_strategy: MergeStrategy, **kwargs) -> ProcessingResult:
        """Process data integration using the specified merge strategy."""
        try:
            self.logger.info("Starting data integration pipeline")
            
            # Step 1: Load all data sources
            loaded_data = self._load_all_sources()
            if not loaded_data:
                return ProcessingResult(
                    status=ProcessingStatus.FAILED,
                    message="No data sources could be loaded"
                )
            
            # Step 2: Standardize each source
            standardized_data = self._standardize_sources(loaded_data)
            
            # Step 3: Merge data according to strategy
            merged_data = self._merge_data_sources(standardized_data, merge_strategy)
            
            # Step 4: Validate merged data
            validation_result = self._validate_merged_data(merged_data)
            
            # Step 5: Generate integration report
            report = self._generate_integration_report(
                loaded_data, standardized_data, merged_data, validation_result
            )
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message=f"Successfully integrated {len(loaded_data)} data sources",
                data={
                    'merged_data': merged_data,
                    'integration_report': report,
                    'validation_result': validation_result
                }
            )
            
        except Exception as e:
            self.logger.error(f"Data integration failed: {str(e)}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=str(e),
                error=e
            )
    
    def _load_all_sources(self) -> Dict[str, Any]:
        """Load data from all configured sources."""
        loaded_data = {}
        
        for source in self.sources:
            try:
                data = self._load_single_source(source)
                if data is not None:
                    loaded_data[source.name] = {
                        'data': data,
                        'source_config': source,
                        'record_count': len(data) if hasattr(data, '__len__') else 0
                    }
                    self.logger.info(f"Loaded {len(data)} records from {source.name}")
                else:
                    self.logger.warning(f"No data loaded from {source.name}")
                    
            except Exception as e:
                self.logger.error(f"Failed to load {source.name}: {e}")
                continue
        
        return loaded_data
    
    def _load_single_source(self, source: DataSource) -> Optional[List[Dict]]:
        """Load data from a single source."""
        if not source.file_path.exists():
            raise FileProcessingError(f"Source file not found: {source.file_path}")
        
        try:
            if source.file_type.lower() == 'csv':
                df = pd.read_csv(source.file_path)
                return df.to_dict('records')
            
            elif source.file_type.lower() == 'json':
                with open(source.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Handle different JSON structures
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    # Convert dict to list of records
                    return [{'id': k, **v} for k, v in data.items()]
                else:
                    raise ValidationError(f"Unsupported JSON structure in {source.file_path}")
            
            elif source.file_type.lower() == 'yaml':
                import yaml
                with open(source.file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return [{'id': k, **v} for k, v in data.items()]
                else:
                    raise ValidationError(f"Unsupported YAML structure in {source.file_path}")
            
            else:
                raise ValidationError(f"Unsupported file type: {source.file_type}")
                
        except Exception as e:
            raise FileProcessingError(f"Error loading {source.name}: {str(e)}")
    
    def _standardize_sources(self, loaded_data: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize data from all sources."""
        standardized_data = {}
        
        for source_name, source_info in loaded_data.items():
            self.logger.info(f"Standardizing data from {source_name}")
            
            try:
                data = source_info['data']
                standardized_records = []
                
                for record in data:
                    result = self.standardizer.process_item(record)
                    if result.status == ProcessingStatus.COMPLETED:
                        standardized_records.append(result.data['standardized_data'])
                    else:
                        self.logger.warning(f"Failed to standardize record in {source_name}: {result.message}")
                        standardized_records.append(record)  # Keep original if standardization fails
                
                standardized_data[source_name] = {
                    **source_info,
                    'data': standardized_records,
                    'standardization_success_rate': len(standardized_records) / len(data) if data else 0
                }
                
            except Exception as e:
                self.logger.error(f"Standardization failed for {source_name}: {e}")
                standardized_data[source_name] = source_info  # Keep original
        
        return standardized_data
    
    def _merge_data_sources(self, standardized_data: Dict[str, Any], merge_strategy: MergeStrategy) -> List[Dict]:
        """Merge data from multiple sources according to strategy."""
        if not standardized_data:
            return []
        
        if merge_strategy.strategy_type == "append_only":
            return self._merge_append_only(standardized_data)
        elif merge_strategy.strategy_type == "exact_match":
            return self._merge_exact_match(standardized_data, merge_strategy)
        elif merge_strategy.strategy_type == "fuzzy_match":
            return self._merge_fuzzy_match(standardized_data, merge_strategy)
        else:
            raise ValidationError(f"Unknown merge strategy: {merge_strategy.strategy_type}")
    
    def _merge_append_only(self, standardized_data: Dict[str, Any]) -> List[Dict]:
        """Simple append-only merge (no duplicate detection)."""
        merged_records = []
        
        for source_name, source_info in standardized_data.items():
            for record in source_info['data']:
                # Add source metadata
                record['_source'] = source_name
                record['_source_priority'] = source_info['source_config'].priority
                merged_records.append(record)
        
        return merged_records
    
    def _merge_exact_match(self, standardized_data: Dict[str, Any], merge_strategy: MergeStrategy) -> List[Dict]:
        """Merge with exact key matching."""
        merged_data = {}
        
        # Sort sources by priority (highest first)
        sorted_sources = sorted(
            standardized_data.items(),
            key=lambda x: x[1]['source_config'].priority,
            reverse=True
        )
        
        for source_name, source_info in sorted_sources:
            key_field = source_info['source_config'].key_field
            
            for record in source_info['data']:
                key_value = record.get(key_field)
                if not key_value:
                    continue
                
                if key_value not in merged_data:
                    # First occurrence
                    record['_source'] = source_name
                    record['_sources'] = [source_name]
                    merged_data[key_value] = record
                else:
                    # Handle duplicate
                    existing_record = merged_data[key_value]
                    merged_record = self._resolve_record_conflict(
                        existing_record, record, merge_strategy, source_name
                    )
                    merged_data[key_value] = merged_record
        
        return list(merged_data.values())
    
    def _merge_fuzzy_match(self, standardized_data: Dict[str, Any], merge_strategy: MergeStrategy) -> List[Dict]:
        """Merge with fuzzy string matching."""
        from difflib import SequenceMatcher
        
        merged_records = []
        potential_matches = {}
        
        # Sort sources by priority
        sorted_sources = sorted(
            standardized_data.items(),
            key=lambda x: x[1]['source_config'].priority,
            reverse=True
        )
        
        for source_name, source_info in sorted_sources:
            key_field = source_info['source_config'].key_field
            
            for record in source_info['data']:
                key_value = str(record.get(key_field, ''))
                if not key_value:
                    continue
                
                # Find best fuzzy match
                best_match = None
                best_score = 0
                
                for existing_key in potential_matches.keys():
                    similarity = SequenceMatcher(None, key_value.lower(), existing_key.lower()).ratio()
                    if similarity > best_score and similarity >= merge_strategy.match_threshold:
                        best_score = similarity
                        best_match = existing_key
                
                if best_match:
                    # Merge with existing record
                    existing_record = potential_matches[best_match]
                    merged_record = self._resolve_record_conflict(
                        existing_record, record, merge_strategy, source_name
                    )
                    potential_matches[best_match] = merged_record
                else:
                    # New record
                    record['_source'] = source_name
                    record['_sources'] = [source_name]
                    record['_fuzzy_key'] = key_value
                    potential_matches[key_value] = record
        
        return list(potential_matches.values())
    
    def _resolve_record_conflict(self, existing_record: Dict, new_record: Dict, 
                               merge_strategy: MergeStrategy, source_name: str) -> Dict:
        """Resolve conflicts between two records."""
        if merge_strategy.conflict_resolution == "priority":
            # Keep existing record (higher priority source was processed first)
            existing_record['_sources'].append(source_name)
            return existing_record
        
        elif merge_strategy.conflict_resolution == "merge":
            # Merge fields, preferring non-empty values
            merged_record = existing_record.copy()
            
            for key, value in new_record.items():
                if key.startswith('_'):
                    continue  # Skip metadata fields
                
                if key not in merged_record or not merged_record[key]:
                    merged_record[key] = value
                elif value and merged_record[key] != value:
                    # Different non-empty values - combine them
                    if isinstance(merged_record[key], list):
                        if value not in merged_record[key]:
                            merged_record[key].append(value)
                    else:
                        merged_record[key] = [merged_record[key], value]
            
            merged_record['_sources'].append(source_name)
            return merged_record
        
        else:  # manual
            # Flag for manual review
            existing_record['_conflict'] = True
            existing_record['_conflicting_sources'] = existing_record.get('_conflicting_sources', [])
            existing_record['_conflicting_sources'].append(source_name)
            existing_record['_sources'].append(source_name)
            return existing_record
    
    def _validate_merged_data(self, merged_data: List[Dict]) -> Dict[str, Any]:
        """Validate the merged dataset."""
        if not merged_data:
            return {'status': 'failed', 'message': 'No data to validate'}
        
        # Run validation on merged data
        validation_result = self.validator.validate_dataset(merged_data)
        
        return {
            'status': 'completed' if validation_result.status == ProcessingStatus.COMPLETED else 'failed',
            'validation_data': validation_result.data,
            'message': validation_result.message
        }
    
    def _generate_integration_report(self, loaded_data: Dict, standardized_data: Dict, 
                                   merged_data: List[Dict], validation_result: Dict) -> Dict[str, Any]:
        """Generate comprehensive integration report."""
        report = {
            'timestamp': self._get_timestamp(),
            'sources': {},
            'integration_summary': {},
            'data_quality': {},
            'recommendations': []
        }
        
        # Source summaries
        for source_name, source_info in loaded_data.items():
            report['sources'][source_name] = {
                'file_path': str(source_info['source_config'].file_path),
                'file_type': source_info['source_config'].file_type,
                'priority': source_info['source_config'].priority,
                'records_loaded': source_info['record_count'],
                'standardization_rate': standardized_data.get(source_name, {}).get('standardization_success_rate', 0)
            }
        
        # Integration summary
        total_input_records = sum(info['record_count'] for info in loaded_data.values())
        conflicts = sum(1 for record in merged_data if record.get('_conflict', False))
        
        report['integration_summary'] = {
            'total_input_records': total_input_records,
            'merged_records': len(merged_data),
            'duplicate_reduction': total_input_records - len(merged_data),
            'conflicts_detected': conflicts,
            'data_reduction_rate': (total_input_records - len(merged_data)) / total_input_records if total_input_records > 0 else 0
        }
        
        # Data quality assessment
        if validation_result.get('validation_data'):
            report['data_quality'] = {
                'average_quality_score': validation_result['validation_data'].get('average_quality', 0),
                'error_records': validation_result['validation_data'].get('error_records', 0),
                'quality_distribution': validation_result['validation_data'].get('summary', {}).get('quality_distribution', {})
            }
        
        # Generate recommendations
        report['recommendations'] = self._generate_recommendations(report)
        
        return report
    
    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on integration results."""
        recommendations = []
        
        # Check data quality
        avg_quality = report.get('data_quality', {}).get('average_quality_score', 0)
        if avg_quality < 0.7:
            recommendations.append("Data quality is below recommended threshold (70%). Consider improving data validation and standardization.")
        
        # Check conflicts
        conflicts = report.get('integration_summary', {}).get('conflicts_detected', 0)
        if conflicts > 0:
            recommendations.append(f"Found {conflicts} merge conflicts. Review conflict resolution strategy or implement manual review process.")
        
        # Check reduction rate
        reduction_rate = report.get('integration_summary', {}).get('data_reduction_rate', 0)
        if reduction_rate < 0.1:
            recommendations.append("Low duplicate detection rate. Consider using fuzzy matching or improving key field selection.")
        
        # Check source quality
        for source_name, source_info in report.get('sources', {}).items():
            std_rate = source_info.get('standardization_rate', 0)
            if std_rate < 0.8:
                recommendations.append(f"Source '{source_name}' has low standardization success rate ({std_rate:.1%}). Review data format and standardization rules.")
        
        return recommendations
    
    def export_merged_data(self, merged_data: List[Dict], output_file: Path, 
                          format: str = 'csv') -> ProcessingResult:
        """Export merged data to file."""
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            if format.lower() == 'csv':
                df = pd.DataFrame(merged_data)
                df.to_csv(output_file, index=False)
            elif format.lower() == 'json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(merged_data, f, indent=2, ensure_ascii=False, default=str)
            else:
                raise ValidationError(f"Unsupported export format: {format}")
            
            self.logger.info(f"Exported {len(merged_data)} records to {output_file}")
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message=f"Exported {len(merged_data)} records to {output_file}",
                data={'output_file': str(output_file), 'record_count': len(merged_data)}
            )
            
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Export failed: {str(e)}",
                error=e
            )
    
    def create_data_lineage(self, merged_data: List[Dict]) -> Dict[str, Any]:
        """Create data lineage information for traceability."""
        lineage = {
            'creation_timestamp': self._get_timestamp(),
            'source_files': [],
            'transformation_steps': [],
            'record_lineage': {}
        }
        
        # Track source files
        for source in self.sources:
            lineage['source_files'].append({
                'name': source.name,
                'file_path': str(source.file_path),
                'file_type': source.file_type,
                'priority': source.priority
            })
        
        # Track transformation steps
        lineage['transformation_steps'] = [
            'Data loading and parsing',
            'Data standardization',
            'Data merging and deduplication',
            'Data validation',
            'Quality assessment'
        ]
        
        # Track record-level lineage
        for record in merged_data:
            record_id = record.get('cite_key') or record.get('id', 'unknown')
            lineage['record_lineage'][record_id] = {
                'sources': record.get('_sources', []),
                'primary_source': record.get('_source', 'unknown'),
                'has_conflicts': record.get('_conflict', False)
            }
        
        return lineage
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().isoformat()


# Factory functions for common integration scenarios

def create_hdm_paper_integration_pipeline(config: Config) -> DataIntegrationPipeline:
    """Create a pipeline specifically for HDM paper data integration."""
    pipeline = DataIntegrationPipeline(config)
    
    # Add common HDM data sources
    base_dir = config.paths.base_dir
    
    # Main research CSV
    if (base_dir / "research_papers_complete.csv").exists():
        pipeline.add_data_source(DataSource(
            name="research_papers_complete",
            file_path=base_dir / "research_papers_complete.csv",
            file_type="csv",
            key_field="cite_key",
            priority=10
        ))
    
    # Missing papers JSON
    if (base_dir / "missing_papers.json").exists():
        pipeline.add_data_source(DataSource(
            name="missing_papers",
            file_path=base_dir / "missing_papers.json",
            file_type="json",
            key_field="cite_key",
            priority=5
        ))
    
    # Legacy CSV files
    for csv_file in base_dir.glob("research_papers*.csv"):
        if csv_file.name != "research_papers_complete.csv":
            pipeline.add_data_source(DataSource(
                name=csv_file.stem,
                file_path=csv_file,
                file_type="csv",
                key_field="cite_key",
                priority=1
            ))
    
    return pipeline


def create_metadata_integration_pipeline(config: Config, markdown_dir: Path) -> DataIntegrationPipeline:
    """Create a pipeline for integrating markdown metadata."""
    pipeline = DataIntegrationPipeline(config)
    
    # Find all paper directories with metadata
    for paper_dir in markdown_dir.iterdir():
        if paper_dir.is_dir():
            yaml_file = paper_dir / "paper.md"
            if yaml_file.exists():
                pipeline.add_data_source(DataSource(
                    name=f"paper_{paper_dir.name}",
                    file_path=yaml_file,
                    file_type="yaml",  # YAML frontmatter
                    key_field="cite_key",
                    priority=3
                ))
    
    return pipeline
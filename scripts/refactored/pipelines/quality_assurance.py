"""
Quality assurance pipeline for automated data validation, monitoring, and reporting.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading
from concurrent.futures import ThreadPoolExecutor

from ..core import BaseProcessor, ProcessingResult, ProcessingStatus, Config
from ..core.exceptions import ValidationError, FileProcessingError
from ..processors import DataValidatorProcessor


@dataclass
class QualityCheck:
    """Definition of a quality check."""
    name: str
    description: str
    check_type: str  # data_quality, schema_validation, business_rule, statistical
    check_function: str  # Function name to execute
    parameters: Dict[str, Any] = field(default_factory=dict)
    severity: str = "error"  # error, warning, info
    enabled: bool = True
    schedule: Optional[str] = None  # cron-like schedule for automated checks


@dataclass
class QualityThreshold:
    """Quality threshold definition."""
    metric_name: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    target_value: Optional[float] = None
    tolerance: float = 0.05


@dataclass
class QualityAlert:
    """Quality alert definition."""
    timestamp: datetime
    severity: str
    check_name: str
    message: str
    affected_records: List[str] = field(default_factory=list)
    recommended_action: Optional[str] = None


class QualityAssurancePipeline(BaseProcessor):
    """Comprehensive quality assurance pipeline for HDM data."""
    
    def __init__(self, config: Config, quality_checks: List[QualityCheck] = None,
                 thresholds: List[QualityThreshold] = None):
        super().__init__(config, "QualityAssurancePipeline")
        self.quality_checks = quality_checks or self._get_default_quality_checks()
        self.thresholds = thresholds or self._get_default_thresholds()
        self.validator = DataValidatorProcessor(config)
        self.alerts = []
        self._lock = threading.Lock()
        
    def process_item(self, data_source: Path, **kwargs) -> ProcessingResult:
        """Run quality assurance checks on a data source."""
        try:
            self.logger.info(f"Starting quality assurance for {data_source}")
            
            # Load data
            data = self._load_data_source(data_source)
            if not data:
                return ProcessingResult(
                    status=ProcessingStatus.FAILED,
                    message="No data could be loaded for quality assessment"
                )
            
            # Run all enabled quality checks
            check_results = self._run_quality_checks(data)
            
            # Evaluate against thresholds
            threshold_results = self._evaluate_thresholds(check_results)
            
            # Generate alerts
            alerts = self._generate_alerts(check_results, threshold_results)
            
            # Create quality report
            quality_report = self._create_quality_report(data, check_results, threshold_results, alerts)
            
            # Determine overall status
            overall_status = self._determine_overall_status(check_results, alerts)
            
            return ProcessingResult(
                status=overall_status,
                message=f"Quality assurance completed with {len(alerts)} alerts",
                data={
                    'quality_report': quality_report,
                    'check_results': check_results,
                    'alerts': [alert.__dict__ for alert in alerts],
                    'data_summary': self._create_data_summary(data)
                }
            )
            
        except Exception as e:
            self.logger.error(f"Quality assurance failed: {str(e)}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=str(e),
                error=e
            )
    
    def _load_data_source(self, data_source: Path) -> Optional[List[Dict]]:
        """Load data from various source formats."""
        if not data_source.exists():
            raise FileProcessingError(f"Data source not found: {data_source}")
        
        try:
            if data_source.suffix.lower() == '.csv':
                df = pd.read_csv(data_source)
                return df.to_dict('records')
            elif data_source.suffix.lower() == '.json':
                with open(data_source, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return [{'id': k, **v} for k, v in data.items()]
            else:
                raise ValidationError(f"Unsupported file format: {data_source.suffix}")
                
        except Exception as e:
            raise FileProcessingError(f"Failed to load {data_source}: {str(e)}")
    
    def _get_default_quality_checks(self) -> List[QualityCheck]:
        """Get default quality checks for HDM data."""
        return [
            # Data completeness checks
            QualityCheck(
                name="required_fields_present",
                description="Check that all required fields are present",
                check_type="data_quality",
                check_function="check_required_fields",
                parameters={"required_fields": ["title", "authors", "year"]},
                severity="error"
            ),
            QualityCheck(
                name="completeness_rate",
                description="Calculate overall data completeness rate",
                check_type="statistical",
                check_function="calculate_completeness_rate",
                severity="warning"
            ),
            
            # Data validity checks
            QualityCheck(
                name="year_validity",
                description="Check that years are within valid range",
                check_type="data_quality",
                check_function="check_year_validity",
                parameters={"min_year": 1900, "max_year": datetime.now().year + 1},
                severity="error"
            ),
            QualityCheck(
                name="doi_format",
                description="Validate DOI format",
                check_type="data_quality",
                check_function="check_doi_format",
                severity="warning"
            ),
            QualityCheck(
                name="url_accessibility",
                description="Check URL accessibility",
                check_type="data_quality",
                check_function="check_url_accessibility",
                severity="info",
                enabled=False  # Disabled by default (slow)
            ),
            
            # Business rule checks
            QualityCheck(
                name="duplicate_detection",
                description="Detect potential duplicate records",
                check_type="business_rule",
                check_function="detect_duplicates",
                parameters={"similarity_threshold": 0.85},
                severity="warning"
            ),
            QualityCheck(
                name="cite_key_uniqueness",
                description="Ensure cite keys are unique",
                check_type="business_rule",
                check_function="check_cite_key_uniqueness",
                severity="error"
            ),
            QualityCheck(
                name="relevancy_consistency",
                description="Check relevancy field consistency",
                check_type="business_rule",
                check_function="check_relevancy_consistency",
                severity="warning"
            ),
            
            # Schema validation checks
            QualityCheck(
                name="schema_compliance",
                description="Validate against expected schema",
                check_type="schema_validation",
                check_function="validate_schema_compliance",
                severity="error"
            ),
            QualityCheck(
                name="data_types",
                description="Check data type consistency",
                check_type="schema_validation",
                check_function="check_data_types",
                severity="warning"
            ),
            
            # Statistical checks
            QualityCheck(
                name="outlier_detection",
                description="Detect statistical outliers",
                check_type="statistical",
                check_function="detect_outliers",
                parameters={"z_threshold": 3.0},
                severity="info"
            ),
            QualityCheck(
                name="distribution_analysis",
                description="Analyze data distribution patterns",
                check_type="statistical",
                check_function="analyze_distributions",
                severity="info"
            )
        ]
    
    def _get_default_thresholds(self) -> List[QualityThreshold]:
        """Get default quality thresholds."""
        return [
            QualityThreshold("completeness_rate", min_value=0.8),
            QualityThreshold("duplicate_rate", max_value=0.05),
            QualityThreshold("error_rate", max_value=0.02),
            QualityThreshold("schema_compliance_rate", min_value=0.95),
            QualityThreshold("data_freshness_days", max_value=30)
        ]
    
    def _run_quality_checks(self, data: List[Dict]) -> Dict[str, Any]:
        """Execute all enabled quality checks."""
        check_results = {}
        
        for check in self.quality_checks:
            if not check.enabled:
                continue
                
            try:
                self.logger.info(f"Running quality check: {check.name}")
                result = self._execute_quality_check(check, data)
                check_results[check.name] = {
                    'check_definition': check,
                    'result': result,
                    'status': 'passed' if result.get('passed', True) else 'failed',
                    'execution_time': result.get('execution_time', 0)
                }
                
            except Exception as e:
                self.logger.error(f"Quality check {check.name} failed: {e}")
                check_results[check.name] = {
                    'check_definition': check,
                    'result': {'error': str(e)},
                    'status': 'error',
                    'execution_time': 0
                }
        
        return check_results
    
    def _execute_quality_check(self, check: QualityCheck, data: List[Dict]) -> Dict[str, Any]:
        """Execute a single quality check."""
        import time
        start_time = time.time()
        
        try:
            # Get the check function
            check_function = getattr(self, check.check_function)
            
            # Execute the check
            result = check_function(data, **check.parameters)
            
            # Add execution metadata
            result['execution_time'] = time.time() - start_time
            result['timestamp'] = datetime.now().isoformat()
            
            return result
            
        except AttributeError:
            raise ValidationError(f"Unknown check function: {check.check_function}")
    
    # Quality check implementations
    
    def check_required_fields(self, data: List[Dict], required_fields: List[str]) -> Dict[str, Any]:
        """Check that required fields are present and non-empty."""
        missing_counts = {field: 0 for field in required_fields}
        total_records = len(data)
        
        for record in data:
            for field in required_fields:
                if field not in record or not str(record[field]).strip():
                    missing_counts[field] += 1
        
        missing_rates = {field: count / total_records for field, count in missing_counts.items()}
        overall_rate = sum(missing_rates.values()) / len(required_fields)
        
        return {
            'passed': all(rate < 0.1 for rate in missing_rates.values()),  # Allow 10% missing
            'missing_counts': missing_counts,
            'missing_rates': missing_rates,
            'overall_missing_rate': overall_rate,
            'total_records': total_records
        }
    
    def calculate_completeness_rate(self, data: List[Dict]) -> Dict[str, Any]:
        """Calculate overall data completeness rate."""
        if not data:
            return {'passed': False, 'completeness_rate': 0}
        
        total_fields = 0
        filled_fields = 0
        
        for record in data:
            for value in record.values():
                total_fields += 1
                if value and str(value).strip():
                    filled_fields += 1
        
        completeness_rate = filled_fields / total_fields if total_fields > 0 else 0
        
        return {
            'passed': completeness_rate >= 0.7,  # 70% minimum
            'completeness_rate': completeness_rate,
            'total_fields': total_fields,
            'filled_fields': filled_fields
        }
    
    def check_year_validity(self, data: List[Dict], min_year: int = 1900, 
                          max_year: int = None) -> Dict[str, Any]:
        """Check that years are within valid range."""
        if max_year is None:
            max_year = datetime.now().year + 1
        
        invalid_years = []
        valid_count = 0
        
        for i, record in enumerate(data):
            year = record.get('year')
            if year:
                try:
                    year_int = int(year)
                    if min_year <= year_int <= max_year:
                        valid_count += 1
                    else:
                        invalid_years.append({'index': i, 'year': year_int})
                except (ValueError, TypeError):
                    invalid_years.append({'index': i, 'year': year, 'error': 'not_numeric'})
        
        total_with_years = len([r for r in data if r.get('year')])
        validity_rate = valid_count / total_with_years if total_with_years > 0 else 0
        
        return {
            'passed': len(invalid_years) == 0,
            'validity_rate': validity_rate,
            'invalid_years': invalid_years,
            'valid_count': valid_count,
            'total_with_years': total_with_years
        }
    
    def check_doi_format(self, data: List[Dict]) -> Dict[str, Any]:
        """Validate DOI format."""
        import re
        doi_pattern = re.compile(r'^10\.\d+/.+')
        
        invalid_dois = []
        valid_count = 0
        
        for i, record in enumerate(data):
            doi = record.get('doi', '').strip()
            if doi:
                if doi_pattern.match(doi):
                    valid_count += 1
                else:
                    invalid_dois.append({'index': i, 'doi': doi})
        
        total_with_dois = len([r for r in data if r.get('doi', '').strip()])
        validity_rate = valid_count / total_with_dois if total_with_dois > 0 else 1.0
        
        return {
            'passed': validity_rate >= 0.9,  # 90% of DOIs should be valid
            'validity_rate': validity_rate,
            'invalid_dois': invalid_dois,
            'valid_count': valid_count,
            'total_with_dois': total_with_dois
        }
    
    def check_url_accessibility(self, data: List[Dict]) -> Dict[str, Any]:
        """Check URL accessibility (disabled by default as it's slow)."""
        import requests
        from urllib.parse import urlparse
        
        accessible_count = 0
        inaccessible_urls = []
        
        for i, record in enumerate(data):
            url = record.get('url', '').strip()
            if url and urlparse(url).scheme:
                try:
                    response = requests.head(url, timeout=5, allow_redirects=True)
                    if response.status_code < 400:
                        accessible_count += 1
                    else:
                        inaccessible_urls.append({'index': i, 'url': url, 'status_code': response.status_code})
                except Exception as e:
                    inaccessible_urls.append({'index': i, 'url': url, 'error': str(e)})
        
        total_with_urls = len([r for r in data if r.get('url', '').strip()])
        accessibility_rate = accessible_count / total_with_urls if total_with_urls > 0 else 1.0
        
        return {
            'passed': accessibility_rate >= 0.8,  # 80% should be accessible
            'accessibility_rate': accessibility_rate,
            'accessible_count': accessible_count,
            'inaccessible_urls': inaccessible_urls,
            'total_with_urls': total_with_urls
        }
    
    def detect_duplicates(self, data: List[Dict], similarity_threshold: float = 0.85) -> Dict[str, Any]:
        """Detect potential duplicate records."""
        from difflib import SequenceMatcher
        
        duplicates = []
        checked_pairs = set()
        
        for i, record1 in enumerate(data):
            title1 = str(record1.get('title', '')).lower().strip()
            if not title1:
                continue
                
            for j, record2 in enumerate(data[i+1:], i+1):
                if (i, j) in checked_pairs:
                    continue
                    
                title2 = str(record2.get('title', '')).lower().strip()
                if not title2:
                    continue
                
                similarity = SequenceMatcher(None, title1, title2).ratio()
                if similarity >= similarity_threshold:
                    duplicates.append({
                        'record1_index': i,
                        'record2_index': j,
                        'similarity': similarity,
                        'title1': record1.get('title', ''),
                        'title2': record2.get('title', ''),
                        'cite_key1': record1.get('cite_key', ''),
                        'cite_key2': record2.get('cite_key', '')
                    })
                
                checked_pairs.add((i, j))
        
        duplicate_rate = len(duplicates) / len(data) if data else 0
        
        return {
            'passed': duplicate_rate <= 0.05,  # Allow 5% duplicates
            'duplicate_rate': duplicate_rate,
            'duplicates': duplicates,
            'duplicate_count': len(duplicates),
            'total_records': len(data)
        }
    
    def check_cite_key_uniqueness(self, data: List[Dict]) -> Dict[str, Any]:
        """Check that cite keys are unique."""
        cite_keys = {}
        duplicates = []
        
        for i, record in enumerate(data):
            cite_key = record.get('cite_key', '').strip()
            if cite_key:
                if cite_key in cite_keys:
                    duplicates.append({
                        'cite_key': cite_key,
                        'indices': [cite_keys[cite_key], i]
                    })
                else:
                    cite_keys[cite_key] = i
        
        return {
            'passed': len(duplicates) == 0,
            'unique_rate': (len(cite_keys) - len(duplicates)) / len(cite_keys) if cite_keys else 1.0,
            'duplicates': duplicates,
            'total_cite_keys': len(cite_keys),
            'duplicate_count': len(duplicates)
        }
    
    def check_relevancy_consistency(self, data: List[Dict]) -> Dict[str, Any]:
        """Check relevancy field consistency."""
        valid_values = {'High', 'Medium', 'Low'}
        invalid_relevancy = []
        valid_count = 0
        
        for i, record in enumerate(data):
            relevancy = record.get('relevancy', '').strip()
            if relevancy:
                if relevancy in valid_values:
                    valid_count += 1
                else:
                    invalid_relevancy.append({'index': i, 'relevancy': relevancy})
        
        total_with_relevancy = len([r for r in data if r.get('relevancy', '').strip()])
        consistency_rate = valid_count / total_with_relevancy if total_with_relevancy > 0 else 1.0
        
        return {
            'passed': consistency_rate >= 0.95,
            'consistency_rate': consistency_rate,
            'invalid_relevancy': invalid_relevancy,
            'valid_count': valid_count,
            'total_with_relevancy': total_with_relevancy
        }
    
    def validate_schema_compliance(self, data: List[Dict]) -> Dict[str, Any]:
        """Validate records against expected schema."""
        expected_fields = {
            'cite_key': str,
            'title': str,
            'authors': str,
            'year': int,
            'relevancy': str
        }
        
        non_compliant = []
        compliant_count = 0
        
        for i, record in enumerate(data):
            violations = []
            
            for field, expected_type in expected_fields.items():
                if field in record:
                    try:
                        if expected_type == int:
                            int(record[field])
                        elif expected_type == str:
                            str(record[field])
                    except (ValueError, TypeError):
                        violations.append(f"{field}: expected {expected_type.__name__}")
                else:
                    violations.append(f"{field}: missing")
            
            if violations:
                non_compliant.append({'index': i, 'violations': violations})
            else:
                compliant_count += 1
        
        compliance_rate = compliant_count / len(data) if data else 1.0
        
        return {
            'passed': compliance_rate >= 0.95,
            'compliance_rate': compliance_rate,
            'non_compliant': non_compliant,
            'compliant_count': compliant_count,
            'total_records': len(data)
        }
    
    def check_data_types(self, data: List[Dict]) -> Dict[str, Any]:
        """Check data type consistency across records."""
        field_types = {}
        type_inconsistencies = []
        
        # Analyze field types
        for record in data:
            for field, value in record.items():
                if field not in field_types:
                    field_types[field] = {}
                
                value_type = type(value).__name__
                field_types[field][value_type] = field_types[field].get(value_type, 0) + 1
        
        # Identify inconsistencies
        for field, type_counts in field_types.items():
            if len(type_counts) > 1:
                # Multiple types found
                total_count = sum(type_counts.values())
                dominant_type = max(type_counts, key=type_counts.get)
                dominant_percentage = type_counts[dominant_type] / total_count
                
                if dominant_percentage < 0.9:  # Less than 90% consistency
                    type_inconsistencies.append({
                        'field': field,
                        'type_distribution': type_counts,
                        'dominant_type': dominant_type,
                        'consistency_rate': dominant_percentage
                    })
        
        return {
            'passed': len(type_inconsistencies) == 0,
            'field_types': field_types,
            'type_inconsistencies': type_inconsistencies,
            'consistency_issues': len(type_inconsistencies)
        }
    
    def detect_outliers(self, data: List[Dict], z_threshold: float = 3.0) -> Dict[str, Any]:
        """Detect statistical outliers in numeric fields."""
        import numpy as np
        
        numeric_fields = ['year']
        outliers = {}
        
        for field in numeric_fields:
            values = []
            indices = []
            
            for i, record in enumerate(data):
                if field in record:
                    try:
                        value = float(record[field])
                        values.append(value)
                        indices.append(i)
                    except (ValueError, TypeError):
                        continue
            
            if len(values) > 10:  # Need sufficient data
                values_array = np.array(values)
                mean = np.mean(values_array)
                std = np.std(values_array)
                
                if std > 0:
                    z_scores = np.abs((values_array - mean) / std)
                    outlier_indices = np.where(z_scores > z_threshold)[0]
                    
                    outliers[field] = []
                    for idx in outlier_indices:
                        outliers[field].append({
                            'record_index': indices[idx],
                            'value': values[idx],
                            'z_score': z_scores[idx]
                        })
        
        total_outliers = sum(len(field_outliers) for field_outliers in outliers.values())
        
        return {
            'passed': total_outliers == 0,
            'outliers': outliers,
            'total_outliers': total_outliers,
            'z_threshold': z_threshold
        }
    
    def analyze_distributions(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze data distribution patterns."""
        distributions = {}
        
        # Analyze categorical fields
        categorical_fields = ['relevancy', 'year']
        
        for field in categorical_fields:
            values = [record.get(field) for record in data if record.get(field)]
            if values:
                value_counts = {}
                for value in values:
                    value_counts[str(value)] = value_counts.get(str(value), 0) + 1
                
                # Calculate entropy for diversity
                total = len(values)
                entropy = 0
                for count in value_counts.values():
                    p = count / total
                    if p > 0:
                        import math
                        entropy -= p * math.log2(p)
                
                distributions[field] = {
                    'value_counts': value_counts,
                    'total_values': total,
                    'unique_values': len(value_counts),
                    'entropy': entropy,
                    'most_common': max(value_counts, key=value_counts.get)
                }
        
        return {
            'passed': True,  # Informational only
            'distributions': distributions
        }
    
    def _evaluate_thresholds(self, check_results: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate check results against defined thresholds."""
        threshold_results = {}
        
        for threshold in self.thresholds:
            metric_value = self._extract_metric_value(check_results, threshold.metric_name)
            
            if metric_value is not None:
                passed = True
                violations = []
                
                if threshold.min_value is not None and metric_value < threshold.min_value:
                    passed = False
                    violations.append(f"Below minimum: {metric_value} < {threshold.min_value}")
                
                if threshold.max_value is not None and metric_value > threshold.max_value:
                    passed = False
                    violations.append(f"Above maximum: {metric_value} > {threshold.max_value}")
                
                threshold_results[threshold.metric_name] = {
                    'threshold_definition': threshold,
                    'metric_value': metric_value,
                    'passed': passed,
                    'violations': violations
                }
        
        return threshold_results
    
    def _extract_metric_value(self, check_results: Dict[str, Any], metric_name: str) -> Optional[float]:
        """Extract metric value from check results."""
        # Map metric names to check results
        metric_mappings = {
            'completeness_rate': ('completeness_rate', 'completeness_rate'),
            'duplicate_rate': ('duplicate_detection', 'duplicate_rate'),
            'error_rate': ('required_fields_present', 'overall_missing_rate'),
            'schema_compliance_rate': ('schema_compliance', 'compliance_rate')
        }
        
        if metric_name in metric_mappings:
            check_name, result_key = metric_mappings[metric_name]
            if check_name in check_results:
                return check_results[check_name]['result'].get(result_key)
        
        return None
    
    def _generate_alerts(self, check_results: Dict[str, Any], threshold_results: Dict[str, Any]) -> List[QualityAlert]:
        """Generate alerts based on check and threshold results."""
        alerts = []
        
        # Alerts from failed checks
        for check_name, check_result in check_results.items():
            if check_result['status'] == 'failed':
                check_def = check_result['check_definition']
                alerts.append(QualityAlert(
                    timestamp=datetime.now(),
                    severity=check_def.severity,
                    check_name=check_name,
                    message=f"Quality check failed: {check_def.description}",
                    recommended_action=self._get_recommended_action(check_name, check_result)
                ))
        
        # Alerts from threshold violations
        for metric_name, threshold_result in threshold_results.items():
            if not threshold_result['passed']:
                alerts.append(QualityAlert(
                    timestamp=datetime.now(),
                    severity="warning",
                    check_name=f"threshold_{metric_name}",
                    message=f"Threshold violation for {metric_name}: {'; '.join(threshold_result['violations'])}",
                    recommended_action=f"Review and improve {metric_name}"
                ))
        
        return alerts
    
    def _get_recommended_action(self, check_name: str, check_result: Dict[str, Any]) -> str:
        """Get recommended action for a failed check."""
        recommendations = {
            'required_fields_present': "Fill in missing required fields",
            'year_validity': "Correct invalid year values",
            'doi_format': "Fix DOI format according to standard",
            'duplicate_detection': "Review and merge duplicate records",
            'cite_key_uniqueness': "Generate unique cite keys for duplicates",
            'schema_compliance': "Update records to match expected schema"
        }
        
        return recommendations.get(check_name, "Review and correct identified issues")
    
    def _determine_overall_status(self, check_results: Dict[str, Any], alerts: List[QualityAlert]) -> ProcessingStatus:
        """Determine overall QA status."""
        error_alerts = [a for a in alerts if a.severity == 'error']
        failed_checks = [r for r in check_results.values() if r['status'] == 'failed']
        
        if error_alerts or failed_checks:
            return ProcessingStatus.FAILED
        else:
            return ProcessingStatus.COMPLETED
    
    def _create_data_summary(self, data: List[Dict]) -> Dict[str, Any]:
        """Create summary statistics about the data."""
        if not data:
            return {'total_records': 0}
        
        # Basic statistics
        total_records = len(data)
        
        # Field coverage
        all_fields = set()
        for record in data:
            all_fields.update(record.keys())
        
        field_coverage = {}
        for field in all_fields:
            non_empty = sum(1 for record in data if record.get(field) and str(record[field]).strip())
            field_coverage[field] = non_empty / total_records
        
        return {
            'total_records': total_records,
            'total_fields': len(all_fields),
            'field_coverage': field_coverage,
            'avg_field_coverage': sum(field_coverage.values()) / len(field_coverage) if field_coverage else 0
        }
    
    def _create_quality_report(self, data: List[Dict], check_results: Dict[str, Any],
                             threshold_results: Dict[str, Any], alerts: List[QualityAlert]) -> Dict[str, Any]:
        """Create comprehensive quality report."""
        return {
            'timestamp': datetime.now().isoformat(),
            'data_summary': self._create_data_summary(data),
            'quality_score': self._calculate_quality_score(check_results, threshold_results),
            'check_summary': {
                'total_checks': len(check_results),
                'passed_checks': len([r for r in check_results.values() if r['status'] == 'passed']),
                'failed_checks': len([r for r in check_results.values() if r['status'] == 'failed']),
                'error_checks': len([r for r in check_results.values() if r['status'] == 'error'])
            },
            'threshold_summary': {
                'total_thresholds': len(threshold_results),
                'passed_thresholds': len([r for r in threshold_results.values() if r['passed']]),
                'violated_thresholds': len([r for r in threshold_results.values() if not r['passed']])
            },
            'alert_summary': {
                'total_alerts': len(alerts),
                'error_alerts': len([a for a in alerts if a.severity == 'error']),
                'warning_alerts': len([a for a in alerts if a.severity == 'warning']),
                'info_alerts': len([a for a in alerts if a.severity == 'info'])
            }
        }
    
    def _calculate_quality_score(self, check_results: Dict[str, Any], threshold_results: Dict[str, Any]) -> float:
        """Calculate overall quality score (0-1)."""
        if not check_results and not threshold_results:
            return 0.0
        
        # Weight check results
        check_score = 0.0
        if check_results:
            passed_checks = len([r for r in check_results.values() if r['status'] == 'passed'])
            check_score = passed_checks / len(check_results)
        
        # Weight threshold results
        threshold_score = 0.0
        if threshold_results:
            passed_thresholds = len([r for r in threshold_results.values() if r['passed']])
            threshold_score = passed_thresholds / len(threshold_results)
        
        # Combine scores (60% checks, 40% thresholds)
        if check_results and threshold_results:
            return 0.6 * check_score + 0.4 * threshold_score
        elif check_results:
            return check_score
        elif threshold_results:
            return threshold_score
        else:
            return 0.0
    
    def export_quality_report(self, quality_report: Dict[str, Any], output_file: Path):
        """Export quality report to file."""
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(quality_report, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"Quality report exported to {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to export quality report: {e}")
    
    def schedule_quality_checks(self, data_sources: List[Path], schedule: str = "daily"):
        """Schedule automated quality checks (placeholder for future implementation)."""
        # This would integrate with a scheduler like Celery or APScheduler
        self.logger.info(f"Quality checks scheduled for {len(data_sources)} sources with {schedule} frequency")
        # Implementation would depend on deployment environment
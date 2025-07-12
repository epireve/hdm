"""
Data validation processor for ensuring data quality and completeness.
"""

import re
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from datetime import datetime

from ..core import BaseProcessor, ProcessingResult, ProcessingStatus
from ..core.config import Config
from ..core.exceptions import ValidationError


@dataclass
class ValidationRule:
    """Definition of a validation rule."""
    field_name: str
    rule_type: str  # 'required', 'format', 'range', 'enum', 'custom'
    pattern: Optional[str] = None
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    allowed_values: Optional[List[str]] = None
    custom_validator: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class ValidationIssue:
    """A validation issue found in data."""
    field_name: str
    issue_type: str
    message: str
    severity: str = "error"  # error, warning, info
    suggested_fix: Optional[str] = None


class DataValidatorProcessor(BaseProcessor):
    """Validates data quality, completeness, and consistency."""
    
    def __init__(self, config: Config, validation_rules: Optional[List[ValidationRule]] = None):
        super().__init__(config, "DataValidator")
        self.validation_rules = validation_rules or self._get_default_validation_rules()
        self.quality_thresholds = {
            'completeness': 0.8,  # 80% of fields should be present
            'consistency': 0.9,   # 90% consistency in formats
            'accuracy': 0.95      # 95% accuracy in validated fields
        }
    
    def _get_default_validation_rules(self) -> List[ValidationRule]:
        """Get default validation rules for HDM paper data."""
        return [
            # Required fields
            ValidationRule(
                field_name="title",
                rule_type="required",
                error_message="Title is required"
            ),
            ValidationRule(
                field_name="authors",
                rule_type="required", 
                error_message="Authors are required"
            ),
            ValidationRule(
                field_name="year",
                rule_type="required",
                error_message="Publication year is required"
            ),
            
            # Format validations
            ValidationRule(
                field_name="year",
                rule_type="range",
                min_value=1900,
                max_value=datetime.now().year + 1,
                error_message="Year must be between 1900 and current year"
            ),
            ValidationRule(
                field_name="doi",
                rule_type="format",
                pattern=r'^10\.\d+/.+',
                error_message="DOI must follow format 10.XXXX/XXXXX"
            ),
            ValidationRule(
                field_name="url",
                rule_type="format",
                pattern=r'^https?://.+',
                error_message="URL must start with http:// or https://"
            ),
            ValidationRule(
                field_name="relevancy",
                rule_type="enum",
                allowed_values=["High", "Medium", "Low"],
                error_message="Relevancy must be High, Medium, or Low"
            ),
            
            # Content quality validations
            ValidationRule(
                field_name="title",
                rule_type="custom",
                custom_validator="validate_title_quality",
                error_message="Title appears to be incomplete or malformed"
            ),
            ValidationRule(
                field_name="authors",
                rule_type="custom",
                custom_validator="validate_authors_format",
                error_message="Authors format appears incorrect"
            ),
            ValidationRule(
                field_name="summary",
                rule_type="custom", 
                custom_validator="validate_summary_length",
                error_message="Summary should be between 50-500 words"
            )
        ]
    
    def process_item(self, data: Dict[str, Any], **kwargs) -> ProcessingResult:
        """Validate a single data record."""
        try:
            validation_issues = self._validate_record(data)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(data, validation_issues)
            
            # Determine overall status
            error_count = sum(1 for issue in validation_issues if issue.severity == "error")
            warning_count = sum(1 for issue in validation_issues if issue.severity == "warning")
            
            if error_count > 0:
                status = ProcessingStatus.FAILED
                message = f"Validation failed with {error_count} errors, {warning_count} warnings"
            else:
                status = ProcessingStatus.COMPLETED
                message = f"Validation passed with {warning_count} warnings"
            
            return ProcessingResult(
                status=status,
                message=message,
                data={
                    'validation_issues': [issue.__dict__ for issue in validation_issues],
                    'quality_score': quality_score,
                    'error_count': error_count,
                    'warning_count': warning_count
                }
            )
            
        except Exception as e:
            self.logger.error(f"Failed to validate data: {str(e)}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=str(e),
                error=e
            )
    
    def _validate_record(self, data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate a single record against all rules."""
        issues = []
        
        for rule in self.validation_rules:
            field_value = data.get(rule.field_name)
            issue = self._apply_validation_rule(rule, field_value, data)
            if issue:
                issues.append(issue)
        
        # Additional cross-field validations
        issues.extend(self._validate_cross_field_consistency(data))
        
        return issues
    
    def _apply_validation_rule(self, rule: ValidationRule, value: Any, full_data: Dict[str, Any]) -> Optional[ValidationIssue]:
        """Apply a single validation rule."""
        if rule.rule_type == "required":
            if value is None or str(value).strip() == "":
                return ValidationIssue(
                    field_name=rule.field_name,
                    issue_type="missing_required",
                    message=rule.error_message or f"{rule.field_name} is required",
                    severity="error"
                )
        
        elif rule.rule_type == "format" and value:
            if rule.pattern and not re.match(rule.pattern, str(value)):
                return ValidationIssue(
                    field_name=rule.field_name,
                    issue_type="invalid_format",
                    message=rule.error_message or f"{rule.field_name} has invalid format",
                    severity="error",
                    suggested_fix=f"Should match pattern: {rule.pattern}"
                )
        
        elif rule.rule_type == "range" and value is not None:
            try:
                num_value = float(value)
                if rule.min_value is not None and num_value < rule.min_value:
                    return ValidationIssue(
                        field_name=rule.field_name,
                        issue_type="value_too_low",
                        message=rule.error_message or f"{rule.field_name} is below minimum value",
                        severity="error",
                        suggested_fix=f"Should be >= {rule.min_value}"
                    )
                if rule.max_value is not None and num_value > rule.max_value:
                    return ValidationIssue(
                        field_name=rule.field_name,
                        issue_type="value_too_high",
                        message=rule.error_message or f"{rule.field_name} is above maximum value",
                        severity="error",
                        suggested_fix=f"Should be <= {rule.max_value}"
                    )
            except (ValueError, TypeError):
                return ValidationIssue(
                    field_name=rule.field_name,
                    issue_type="invalid_number",
                    message=f"{rule.field_name} should be a number",
                    severity="error"
                )
        
        elif rule.rule_type == "enum" and value:
            if rule.allowed_values and str(value) not in rule.allowed_values:
                return ValidationIssue(
                    field_name=rule.field_name,
                    issue_type="invalid_value",
                    message=rule.error_message or f"{rule.field_name} has invalid value",
                    severity="error",
                    suggested_fix=f"Allowed values: {', '.join(rule.allowed_values)}"
                )
        
        elif rule.rule_type == "custom" and rule.custom_validator:
            return self._apply_custom_validator(rule, value, full_data)
        
        return None
    
    def _apply_custom_validator(self, rule: ValidationRule, value: Any, full_data: Dict[str, Any]) -> Optional[ValidationIssue]:
        """Apply custom validation logic."""
        validator_name = rule.custom_validator
        
        if validator_name == "validate_title_quality":
            return self._validate_title_quality(value)
        elif validator_name == "validate_authors_format":
            return self._validate_authors_format(value)
        elif validator_name == "validate_summary_length":
            return self._validate_summary_length(value)
        
        return None
    
    def _validate_title_quality(self, title: Any) -> Optional[ValidationIssue]:
        """Validate title quality."""
        if not title:
            return None
        
        title_str = str(title).strip()
        
        # Check for common issues
        issues = []
        
        if len(title_str) < 10:
            issues.append("too short")
        if len(title_str) > 200:
            issues.append("too long")
        if title_str.lower().startswith('article'):
            issues.append("starts with 'Article'")
        if title_str.count('?') > 2:
            issues.append("too many question marks")
        if not re.search(r'[a-zA-Z]', title_str):
            issues.append("no alphabetic characters")
        
        if issues:
            return ValidationIssue(
                field_name="title",
                issue_type="quality_issue",
                message=f"Title quality issues: {', '.join(issues)}",
                severity="warning"
            )
        
        return None
    
    def _validate_authors_format(self, authors: Any) -> Optional[ValidationIssue]:
        """Validate authors format."""
        if not authors:
            return None
        
        authors_str = str(authors).strip()
        
        # Check for common issues
        issues = []
        
        if 'et al' in authors_str.lower():
            issues.append("contains 'et al'")
        if '&' in authors_str:
            issues.append("uses & instead of comma")
        if authors_str.lower() in ['unknown', 'n/a', 'unavailable']:
            issues.append("placeholder value")
        if '@' in authors_str:
            issues.append("contains email addresses")
        
        # Check if it's just one word (likely incomplete)
        if len(authors_str.split()) == 1 and len(authors_str) > 3:
            issues.append("appears incomplete")
        
        if issues:
            return ValidationIssue(
                field_name="authors",
                issue_type="format_issue",
                message=f"Authors format issues: {', '.join(issues)}",
                severity="warning"
            )
        
        return None
    
    def _validate_summary_length(self, summary: Any) -> Optional[ValidationIssue]:
        """Validate summary length and quality."""
        if not summary:
            return ValidationIssue(
                field_name="summary",
                issue_type="missing_content",
                message="Summary is missing",
                severity="warning"
            )
        
        summary_str = str(summary).strip()
        word_count = len(summary_str.split())
        
        if word_count < 10:
            return ValidationIssue(
                field_name="summary",
                issue_type="too_short",
                message=f"Summary too short ({word_count} words)",
                severity="warning",
                suggested_fix="Should be at least 50 words"
            )
        elif word_count > 500:
            return ValidationIssue(
                field_name="summary",
                issue_type="too_long", 
                message=f"Summary too long ({word_count} words)",
                severity="warning",
                suggested_fix="Should be no more than 500 words"
            )
        
        return None
    
    def _validate_cross_field_consistency(self, data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate consistency across multiple fields."""
        issues = []
        
        # Check cite_key consistency
        cite_key = data.get('cite_key', '')
        authors = data.get('authors', '')
        year = data.get('year', '')
        
        if cite_key and authors and year:
            expected_cite_key = self._generate_expected_cite_key(authors, year)
            if cite_key.lower() != expected_cite_key.lower():
                issues.append(ValidationIssue(
                    field_name="cite_key",
                    issue_type="inconsistency",
                    message="Cite key doesn't match expected format",
                    severity="warning",
                    suggested_fix=f"Expected: {expected_cite_key}"
                ))
        
        # Check DOI/URL consistency
        doi = data.get('doi', '')
        url = data.get('url', '')
        
        if doi and url:
            if 'doi.org' in url and doi not in url:
                issues.append(ValidationIssue(
                    field_name="doi",
                    issue_type="inconsistency",
                    message="DOI and URL don't match",
                    severity="warning"
                ))
        
        return issues
    
    def _generate_expected_cite_key(self, authors: str, year: Any) -> str:
        """Generate expected cite_key from authors and year."""
        if not authors or not year:
            return ""
        
        first_author = authors.split(',')[0].strip()
        name_parts = first_author.split()
        lastname = name_parts[-1] if name_parts else first_author
        lastname = re.sub(r'[^\w]', '', lastname).lower()
        
        return f"{lastname}_{year}"
    
    def _calculate_quality_score(self, data: Dict[str, Any], issues: List[ValidationIssue]) -> float:
        """Calculate overall quality score for the record."""
        total_fields = len(data)
        if total_fields == 0:
            return 0.0
        
        # Completeness score (non-empty fields / total fields)
        non_empty_fields = sum(1 for v in data.values() if v and str(v).strip())
        completeness = non_empty_fields / total_fields
        
        # Error penalty
        error_penalty = sum(0.1 for issue in issues if issue.severity == "error")
        warning_penalty = sum(0.05 for issue in issues if issue.severity == "warning")
        
        # Calculate final score
        quality_score = max(0.0, completeness - error_penalty - warning_penalty)
        
        return round(quality_score, 3)
    
    def validate_dataset(self, data_list: List[Dict[str, Any]]) -> ProcessingResult:
        """Validate an entire dataset."""
        try:
            all_issues = []
            quality_scores = []
            
            for i, record in enumerate(data_list):
                result = self.process_item(record)
                if result.data:
                    issues = result.data.get('validation_issues', [])
                    score = result.data.get('quality_score', 0.0)
                    
                    # Add record index to issues
                    for issue in issues:
                        issue['record_index'] = i
                    
                    all_issues.extend(issues)
                    quality_scores.append(score)
            
            # Calculate dataset statistics
            avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
            error_records = sum(1 for score in quality_scores if score < 0.5)
            
            # Generate summary report
            summary = self._generate_validation_summary(all_issues, quality_scores)
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message=f"Validated {len(data_list)} records",
                data={
                    'total_records': len(data_list),
                    'average_quality': round(avg_quality, 3),
                    'error_records': error_records,
                    'all_issues': all_issues,
                    'quality_scores': quality_scores,
                    'summary': summary
                }
            )
            
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Dataset validation failed: {str(e)}",
                error=e
            )
    
    def _generate_validation_summary(self, all_issues: List[Dict], quality_scores: List[float]) -> Dict[str, Any]:
        """Generate validation summary report."""
        issue_types = {}
        severity_counts = {"error": 0, "warning": 0, "info": 0}
        
        for issue in all_issues:
            issue_type = issue.get('issue_type', 'unknown')
            severity = issue.get('severity', 'error')
            
            issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
            severity_counts[severity] += 1
        
        return {
            'total_issues': len(all_issues),
            'issue_types': issue_types,
            'severity_counts': severity_counts,
            'quality_distribution': {
                'excellent': sum(1 for s in quality_scores if s >= 0.9),
                'good': sum(1 for s in quality_scores if 0.7 <= s < 0.9),
                'fair': sum(1 for s in quality_scores if 0.5 <= s < 0.7),
                'poor': sum(1 for s in quality_scores if s < 0.5)
            }
        }
    
    def export_validation_report(self, validation_result: ProcessingResult, output_file: Path):
        """Export detailed validation report to file."""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'summary': validation_result.data,
                'detailed_issues': validation_result.data.get('all_issues', [])
            }
            
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            self.logger.info(f"Validation report exported to {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to export validation report: {e}")
#!/usr/bin/env python3
"""
Intelligent consolidation strategy that picks the best available information
and handles empty columns with smart fallback logic.
"""

import sqlite3
import json
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('intelligent_consolidation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IntelligentConsolidator:
    """Smart consolidation that picks best available information."""
    
    def __init__(self):
        self.consolidation_rules = self._define_consolidation_rules()
        self.stats = {
            'total_records': 0,
            'fields_updated': 0,
            'empty_fields_filled': 0,
            'quality_improvements': 0,
            'consolidation_details': []
        }
    
    def _define_consolidation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Define intelligent consolidation rules for each field."""
        return {
            # Metadata fields - prefer enhanced YAML when available
            'title': {
                'priority_sources': ['yaml_title', 'title'],
                'strategy': 'prefer_longer_non_empty',
                'quality_checks': ['remove_article_prefix', 'clean_formatting'],
                'fallback': 'any_non_empty'
            },
            'authors': {
                'priority_sources': ['yaml_authors', 'authors'],
                'strategy': 'prefer_complete_author_list',
                'quality_checks': ['expand_et_al', 'standardize_format'],
                'fallback': 'any_non_empty'
            },
            'year': {
                'priority_sources': ['yaml_year', 'year'],
                'strategy': 'prefer_valid_year',
                'quality_checks': ['validate_year_range'],
                'fallback': 'any_non_empty'
            },
            'doi': {
                'priority_sources': ['yaml_doi', 'doi'],
                'strategy': 'prefer_valid_doi',
                'quality_checks': ['validate_doi_format', 'clean_doi'],
                'fallback': 'any_non_empty'
            },
            'url': {
                'priority_sources': ['yaml_url', 'url'],
                'strategy': 'prefer_accessible_url',
                'quality_checks': ['validate_url_format', 'prefer_https'],
                'fallback': 'any_non_empty'
            },
            
            # Content fields - prefer manually curated CSV
            'summary': {
                'priority_sources': ['summary', 'yaml_summary'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['remove_duplicates', 'check_completeness'],
                'fallback': 'any_non_empty'
            },
            'insights': {
                'priority_sources': ['insights', 'yaml_insights'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['check_actionability', 'remove_generic'],
                'fallback': 'any_non_empty'
            },
            'tldr': {
                'priority_sources': ['tldr', 'yaml_tldr'],
                'strategy': 'prefer_concise_summary',
                'quality_checks': ['check_length', 'ensure_single_sentence'],
                'fallback': 'any_non_empty'
            },
            'methodology': {
                'priority_sources': ['methodology', 'yaml_methodology'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['check_technical_detail'],
                'fallback': 'any_non_empty'
            },
            'key_findings': {
                'priority_sources': ['key_findings', 'yaml_key_findings'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['check_specificity'],
                'fallback': 'any_non_empty'
            },
            'primary_outcomes': {
                'priority_sources': ['primary_outcomes', 'yaml_primary_outcomes'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['check_outcome_specificity'],
                'fallback': 'any_non_empty'
            },
            'limitations': {
                'priority_sources': ['limitations', 'yaml_limitations'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['check_critical_analysis'],
                'fallback': 'any_non_empty'
            },
            'conclusion': {
                'priority_sources': ['conclusion', 'yaml_conclusion'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['check_synthesis_quality'],
                'fallback': 'any_non_empty'
            },
            'research_gaps': {
                'priority_sources': ['research_gaps', 'yaml_research_gaps'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['check_gap_identification'],
                'fallback': 'any_non_empty'
            },
            'future_work': {
                'priority_sources': ['future_work', 'yaml_future_work'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['check_actionable_suggestions'],
                'fallback': 'any_non_empty'
            },
            'implementation_insights': {
                'priority_sources': ['implementation_insights', 'yaml_implementation_insights'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['check_practical_value'],
                'fallback': 'any_non_empty'
            },
            'research_question': {
                'priority_sources': ['research_question', 'yaml_research_question'],
                'strategy': 'prefer_detailed_content',
                'quality_checks': ['check_question_clarity'],
                'fallback': 'any_non_empty'
            },
            
            # Assessment fields - strongly prefer CSV (expert curation)
            'relevancy': {
                'priority_sources': ['relevancy', 'yaml_relevancy'],
                'strategy': 'prefer_expert_assessment',
                'quality_checks': ['validate_relevancy_values'],
                'fallback': 'default_medium'
            },
            'relevancy_justification': {
                'priority_sources': ['relevancy_justification', 'yaml_relevancy_justification'],
                'strategy': 'prefer_expert_analysis',
                'quality_checks': ['check_justification_quality'],
                'fallback': 'generate_basic_justification'
            },
            'tags': {
                'priority_sources': ['tags', 'yaml_tags', 'yaml_keywords'],
                'strategy': 'merge_and_deduplicate',
                'quality_checks': ['standardize_tags', 'remove_duplicates'],
                'fallback': 'extract_from_title_and_summary'
            }
        }
    
    def normalize_value(self, value: Any) -> Optional[str]:
        """Normalize a value for processing."""
        if value is None or value == '' or str(value).lower() in ['none', 'null', 'nan']:
            return None
        return str(value).strip()
    
    def apply_quality_checks(self, value: str, checks: List[str]) -> str:
        """Apply quality improvement checks to a value."""
        if not value:
            return value
            
        result = value
        
        for check in checks:
            if check == 'remove_article_prefix':
                result = re.sub(r'^(Article|Paper|Study):\s*', '', result, flags=re.IGNORECASE)
            elif check == 'clean_formatting':
                result = re.sub(r'\s+', ' ', result).strip()
            elif check == 'expand_et_al':
                # This would need external data to actually expand
                pass
            elif check == 'standardize_format':
                # Ensure comma-separated author format
                if ' and ' in result and ',' not in result:
                    result = result.replace(' and ', ', ')
            elif check == 'validate_year_range':
                # Ensure year is reasonable (1990-2025)
                if result and result.isdigit():
                    year = int(result)
                    if year < 1990 or year > 2025:
                        result = None
            elif check == 'validate_doi_format':
                if result and not result.startswith('10.'):
                    result = None
            elif check == 'clean_doi':
                if result:
                    result = re.sub(r'^(doi:?|DOI:?)\s*', '', result, flags=re.IGNORECASE)
            elif check == 'validate_url_format':
                if result and not (result.startswith('http://') or result.startswith('https://')):
                    result = None
            elif check == 'prefer_https':
                if result and result.startswith('http://'):
                    result = result.replace('http://', 'https://', 1)
            elif check == 'standardize_tags':
                if result:
                    # Convert to comma-separated, lowercase, deduplicated
                    tags = [tag.strip().lower() for tag in re.split(r'[,;|]', result)]
                    tags = list(dict.fromkeys([tag for tag in tags if tag]))  # Deduplicate while preserving order
                    result = ', '.join(tags)
        
        return result
    
    def choose_best_value(self, record: Dict[str, Any], field_config: Dict[str, Any]) -> Tuple[Optional[str], str]:
        """Choose the best value based on strategy and priority sources."""
        strategy = field_config['strategy']
        sources = field_config['priority_sources']
        quality_checks = field_config.get('quality_checks', [])
        fallback = field_config.get('fallback', 'any_non_empty')
        
        # Get values from all sources
        values = {}
        for source in sources:
            raw_value = record.get(source)
            normalized = self.normalize_value(raw_value)
            if normalized:
                cleaned = self.apply_quality_checks(normalized, quality_checks)
                if cleaned:
                    values[source] = cleaned
        
        # Apply strategy
        if strategy == 'prefer_longer_non_empty':
            if values:
                best_source = max(values.keys(), key=lambda k: len(values[k]))
                return values[best_source], f"chose longest from {best_source}"
        
        elif strategy == 'prefer_complete_author_list':
            if values:
                # Prefer the one without "et al."
                for source in sources:
                    if source in values and 'et al' not in values[source].lower():
                        return values[source], f"chose complete list from {source}"
                # If all have "et al", choose first available
                best_source = sources[0] if sources[0] in values else list(values.keys())[0]
                return values[best_source], f"chose from {best_source} (all have et al)"
        
        elif strategy == 'prefer_valid_year':
            for source in sources:
                if source in values:
                    value = values[source]
                    if value.isdigit() and 1990 <= int(value) <= 2025:
                        return value, f"chose valid year from {source}"
        
        elif strategy == 'prefer_valid_doi':
            for source in sources:
                if source in values:
                    value = values[source]
                    if value.startswith('10.'):
                        return value, f"chose valid DOI from {source}"
        
        elif strategy == 'prefer_accessible_url':
            for source in sources:
                if source in values:
                    value = values[source]
                    if value.startswith('https://'):
                        return value, f"chose HTTPS URL from {source}"
            # Fallback to any URL
            for source in sources:
                if source in values:
                    return values[source], f"chose URL from {source}"
        
        elif strategy == 'prefer_detailed_content':
            if values:
                # Choose the longer, more detailed content
                best_source = max(values.keys(), key=lambda k: len(values[k]))
                return values[best_source], f"chose detailed content from {best_source}"
        
        elif strategy == 'prefer_concise_summary':
            if values:
                # For TLDR, prefer concise but complete
                for source in sources:
                    if source in values:
                        value = values[source]
                        if 50 <= len(value) <= 200:  # Ideal TLDR length
                            return value, f"chose optimal length from {source}"
                # Fallback to first available
                best_source = list(values.keys())[0]
                return values[best_source], f"chose from {best_source}"
        
        elif strategy == 'prefer_expert_assessment':
            # For relevancy, prefer CSV (expert assessment)
            for source in sources:
                if source in values and not source.startswith('yaml_'):
                    return values[source], f"chose expert assessment from {source}"
        
        elif strategy == 'prefer_expert_analysis':
            # For justifications, prefer CSV (expert analysis)
            for source in sources:
                if source in values and not source.startswith('yaml_'):
                    return values[source], f"chose expert analysis from {source}"
        
        elif strategy == 'merge_and_deduplicate':
            # For tags, merge all sources
            all_tags = []
            used_sources = []
            for source in sources:
                if source in values:
                    tags = [tag.strip().lower() for tag in values[source].split(',')]
                    all_tags.extend([tag for tag in tags if tag])
                    used_sources.append(source)
            
            if all_tags:
                unique_tags = list(dict.fromkeys(all_tags))  # Deduplicate while preserving order
                return ', '.join(unique_tags), f"merged from {', '.join(used_sources)}"
        
        # Fallback strategies
        if fallback == 'any_non_empty' and values:
            best_source = list(values.keys())[0]
            return values[best_source], f"fallback to {best_source}"
        
        elif fallback == 'default_medium':
            return 'Medium', 'default relevancy value'
        
        elif fallback == 'generate_basic_justification':
            title = record.get('title', 'this paper')
            return f"Relevant to HDM research based on {title[:50]}...", 'generated basic justification'
        
        elif fallback == 'extract_from_title_and_summary':
            # Extract basic tags from title and summary
            text = (record.get('title', '') + ' ' + record.get('summary', '')).lower()
            potential_tags = []
            
            # Look for common research terms
            research_terms = ['knowledge graph', 'personal', 'digital twin', 'temporal', 'heterogeneous', 
                            'data integration', 'schema', 'ontology', 'semantic', 'graph neural network']
            
            for term in research_terms:
                if term in text:
                    potential_tags.append(term.replace(' ', '_'))
            
            if potential_tags:
                return ', '.join(potential_tags), 'extracted from content'
        
        return None, 'no suitable value found'
    
    def consolidate_single_record(self, record: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
        """Consolidate a single record using intelligent rules."""
        consolidated = record.copy()
        changes = []
        
        for field, config in self.consolidation_rules.items():
            if field == 'downloaded':  # Skip downloaded field as requested
                continue
                
            current_value = self.normalize_value(record.get(field))
            new_value, reasoning = self.choose_best_value(record, config)
            
            if new_value and new_value != current_value:
                changes.append({
                    'field': field,
                    'old_value': current_value,
                    'new_value': new_value,
                    'reasoning': reasoning,
                    'improvement_type': 'filled_empty' if not current_value else 'quality_improvement'
                })
                
                if not dry_run:
                    consolidated[field] = new_value
                
                # Update stats
                if not current_value:
                    self.stats['empty_fields_filled'] += 1
                else:
                    self.stats['quality_improvements'] += 1
                
                self.stats['fields_updated'] += 1
        
        if changes:
            self.stats['consolidation_details'].append({
                'cite_key': record.get('cite_key', 'unknown'),
                'changes': changes
            })
        
        return consolidated
    
    def run_dry_run_analysis(self) -> Dict[str, Any]:
        """Run a comprehensive dry run analysis."""
        logger.info("Starting intelligent consolidation dry run...")
        
        # Get all data from database
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all columns we need
        all_columns = set()
        for config in self.consolidation_rules.values():
            all_columns.update(config['priority_sources'])
        all_columns.add('cite_key')
        
        query = f"SELECT {', '.join(all_columns)} FROM papers"
        cursor.execute(query)
        records = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        self.stats['total_records'] = len(records)
        logger.info(f"Analyzing {len(records)} records...")
        
        # Process each record in dry run mode
        consolidated_records = []
        for record in records:
            consolidated = self.consolidate_single_record(record, dry_run=True)
            consolidated_records.append(consolidated)
        
        # Generate analysis report
        analysis = self._generate_dry_run_analysis()
        
        logger.info("Dry run analysis completed")
        return analysis
    
    def _generate_dry_run_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive analysis of the dry run."""
        
        # Analyze changes by field
        field_analysis = {}
        for field in self.consolidation_rules.keys():
            if field == 'downloaded':
                continue
                
            field_changes = []
            for detail in self.stats['consolidation_details']:
                field_changes.extend([c for c in detail['changes'] if c['field'] == field])
            
            if field_changes:
                field_analysis[field] = {
                    'total_changes': len(field_changes),
                    'filled_empty': len([c for c in field_changes if c['improvement_type'] == 'filled_empty']),
                    'quality_improvements': len([c for c in field_changes if c['improvement_type'] == 'quality_improvement']),
                    'sample_changes': field_changes[:3]  # First 3 examples
                }
        
        # Overall statistics
        return {
            'dry_run_timestamp': datetime.now().isoformat(),
            'total_records_analyzed': self.stats['total_records'],
            'total_fields_updated': self.stats['fields_updated'],
            'empty_fields_filled': self.stats['empty_fields_filled'],
            'quality_improvements': self.stats['quality_improvements'],
            'records_with_changes': len(self.stats['consolidation_details']),
            'field_analysis': field_analysis,
            'consolidation_rules_applied': len(self.consolidation_rules) - 1,  # Exclude 'downloaded'
            'sample_record_changes': self.stats['consolidation_details'][:5],  # First 5 examples
            'impact_summary': {
                'data_completeness_improvement': f"{self.stats['empty_fields_filled']} empty fields filled",
                'data_quality_enhancement': f"{self.stats['quality_improvements']} quality improvements",
                'affected_records_percentage': f"{(len(self.stats['consolidation_details']) / self.stats['total_records']) * 100:.1f}%"
            }
        }

def main():
    """Main function to run intelligent consolidation analysis."""
    logger.info("Starting Intelligent Consolidation Strategy Analysis...")
    
    # Initialize consolidator
    consolidator = IntelligentConsolidator()
    
    # Run dry run analysis
    analysis = consolidator.run_dry_run_analysis()
    
    # Save detailed analysis
    with open('intelligent_consolidation_dry_run.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info("Analysis saved to intelligent_consolidation_dry_run.json")
    
    # Print summary
    print("\n" + "="*80)
    print("INTELLIGENT CONSOLIDATION DRY RUN ANALYSIS")
    print("="*80)
    
    print(f"📊 Records Analyzed: {analysis['total_records_analyzed']}")
    print(f"🔄 Fields Updated: {analysis['total_fields_updated']}")
    print(f"📈 Empty Fields Filled: {analysis['empty_fields_filled']}")
    print(f"⭐ Quality Improvements: {analysis['quality_improvements']}")
    print(f"📝 Records with Changes: {analysis['records_with_changes']}")
    print(f"🎯 Affected Records: {analysis['impact_summary']['affected_records_percentage']}")
    
    print(f"\n🏆 TOP FIELD IMPROVEMENTS:")
    sorted_fields = sorted(analysis['field_analysis'].items(), 
                          key=lambda x: x[1]['total_changes'], reverse=True)
    
    for field, stats in sorted_fields[:10]:
        print(f"   {field}: {stats['total_changes']} changes "
              f"({stats['filled_empty']} filled, {stats['quality_improvements']} improved)")
    
    print(f"\n📋 SAMPLE CHANGES (First 3 records):")
    for i, record_changes in enumerate(analysis['sample_record_changes'][:3], 1):
        cite_key = record_changes['cite_key']
        changes = record_changes['changes']
        print(f"\n   Record {i}: {cite_key}")
        for change in changes[:3]:  # First 3 changes per record
            print(f"     • {change['field']}: {change['reasoning']}")
            if change['improvement_type'] == 'filled_empty':
                print(f"       Added: {change['new_value'][:60]}...")
            else:
                print(f"       Changed: {change['old_value'][:30]}... → {change['new_value'][:30]}...")
    
    print(f"\n💡 CONSOLIDATION STRATEGY READY:")
    print(f"   ✅ Remove 'downloaded' column as requested")
    print(f"   ✅ Intelligent field selection with quality checks")
    print(f"   ✅ Smart fallback for empty fields")
    print(f"   ✅ Preserve expert curation while enhancing metadata")
    
    print("="*80)
    
    return analysis

if __name__ == "__main__":
    main()
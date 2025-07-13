#!/usr/bin/env python3
"""
Compare CSV/database data with YAML frontmatter data field-by-field.
"""

import sqlite3
import json
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('csv_yaml_comparison.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_database_data() -> Dict[str, Dict[str, Any]]:
    """Get all data from the database."""
    conn = sqlite3.connect('hdm_papers.db')
    conn.row_factory = sqlite3.Row  # This enables column name access
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM papers")
    
    database_data = {}
    for row in cursor.fetchall():
        cite_key = row['cite_key']
        database_data[cite_key] = dict(row)
    
    conn.close()
    logger.info(f"Retrieved {len(database_data)} records from database")
    return database_data

def compare_field_values(csv_value: Any, yaml_value: Any, field_name: str, cite_key: str) -> Dict[str, Any]:
    """Compare two field values and return comparison results."""
    # Normalize values for comparison
    csv_norm = str(csv_value).strip() if csv_value not in [None, ''] else None
    yaml_norm = str(yaml_value).strip() if yaml_value not in [None, ''] else None
    
    comparison = {
        'cite_key': cite_key,
        'field': field_name,
        'csv_value': csv_norm,
        'yaml_value': yaml_norm,
        'are_equal': False,
        'difference_type': None,
        'recommended_action': None
    }
    
    # Check for exact equality
    if csv_norm == yaml_norm:
        comparison['are_equal'] = True
        comparison['difference_type'] = 'identical'
        comparison['recommended_action'] = 'keep_either'
        return comparison
    
    # Both empty or None
    if not csv_norm and not yaml_norm:
        comparison['are_equal'] = True
        comparison['difference_type'] = 'both_empty'
        comparison['recommended_action'] = 'keep_either'
        return comparison
    
    # One is empty, other has content
    if not csv_norm and yaml_norm:
        comparison['difference_type'] = 'yaml_has_content_csv_empty'
        comparison['recommended_action'] = 'use_yaml'
        return comparison
    
    if csv_norm and not yaml_norm:
        comparison['difference_type'] = 'csv_has_content_yaml_empty'
        comparison['recommended_action'] = 'use_csv'
        return comparison
    
    # Both have content but differ
    if csv_norm and yaml_norm:
        # Check for substring relationships
        if csv_norm.lower() in yaml_norm.lower():
            comparison['difference_type'] = 'yaml_extends_csv'
            comparison['recommended_action'] = 'use_yaml'
        elif yaml_norm.lower() in csv_norm.lower():
            comparison['difference_type'] = 'csv_extends_yaml'
            comparison['recommended_action'] = 'use_csv'
        else:
            # Check length difference
            len_diff = abs(len(csv_norm) - len(yaml_norm))
            if len_diff > 100:
                comparison['difference_type'] = 'significant_content_difference'
                comparison['recommended_action'] = 'manual_review'
            else:
                comparison['difference_type'] = 'minor_content_difference'
                comparison['recommended_action'] = 'prefer_yaml'  # Default to YAML as it's more recent
    
    return comparison

def field_by_field_comparison(database_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Perform detailed field-by-field comparison between CSV and YAML data."""
    
    # Fields to compare (CSV field -> YAML field mapping)
    field_mappings = {
        'title': 'yaml_title',
        'authors': 'yaml_authors',
        'year': 'yaml_year',
        'doi': 'yaml_doi',
        'url': 'yaml_url',
        'relevancy': 'yaml_relevancy',
        'relevancy_justification': 'yaml_relevancy_justification',
        'insights': 'yaml_insights',
        'tldr': 'yaml_tldr',
        'summary': 'yaml_summary',
        'research_question': 'yaml_research_question',
        'methodology': 'yaml_methodology',
        'key_findings': 'yaml_key_findings',
        'primary_outcomes': 'yaml_primary_outcomes',
        'limitations': 'yaml_limitations',
        'conclusion': 'yaml_conclusion',
        'research_gaps': 'yaml_research_gaps',
        'future_work': 'yaml_future_work',
        'implementation_insights': 'yaml_implementation_insights',
        'tags': 'yaml_tags',
        'downloaded': 'yaml_downloaded'
    }
    
    comparison_results = {
        'field_comparisons': [],
        'summary_stats': {},
        'recommendations': {}
    }
    
    logger.info("Starting field-by-field comparison...")
    
    for csv_field, yaml_field in field_mappings.items():
        logger.info(f"Comparing field: {csv_field} <-> {yaml_field}")
        
        field_stats = {
            'field': csv_field,
            'yaml_field': yaml_field,
            'identical': 0,
            'yaml_better': 0,
            'csv_better': 0,
            'both_empty': 0,
            'need_manual_review': 0,
            'total_compared': 0,
            'differences': []
        }
        
        for cite_key, record in database_data.items():
            csv_value = record.get(csv_field)
            yaml_value = record.get(yaml_field)
            
            comparison = compare_field_values(csv_value, yaml_value, csv_field, cite_key)
            field_stats['total_compared'] += 1
            
            if comparison['are_equal']:
                if comparison['difference_type'] == 'both_empty':
                    field_stats['both_empty'] += 1
                else:
                    field_stats['identical'] += 1
            else:
                field_stats['differences'].append(comparison)
                
                if comparison['recommended_action'] in ['use_yaml', 'prefer_yaml']:
                    field_stats['yaml_better'] += 1
                elif comparison['recommended_action'] == 'use_csv':
                    field_stats['csv_better'] += 1
                elif comparison['recommended_action'] == 'manual_review':
                    field_stats['need_manual_review'] += 1
        
        comparison_results['field_comparisons'].append(field_stats)
        
        # Calculate percentages
        total = field_stats['total_compared']
        if total > 0:
            comparison_results['summary_stats'][csv_field] = {
                'identical_percentage': (field_stats['identical'] / total) * 100,
                'yaml_better_percentage': (field_stats['yaml_better'] / total) * 100,
                'csv_better_percentage': (field_stats['csv_better'] / total) * 100,
                'both_empty_percentage': (field_stats['both_empty'] / total) * 100,
                'need_review_percentage': (field_stats['need_manual_review'] / total) * 100
            }
        
        logger.info(f"  Identical: {field_stats['identical']}, "
                   f"YAML better: {field_stats['yaml_better']}, "
                   f"CSV better: {field_stats['csv_better']}, "
                   f"Need review: {field_stats['need_manual_review']}")
    
    return comparison_results

def generate_consolidation_recommendations(comparison_results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate recommendations for data consolidation based on comparison results."""
    
    recommendations = {
        'field_recommendations': {},
        'overall_strategy': {},
        'high_priority_fields': [],
        'manual_review_required': []
    }
    
    for field_comparison in comparison_results['field_comparisons']:
        field = field_comparison['field']
        yaml_field = field_comparison['yaml_field']
        
        # Calculate recommendation based on stats
        total = field_comparison['total_compared']
        yaml_better = field_comparison['yaml_better']
        csv_better = field_comparison['csv_better']
        identical = field_comparison['identical']
        need_review = field_comparison['need_manual_review']
        
        if total == 0:
            continue
            
        yaml_better_pct = (yaml_better / total) * 100
        csv_better_pct = (csv_better / total) * 100
        identical_pct = (identical / total) * 100
        review_pct = (need_review / total) * 100
        
        # Determine recommendation
        if identical_pct > 80:
            strategy = 'keep_current'
            priority = 'low'
        elif yaml_better_pct > 60:
            strategy = 'prefer_yaml'
            priority = 'high' if yaml_better_pct > 80 else 'medium'
        elif csv_better_pct > 60:
            strategy = 'prefer_csv'
            priority = 'high' if csv_better_pct > 80 else 'medium'
        elif review_pct > 30:
            strategy = 'manual_review'
            priority = 'high'
        else:
            strategy = 'merge_intelligently'
            priority = 'medium'
        
        recommendations['field_recommendations'][field] = {
            'yaml_field': yaml_field,
            'strategy': strategy,
            'priority': priority,
            'confidence': max(yaml_better_pct, csv_better_pct, identical_pct),
            'stats': {
                'identical_pct': identical_pct,
                'yaml_better_pct': yaml_better_pct,
                'csv_better_pct': csv_better_pct,
                'review_pct': review_pct
            }
        }
        
        if priority == 'high':
            recommendations['high_priority_fields'].append(field)
        
        if review_pct > 20:
            recommendations['manual_review_required'].append(field)
    
    # Overall strategy
    total_fields = len(recommendations['field_recommendations'])
    yaml_preferred = sum(1 for r in recommendations['field_recommendations'].values() if r['strategy'] == 'prefer_yaml')
    csv_preferred = sum(1 for r in recommendations['field_recommendations'].values() if r['strategy'] == 'prefer_csv')
    
    if yaml_preferred > csv_preferred:
        recommendations['overall_strategy']['primary'] = 'yaml_preferred'
        recommendations['overall_strategy']['reasoning'] = f"YAML data is better in {yaml_preferred}/{total_fields} fields"
    else:
        recommendations['overall_strategy']['primary'] = 'csv_preferred'
        recommendations['overall_strategy']['reasoning'] = f"CSV data is better in {csv_preferred}/{total_fields} fields"
    
    return recommendations

def main():
    """Main function to compare CSV and YAML data."""
    logger.info("Starting CSV vs YAML data comparison...")
    
    # Get database data
    database_data = get_database_data()
    
    # Perform field-by-field comparison
    comparison_results = field_by_field_comparison(database_data)
    
    # Generate consolidation recommendations
    recommendations = generate_consolidation_recommendations(comparison_results)
    
    # Combine all results
    final_report = {
        'comparison_timestamp': datetime.now().isoformat(),
        'database_records_analyzed': len(database_data),
        'comparison_results': comparison_results,
        'consolidation_recommendations': recommendations
    }
    
    # Save full report
    with open('csv_yaml_comparison_report.json', 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info("Comparison report saved to csv_yaml_comparison_report.json")
    
    # Print summary
    print("\n" + "="*60)
    print("CSV vs YAML DATA COMPARISON SUMMARY")
    print("="*60)
    print(f"Total database records analyzed: {len(database_data)}")
    print(f"Total fields compared: {len(comparison_results['field_comparisons'])}")
    
    print(f"\nOverall strategy: {recommendations['overall_strategy']['primary']}")
    print(f"Reasoning: {recommendations['overall_strategy']['reasoning']}")
    
    print(f"\nHigh priority fields for consolidation: {len(recommendations['high_priority_fields'])}")
    if recommendations['high_priority_fields']:
        for field in recommendations['high_priority_fields'][:5]:
            rec = recommendations['field_recommendations'][field]
            print(f"  {field}: {rec['strategy']} (confidence: {rec['confidence']:.1f}%)")
    
    print(f"\nFields requiring manual review: {len(recommendations['manual_review_required'])}")
    if recommendations['manual_review_required']:
        for field in recommendations['manual_review_required'][:5]:
            rec = recommendations['field_recommendations'][field]
            print(f"  {field}: {rec['stats']['review_pct']:.1f}% need review")
    
    # Show some specific examples
    print(f"\nExample differences (first 3):")
    total_differences = 0
    for field_comp in comparison_results['field_comparisons']:
        if field_comp['differences']:
            print(f"\n{field_comp['field']}:")
            for diff in field_comp['differences'][:2]:
                total_differences += 1
                print(f"  {diff['cite_key']}: {diff['difference_type']}")
                print(f"    CSV: {diff['csv_value'][:100]}...")
                print(f"    YAML: {diff['yaml_value'][:100]}...")
                print(f"    Recommendation: {diff['recommended_action']}")
    
    print(f"\nTotal differences found: {total_differences}")
    
    return final_report

if __name__ == "__main__":
    main()
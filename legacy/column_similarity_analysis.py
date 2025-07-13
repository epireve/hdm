#!/usr/bin/env python3
"""
Comprehensive similarity analysis between YAML and original CSV columns.
"""

import sqlite3
import json
import re
from typing import Dict, Any, List, Tuple, Optional
import logging
from datetime import datetime
from collections import defaultdict
import difflib

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('column_similarity_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimilarityAnalyzer:
    """Analyze similarity between YAML and original CSV columns."""
    
    def __init__(self):
        self.similarity_metrics = {}
        self.field_mappings = {
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
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        if not text or text in ['', 'None', 'null']:
            return ""
        
        # Convert to string and lowercase
        text = str(text).lower().strip()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common prefixes/suffixes that might differ
        text = re.sub(r'^(article|paper|study):\s*', '', text)
        text = re.sub(r'\s*\.\s*$', '', text)
        
        # Remove quotes
        text = text.strip('"\'')
        
        return text
    
    def calculate_text_similarity(self, text1: str, text2: str) -> Dict[str, float]:
        """Calculate various similarity metrics between two texts."""
        norm1 = self.normalize_text(text1)
        norm2 = self.normalize_text(text2)
        
        if not norm1 and not norm2:
            return {'exact_match': 1.0, 'sequence_match': 1.0, 'jaccard': 1.0, 'length_ratio': 1.0}
        
        if not norm1 or not norm2:
            return {'exact_match': 0.0, 'sequence_match': 0.0, 'jaccard': 0.0, 'length_ratio': 0.0}
        
        # Exact match
        exact_match = 1.0 if norm1 == norm2 else 0.0
        
        # Sequence similarity using difflib
        sequence_match = difflib.SequenceMatcher(None, norm1, norm2).ratio()
        
        # Jaccard similarity (word-based)
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        if words1 or words2:
            jaccard = len(words1.intersection(words2)) / len(words1.union(words2))
        else:
            jaccard = 1.0
        
        # Length ratio similarity
        len1, len2 = len(norm1), len(norm2)
        if len1 == 0 and len2 == 0:
            length_ratio = 1.0
        elif len1 == 0 or len2 == 0:
            length_ratio = 0.0
        else:
            length_ratio = min(len1, len2) / max(len1, len2)
        
        return {
            'exact_match': exact_match,
            'sequence_match': sequence_match,
            'jaccard': jaccard,
            'length_ratio': length_ratio
        }
    
    def analyze_field_similarity(self, records: List[Dict], csv_field: str, yaml_field: str) -> Dict[str, Any]:
        """Analyze similarity for a specific field across all records."""
        logger.info(f"Analyzing similarity for {csv_field} <-> {yaml_field}")
        
        similarities = []
        distribution = {
            'both_empty': 0,
            'csv_only': 0,
            'yaml_only': 0,
            'both_present': 0,
            'identical': 0,
            'similar': 0,
            'different': 0
        }
        
        detailed_comparisons = []
        
        for record in records:
            csv_value = record.get(csv_field)
            yaml_value = record.get(yaml_field)
            cite_key = record.get('cite_key', 'unknown')
            
            # Categorize by presence
            csv_present = csv_value not in [None, '', 'None']
            yaml_present = yaml_value not in [None, '', 'None']
            
            if not csv_present and not yaml_present:
                distribution['both_empty'] += 1
                continue
            elif csv_present and not yaml_present:
                distribution['csv_only'] += 1
                continue
            elif not csv_present and yaml_present:
                distribution['yaml_only'] += 1
                continue
            else:
                distribution['both_present'] += 1
            
            # Calculate similarity metrics
            sim_metrics = self.calculate_text_similarity(csv_value, yaml_value)
            similarities.append(sim_metrics)
            
            # Categorize by similarity
            if sim_metrics['exact_match'] == 1.0:
                distribution['identical'] += 1
            elif sim_metrics['sequence_match'] > 0.8:
                distribution['similar'] += 1
            else:
                distribution['different'] += 1
            
            # Store detailed comparison for different cases
            if sim_metrics['exact_match'] < 1.0 and len(detailed_comparisons) < 10:
                detailed_comparisons.append({
                    'cite_key': cite_key,
                    'csv_value': str(csv_value)[:200] + '...' if len(str(csv_value)) > 200 else str(csv_value),
                    'yaml_value': str(yaml_value)[:200] + '...' if len(str(yaml_value)) > 200 else str(yaml_value),
                    'similarity_metrics': sim_metrics
                })
        
        # Calculate aggregate statistics
        if similarities:
            avg_similarity = {
                metric: sum(s[metric] for s in similarities) / len(similarities)
                for metric in similarities[0].keys()
            }
        else:
            avg_similarity = {'exact_match': 0.0, 'sequence_match': 0.0, 'jaccard': 0.0, 'length_ratio': 0.0}
        
        # Calculate overall similarity score
        overall_score = (
            avg_similarity['exact_match'] * 0.4 +
            avg_similarity['sequence_match'] * 0.3 +
            avg_similarity['jaccard'] * 0.2 +
            avg_similarity['length_ratio'] * 0.1
        )
        
        return {
            'field_pair': f"{csv_field} <-> {yaml_field}",
            'total_records': len(records),
            'records_compared': len(similarities),
            'distribution': distribution,
            'average_similarity': avg_similarity,
            'overall_similarity_score': overall_score,
            'detailed_comparisons': detailed_comparisons,
            'quality_assessment': self.assess_field_quality(distribution, avg_similarity)
        }
    
    def assess_field_quality(self, distribution: Dict, avg_similarity: Dict) -> Dict[str, Any]:
        """Assess the quality of field comparison."""
        total_records = sum(distribution.values())
        
        # Data availability score
        data_availability = (distribution['both_present'] + distribution['csv_only'] + distribution['yaml_only']) / total_records
        
        # Consistency score (how often they match when both present)
        if distribution['both_present'] > 0:
            consistency = distribution['identical'] / distribution['both_present']
        else:
            consistency = 0.0
        
        # Completeness score (how often both sources have data)
        completeness = distribution['both_present'] / total_records if total_records > 0 else 0.0
        
        # Overall quality score
        quality_score = (data_availability * 0.3 + consistency * 0.5 + completeness * 0.2)
        
        # Determine recommendation
        if quality_score > 0.8 and avg_similarity['sequence_match'] > 0.9:
            recommendation = "EXCELLENT - High consistency, prefer either source"
        elif quality_score > 0.6 and avg_similarity['sequence_match'] > 0.7:
            recommendation = "GOOD - Generally consistent, minor differences"
        elif distribution['csv_only'] > distribution['yaml_only']:
            recommendation = "PREFER CSV - More complete in original source"
        elif distribution['yaml_only'] > distribution['csv_only']:
            recommendation = "PREFER YAML - More complete in enhanced source"
        else:
            recommendation = "NEEDS REVIEW - Significant differences found"
        
        return {
            'data_availability_score': data_availability,
            'consistency_score': consistency,
            'completeness_score': completeness,
            'overall_quality_score': quality_score,
            'recommendation': recommendation
        }
    
    def create_similarity_heatmap_data(self, field_analyses: List[Dict]) -> Dict[str, Any]:
        """Create data structure for similarity heatmap visualization."""
        heatmap_data = []
        
        for analysis in field_analyses:
            field_name = analysis['field_pair'].split(' <-> ')[0]
            
            heatmap_data.append({
                'field': field_name,
                'exact_match': analysis['average_similarity']['exact_match'],
                'sequence_match': analysis['average_similarity']['sequence_match'],
                'jaccard': analysis['average_similarity']['jaccard'],
                'length_ratio': analysis['average_similarity']['length_ratio'],
                'overall_score': analysis['overall_similarity_score'],
                'quality_score': analysis['quality_assessment']['overall_quality_score'],
                'recommendation': analysis['quality_assessment']['recommendation']
            })
        
        # Sort by overall similarity score
        heatmap_data.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return {
            'heatmap_data': heatmap_data,
            'metrics_explanation': {
                'exact_match': 'Percentage of records with identical values',
                'sequence_match': 'Average text sequence similarity (0-1)',
                'jaccard': 'Average word-based Jaccard similarity (0-1)',
                'length_ratio': 'Average length ratio similarity (0-1)',
                'overall_score': 'Weighted combination of all metrics',
                'quality_score': 'Data quality and consistency assessment'
            }
        }
    
    def generate_improvement_recommendations(self, field_analyses: List[Dict]) -> List[Dict[str, Any]]:
        """Generate specific recommendations for improving data consistency."""
        recommendations = []
        
        for analysis in field_analyses:
            field_name = analysis['field_pair'].split(' <-> ')[0]
            quality = analysis['quality_assessment']
            distribution = analysis['distribution']
            
            # High-priority recommendations
            if quality['overall_quality_score'] < 0.5:
                recommendations.append({
                    'priority': 'HIGH',
                    'field': field_name,
                    'issue': 'Low overall quality score',
                    'action': quality['recommendation'],
                    'details': f"Only {quality['completeness_score']:.1%} completeness, {quality['consistency_score']:.1%} consistency"
                })
            
            # Medium-priority recommendations
            elif distribution['different'] > distribution['identical']:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'field': field_name,
                    'issue': 'More differences than similarities',
                    'action': 'Review and standardize data entry processes',
                    'details': f"{distribution['different']} different vs {distribution['identical']} identical"
                })
            
            # Data completeness recommendations
            if distribution['csv_only'] > 0 or distribution['yaml_only'] > 0:
                missing_source = 'YAML' if distribution['csv_only'] > distribution['yaml_only'] else 'CSV'
                recommendations.append({
                    'priority': 'LOW',
                    'field': field_name,
                    'issue': f'Missing data in {missing_source} source',
                    'action': f'Backfill {missing_source} data where possible',
                    'details': f"CSV only: {distribution['csv_only']}, YAML only: {distribution['yaml_only']}"
                })
        
        # Sort by priority
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        recommendations.sort(key=lambda x: priority_order[x['priority']])
        
        return recommendations

def main():
    """Main function to perform comprehensive similarity analysis."""
    logger.info("Starting comprehensive column similarity analysis...")
    
    # Initialize analyzer
    analyzer = SimilarityAnalyzer()
    
    # Get data from database
    conn = sqlite3.connect('hdm_papers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all records with both CSV and YAML columns
    all_columns = list(analyzer.field_mappings.keys()) + list(analyzer.field_mappings.values()) + ['cite_key']
    query = f"SELECT {', '.join(all_columns)} FROM papers"
    
    cursor.execute(query)
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    logger.info(f"Analyzing {len(records)} records across {len(analyzer.field_mappings)} field pairs")
    
    # Analyze each field pair
    field_analyses = []
    for csv_field, yaml_field in analyzer.field_mappings.items():
        analysis = analyzer.analyze_field_similarity(records, csv_field, yaml_field)
        field_analyses.append(analysis)
    
    # Create heatmap visualization data
    heatmap_data = analyzer.create_similarity_heatmap_data(field_analyses)
    
    # Generate improvement recommendations
    recommendations = analyzer.generate_improvement_recommendations(field_analyses)
    
    # Create comprehensive report
    similarity_report = {
        'analysis_timestamp': datetime.now().isoformat(),
        'total_records_analyzed': len(records),
        'total_field_pairs': len(analyzer.field_mappings),
        'field_analyses': field_analyses,
        'heatmap_visualization': heatmap_data,
        'improvement_recommendations': recommendations,
        'summary_statistics': {
            'best_performing_fields': [
                analysis['field_pair'] for analysis in 
                sorted(field_analyses, key=lambda x: x['overall_similarity_score'], reverse=True)[:5]
            ],
            'worst_performing_fields': [
                analysis['field_pair'] for analysis in 
                sorted(field_analyses, key=lambda x: x['overall_similarity_score'])[:5]
            ],
            'average_overall_similarity': sum(a['overall_similarity_score'] for a in field_analyses) / len(field_analyses),
            'high_priority_issues': len([r for r in recommendations if r['priority'] == 'HIGH'])
        }
    }
    
    # Save report
    with open('column_similarity_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(similarity_report, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info("Similarity analysis report saved to column_similarity_analysis_report.json")
    
    # Print executive summary
    print("\n" + "="*80)
    print("COLUMN SIMILARITY ANALYSIS - EXECUTIVE SUMMARY")
    print("="*80)
    
    stats = similarity_report['summary_statistics']
    print(f"📊 Records Analyzed: {len(records)}")
    print(f"🔍 Field Pairs Compared: {len(analyzer.field_mappings)}")
    print(f"📈 Average Similarity Score: {stats['average_overall_similarity']:.2f}")
    print(f"⚠️  High Priority Issues: {stats['high_priority_issues']}")
    
    print(f"\n🏆 BEST PERFORMING FIELDS:")
    for field in stats['best_performing_fields']:
        score = next(a['overall_similarity_score'] for a in field_analyses if a['field_pair'] == field)
        print(f"   • {field}: {score:.2f}")
    
    print(f"\n⚠️  WORST PERFORMING FIELDS:")
    for field in stats['worst_performing_fields']:
        score = next(a['overall_similarity_score'] for a in field_analyses if a['field_pair'] == field)
        print(f"   • {field}: {score:.2f}")
    
    print(f"\n🎯 TOP RECOMMENDATIONS:")
    for rec in recommendations[:5]:
        print(f"   {rec['priority']}: {rec['field']} - {rec['action']}")
    
    # Create visualization summary
    print(f"\n📊 SIMILARITY HEATMAP SUMMARY:")
    print("   Field                    | Exact | Sequence | Jaccard | Overall | Quality")
    print("   " + "-" * 70)
    
    for item in heatmap_data['heatmap_data'][:10]:
        print(f"   {item['field']:<24} | {item['exact_match']:.2f}  | {item['sequence_match']:.2f}     | {item['jaccard']:.2f}    | {item['overall_score']:.2f}    | {item['quality_score']:.2f}")
    
    print("="*80)
    
    return similarity_report

if __name__ == "__main__":
    main()
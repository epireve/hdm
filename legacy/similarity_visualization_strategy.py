#!/usr/bin/env python3
"""
Visualization strategy for column similarity analysis using text-based charts and HTML output.
"""

import json
import sqlite3
from typing import Dict, Any, List
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimilarityVisualizationStrategy:
    """Create various visualizations for similarity analysis."""
    
    def __init__(self, report_file: str = 'column_similarity_analysis_report.json'):
        """Initialize with similarity report data."""
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                self.report = json.load(f)
            logger.info(f"Loaded similarity report from {report_file}")
        except FileNotFoundError:
            logger.error(f"Report file {report_file} not found. Run column_similarity_analysis.py first.")
            raise
    
    def create_ascii_heatmap(self) -> str:
        """Create ASCII-based heatmap of similarity scores."""
        heatmap_data = self.report['heatmap_visualization']['heatmap_data']
        
        # Create ASCII heatmap
        output = ["", "📊 SIMILARITY HEATMAP (ASCII)", "=" * 80]
        
        # Header
        header = f"{'Field':<25} | {'Exact':<5} | {'Seq':<5} | {'Jacc':<5} | {'Len':<5} | {'Overall':<7} | {'Quality':<7} | {'Recommendation'}"
        output.append(header)
        output.append("-" * len(header))
        
        # Data rows with color coding
        for item in heatmap_data:
            # Create visual indicators
            exact_bar = self._create_bar(item['exact_match'], 5)
            seq_bar = self._create_bar(item['sequence_match'], 5)
            jacc_bar = self._create_bar(item['jaccard'], 5)
            len_bar = self._create_bar(item['length_ratio'], 5)
            overall_bar = self._create_bar(item['overall_score'], 7)
            quality_bar = self._create_bar(item['quality_score'], 7)
            
            # Truncate recommendation
            rec = item['recommendation'].split(' - ')[0][:12]
            
            row = f"{item['field']:<25} | {exact_bar} | {seq_bar} | {jacc_bar} | {len_bar} | {overall_bar} | {quality_bar} | {rec}"
            output.append(row)
        
        output.extend(["", "Legend: █ = High (>0.8), ▓ = Medium (0.4-0.8), ░ = Low (<0.4), · = None", ""])
        return "\n".join(output)
    
    def _create_bar(self, value: float, width: int) -> str:
        """Create ASCII bar representation of a value."""
        if value >= 0.8:
            return "█" * width
        elif value >= 0.6:
            return "▓" * width
        elif value >= 0.4:
            return "░" * width
        elif value > 0.0:
            return "·" * width
        else:
            return " " * width
    
    def create_distribution_chart(self) -> str:
        """Create ASCII distribution chart."""
        output = ["", "📈 DATA DISTRIBUTION ANALYSIS", "=" * 60]
        
        for analysis in self.report['field_analyses'][:10]:  # Top 10 fields
            field = analysis['field_pair'].split(' <-> ')[0]
            dist = analysis['distribution']
            total = analysis['total_records']
            
            output.append(f"\n{field}:")
            
            # Calculate percentages
            both_present_pct = (dist['both_present'] / total) * 100
            csv_only_pct = (dist['csv_only'] / total) * 100
            yaml_only_pct = (dist['yaml_only'] / total) * 100
            both_empty_pct = (dist['both_empty'] / total) * 100
            
            # Create bar charts
            output.append(f"  Both Present: {self._create_percentage_bar(both_present_pct, 30)} {both_present_pct:.1f}%")
            output.append(f"  CSV Only:     {self._create_percentage_bar(csv_only_pct, 30)} {csv_only_pct:.1f}%")
            output.append(f"  YAML Only:    {self._create_percentage_bar(yaml_only_pct, 30)} {yaml_only_pct:.1f}%")
            output.append(f"  Both Empty:   {self._create_percentage_bar(both_empty_pct, 30)} {both_empty_pct:.1f}%")
        
        return "\n".join(output)
    
    def _create_percentage_bar(self, percentage: float, width: int) -> str:
        """Create percentage bar."""
        filled = int((percentage / 100) * width)
        return "█" * filled + "░" * (width - filled)
    
    def create_quality_matrix(self) -> str:
        """Create quality assessment matrix."""
        output = ["", "🎯 QUALITY ASSESSMENT MATRIX", "=" * 70]
        
        # Group by quality scores
        excellent = []
        good = []
        needs_review = []
        
        for analysis in self.report['field_analyses']:
            field = analysis['field_pair'].split(' <-> ')[0]
            quality_score = analysis['quality_assessment']['overall_quality_score']
            recommendation = analysis['quality_assessment']['recommendation']
            
            if quality_score >= 0.8:
                excellent.append((field, quality_score, recommendation))
            elif quality_score >= 0.6:
                good.append((field, quality_score, recommendation))
            else:
                needs_review.append((field, quality_score, recommendation))
        
        output.append(f"\n✅ EXCELLENT QUALITY ({len(excellent)} fields):")
        for field, score, rec in excellent[:5]:
            output.append(f"   {field:<25} | {score:.2f} | {rec}")
        
        output.append(f"\n⚠️  GOOD QUALITY ({len(good)} fields):")
        for field, score, rec in good[:5]:
            output.append(f"   {field:<25} | {score:.2f} | {rec}")
        
        output.append(f"\n🔥 NEEDS REVIEW ({len(needs_review)} fields):")
        for field, score, rec in needs_review:
            output.append(f"   {field:<25} | {score:.2f} | {rec}")
        
        return "\n".join(output)
    
    def create_trend_analysis(self) -> str:
        """Analyze trends in similarity patterns."""
        output = ["", "📊 SIMILARITY TREND ANALYSIS", "=" * 60]
        
        # Analyze by field type
        metadata_fields = ['title', 'authors', 'year', 'doi', 'url']
        content_fields = ['summary', 'insights', 'tldr', 'methodology', 'key_findings']
        assessment_fields = ['relevancy', 'relevancy_justification', 'downloaded', 'tags']
        
        categories = {
            'Metadata Fields': metadata_fields,
            'Content Fields': content_fields,
            'Assessment Fields': assessment_fields
        }
        
        for category, fields in categories.items():
            scores = []
            for analysis in self.report['field_analyses']:
                field = analysis['field_pair'].split(' <-> ')[0]
                if field in fields:
                    scores.append(analysis['overall_similarity_score'])
            
            if scores:
                avg_score = sum(scores) / len(scores)
                output.append(f"\n{category}:")
                output.append(f"   Average Similarity: {avg_score:.2f}")
                output.append(f"   Range: {min(scores):.2f} - {max(scores):.2f}")
                output.append(f"   Fields Analyzed: {len(scores)}")
                output.append(f"   Trend: {self._get_trend_description(avg_score)}")
        
        return "\n".join(output)
    
    def _get_trend_description(self, score: float) -> str:
        """Get trend description based on score."""
        if score >= 0.9:
            return "Excellent consistency ✅"
        elif score >= 0.8:
            return "Good consistency ⚠️"
        elif score >= 0.7:
            return "Moderate consistency 🔶"
        else:
            return "Poor consistency ❌"
    
    def create_actionable_insights(self) -> str:
        """Create actionable insights from the analysis."""
        output = ["", "💡 ACTIONABLE INSIGHTS & STRATEGY", "=" * 60]
        
        recommendations = self.report['improvement_recommendations']
        
        # High priority actions
        high_priority = [r for r in recommendations if r['priority'] == 'HIGH']
        if high_priority:
            output.append(f"\n🚨 IMMEDIATE ACTIONS REQUIRED ({len(high_priority)} items):")
            for rec in high_priority:
                output.append(f"   • {rec['field']}: {rec['action']}")
                output.append(f"     Issue: {rec['issue']}")
                output.append(f"     Details: {rec['details']}")
        
        # Strategic recommendations
        output.append(f"\n🎯 STRATEGIC RECOMMENDATIONS:")
        
        # Data source preference analysis
        yaml_preferred = sum(1 for a in self.report['field_analyses'] 
                           if 'YAML' in a['quality_assessment']['recommendation'])
        csv_preferred = sum(1 for a in self.report['field_analyses'] 
                          if 'CSV' in a['quality_assessment']['recommendation'])
        
        output.append(f"   • CSV Source Preference: {csv_preferred} fields")
        output.append(f"   • YAML Source Preference: {yaml_preferred} fields")
        output.append(f"   • Overall Strategy: {'Focus on CSV data quality' if csv_preferred > yaml_preferred else 'Balance both sources'}")
        
        # Data completeness strategy
        total_missing = sum(a['distribution']['csv_only'] + a['distribution']['yaml_only'] 
                          for a in self.report['field_analyses'])
        output.append(f"   • Missing Data Points: {total_missing} across all fields")
        output.append(f"   • Completeness Priority: Focus on backfilling missing values")
        
        return "\n".join(output)
    
    def create_html_report(self) -> str:
        """Create comprehensive HTML report."""
        html_template = """<!DOCTYPE html>
        <html>
        <head>
            <title>Column Similarity Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
                .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
                .metric-card {{ background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff; }}
                .metric-value {{ font-size: 2em; font-weight: bold; color: #007bff; }}
                .metric-label {{ color: #666; text-transform: uppercase; font-size: 0.9em; }}
                .heatmap-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .heatmap-table th, .heatmap-table td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                .heatmap-table th {{ background-color: #f2f2f2; }}
                .score-excellent {{ background-color: #d4edda; color: #155724; }}
                .score-good {{ background-color: #fff3cd; color: #856404; }}
                .score-poor {{ background-color: #f8d7da; color: #721c24; }}
                .recommendation {{ padding: 10px; margin: 10px 0; border-radius: 4px; }}
                .rec-high {{ background-color: #f8d7da; border-left: 4px solid #dc3545; }}
                .rec-medium {{ background-color: #fff3cd; border-left: 4px solid #ffc107; }}
                .rec-low {{ background-color: #d4edda; border-left: 4px solid #28a745; }}
                .progress-bar {{ width: 100%; height: 20px; background-color: #e9ecef; border-radius: 10px; overflow: hidden; }}
                .progress-fill {{ height: 100%; background-color: #007bff; transition: width 0.3s ease; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Column Similarity Analysis Report</h1>
                    <p>Generated on {timestamp}</p>
                </div>
                
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-value">{total_records}</div>
                        <div class="metric-label">Records Analyzed</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{field_pairs}</div>
                        <div class="metric-label">Field Pairs</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{avg_similarity:.2f}</div>
                        <div class="metric-label">Avg Similarity</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{high_priority}</div>
                        <div class="metric-label">High Priority Issues</div>
                    </div>
                </div>
                
                <h2>Similarity Heatmap</h2>
                <table class="heatmap-table">
                    <thead>
                        <tr>
                            <th>Field</th>
                            <th>Exact Match</th>
                            <th>Sequence Match</th>
                            <th>Jaccard Score</th>
                            <th>Overall Score</th>
                            <th>Quality Score</th>
                            <th>Recommendation</th>
                        </tr>
                    </thead>
                    <tbody>
                        {heatmap_rows}
                    </tbody>
                </table>
                
                <h2>Recommendations</h2>
                {recommendations_html}
                
                <h2>Detailed Analysis</h2>
                <p>This analysis compared {total_records} records across {field_pairs} field pairs to assess data consistency between original CSV columns and enhanced YAML frontmatter columns.</p>
                
                <h3>Key Findings:</h3>
                <ul>
                    <li>Average similarity score: {avg_similarity:.2f}</li>
                    <li>Best performing fields show perfect consistency</li>
                    <li>Areas needing attention identified for data quality improvement</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        # Prepare data for HTML template
        heatmap_data = self.report['heatmap_visualization']['heatmap_data']
        
        # Create heatmap rows
        heatmap_rows = ""
        for item in heatmap_data:
            score_class = self._get_score_class(item['overall_score'])
            heatmap_rows += f"""
                <tr class="{score_class}">
                    <td>{item['field']}</td>
                    <td>{item['exact_match']:.2f}</td>
                    <td>{item['sequence_match']:.2f}</td>
                    <td>{item['jaccard']:.2f}</td>
                    <td>{item['overall_score']:.2f}</td>
                    <td>{item['quality_score']:.2f}</td>
                    <td>{item['recommendation']}</td>
                </tr>
            """
        
        # Create recommendations HTML
        recommendations_html = ""
        for rec in self.report['improvement_recommendations'][:10]:
            rec_class = f"rec-{rec['priority'].lower()}"
            recommendations_html += f"""
                <div class="recommendation {rec_class}">
                    <strong>{rec['priority']} Priority:</strong> {rec['field']}<br>
                    <strong>Issue:</strong> {rec['issue']}<br>
                    <strong>Action:</strong> {rec['action']}<br>
                    <strong>Details:</strong> {rec['details']}
                </div>
            """
        
        # Fill template
        html_content = html_template.format(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_records=self.report['total_records_analyzed'],
            field_pairs=self.report['total_field_pairs'],
            avg_similarity=self.report['summary_statistics']['average_overall_similarity'],
            high_priority=self.report['summary_statistics']['high_priority_issues'],
            heatmap_rows=heatmap_rows,
            recommendations_html=recommendations_html
        )
        
        return html_content
    
    def _get_score_class(self, score: float) -> str:
        """Get CSS class based on score."""
        if score >= 0.8:
            return "score-excellent"
        elif score >= 0.6:
            return "score-good"
        else:
            return "score-poor"
    
    def generate_all_visualizations(self):
        """Generate all visualization outputs."""
        logger.info("Generating comprehensive similarity visualizations...")
        
        # Create text-based visualizations
        ascii_heatmap = self.create_ascii_heatmap()
        distribution_chart = self.create_distribution_chart()
        quality_matrix = self.create_quality_matrix()
        trend_analysis = self.create_trend_analysis()
        actionable_insights = self.create_actionable_insights()
        
        # Combine all text visualizations
        full_report = "\n".join([
            ascii_heatmap,
            distribution_chart,
            quality_matrix,
            trend_analysis,
            actionable_insights
        ])
        
        # Save text report
        with open('similarity_visualization_report.txt', 'w', encoding='utf-8') as f:
            f.write(full_report)
        
        # Create and save HTML report
        html_report = self.create_html_report()
        with open('similarity_analysis_report.html', 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        # Print the text visualizations
        print(full_report)
        
        logger.info("Visualizations saved to:")
        logger.info("  - similarity_visualization_report.txt (text-based charts)")
        logger.info("  - similarity_analysis_report.html (interactive HTML report)")
        
        return {
            'text_report': full_report,
            'html_report': html_report,
            'files_created': [
                'similarity_visualization_report.txt',
                'similarity_analysis_report.html'
            ]
        }

def main():
    """Main function to generate all visualizations."""
    try:
        visualizer = SimilarityVisualizationStrategy()
        results = visualizer.generate_all_visualizations()
        
        print(f"\n🎉 Visualization generation completed!")
        print(f"📄 Files created: {', '.join(results['files_created'])}")
        
        return results
    
    except Exception as e:
        logger.error(f"Error generating visualizations: {e}")
        raise

if __name__ == "__main__":
    main()
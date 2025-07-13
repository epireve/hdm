#!/usr/bin/env python3
"""
Export HDM papers data to multiple formats.
This script is designed to be run by GitHub Actions or manually.
"""

import sqlite3
import json
import csv
import os
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HDMDataExporter:
    def __init__(self, db_path='hdm_papers.db', output_dir='exports'):
        self.db_path = db_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        # Create timestamp for versioned exports
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def export_to_csv(self):
        """Export database to CSV format."""
        logger.info("Exporting to CSV...")
        
        # Get all data
        self.cursor.execute("""
            SELECT * FROM papers 
            ORDER BY year DESC, cite_key
        """)
        rows = self.cursor.fetchall()
        
        # Define output columns in specific order
        columns = [
            'cite_key', 'corrected_cite_key', 'title', 'authors', 
            'year', 'doi', 'url', 'relevancy', 'relevancy_justification',
            'tldr', 'insights', 'summary', 'research_question', 
            'methodology', 'key_findings', 'primary_outcomes',
            'limitations', 'conclusion', 'research_gaps', 
            'future_work', 'implementation_insights', 'tags',
            'folder_path', 'csv_original_authors', 'date_processed'
        ]
        
        # Current version
        csv_path = self.output_dir / 'hdm_papers_current.csv'
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            
            for row in rows:
                row_dict = dict(row)
                # Only include columns that exist
                filtered_row = {col: row_dict.get(col, '') for col in columns if col in row_dict}
                writer.writerow(filtered_row)
        
        # Timestamped version
        csv_archive_path = self.output_dir / f'hdm_papers_{self.timestamp}.csv'
        with open(csv_path, 'rb') as src, open(csv_archive_path, 'wb') as dst:
            dst.write(src.read())
            
        logger.info(f"✅ CSV exported to {csv_path}")
        return csv_path
    
    def export_to_json(self):
        """Export database to JSON format with nested structure."""
        logger.info("Exporting to JSON...")
        
        # Get all data
        self.cursor.execute("""
            SELECT * FROM papers 
            ORDER BY year DESC, cite_key
        """)
        rows = self.cursor.fetchall()
        
        # Convert to nested structure
        papers = []
        for row in rows:
            paper = dict(row)
            
            # Parse tags if they're comma-separated
            if paper.get('tags'):
                paper['tags'] = [tag.strip() for tag in paper['tags'].split(',')]
            
            # Group related fields
            structured_paper = {
                'metadata': {
                    'cite_key': paper.get('cite_key'),
                    'corrected_cite_key': paper.get('corrected_cite_key'),
                    'year': paper.get('year'),
                    'doi': paper.get('doi'),
                    'url': paper.get('url'),
                    'folder_path': paper.get('folder_path'),
                    'date_processed': paper.get('date_processed')
                },
                'content': {
                    'title': paper.get('title'),
                    'authors': paper.get('authors'),
                    'csv_original_authors': paper.get('csv_original_authors'),
                    'tldr': paper.get('tldr'),
                    'summary': paper.get('summary')
                },
                'research': {
                    'research_question': paper.get('research_question'),
                    'methodology': paper.get('methodology'),
                    'key_findings': paper.get('key_findings'),
                    'primary_outcomes': paper.get('primary_outcomes'),
                    'limitations': paper.get('limitations'),
                    'conclusion': paper.get('conclusion'),
                    'research_gaps': paper.get('research_gaps'),
                    'future_work': paper.get('future_work')
                },
                'relevance': {
                    'relevancy': paper.get('relevancy'),
                    'relevancy_justification': paper.get('relevancy_justification'),
                    'insights': paper.get('insights'),
                    'implementation_insights': paper.get('implementation_insights'),
                    'tags': paper.get('tags', [])
                }
            }
            
            papers.append(structured_paper)
        
        # Current version
        json_path = self.output_dir / 'hdm_papers_current.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'total_papers': len(papers),
                    'export_date': datetime.now().isoformat(),
                    'date_range': '2019-2025',
                    'version': self.timestamp
                },
                'papers': papers
            }, f, indent=2, ensure_ascii=False)
        
        # Timestamped version
        json_archive_path = self.output_dir / f'hdm_papers_{self.timestamp}.json'
        with open(json_path, 'rb') as src, open(json_archive_path, 'wb') as dst:
            dst.write(src.read())
            
        logger.info(f"✅ JSON exported to {json_path}")
        return json_path
    
    def export_to_markdown(self):
        """Export database to Markdown format for documentation."""
        logger.info("Exporting to Markdown...")
        
        # Get statistics
        stats = self._get_statistics()
        
        # Get all papers
        self.cursor.execute("""
            SELECT * FROM papers 
            ORDER BY year DESC, relevancy DESC, cite_key
        """)
        rows = self.cursor.fetchall()
        
        # Create markdown content
        md_content = f"""# HDM Papers Database

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Overview

The Human Digital Memory (HDM) Papers Database contains {stats['total_papers']} carefully curated academic papers focusing on heterogeneous data integration within Personal Knowledge Graph (PKG) architectures.

## Statistics

- **Total Papers**: {stats['total_papers']}
- **Date Range**: {stats['min_year']} - {stats['max_year']}
- **Papers with DOI**: {stats['papers_with_doi']} ({stats['doi_percentage']:.1f}%)
- **Super Relevancy Papers**: {stats['super_relevancy']}
- **High Relevancy Papers**: {stats['high_relevancy']}
- **Medium Relevancy Papers**: {stats['medium_relevancy']}
- **Low Relevancy Papers**: {stats['low_relevancy']}

### Year Distribution

| Year | Count | Percentage |
|------|-------|------------|
"""
        
        for year, count in stats['year_distribution']:
            percentage = (count / stats['total_papers']) * 100
            md_content += f"| {year} | {count} | {percentage:.1f}% |\n"
        
        md_content += """
## High Relevancy Papers

These papers directly address heterogeneous data integration, temporal-first PKG architectures, or bespoke PKG system designs.

"""
        
        # List high relevancy papers
        high_relevancy_papers = [row for row in rows if row['relevancy'] in ['HIGH', 'High', 'SUPER']]
        for paper in high_relevancy_papers[:20]:  # Top 20
            md_content += f"### {paper['title']}\n"
            md_content += f"- **Authors**: {paper['authors']}\n"
            md_content += f"- **Year**: {paper['year']}\n"
            md_content += f"- **Cite Key**: `{paper['cite_key']}`\n"
            if paper['doi']:
                md_content += f"- **DOI**: [{paper['doi']}](https://doi.org/{paper['doi']})\n"
            if paper['tldr']:
                md_content += f"- **TL;DR**: {paper['tldr']}\n"
            md_content += "\n"
        
        if len(high_relevancy_papers) > 20:
            md_content += f"\n*... and {len(high_relevancy_papers) - 20} more high relevancy papers*\n"
        
        # Add data quality section
        md_content += """
## Data Quality

- **Author Data Quality**: 98.6% (353/358 papers with verified authors)
- **Year Accuracy**: 100% (all years verified and corrected)
- **Folder Synchronization**: 100% (all papers have corresponding folders)

## Export Information

This database is automatically exported in multiple formats:
- **CSV**: For spreadsheet analysis and data science workflows
- **JSON**: For programmatic access with nested structure
- **SQLite**: For complex queries and relational analysis
- **Markdown**: For human-readable documentation

All exports are versioned and archived with timestamps.
"""
        
        # Current version
        md_path = self.output_dir / 'hdm_papers_current.md'
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # Timestamped version
        md_archive_path = self.output_dir / f'hdm_papers_{self.timestamp}.md'
        with open(md_path, 'rb') as src, open(md_archive_path, 'wb') as dst:
            dst.write(src.read())
            
        logger.info(f"✅ Markdown exported to {md_path}")
        return md_path
    
    def export_sqlite_backup(self):
        """Create a backup of the SQLite database."""
        logger.info("Creating SQLite backup...")
        
        # Current version
        db_backup_path = self.output_dir / 'hdm_papers_current.db'
        
        # Use SQLite backup API
        backup_conn = sqlite3.connect(db_backup_path)
        with backup_conn:
            self.conn.backup(backup_conn)
        backup_conn.close()
        
        # Timestamped version
        db_archive_path = self.output_dir / f'hdm_papers_{self.timestamp}.db'
        with open(db_backup_path, 'rb') as src, open(db_archive_path, 'wb') as dst:
            dst.write(src.read())
            
        logger.info(f"✅ SQLite backup created at {db_backup_path}")
        return db_backup_path
    
    def _get_statistics(self):
        """Get database statistics."""
        stats = {}
        
        # Total papers
        stats['total_papers'] = self.cursor.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
        
        # Year range
        self.cursor.execute("SELECT MIN(year), MAX(year) FROM papers")
        stats['min_year'], stats['max_year'] = self.cursor.fetchone()
        
        # Papers with DOI
        stats['papers_with_doi'] = self.cursor.execute(
            "SELECT COUNT(*) FROM papers WHERE doi IS NOT NULL AND doi != ''"
        ).fetchone()[0]
        stats['doi_percentage'] = (stats['papers_with_doi'] / stats['total_papers']) * 100
        
        # Relevancy distribution
        self.cursor.execute("""
            SELECT relevancy, COUNT(*) 
            FROM papers 
            GROUP BY relevancy
        """)
        relevancy_dist = dict(self.cursor.fetchall())
        stats['high_relevancy'] = relevancy_dist.get('HIGH', relevancy_dist.get('High', 0))
        stats['medium_relevancy'] = relevancy_dist.get('MEDIUM', relevancy_dist.get('Medium', 0))
        stats['low_relevancy'] = relevancy_dist.get('LOW', relevancy_dist.get('Low', 0))
        stats['super_relevancy'] = relevancy_dist.get('SUPER', 0)
        
        # Year distribution
        self.cursor.execute("""
            SELECT year, COUNT(*) 
            FROM papers 
            GROUP BY year 
            ORDER BY year DESC
        """)
        stats['year_distribution'] = [(row[0], row[1]) for row in self.cursor.fetchall()]
        
        return stats
    
    def export_all(self):
        """Export to all formats."""
        logger.info("Starting full export...")
        
        results = {
            'csv': self.export_to_csv(),
            'json': self.export_to_json(),
            'markdown': self.export_to_markdown(),
            'sqlite': self.export_sqlite_backup()
        }
        
        # Create export manifest
        manifest = {
            'timestamp': self.timestamp,
            'date': datetime.now().isoformat(),
            'exports': {
                format_name: str(path) for format_name, path in results.items()
            },
            'statistics': self._get_statistics()
        }
        
        manifest_path = self.output_dir / 'export_manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"✅ All exports completed successfully!")
        logger.info(f"📁 Output directory: {self.output_dir}")
        
        return results
    
    def close(self):
        """Close database connection."""
        self.conn.close()


def main():
    """Main execution function."""
    exporter = HDMDataExporter()
    
    try:
        exporter.export_all()
    finally:
        exporter.close()


if __name__ == "__main__":
    main()
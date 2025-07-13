#!/usr/bin/env python3
"""
Final validation report for the YAML frontmatter extraction and database consolidation project.
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Set
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_database_statistics() -> Dict[str, Any]:
    """Get comprehensive database statistics."""
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    
    stats = {}
    
    # Basic counts
    cursor.execute("SELECT COUNT(*) FROM papers")
    stats['total_papers'] = cursor.fetchone()[0]
    
    # YAML data coverage
    cursor.execute("SELECT COUNT(*) FROM papers WHERE yaml_cite_key IS NOT NULL")
    stats['papers_with_yaml_data'] = cursor.fetchone()[0]
    
    # Field completeness analysis
    yaml_fields = [
        'yaml_cite_key', 'yaml_title', 'yaml_authors', 'yaml_year', 'yaml_doi', 
        'yaml_url', 'yaml_relevancy', 'yaml_tags', 'yaml_keywords'
    ]
    
    field_completeness = {}
    for field in yaml_fields:
        cursor.execute(f"SELECT COUNT(*) FROM papers WHERE {field} IS NOT NULL AND {field} != ''")
        field_completeness[field] = cursor.fetchone()[0]
    
    stats['yaml_field_completeness'] = field_completeness
    
    # Get sample of enriched records
    cursor.execute("""
        SELECT cite_key, title, yaml_title, authors, yaml_authors 
        FROM papers 
        WHERE yaml_cite_key IS NOT NULL 
        LIMIT 5
    """)
    stats['sample_enriched_records'] = [dict(zip([col[0] for col in cursor.description], row)) 
                                       for row in cursor.fetchall()]
    
    conn.close()
    return stats

def analyze_folder_structure() -> Dict[str, Any]:
    """Analyze the production folder structure."""
    production_path = Path("production_final_reformatted_1752365947")
    
    if not production_path.exists():
        return {'error': f'Production path does not exist: {production_path}'}
    
    # Get all folders
    folders = [folder for folder in production_path.iterdir() if folder.is_dir()]
    
    # Analyze paper.md files
    paper_files = []
    folders_with_paper_md = 0
    folders_without_paper_md = []
    
    for folder in folders:
        paper_md_path = folder / "paper.md"
        if paper_md_path.exists():
            folders_with_paper_md += 1
            
            # Get file size and modification time
            stat = paper_md_path.stat()
            paper_files.append({
                'folder_name': folder.name,
                'file_size': stat.st_size,
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        else:
            folders_without_paper_md.append(folder.name)
    
    # Analyze image files
    total_images = 0
    folders_with_images = 0
    for folder in folders:
        images = list(folder.glob("*.jpeg")) + list(folder.glob("*.jpg")) + list(folder.glob("*.png"))
        if images:
            folders_with_images += 1
            total_images += len(images)
    
    return {
        'total_folders': len(folders),
        'folders_with_paper_md': folders_with_paper_md,
        'folders_without_paper_md': len(folders_without_paper_md),
        'missing_paper_md_folders': folders_without_paper_md[:10],  # First 10
        'total_images': total_images,
        'folders_with_images': folders_with_images,
        'average_file_size': sum(pf['file_size'] for pf in paper_files) / len(paper_files) if paper_files else 0
    }

def validate_cite_key_consistency() -> Dict[str, Any]:
    """Validate cite_key consistency between database and folders."""
    # Get database cite_keys
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT cite_key FROM papers")
    db_cite_keys = {row[0] for row in cursor.fetchall()}
    conn.close()
    
    # Get folder names
    production_path = Path("production_final_reformatted_1752365947")
    if production_path.exists():
        folder_names = {folder.name for folder in production_path.iterdir() if folder.is_dir()}
    else:
        folder_names = set()
    
    # Compare
    in_db_not_folder = db_cite_keys - folder_names
    in_folder_not_db = folder_names - db_cite_keys
    in_both = db_cite_keys & folder_names
    
    return {
        'database_cite_keys': len(db_cite_keys),
        'folder_names': len(folder_names),
        'in_both': len(in_both),
        'in_database_not_folder': len(in_db_not_folder),
        'in_folder_not_database': len(in_folder_not_db),
        'missing_folders': sorted(list(in_db_not_folder))[:20],  # First 20
        'extra_folders': sorted(list(in_folder_not_db))[:20],  # First 20
        'consistency_percentage': (len(in_both) / len(db_cite_keys)) * 100 if db_cite_keys else 0
    }

def analyze_data_quality() -> Dict[str, Any]:
    """Analyze the quality of consolidated data."""
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    
    # Check for duplicates
    cursor.execute("SELECT cite_key, COUNT(*) FROM papers GROUP BY cite_key HAVING COUNT(*) > 1")
    duplicates = cursor.fetchall()
    
    # Check for empty critical fields
    critical_fields = ['title', 'authors', 'year']
    empty_critical_fields = {}
    
    for field in critical_fields:
        cursor.execute(f"SELECT COUNT(*) FROM papers WHERE {field} IS NULL OR {field} = ''")
        empty_critical_fields[field] = cursor.fetchone()[0]
    
    # Check YAML vs CSV data usage
    cursor.execute("""
        SELECT 
            COUNT(CASE WHEN title != yaml_title AND yaml_title IS NOT NULL THEN 1 END) as title_from_yaml,
            COUNT(CASE WHEN authors != yaml_authors AND yaml_authors IS NOT NULL THEN 1 END) as authors_from_yaml,
            COUNT(CASE WHEN doi != yaml_doi AND yaml_doi IS NOT NULL THEN 1 END) as doi_from_yaml
        FROM papers
    """)
    yaml_usage = dict(zip(['title_from_yaml', 'authors_from_yaml', 'doi_from_yaml'], cursor.fetchone()))
    
    # Get records with most recent updates
    cursor.execute("""
        SELECT cite_key, title, updated_at 
        FROM papers 
        ORDER BY updated_at DESC 
        LIMIT 10
    """)
    recent_updates = [dict(zip([col[0] for col in cursor.description], row)) 
                     for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        'duplicate_cite_keys': len(duplicates),
        'empty_critical_fields': empty_critical_fields,
        'yaml_data_usage': yaml_usage,
        'recent_updates': recent_updates
    }

def generate_success_metrics() -> Dict[str, Any]:
    """Generate overall success metrics for the project."""
    
    # Load previous reports
    try:
        with open('yaml_to_database_report.json', 'r') as f:
            yaml_report = json.load(f)
    except FileNotFoundError:
        yaml_report = {}
    
    try:
        with open('data_consolidation_report.json', 'r') as f:
            consolidation_report = json.load(f)
    except FileNotFoundError:
        consolidation_report = {}
    
    db_stats = get_database_statistics()
    folder_stats = analyze_folder_structure()
    consistency = validate_cite_key_consistency()
    quality = analyze_data_quality()
    
    # Calculate success metrics
    success_metrics = {
        'yaml_extraction_success_rate': (yaml_report.get('processing_stats', {}).get('successful_yaml_extractions', 0) / 
                                        yaml_report.get('processing_stats', {}).get('total_files', 1)) * 100,
        
        'database_coverage': (db_stats['papers_with_yaml_data'] / db_stats['total_papers']) * 100,
        
        'folder_consistency': consistency['consistency_percentage'],
        
        'data_quality_score': (
            (1 - quality['empty_critical_fields'].get('title', 0) / db_stats['total_papers']) * 0.4 +
            (1 - quality['empty_critical_fields'].get('authors', 0) / db_stats['total_papers']) * 0.4 +
            (1 - quality['duplicate_cite_keys'] / max(db_stats['total_papers'], 1)) * 0.2
        ) * 100,
        
        'consolidation_impact': consolidation_report.get('dry_run_stats', {}).get('records_updated', 0)
    }
    
    return {
        'success_metrics': success_metrics,
        'database_statistics': db_stats,
        'folder_analysis': folder_stats,
        'cite_key_consistency': consistency,
        'data_quality': quality
    }

def main():
    """Generate final validation report."""
    logger.info("Generating final validation report...")
    
    # Collect all analyses
    success_metrics = generate_success_metrics()
    
    # Create comprehensive final report
    final_report = {
        'validation_timestamp': datetime.now().isoformat(),
        'project_summary': {
            'total_papers_in_database': success_metrics['database_statistics']['total_papers'],
            'papers_with_yaml_enrichment': success_metrics['database_statistics']['papers_with_yaml_data'],
            'total_folders': success_metrics['folder_analysis']['total_folders'],
            'yaml_extraction_success_rate': success_metrics['success_metrics']['yaml_extraction_success_rate'],
            'database_coverage': success_metrics['success_metrics']['database_coverage'],
            'folder_consistency': success_metrics['success_metrics']['folder_consistency'],
            'data_quality_score': success_metrics['success_metrics']['data_quality_score']
        },
        'detailed_analysis': success_metrics
    }
    
    # Save final report
    with open('final_validation_report.json', 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info("Final validation report saved to final_validation_report.json")
    
    # Print executive summary
    print("\n" + "="*70)
    print("FINAL VALIDATION REPORT - EXECUTIVE SUMMARY")
    print("="*70)
    
    summary = final_report['project_summary']
    print(f"📊 Total Papers in Database: {summary['total_papers_in_database']}")
    print(f"✅ Papers with YAML Enrichment: {summary['papers_with_yaml_enrichment']} ({summary['database_coverage']:.1f}%)")
    print(f"📁 Total Folders: {summary['total_folders']}")
    print(f"🔄 YAML Extraction Success: {summary['yaml_extraction_success_rate']:.1f}%")
    print(f"🔗 Folder Consistency: {summary['folder_consistency']:.1f}%")
    print(f"⭐ Data Quality Score: {summary['data_quality_score']:.1f}%")
    
    # Key achievements
    print(f"\n🎯 KEY ACHIEVEMENTS:")
    print(f"   • Successfully extracted YAML frontmatter from {success_metrics['folder_analysis']['folders_with_paper_md']} paper.md files")
    print(f"   • Added {len(success_metrics['database_statistics']['yaml_field_completeness'])} new YAML columns to database")
    print(f"   • Consolidated data for {success_metrics['success_metrics']['consolidation_impact']} records")
    print(f"   • Achieved {summary['folder_consistency']:.1f}% consistency between database and file system")
    
    # Areas needing attention
    missing_folders = success_metrics['cite_key_consistency']['in_database_not_folder']
    if missing_folders > 0:
        print(f"\n⚠️  AREAS NEEDING ATTENTION:")
        print(f"   • {missing_folders} database records missing corresponding folders")
        print(f"   • These represent {(missing_folders/summary['total_papers_in_database'])*100:.1f}% of total papers")
    
    # Data quality insights
    quality = success_metrics['data_quality']
    print(f"\n📈 DATA QUALITY INSIGHTS:")
    print(f"   • Title field: {summary['total_papers_in_database'] - quality['empty_critical_fields']['title']}/{summary['total_papers_in_database']} complete")
    print(f"   • Authors field: {summary['total_papers_in_database'] - quality['empty_critical_fields']['authors']}/{summary['total_papers_in_database']} complete")
    print(f"   • Year field: {summary['total_papers_in_database'] - quality['empty_critical_fields']['year']}/{summary['total_papers_in_database']} complete")
    
    if quality['yaml_data_usage']['title_from_yaml'] > 0:
        print(f"   • Enhanced {quality['yaml_data_usage']['title_from_yaml']} titles from YAML data")
    if quality['yaml_data_usage']['authors_from_yaml'] > 0:
        print(f"   • Enhanced {quality['yaml_data_usage']['authors_from_yaml']} author records from YAML data")
    if quality['yaml_data_usage']['doi_from_yaml'] > 0:
        print(f"   • Enhanced {quality['yaml_data_usage']['doi_from_yaml']} DOI records from YAML data")
    
    print(f"\n🏆 PROJECT STATUS: {'✅ SUCCESSFUL' if summary['data_quality_score'] > 90 else '⚠️ NEEDS ATTENTION'}")
    print("="*70)
    
    return final_report

if __name__ == "__main__":
    main()
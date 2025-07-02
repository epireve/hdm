#!/usr/bin/env python3
"""
HDM Project Spring Cleaning Script
Organizes and archives files while preserving important data
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

def create_archive_structure():
    """Create organized folder structure"""
    folders_to_create = [
        'archive/old_scripts',
        'archive/old_logs', 
        'archive/old_reports',
        'archive/old_csvs',
        'archive/old_checkpoints',
        'scripts/processing',
        'scripts/analysis',
        'scripts/utilities',
        'reports/current',
        'reports/archive'
    ]
    
    for folder in folders_to_create:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"Created: {folder}")

def move_processing_scripts():
    """Move processing and conversion scripts to organized folders"""
    processing_scripts = [
        # PDF/Markdown converters
        'pdf-markdown-converter.py',
        'batch_converter.py', 
        'converter_with_status.py',
        'one_by_one_converter.py',
        'reliable_converter.py',
        'robust_converter.py',
        'sequential_converter.py',
        'simple_converter.py',
        'smart_converter.py',
        'two-phase-converter.py',
        'convert_batch.sh',
        'batch_convert_pdfs.py',
        'convert_new_papers.py',
        'process_new_papers_batch.py',
        'run_batch_conversion.py',
        
        # Image processing
        'basic_image_descriptor.py',
        'batch_image_descriptor.py',
        'concurrent_image_descriptor.py',
        'concurrent_image_descriptor_fixed.py',
        'concurrent_image_descriptor_updated.py',
        'image_descriptor_with_comments.py',
        'multiprocess_image_descriptor.py',
        'simple_image_descriptor.py',
        'add_basic_image_descriptions.py',
        'describe_images_for_renamed_folders.py',
        'find_papers_needing_image_descriptions.py',
        'fix_image_description_format.py',
        'update_papers_needing_descriptions.py',
        'check_image_description_status.py',
        
        # CSV/Data processing
        'create_papers_csv.py',
        'create_clean_papers_csv.py',
        'generate_clean_csv.py',
        'regenerate_clean_csv.py',
        'compare_and_merge_csvs.py',
        'merge_csv_files.py',
        'csv_update_summary.py',
        
        # Cite key and folder management
        'fix_cite_keys.py',
        'fix_conflicting_cite_keys.py',
        'fix_conflicting_folders.py',
        'fix_specific_folders.py',
        'rename_folders_by_csv.py',
        'rename_folders_to_cite_keys.py',
        'rename_to_abc_format.py',
        'rename_base_to_a.py',
        'update_cite_keys_final.py',
        'update_csv_abc_format.py',
        'update_csv_with_new_citekeys.py',
        'generate_cite_keys_for_untouched.py',
        
        # Metadata fixes
        'fix_title_authors_format.py',
        'fix_title_authors_simple.py',
        'fix_uppercase_titles.py',
        'fix_yaml_issues.py',
        'fix_zha_2024_authors.py',
        'fix_author_extraction.py',
        'extract_full_authors.py',
        'update_missing_authors.py',
        'fix_missing_metadata.py',
        'fix_found_dois.py',
        'fix_remaining_issues.py',
        'validate_and_fix_yaml.py',
        'validate_metadata.py',
        
        # Duplicate handling
        'analyze_paper_duplicates.py',
        'handle_duplicates.py',
        'handle_similar_papers.py',
        'remove_duplicates.py',
        'remove_final_duplicates.py',
        'remove_remaining_duplicates.py',
        'verify_duplicates_thoroughly.py',
        'safe_delete_confirmed_duplicates.py',
        
        # Other utilities
        'monitor_conversion.py',
        'check_rename_results.py',
        'identify_problematic_files.py',
        'standardize_file_names.py',
        'delete_empty_folders.py',
        'extract_failed_pdfs.py',
        'process_untouched_folders.py',
        'analyze_untouched_folders.py',
        'update_keywords.py',
        'robust_keyword_updater.py',
        'show_status.py'
    ]
    
    for script in processing_scripts:
        if Path(script).exists():
            shutil.move(script, f'scripts/processing/{script}')
            print(f"Moved: {script} → scripts/processing/")

def move_analysis_scripts():
    """Move analysis and report generation scripts"""
    analysis_scripts = [
        'analyze_similar_and_incomplete.py',
        'analyze_doi_issues.py',
        'final_cleanup_summary.py',
        'final_processing_summary.py',
        'final_validation_report.py',
        'metadata_attention_summary.py',
        'sort_and_dedupe_papers.py',
        'create_final_research_csv.py',
        'update_research_papers_complete.py'
    ]
    
    for script in analysis_scripts:
        if Path(script).exists():
            shutil.move(script, f'scripts/analysis/{script}')
            print(f"Moved: {script} → scripts/analysis/")

def archive_old_logs():
    """Archive old log files"""
    log_patterns = [
        'batch_conversion.log',
        '*.log',
        'logs/*'
    ]
    
    # Move entire logs directory
    if Path('logs').exists():
        shutil.move('logs', 'archive/old_logs/logs')
        print("Moved: logs/ → archive/old_logs/")
    
    # Move individual log files
    for log_file in Path('.').glob('*.log'):
        if log_file.exists():
            shutil.move(str(log_file), f'archive/old_logs/{log_file.name}')
            print(f"Moved: {log_file} → archive/old_logs/")

def archive_old_reports():
    """Archive old report files"""
    report_files = [
        'duplicate_analysis_report.md',
        'duplicate_handling_report.txt',
        'duplicate_report.txt', 
        'duplicate_verification_report.md',
        'merge_summary_report.md',
        'metadata_update_report.md',
        'pdf_url_mapping_report.md',
        'clean_papers_report.txt',
        'doi_fixes_report.txt',
        'doi_issues_analysis.txt',
        'final_cleanup_summary.txt',
        'final_processing_summary.txt',
        'final_validation_report.md',
        'metadata_attention_summary.txt',
        'new_papers_conversion_summary.md',
        'paper_processing_summary.md',
        'complete_processing_summary.md',
        'file_standardization_summary.md',
        'untouched_folders_final_report.md',
        'untouched_folders_report.md',
        'untouched_folders_summary.md',
        'untouched_folders_action_plan.md',
        'final_abc_format_summary.md',
        'final_cleanup_summary.md',
        'markdown_standardization_report_*.txt',
        'image_description_report_*.txt',
        'image_description_status_*.txt',
        'concurrent_image_description_report_*.txt',
        'research_csv_merge_report.txt',
        'research_csv_update_report.txt'
    ]
    
    for pattern in report_files:
        for report_file in Path('.').glob(pattern):
            if report_file.exists():
                shutil.move(str(report_file), f'archive/old_reports/{report_file.name}')
                print(f"Moved: {report_file} → archive/old_reports/")

def archive_old_csvs():
    """Archive redundant CSV files but keep the important ones"""
    # Keep these important CSVs
    keep_csvs = {
        'research_papers_complete.csv',
        'papers_clean.csv',
        'missing_papers.csv'
    }
    
    # Archive these old/redundant CSVs
    csv_files = [
        'research_papers_clean.csv',
        'research_papers_merged.csv',
        'research_papers_sorted.csv',
        'research_papers_final.csv',
        'research_papers_merged_final.csv',
        'research_papers_clean_final.csv',
        'research_table.csv',
        'research_table_with_citekeys.csv',
        'papers_analysis.csv',
        'papers_needing_attention.csv',
        'failed_pdf_conversions.csv',
        'pdf_redownload_list.csv',
        'dois_to_fix.csv',
        'papers_for_concurrent_processing.txt',
        'papers_needing_image_descriptions.txt',
        'papers_needing_image_descriptions_updated.txt',
        'problematic_files_list.txt',
        'untouched_folders_complete_list.txt'
    ]
    
    # Archive backup CSVs
    for csv_file in Path('.').glob('*_backup*.csv'):
        if csv_file.exists():
            shutil.move(str(csv_file), f'archive/old_csvs/{csv_file.name}')
            print(f"Moved: {csv_file} → archive/old_csvs/")
    
    for csv_file in csv_files:
        if Path(csv_file).exists():
            shutil.move(csv_file, f'archive/old_csvs/{csv_file}')
            print(f"Moved: {csv_file} → archive/old_csvs/")

def archive_checkpoints_and_configs():
    """Archive checkpoint and configuration files"""
    checkpoint_files = [
        '*.json',
        'checkpoint_markdown_papers.json',
        'reliable_checkpoint.json',
        'robust_converter_checkpoint.json',
        'simple_batch_checkpoint.json',
        'simple_checkpoint.json',
        'smart_checkpoint.json',
        'new_papers_checkpoint.json'
    ]
    
    # Archive JSON files but keep important ones
    keep_json = {
        'missing_papers.json'
    }
    
    for json_file in Path('.').glob('*.json'):
        if json_file.name not in keep_json and json_file.exists():
            shutil.move(str(json_file), f'archive/old_checkpoints/{json_file.name}')
            print(f"Moved: {json_file} → archive/old_checkpoints/")

def organize_core_files():
    """Organize remaining core files"""
    # Create docs folder and move documentation
    Path('docs').mkdir(exist_ok=True)
    
    docs_to_move = [
        'README.md',
        'changelog.md',
        'PDF_MARKDOWN_CONVERTER_README.md'
    ]
    
    for doc in docs_to_move:
        if Path(doc).exists():
            shutil.move(doc, f'docs/{doc}')
            print(f"Moved: {doc} → docs/")

def create_cleanup_summary():
    """Create a summary of what was cleaned up"""
    summary = f"""
# HDM Project Spring Cleaning Summary
Generated: {datetime.now().isoformat()}

## Folder Structure Created:
- archive/old_scripts/ - Processing and utility scripts
- archive/old_logs/ - Log files and monitoring outputs  
- archive/old_reports/ - Analysis and status reports
- archive/old_csvs/ - Redundant CSV files and backups
- archive/old_checkpoints/ - JSON configs and checkpoints
- scripts/processing/ - PDF/markdown conversion scripts
- scripts/analysis/ - Data analysis and report scripts
- scripts/utilities/ - General utility scripts
- reports/current/ - Active reports
- reports/archive/ - Old reports
- docs/ - Documentation files

## Files Kept in Root:
- CLAUDE.md - Project instructions
- GEMINI.md - Previous agent directives  
- research_papers_complete.csv - Main research data
- papers_clean.csv - Clean research data
- missing_papers.json - Additional paper metadata
- research_findings.html - Web interface
- spring_cleaning.py - This cleanup script

## Key Folders Preserved:
- markdown_papers/ - All research paper content
- papers/ - PDF files
- analysis/ - Research analysis documents
- plan/ - Research methodology
- inbox/ - Input data files
- archieved/ - Previously archived data
- scripts/ - Script directory (organized)
- venv/ - Python virtual environment
- marker_env/ - Marker environment

## Next Steps:
1. Review archived files to ensure nothing important was moved
2. Update any scripts that reference moved files
3. Consider removing very old archives after backup
4. Maintain this organization going forward
"""
    
    with open('cleanup_summary.md', 'w') as f:
        f.write(summary)
    
    print("Created cleanup_summary.md")

def main():
    """Main cleanup function"""
    print("🧹 Starting HDM Project Spring Cleaning...")
    print("=" * 50)
    
    print("\n1. Creating archive folder structure...")
    create_archive_structure()
    
    print("\n2. Moving processing scripts...")
    move_processing_scripts()
    
    print("\n3. Moving analysis scripts...")
    move_analysis_scripts() 
    
    print("\n4. Archiving old logs...")
    archive_old_logs()
    
    print("\n5. Archiving old reports...")
    archive_old_reports()
    
    print("\n6. Archiving redundant CSVs...")
    archive_old_csvs()
    
    print("\n7. Archiving checkpoints and configs...")
    archive_checkpoints_and_configs()
    
    print("\n8. Organizing core files...")
    organize_core_files()
    
    print("\n9. Creating cleanup summary...")
    create_cleanup_summary()
    
    print("\n✅ Spring cleaning completed!")
    print("📋 See cleanup_summary.md for details")
    print("\n📁 Current root directory now contains:")
    print("   - Core files (CLAUDE.md, research_papers_complete.csv, etc.)")
    print("   - Organized scripts/ folder")
    print("   - Research content (markdown_papers/, papers/, analysis/)")
    print("   - Archive/ folder with old files")

if __name__ == '__main__':
    main()
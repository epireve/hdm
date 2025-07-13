#!/usr/bin/env python3
"""
Refactor and organize the HDM codebase.
This script helps clean up residual code and organize the project structure.
"""

import os
import shutil
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodebaseOrganizer:
    def __init__(self, base_path='.'):
        self.base_path = Path(base_path)
        
        # Define the target structure
        self.target_structure = {
            'scripts': {
                'data_processing': [
                    'consolidate_yaml_and_csv.py',
                    'yaml_data_extractor.py',
                    'intelligent_data_merger.py',
                    'smart_converter.py',
                    'process_new_papers_batch.py'
                ],
                'data_quality': [
                    'add_csv_original_authors.py',
                    'analyze_specific_issues.py',
                    'fix_critical_issues.py',
                    'investigate_questionable_authors.py',
                    'apply_high_priority_author_fixes.py',
                    'verify_paper_years.py'
                ],
                'folder_management': [
                    'rename_folders_to_cite_keys.py',
                    'create_missing_folders.py',
                    'update_folder_names.py'
                ],
                'data_export': [
                    'export_data.py'
                ],
                'utilities': [
                    'refactor_and_organize.py'
                ]
            },
            'legacy': {
                'description': 'Old scripts kept for reference',
                'files': []
            },
            'docs': {
                'description': 'Documentation and reports',
                'files': [
                    'year_verification_report.md',
                    'consolidation_report.md',
                    'data_quality_report.md'
                ]
            },
            'exports': {
                'description': 'Data exports in various formats'
            },
            'data': {
                'intermediate': {
                    'description': 'Intermediate processing files'
                },
                'logs': {
                    'description': 'Processing logs and reports'
                }
            }
        }
        
        self.files_to_archive = []
        self.files_to_move = []
        
    def analyze_current_structure(self):
        """Analyze the current file structure."""
        
        # Get all Python files in root
        root_py_files = list(self.base_path.glob('*.py'))
        
        # Get all JSON files in root
        root_json_files = list(self.base_path.glob('*.json'))
        
        # Get all other files
        other_files = [
            f for f in self.base_path.iterdir() 
            if f.is_file() and f.suffix not in ['.py', '.json', '.db', '.md']
        ]
        
        print(f"\n📊 CURRENT CODEBASE ANALYSIS")
        print(f"=" * 70)
        print(f"Python files in root: {len(root_py_files)}")
        print(f"JSON files in root: {len(root_json_files)}")
        print(f"Other files: {len(other_files)}")
        
        # Categorize files
        categorized = {
            'data_processing': [],
            'data_quality': [],
            'folder_management': [],
            'intermediate_files': [],
            'logs': [],
            'unknown': []
        }
        
        # Categorize Python files
        for py_file in root_py_files:
            name = py_file.name
            
            if any(keyword in name for keyword in ['yaml', 'csv', 'consolidat', 'merg', 'process']):
                categorized['data_processing'].append(name)
            elif any(keyword in name for keyword in ['author', 'year', 'quality', 'fix', 'investigat']):
                categorized['data_quality'].append(name)
            elif any(keyword in name for keyword in ['folder', 'rename']):
                categorized['folder_management'].append(name)
            else:
                categorized['unknown'].append(name)
                
        # Categorize JSON files
        for json_file in root_json_files:
            name = json_file.name
            
            if any(keyword in name for keyword in ['checkpoint', 'cache', 'progress']):
                categorized['intermediate_files'].append(name)
            elif any(keyword in name for keyword in ['log', 'report']):
                categorized['logs'].append(name)
            else:
                categorized['intermediate_files'].append(name)
                
        return categorized
    
    def create_organized_structure(self):
        """Create the organized directory structure."""
        
        # Create main directories
        directories = [
            'scripts/data_processing',
            'scripts/data_quality',
            'scripts/folder_management',
            'scripts/data_export',
            'scripts/utilities',
            'legacy',
            'docs',
            'exports',
            'data/intermediate',
            'data/logs'
        ]
        
        for dir_path in directories:
            path = self.base_path / dir_path
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {dir_path}")
            
        # Create README files
        self._create_readme_files()
        
    def _create_readme_files(self):
        """Create README files for each directory."""
        
        readmes = {
            'scripts/README.md': """# Scripts Directory

This directory contains all processing scripts organized by function:

- **data_processing/**: Scripts for processing papers and extracting data
- **data_quality/**: Scripts for validating and fixing data quality issues
- **folder_management/**: Scripts for managing paper folders and organization
- **data_export/**: Scripts for exporting data in various formats
- **utilities/**: Helper scripts and utilities
""",
            'scripts/data_processing/README.md': """# Data Processing Scripts

Scripts for processing academic papers and extracting metadata:

- `yaml_data_extractor.py`: Extract YAML frontmatter from paper.md files
- `consolidate_yaml_and_csv.py`: Merge YAML and CSV data
- `intelligent_data_merger.py`: Smart merging with conflict resolution
- `smart_converter.py`: Convert PDFs to markdown format
- `process_new_papers_batch.py`: Batch process new papers
""",
            'scripts/data_quality/README.md': """# Data Quality Scripts

Scripts for ensuring data quality and fixing issues:

- `add_csv_original_authors.py`: Add original CSV authors for comparison
- `analyze_specific_issues.py`: Analyze specific data quality issues
- `fix_critical_issues.py`: Fix critical data problems
- `investigate_questionable_authors.py`: Deep investigation of author data
- `apply_high_priority_author_fixes.py`: Apply author corrections
- `verify_paper_years.py`: Verify and correct publication years
""",
            'legacy/README.md': """# Legacy Scripts

This directory contains old scripts preserved for reference.
These scripts have been superseded by newer versions but may contain
useful code or logic for future reference.
""",
            'data/README.md': """# Data Directory

- **intermediate/**: Temporary files created during processing
- **logs/**: Processing logs and reports

Note: This directory is excluded from version control.
""",
            'exports/README.md': """# Exports Directory

This directory contains data exports in various formats:
- CSV files for spreadsheet analysis
- JSON files for programmatic access
- SQLite database backups
- Markdown documentation

Exports are automatically generated by GitHub Actions.
"""
        }
        
        for path, content in readmes.items():
            readme_path = self.base_path / path
            readme_path.parent.mkdir(parents=True, exist_ok=True)
            with open(readme_path, 'w') as f:
                f.write(content)
                
    def move_files(self, dry_run=True):
        """Move files to their organized locations."""
        
        categorized = self.analyze_current_structure()
        moves = []
        
        # Define move operations
        for py_file in self.base_path.glob('*.py'):
            name = py_file.name
            
            # Skip if already in scripts
            if 'scripts' in str(py_file):
                continue
                
            # Determine destination
            if name in ['yaml_data_extractor.py', 'consolidate_yaml_and_csv.py', 
                       'intelligent_data_merger.py', 'smart_converter.py',
                       'process_new_papers_batch.py']:
                dest = self.base_path / 'scripts' / 'data_processing' / name
            elif name in ['add_csv_original_authors.py', 'analyze_specific_issues.py',
                         'fix_critical_issues.py', 'investigate_questionable_authors.py',
                         'apply_high_priority_author_fixes.py', 'verify_paper_years.py']:
                dest = self.base_path / 'scripts' / 'data_quality' / name
            elif name in ['rename_folders_to_cite_keys.py', 'create_missing_folders.py',
                         'update_folder_names.py']:
                dest = self.base_path / 'scripts' / 'folder_management' / name
            elif name == 'export_data.py':
                dest = self.base_path / 'scripts' / 'data_export' / name
            else:
                # Move to legacy
                dest = self.base_path / 'legacy' / name
                
            moves.append((py_file, dest))
            
        # Move JSON files
        for json_file in self.base_path.glob('*.json'):
            name = json_file.name
            
            if name in ['progress_cache.json', 'missing_papers.json', 
                       'cite_key_mapping.json']:
                # Keep in root - these are active data files
                continue
            elif 'checkpoint' in name or 'cache' in name:
                dest = self.base_path / 'data' / 'intermediate' / name
            elif 'log' in name or 'report' in name:
                dest = self.base_path / 'data' / 'logs' / name
            else:
                dest = self.base_path / 'data' / 'intermediate' / name
                
            moves.append((json_file, dest))
            
        # Execute moves
        if dry_run:
            print(f"\n🔍 DRY RUN - Proposed file moves:")
            for src, dest in moves:
                print(f"  {src.name} → {dest.relative_to(self.base_path)}")
        else:
            print(f"\n🚀 Moving files...")
            for src, dest in moves:
                if src.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dest))
                    print(f"  ✅ Moved {src.name}")
                    
        return len(moves)
    
    def create_gitignore(self):
        """Create or update .gitignore file."""
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Data files
data/intermediate/
data/logs/
*.db-journal
*.db-wal

# Temporary files
*.tmp
*.bak
*.swp
*~
.DS_Store

# IDE
.vscode/
.idea/
*.sublime-*

# Exports (keep current versions only)
exports/*_2*.csv
exports/*_2*.json
exports/*_2*.db
exports/*_2*.md
!exports/*_current.*

# Large data files
papers/
new_papers/
markdown_papers/
production_final_reformatted_*/

# Logs
*.log
"""
        
        gitignore_path = self.base_path / '.gitignore'
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
            
        print(f"\n✅ Created/updated .gitignore")
        
    def create_project_readme(self):
        """Create main project README."""
        
        readme_content = """# HDM Papers Database

A comprehensive database of academic papers focusing on Human Digital Memory (HDM) systems, specifically investigating heterogeneous data integration within Personal Knowledge Graph (PKG) architectures.

## Overview

This project maintains a curated collection of 358 academic papers (2019-2025) with detailed metadata, quality-assured author information, and structured research insights.

## Project Structure

```
hdm/
├── scripts/              # Processing and analysis scripts
│   ├── data_processing/  # Paper processing and metadata extraction
│   ├── data_quality/     # Data validation and correction
│   ├── folder_management/# Folder organization utilities
│   ├── data_export/      # Export to various formats
│   └── utilities/        # Helper scripts
├── exports/              # Data exports (CSV, JSON, SQLite, Markdown)
├── docs/                 # Documentation and reports
├── data/                 # Intermediate data and logs
├── markdown_papers/      # Processed papers in markdown format
└── hdm_papers.db        # Main SQLite database

```

## Key Features

- **Data Quality**: 98.6% author accuracy, 100% year verification
- **Multiple Formats**: Automatic export to CSV, JSON, SQLite, and Markdown
- **Automated Updates**: GitHub Actions for continuous data refresh
- **Comprehensive Metadata**: 21+ fields per paper including research insights

## Quick Start

### Export Data
```bash
python scripts/data_export/export_data.py
```

### Update Folder Names
```bash
python scripts/folder_management/update_folder_names.py --execute
```

### Verify Data Quality
```bash
python scripts/data_quality/verify_paper_years.py
```

## Data Schema

Each paper contains:
- Basic metadata (title, authors, year, DOI, URL)
- Research details (question, methodology, findings, outcomes)
- Analysis (limitations, gaps, future work, insights)
- HDM relevance (relevancy rating, justification, implementation insights)

## Automated Workflows

GitHub Actions automatically:
- Export data on every push
- Create versioned backups
- Generate documentation
- Validate data quality

## Contributing

See CONTRIBUTING.md for guidelines on adding new papers or improving data quality.

## License

This project is licensed under the MIT License - see LICENSE file for details.
"""
        
        readme_path = self.base_path / 'README.md'
        with open(readme_path, 'w') as f:
            f.write(readme_content)
            
        print(f"\n✅ Created project README.md")


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Refactor and organize HDM codebase')
    parser.add_argument('--execute', action='store_true',
                       help='Execute the reorganization (default is dry run)')
    parser.add_argument('--skip-move', action='store_true',
                       help='Skip file moving, only create structure')
    
    args = parser.parse_args()
    
    organizer = CodebaseOrganizer()
    
    # Step 1: Analyze current structure
    organizer.analyze_current_structure()
    
    # Step 2: Create organized structure
    print(f"\n📁 Creating organized directory structure...")
    organizer.create_organized_structure()
    
    # Step 3: Move files
    if not args.skip_move:
        move_count = organizer.move_files(dry_run=not args.execute)
        
        if not args.execute:
            print(f"\n💡 To execute reorganization, run with --execute flag")
    
    # Step 4: Create project files
    organizer.create_gitignore()
    organizer.create_project_readme()
    
    print(f"\n✅ Codebase organization complete!")


if __name__ == "__main__":
    main()
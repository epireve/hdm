# HDM Papers Database

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

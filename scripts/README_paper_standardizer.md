# Paper.md Comprehensive Standardizer

This tool standardizes all `paper.md` files in the `markdown_papers` directory to ensure consistency, integrity, and both human and machine readability.

## Features

- **Comprehensive Standardization**: Reorganizes papers into a consistent structure
- **CSV Validation**: Cross-validates metadata with `hdm_research_papers_merged_20250710.csv`
- **Content Preservation**: Maintains all original content, only reorganizes
- **Gemini 2.5 Pro Integration**: Uses advanced AI for intelligent standardization
- **Backup System**: Creates timestamped backups before any modifications
- **Detailed Reporting**: Generates comprehensive reports and error logs
- **Batch Processing**: Processes papers in configurable batches
- **Dry Run Mode**: Preview changes without modifying files

## Requirements

- Python 3.7+
- OpenAI library: `pip install openai`
- Other dependencies: `pip install tqdm pyyaml`
- Kilocode API token in `.env` file

## Usage

### Basic Usage
```bash
# Standardize all papers
python scripts/paper_md_comprehensive_standardizer.py

# Dry run mode (preview changes)
python scripts/paper_md_comprehensive_standardizer.py --dry-run

# Process specific papers
python scripts/paper_md_comprehensive_standardizer.py --papers abdallah_2021 ai_2025

# Adjust batch size
python scripts/paper_md_comprehensive_standardizer.py --batch-size 10

# Use different CSV file
python scripts/paper_md_comprehensive_standardizer.py --csv path/to/csv
```

### Command Line Options

- `--csv`: Path to CSV file with paper metadata (default: hdm_research_papers_merged_20250710.csv)
- `--dry-run`: Preview changes without modifying files
- `--batch-size`: Number of papers to process in each batch (default: 5)
- `--papers`: Specific paper cite_keys to process (space-separated)

## Standardized Paper Structure

Each standardized paper will have the following structure:

```markdown
---
# Core Metadata
cite_key: from_folder_name
title: Full Paper Title
authors: First Author, Second Author
year: YYYY
doi: 10.xxxx/xxxxx
url: https://example.com

# Relevancy & Classification
relevancy: High/Medium/Low
relevancy_justification: Explanation
tags:
  - tag1
  - tag2

# Processing Metadata
date_processed: YYYY-MM-DD
standardization_date: YYYY-MM-DD
standardization_version: 1.0

# Document Statistics
word_count: N
sections_count: N
---

# Full Paper Title

## Authors
[Formatted author list]

## Abstract
[Original abstract]

## TL;DR
[One-sentence summary from CSV]

## Key Insights
[Implementation insights from CSV]

## 1. Introduction
[Original content]

## 2. [Next Section]
[Original content]

[... more sections ...]

## References
[Formatted references]

## Metadata Summary
### Research Context
- Research Question
- Methodology
- Key Findings
- Primary Outcomes

### Analysis
- Limitations
- Research Gaps
- Future Work
- Conclusion

### Implementation Notes
[HDM-specific insights]
```

## Output Files

1. **Standardized Papers**: Updated in place at `markdown_papers/*/paper.md`
2. **Processing Report**: `standardization_report_YYYYMMDD_HHMMSS.json`
3. **Error Log**: `standardization_errors.log`
4. **Backups**: `paper_backups_YYYYMMDD_HHMMSS/`

## Processing Report

The JSON report includes:
- Processing timestamp
- CSV file used
- Statistics (total, processed, successful, failed)
- Per-paper results with warnings and errors
- Validation issues found

## Error Handling

- **API Failures**: Logged and skipped, processing continues
- **Validation Warnings**: Recorded but doesn't stop processing
- **File Errors**: Logged with full traceback
- **Backup Failures**: Stops processing for that paper

## Best Practices

1. **Always run dry-run first** to preview changes
2. **Check the report** after processing for any warnings
3. **Keep backups** until you've verified the results
4. **Process in smaller batches** if you have API rate limits
5. **Review papers with warnings** manually

## Troubleshooting

### Common Issues

1. **API Rate Limits**: Reduce batch size or add delays
2. **Memory Issues**: Process fewer papers at once
3. **Invalid YAML**: Check error log for specific papers
4. **Missing CSV Data**: Warnings logged, paper still processed

### Recovery

If something goes wrong:
1. Check `standardization_errors.log` for details
2. Restore from backups in `paper_backups_YYYYMMDD_HHMMSS/`
3. Fix any issues and re-run specific papers

## Future Enhancements

- Parallel processing support
- Interactive mode for reviewing changes
- Automatic cite_key correction
- Custom standardization templates
- Integration with other HDM tools
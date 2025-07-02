# Phase 2 CSV Workflow Guide

## Overview
The Phase 2 processing has been updated to work with CSV files for better scalability and easier data management.

## Key Changes

### 1. New Files Created
- `csv_utils.py` - CSV handling utilities
- `convert_to_csv.py` - One-time conversion from markdown to CSV
- `research_table_updater_csv.py` - CSV version of cite key generator
- `run_phase2_csv.py` - Main runner with CSV support

### 2. New Configuration
- `RESEARCH_TABLE_CSV` = research_table.csv
- `UPDATED_RESEARCH_TABLE_CSV` = research_table_with_citekeys.csv

### 3. CSV Format
The CSV preserves all 21 columns from the markdown table:
1. Paper Title
2. cite_key (newly added)
3. Authors
4. Year
5. Downloaded
6. Relevancy
7. Relevancy Justification
8. Insights
9. TL;DR
10. Summary
11. Research Question
12. Methodology
13. Key Findings
14. Primary Outcomes
15. Limitations
16. Conclusion
17. Research Gaps
18. Future Work
19. Implementation Insights
20. url
21. DOI
22. Tags

## Usage

### Initial Setup (One-time)
```bash
# Convert markdown table to CSV
python scripts/phase2/convert_to_csv.py
```

### Generate Cite Keys

#### Test Mode (5 papers)
```bash
python scripts/phase2/run_phase2_csv.py --test --step update-table
```

#### Full Mode (all papers)
```bash
python scripts/phase2/run_phase2_csv.py --full --step update-table
```

### Run Complete Phase 2
```bash
# Test mode
python scripts/phase2/run_phase2_csv.py --test

# Full mode
python scripts/phase2/run_phase2_csv.py --full
```

## Current Status
✅ Markdown to CSV conversion - Complete
✅ Cite key generation - Complete (122 papers)
⚠️ Paper analysis - Needs CSV integration
⚠️ Markdown standardization - Needs CSV integration
⚠️ Metadata integration - Needs CSV integration
⚠️ Image description - Needs CSV integration
⚠️ Folder reorganization - Needs CSV integration

## Cite Key Format
- Format: `lastname + year` (e.g., smith2024)
- Duplicates: Append letters (smith2024b, smith2024c)
- Missing author: Uses "unknown"
- Missing year: Uses "nd" (no date)

## Benefits of CSV Format
1. **Scalability**: Can append new papers without loading entire table
2. **Compatibility**: Works with standard data analysis tools
3. **Performance**: Faster processing for large datasets
4. **Simplicity**: Easier to parse and manipulate

## Next Steps
To complete Phase 2 integration, the following scripts need to be updated to read cite keys from CSV:
- paper_analyzer.py
- markdown_standardizer.py
- metadata_integrator.py
- image_descriptor.py
- cite_key_reorganizer.py

## Backup Strategy
All operations create timestamped backups in:
- `backup_phase2/` - Markdown backups
- `backup_phase2/csv_backup/` - CSV backups
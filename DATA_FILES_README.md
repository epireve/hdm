# HDM Research Data Files

## Final Dataset Files

This directory contains the final, cleaned datasets for the Human Digital Memory (HDM) research project.

### Naming Convention

All final CSV files follow this standardized naming convention:
```
hdm_research_papers_[type]_[YYYYMMDD].csv
```

Where:
- `hdm_research_papers` - Standard prefix for all research paper datasets
- `[type]` - Dataset type (complete, merged, etc.)
- `[YYYYMMDD]` - Date of file generation

### Current Files

1. **hdm_research_papers_complete_20250710.csv** (760KB)
   - Complete dataset of 358 research papers
   - All fields populated including Relevancy and Relevancy Justification
   - Tags normalized and standardized
   - Primary research dataset

2. **hdm_research_papers_merged_20250710.csv** (1.1MB)
   - Merged dataset combining primary papers with PKG enrichment data
   - Contains additional columns prefixed with "pkg_" from personalized PKG analysis
   - 277 papers matched (89.4% match rate)
   - Includes match_type and match_score columns

3. **personalized_pkg_paperguide_clean.csv** (1.6MB)
   - Clean extracted PKG dataset
   - 310 papers with enriched analysis
   - Source data for the merge operation

### Column Structure

All datasets contain these core columns:
- Paper Title
- Authors
- Year
- Downloaded
- Relevancy (High/Medium/Low)
- Relevancy Justification
- Insights
- TL;DR
- Summary
- Research Question
- Methodology
- Key Findings
- Primary Outcomes
- Limitations
- Conclusion
- Research Gaps
- Future Work
- Implementation Insights
- url
- DOI
- Tags (normalized, comma-separated)

The merged dataset additionally contains:
- match_type (exact_title/fuzzy_title)
- match_score (similarity score 0-1)
- pkg_* columns (enrichment data from PKG analysis)

### Usage

For most analyses, use:
- **hdm_research_papers_complete_[date].csv** - For analysis of the full paper collection
- **hdm_research_papers_merged_[date].csv** - For analysis including PKG enrichment data

### Processing Scripts

Core scripts for data processing are located in `scripts/processing/`:
- `merge_datasets_final.py` - Merge datasets with fuzzy matching
- `normalize_tags.py` - Normalize and standardize tags
- `process_new_papers_batch.py` - Process new papers into the dataset

### Data Quality

- All papers have complete metadata (21 columns filled)
- Tags are normalized (e.g., "knowledge-graph" instead of "Knowledge Graphs")
- Relevancy ratings are standardized (High/Medium/Low)
- No duplicate entries
- Consistent formatting across all fields
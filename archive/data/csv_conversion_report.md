# Excel to CSV Conversion Report

## Conversion Summary

- **Source File**: Pesonalised PKG Paperguide compiled.xlsx
- **Output File**: personalized_pkg_paperguide.csv
- **Status**: ✅ Successfully converted

## Data Overview

- **Total Rows**: 360 papers
- **Total Columns**: 22 fields

### Column List:
1. Papers
2. Authors
3. Published Year
4. Journal
5. DOI
6. Implementation Insights
7. Tags
8. TL;DR
9. Summary
10. Insights
11. Research Question
12. Methodology
13. Reproducibility
14. Key Findings
15. Primary Outcomes
16. Limitations
17. Conclusion
18. Research Gaps
19. Future Research
20. Study design
21. Discussion Summary
22. Objectives

## Data Integrity Analysis

### Missing Values
- **DOI**: 150 missing (41.7%)
- **Implementation Insights**: 200 missing (55.6%)
- **Tags**: 298 missing (82.8%)
- **Insights**: 360 missing (100% - entire column empty)
- **Study design**: 247 missing (68.6%)
- **Discussion Summary**: 264 missing (73.3%)
- **Reproducibility**: 194 missing (53.9%)
- **Objectives**: 166 missing (46.1%)

### Multi-line Content
The following columns contain cells with line breaks (preserved as \n):
- **Methodology**: 310 cells (86.1%)
- **Conclusion**: 357 cells (99.2%)
- **Research Gaps**: 343 cells (95.3%)
- **Key Findings**: 299 cells (83.1%)
- **Primary Outcomes**: 274 cells (76.1%)
- **Limitations**: 327 cells (90.8%)

## Line Break Preservation
✅ Line breaks have been successfully preserved in the CSV format using standard newline characters (\n).

## Example of Preserved Multi-line Content
```
Column: Papers, Row: 164
Content: "Integrating Manifold Knowledge for Global Entity Linking with\nHeterogeneous Graphs"
```

## Recommendations

1. **Empty Column**: The "Insights" column is completely empty and could be removed if not needed.

2. **High Missing Data**: Several columns have >50% missing data:
   - Tags (82.8% missing)
   - Discussion Summary (73.3% missing)
   - Study design (68.6% missing)
   - Implementation Insights (55.6% missing)

3. **Data Validation**: Consider reviewing papers with missing DOIs for completeness.

4. **Line Breaks**: All multi-line content has been preserved correctly. When importing this CSV into other tools, ensure they properly handle quoted fields with newlines.

## Technical Notes

- Encoding: UTF-8
- Quoting: QUOTE_MINIMAL (only quotes fields containing delimiters or newlines)
- Line Terminator: Standard Unix newline (\n)
- No index column included
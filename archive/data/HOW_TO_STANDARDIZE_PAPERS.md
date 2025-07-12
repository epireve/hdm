# How to Standardize Papers - Complete Guide

## What the Standardization Does

The standardization process:
1. **Reads** the original `markdown_papers/{cite_key}/paper.md`
2. **Creates a backup** in `paper_backups/{cite_key}/`
3. **Processes** with Gemini API to add new sections
4. **REPLACES** the original paper.md with standardized version

## Single Paper Standardization

To standardize one paper at a time:

```bash
python scripts/standardize_and_replace.py ai_2025
```

This will:
- ✅ Replace `markdown_papers/ai_2025/paper.md` with standardized version
- ✅ Create backup in `paper_backups/ai_2025/paper_backup_YYYYMMDD_HHMMSS.md`
- ✅ Add TL;DR, Key Insights, and Metadata Summary sections

## Batch Processing All Papers

### Option 1: Sequential Processing (Works Now)
```bash
# Process all papers one by one
for paper in $(ls markdown_papers); do
    echo "Processing $paper..."
    python scripts/standardize_and_replace.py $paper
    sleep 2  # Brief pause between API calls
done
```

### Option 2: Concurrent Processing (After API Fix)
```bash
# Process all papers with 20 workers
python scripts/standardize_all_papers_concurrent.py --workers 20
```

## What Gets Changed

### Before (Original):
```markdown
---
cite_key: ai_2025
title: Paper Title
tags:
  - tag1
  - tag2
---

# Paper Title

## Abstract
[content]

## Introduction
[content]
```

### After (Standardized):
```markdown
---
cite_key: ai_2025
title: Paper Title
authors: Author Names
year: 2025
doi: 10.xxxx/xxxxx
url: https://...
relevancy: HIGH
relevancy_justification: [from CSV]
tags:
  - tag1
  - tag2
standardization_date: 2025-07-10
standardization_version: 1.0
word_count: 1234
sections_count: 15
---

# Paper Title

## Authors
- Author Name (email)

## Abstract
[original content preserved]

## TL;DR
[Added from CSV]

## Key Insights
[Added from CSV]

## Introduction
[original content preserved]

[... all original sections preserved ...]

## References
[original references preserved]

## Metadata Summary
### Research Context
- **Research Question**: [from CSV]
- **Methodology**: [from CSV]
- **Key Findings**: [from CSV]
- **Primary Outcomes**: [from CSV]

### Analysis
- **Limitations**: [from CSV]
- **Research Gaps**: [from CSV]
- **Future Work**: [from CSV]
- **Conclusion**: [from CSV]

### Implementation Notes
[from CSV]
```

## File Locations

- **Original Papers**: `markdown_papers/{cite_key}/paper.md` (replaced in-place)
- **Backups**: `paper_backups/{cite_key}/paper_backup_YYYYMMDD_HHMMSS.md`
- **Logs**: `logs/standardization_*.log`
- **Progress**: `standardization_state.json` (for resume capability)

## Important Notes

1. **The original paper.md files ARE replaced** - not separate files
2. **All original content is preserved** - only reorganized
3. **Backups are created** before any modifications
4. **Process is resumable** if interrupted

## Example Output

When you run the standardizer:
```
============================================================
Standardizing: ai_2025
============================================================
✓ Read original: 45064 characters
✓ Backup saved: paper_backups/ai_2025/paper_backup_20250710_195310.md
🤖 Calling Gemini API to standardize...
✅ REPLACED original paper.md with standardized version
   File: markdown_papers/ai_2025/paper.md
   New size: 6575 characters
   Added sections: TL;DR, Key Insights, Metadata Summary

✅ Success! The paper.md has been standardized in-place.
```

The paper at `markdown_papers/ai_2025/paper.md` is now the standardized version!
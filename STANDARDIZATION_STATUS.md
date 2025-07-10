# Paper Standardization Status

## Overview

The standardization process updates all `paper.md` files in the `markdown_papers` directory to have:
1. Consistent YAML frontmatter
2. Added TL;DR and Key Insights sections after Abstract
3. Metadata Summary section at the end with research context and analysis

## Current Status

- **Total Papers**: ~358 in markdown_papers directory
- **Completed**: 4 papers (as of last run)
- **In Progress**: Batch processing underway

## Running the Standardization

### Option 1: Automated Batch Processing (Recommended)
```bash
# This runs the standardization in batches of 5 papers
# It automatically handles timeouts and saves progress
./scripts/run_standardization.sh
```

### Option 2: Process Single Paper
```bash
python scripts/standardize_and_replace.py [cite_key]
```

### Option 3: Manual Batch Control
```bash
# Process next 10 papers
python scripts/standardize_papers_batch.py --limit 10

# Reset and start over
python scripts/standardize_papers_batch.py --reset --limit 5
```

## Files Created

- `standardization_progress.json` - Tracks which papers are completed/failed
- `paper_backups/[cite_key]/` - Backups of original papers before standardization
- Each paper is updated IN-PLACE at `markdown_papers/[cite_key]/paper.md`

## What Gets Standardized

### YAML Frontmatter Updates:
- Removes: `images_total`, `images_kept`, `images_removed`
- Adds: `standardization_date`, `standardization_version`
- Ensures consistent formatting

### New Sections Added:
1. **TL;DR** - One-line summary from CSV
2. **Key Insights** - Key insights from CSV  
3. **Metadata Summary** - Comprehensive research metadata including:
   - Research Context (Question, Methodology, Findings, Outcomes)
   - Analysis (Limitations, Gaps, Future Work, Conclusion)
   - Implementation Notes

## Monitoring Progress

Check current status:
```bash
# View progress file
cat standardization_progress.json | python -m json.tool

# Count completed papers
python -c "import json; print(len(json.load(open('standardization_progress.json'))['completed']))"
```

## Known Issues

1. Large papers (>40KB) may timeout - these are skipped and processed later
2. API rate limits may slow processing - script handles this with retries
3. Some papers may have incomplete CSV data - standardization proceeds with available data

## Next Steps

After standardization completes:
1. Review a sample of standardized papers for quality
2. Process any failed papers manually if needed
3. Consider updating cite_keys if needed (separate process)
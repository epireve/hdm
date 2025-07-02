# HDM Processing Scripts

## Phase 2: Markdown Standardization

This phase performs comprehensive standardization of the markdown papers including:
- Adding cite_key column to research_table.md
- Analyzing papers and generating unique cite keys
- Standardizing markdown formatting
- Adding YAML front matter with metadata
- Generating image descriptions
- Reorganizing folders based on cite keys

### Setup

1. Install required dependencies:
```bash
pip install -r scripts/requirements.txt
```

2. Ensure you have the following files:
- `research_table.md` - The main research table
- `markdown_papers/` - Directory with converted markdown papers

### Configuration

Edit `scripts/phase2/config.py` to customize:
- `TEST_MODE`: Set to `True` to process only 5 papers for testing
- `BATCH_SIZE`: Number of papers to process in each batch
- Image patterns to keep/remove
- Other directory paths

### Running Phase 2

#### Test Mode (Recommended First)
Process only 5 papers to verify everything works:
```bash
python scripts/phase2/run_phase2.py --test
```

#### Full Processing
Process all papers:
```bash
python scripts/phase2/run_phase2.py
```

#### Individual Steps
Run specific steps:
```bash
# Update research table with cite_key column
python scripts/phase2/run_phase2.py --step update-table

# Analyze papers and generate cite keys
python scripts/phase2/run_phase2.py --step analyze
```

### Scripts Overview

1. **research_table_updater.py**
   - Adds cite_key as the second column in research_table.md
   - Generates unique cite keys based on author names and years
   - Creates backup before modification

2. **paper_analyzer.py**
   - Scans all markdown papers
   - Extracts metadata (title, authors, year)
   - Matches papers with research table entries
   - Identifies images to keep/remove
   - Generates cite_key_mapping.json

3. **markdown_standardizer.py**
   - Fixes header hierarchy and consistency
   - Removes non-relevant images based on patterns
   - Standardizes formatting and spacing
   - Creates backups before modification

4. **metadata_integrator.py**
   - Adds YAML front matter to markdown files
   - Integrates data from research table
   - Preserves existing metadata if present
   - Includes processing statistics

5. **image_descriptor.py**
   - Generates descriptions for images using Gemini Vision API
   - Adds descriptions below images in markdown
   - Requires GOOGLE_API_KEY environment variable
   - Skips images that already have descriptions

6. **cite_key_reorganizer.py**
   - Renames folders to use cite keys
   - Updates internal image references
   - Creates full backup before reorganization
   - Generates reorganization report

### Output Files

- `research_table_with_citekeys.md` - Updated research table (test mode)
- `cite_key_mapping.json` - Complete analysis results and mappings
- `logs/phase2/` - Detailed logs for each run
- `backup_phase2/` - Backups of original files

### Cite Key Format

Cite keys follow the format: `{author_lastname}{year}{suffix}`
- `xu2015` - First paper by Xu in 2015
- `xu2015b` - Second paper by Xu in 2015
- `skjaeveland2024` - Paper by Skjæveland et al. in 2024

### Troubleshooting

1. **Missing dependencies**: Run `pip install -r scripts/requirements.txt`
2. **Permission errors**: Ensure write permissions for all directories
3. **API errors**: Check GOOGLE_API_KEY environment variable for image descriptions
4. **Memory issues**: Reduce BATCH_SIZE in config.py

### Next Steps

After Phase 2 completes:
1. Review the updated research table
2. Check cite_key_mapping.json for accuracy
3. Verify standardized markdown files
4. Proceed with remaining Phase 2 scripts
# Paper Reformatter Documentation

## Overview

The Paper Reformatter is a comprehensive tool designed to fix formatting issues in academic papers stored in the `markdown_papers` directory. It uses Google's Gemini 2.5 Pro AI model via KiloCode API to intelligently reformat papers while preserving all academic content.

## Features

### 1. HTML to Markdown Conversion
- Converts `<sup>`, `<sub>`, `<span>` and other HTML tags to proper Markdown
- Handles HTML entities (`&lt;`, `&gt;`, `&amp;`)
- Removes HTML-specific attributes and IDs

### 2. Reference Fixing
- Fixes broken citation formats like `[[1]]`, `[\[1\]]`
- Removes page-specific anchors (`#page-x-y`)
- Standardizes all citations to `[N]` format

### 3. Formatting Standardization
- Ensures proper Markdown headers
- Fixes broken italic/bold formatting
- Standardizes list formatting
- Preserves mathematical notation

### 4. Logo Removal
- Removes logo references from images
- Cleans up publisher logo mentions
- Preserves actual research content images

### 5. Cite Key Validation
- Extracts first author's last name from paper content
- Validates publication year
- Generates correct `lastname_year` format
- Handles duplicates with a/b/c suffixes
- Renames folders to match cite_keys

## Setup

### Prerequisites
1. Python 3.8+
2. KiloCode API token (already configured in .env file)
3. Required packages:
   ```bash
   pip install openai pyyaml
   ```

### Configuration
The script uses KiloCode API configuration from the `.env` file:
- `KILOCODE_TOKEN`: Your KiloCode JWT token (already set)
- `KILOCODE_DEFAULT_MODEL`: Model to use (default: google/gemini-2.5-pro-preview)

No additional configuration needed if `.env` is properly set up.

## Usage

### Test Mode (Recommended First)
Test on 3 papers to verify functionality:
```bash
python scripts/paper_reformatter.py --test
```

### Single Paper Test
Test on one specific paper:
```bash
python scripts/test_paper_reformatter.py
```

### Full Processing
Process all papers in batches:
```bash
python scripts/paper_reformatter.py --batch-size 10
```

### Command Line Options
- `--markdown-dir`: Directory containing papers (default: markdown_papers)
- `--batch-size`: Papers per batch (default: 10)
- `--test`: Test mode - process only 3 papers
- `--model`: Model to use (default: google/gemini-2.5-pro-preview)

## Process Flow

1. **Backup Creation**: Original files backed up to `backups/paper_reformatter/`
2. **Content Extraction**: Separates YAML frontmatter from content
3. **AI Reformatting**: Sends content to Gemini for processing
4. **Cite Key Validation**: Verifies and corrects cite_key format
5. **Folder Renaming**: Renames folders to match corrected cite_keys
6. **Progress Tracking**: Saves checkpoint for resumability

## Output Files

### 1. Checkpoint File
`paper_reformatter_checkpoint.json` - Tracks processing progress:
```json
{
  "processed": ["markdown_papers/smith_2023/paper.md"],
  "failed": [],
  "last_processed": "markdown_papers/smith_2023/paper.md"
}
```

### 2. Log File
`paper_reformatter_YYYYMMDD_HHMMSS.log` - Detailed processing log

### 3. Report File
`reformatting_report_YYYYMMDD_HHMMSS.json` - Comprehensive results:
```json
{
  "timestamp": "2025-01-12T10:30:00",
  "total_processed": 100,
  "successful": 95,
  "failed": 5,
  "cite_keys_updated": 23,
  "folders_renamed": 20,
  "details": [...]
}
```

## Error Handling

### API Errors
- Implements 1-second delay between requests (KiloCode rate limiting)
- Automatic retry with exponential backoff
- Saves progress for resume capability

### Content Errors
- Logs specific parsing failures
- Continues processing other papers
- Failed papers tracked for manual review

### File System Errors
- Atomic operations prevent partial updates
- Backups enable rollback if needed

## Common Issues and Solutions

### Issue: "Empty response from API"
**Solution**: Check KiloCode token validity and rate limits

### Issue: Cite key not updating
**Solution**: Ensure paper has clear author information after title

### Issue: Folder rename conflicts
**Solution**: Script handles duplicates with suffix (a/b/c)

## Best Practices

1. **Always run test mode first** to verify configuration
2. **Check backups** before running full processing
3. **Review the report** after processing
4. **Monitor API usage** to avoid quota issues

## Resuming Interrupted Processing

The script automatically resumes from where it left off:
```bash
# Just run the same command again
python scripts/paper_reformatter.py
```

## Manual Verification

After processing, verify:
1. No HTML tags remain in papers
2. All references use `[N]` format
3. Cite keys match `lastname_year` convention
4. Folder names match cite_keys
5. Academic content is preserved

## Rollback Procedure

If issues occur:
1. Stop the script (Ctrl+C)
2. Restore from backups:
   ```bash
   cp -r backups/paper_reformatter/* markdown_papers/
   ```
3. Review logs to identify issue
4. Adjust parameters and retry

## Performance Metrics

- **Processing Speed**: ~2-4 seconds per paper (via KiloCode)
- **Success Rate**: Typically 95%+
- **API Usage**: 1 request per paper
- **Memory Usage**: Minimal (<100MB)

## Support

For issues:
1. Check the log file for detailed errors
2. Review the report file for patterns
3. Verify KiloCode token is valid in .env file
4. Ensure paper format matches expected structure
5. Check KiloCode API status and quotas
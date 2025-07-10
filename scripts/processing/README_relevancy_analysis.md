# Relevancy Analysis Script

This script completes missing Relevancy and Relevancy Justification values in the research_papers_complete.csv file using KiloCode API (OpenRouter proxy) with Claude Sonnet 3.5.

## Features

- Automatically assesses paper relevancy (super/high/medium/low) based on research focus
- Generates detailed justifications for relevancy ratings
- Checkpoint system for resuming interrupted processing
- Test mode for validating functionality
- Detailed logging
- Uses KiloCode for managed billing and API access

## Prerequisites

1. **KiloCode Token**: Get one from https://kilocode.ai/auth/signin
2. **Python 3**: The script requires Python 3.6+
3. **Dependencies**: Install with `pip install -r requirements_relevancy.txt`

## Setup

1. Create a `.env` file in the project root directory:
   ```bash
   touch .env
   ```

2. Add your KiloCode token to the `.env` file:
   ```
   KILOCODE_TOKEN='your-token-here'
   ```

3. Install dependencies:
   ```bash
   pip install -r scripts/processing/requirements_relevancy.txt
   ```

## Usage

### Easy Method: Use the Run Script

```bash
cd scripts/processing
./run_relevancy_analysis.sh
```

This will show a menu with options:
1. Test mode (process 5 papers)
2. Full processing (all missing papers)
3. Show statistics

### Direct Method: Run Python Script

```bash
# Test mode (process first 5 papers)
python3 scripts/processing/complete_relevancy_analysis.py --test

# Full processing
python3 scripts/processing/complete_relevancy_analysis.py
```

## How It Works

### Relevancy Assessment Levels

- **SUPER**: Papers directly addressing heterogeneous data integration in PKG
- **HIGH**: Papers strongly related to PKG construction with data integration focus
- **MEDIUM**: Supporting technologies (graph databases, ETL, schema evolution)
- **LOW**: General knowledge graphs without heterogeneous data focus

### Processing Flow

1. Reads research_papers_complete.csv
2. For each paper with missing values:
   - Analyzes title, summary, research question, findings, and tags
   - Assigns relevancy level based on research focus alignment
   - Generates detailed justification
3. Saves progress in checkpoint file
4. Outputs to research_papers_complete_updated.csv

### Files Created

- `relevancy_analysis.log`: Detailed processing log
- `relevancy_checkpoint.json`: Progress tracking
- `research_papers_complete_updated.csv`: Updated CSV with filled values
- `research_papers_test_output.csv`: Test mode output (if using --test)

## Cost Estimation

KiloCode manages all billing automatically. Typical costs:
- Approximately $0.003 per paper (varies by content length)
- 225 papers ≈ $0.68 total
- Test mode (5 papers) ≈ $0.015

## Troubleshooting

### Token Issues
```bash
# Check if token is in .env file
cat .env | grep KILOCODE_TOKEN

# Test KiloCode configuration
python3 scripts/processing/kilocode_config.py
```

### Resume After Interruption
The script automatically saves progress. Simply run again to resume:
```bash
python3 scripts/processing/complete_relevancy_analysis.py
```

### Reset Progress
To start fresh:
```bash
rm relevancy_checkpoint.json
```

## Monitoring Progress

Check the log file in real-time:
```bash
tail -f relevancy_analysis.log
```

## Next Steps

After running:
1. Review the updated CSV file
2. Check log for any errors
3. Manually verify a sample of assignments
4. Rename output file if satisfied:
   ```bash
   mv research_papers_complete_updated.csv research_papers_complete.csv
   ```
# HDM Processing Scripts Refactored Architecture

This directory contains the refactored processing architecture for the Human Digital Memory (HDM) project. The refactoring improves code organization, error handling, configurability, and maintainability.

## Architecture Overview

### Core Framework (`core/`)
- **`config.py`** - Centralized configuration management with YAML + environment variable support
- **`base.py`** - Base processor classes with checkpoint management and recovery
- **`logger.py`** - Unified logging system with colored console output
- **`exceptions.py`** - Custom exception hierarchy for better error handling

### Processing Modules (`processors/`)
- **`pdf_converter.py`** - PDF to markdown conversion with multiple backend support (marker/pypdf)
- **`metadata_extractor.py`** - Metadata extraction and YAML frontmatter generation
- **`standardizer.py`** - Data standardization and normalization with configurable rules
- **`validator.py`** - Data quality validation and comprehensive reporting
- **`image_processor.py`** - Image description generation using AI models (Gemini)

### Pipeline Orchestration (`pipelines/`)
- **`paper_processing.py`** - Complete paper processing workflow with parallel execution
- **`data_integration.py`** - Data integration and merging pipelines *(planned)*
- **`quality_assurance.py`** - Quality assurance and validation workflows *(planned)*

### Command Line Interface (`cli/`)
- **`main.py`** - Unified CLI with subcommands for all processing operations

## Key Improvements

### 1. Dependency Injection & Configuration
- YAML configuration with environment variable overrides
- Configuration passed to all processors for consistency
- Easy to test and mock dependencies
- Clear separation of concerns

### 2. Error Handling & Recovery
- Structured exceptions with context and recovery hints
- Checkpoint-based recovery system for long-running processes
- Graceful degradation and fallback mechanisms
- Detailed error reporting and logging

### 3. Processing Features
- **Parallel Processing**: Multi-threaded execution for improved performance
- **Checkpoint Management**: Resume failed processing from last successful point
- **Batch Processing**: Efficient handling of large document sets
- **Quality Validation**: Comprehensive data quality checks and reporting

### 4. Logging & Monitoring
- Structured logging with configurable levels
- Colored console output for better readability
- File and console handlers with rotation
- Processing time tracking and performance metrics

### 5. Modular Design
- Single responsibility processors for specific tasks
- Composable pipeline architecture
- Easy to extend with new processors
- Clean interfaces and abstractions

## Quick Start

### 1. Setup Configuration
```bash
# Copy example configuration
cp scripts/refactored/config.example.yaml scripts/refactored/config.yaml

# Edit with your settings (paths, API keys)
nano scripts/refactored/config.yaml
```

### 2. Set Environment Variables
```bash
export GOOGLE_API_KEY="your-gemini-api-key"
export TURSO_DATABASE_URL="your-database-url"
export TURSO_AUTH_TOKEN="your-auth-token"
```

### 3. Run Processing Pipeline
```bash
# Process PDFs in new_papers directory
python -m scripts.refactored.cli.main process-papers new_papers/ \
  --parallel --workers 4 --report results.json
```

## Usage Examples

### Complete Paper Processing
```bash
# Full pipeline with all steps
python -m scripts.refactored.cli.main process-papers new_papers/ \
  --config config.yaml \
  --parallel \
  --workers 8 \
  --report pipeline_report.json

# Force reconversion of existing files
python -m scripts.refactored.cli.main process-papers new_papers/ \
  --force-reconvert \
  --skip-validation
```

### Individual Processing Steps
```bash
# Convert PDFs only (marker or pypdf)
python -m scripts.refactored.cli.main convert-pdf new_papers/ \
  --output markdown_papers/ \
  --tool marker \
  --force

# Extract and add metadata to markdown files
python -m scripts.refactored.cli.main extract-metadata markdown_papers/ \
  --sources missing_papers.json research_papers_complete.csv

# Process images with AI descriptions
python -m scripts.refactored.cli.main process-images markdown_papers/ \
  --model gemini \
  --index image_index.json
```

### Data Quality Operations
```bash
# Standardize data formats and values
python -m scripts.refactored.cli.main standardize-data research_papers.csv \
  --output standardized_papers.csv \
  --rules custom_rules.json

# Comprehensive data validation
python -m scripts.refactored.cli.main validate-data research_papers.csv \
  --report validation_report.json \
  --rules validation_rules.json
```

### Development & Debugging
```bash
# Dry run to see what would be processed
python -m scripts.refactored.cli.main process-papers new_papers/ \
  --dry-run \
  --log-level DEBUG

# Quiet mode for scripts
python -m scripts.refactored.cli.main convert-pdf new_papers/ --quiet
```

## Configuration

The system uses a hierarchical configuration approach:

**1. YAML Configuration File** (`config.yaml`):
```yaml
paths:
  base_dir: "/path/to/hdm"
  papers_dir: "papers"
  markdown_dir: "markdown_papers"
  
api:
  gemini_api_key: "your-key"
  timeout: 60
  max_retries: 3
  
processing:
  batch_size: 10
  max_workers: 4
  backup_enabled: true
  checkpoint_enabled: true
  
logging:
  level: "INFO"
  file_enabled: true
```

**2. Environment Variables** (override YAML):
- `TURSO_DATABASE_URL` - Database connection URL
- `TURSO_AUTH_TOKEN` - Database authentication token
- `GOOGLE_API_KEY` - Gemini AI API key
- `KILOCODE_API_TOKEN` - Kilocode service token
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `TEST_MODE` - Enable test mode (true/false)
- `DRY_RUN` - Enable dry run mode (true/false)

**3. Command Line Arguments** (override all):
- `--config` - Custom configuration file
- `--log-level` - Logging level
- `--dry-run` - Dry run mode
- `--parallel` - Enable parallel processing
- `--workers N` - Number of worker threads

## Processing Pipeline Details

### 1. PDF Conversion
- **Primary**: Marker library for high-quality conversion with image extraction
- **Fallback**: PyPDF for basic text extraction when Marker unavailable
- **Output**: Structured markdown with preserved formatting and images
- **Features**: Automatic image extraction, metadata preservation, error recovery

### 2. Metadata Extraction
- **Sources**: JSON files, CSV databases, existing YAML frontmatter
- **Processing**: Intelligent title/author extraction, cite key generation
- **Output**: YAML frontmatter added to markdown files
- **Features**: Conflict resolution, data validation, backup creation

### 3. Data Standardization
- **Rules**: Configurable standardization rules (format, value mapping, validation)
- **Processing**: Title cleaning, author formatting, cite key normalization
- **Output**: Standardized data with change tracking
- **Features**: Duplicate detection, consistency checking, format normalization

### 4. Data Validation
- **Checks**: Required fields, format validation, cross-field consistency
- **Quality**: Completeness scoring, error categorization, improvement suggestions
- **Output**: Detailed validation reports with actionable recommendations
- **Features**: Custom validation rules, quality thresholds, batch validation

### 5. Image Processing
- **AI Models**: Gemini 1.5 Flash for intelligent image description
- **Processing**: Alt text generation, detailed analysis, figure detection
- **Output**: Image descriptions in JSON format and updated markdown
- **Features**: Batch processing, index generation, fallback descriptions

## Performance & Scalability

### Parallel Processing
- Multi-threaded execution with configurable worker count
- Automatic load balancing across available CPU cores
- Memory-efficient batch processing for large document sets
- Progress tracking and real-time status updates

### Checkpoint Recovery
- Automatic checkpoint creation at key processing milestones
- Resume processing from last successful point after failures
- Granular recovery at individual paper level
- Configurable checkpoint frequency and retention

### Error Handling
- Structured exception hierarchy with recovery hints
- Graceful degradation when external services unavailable
- Comprehensive error logging with context preservation
- Automatic retry logic with exponential backoff

## Implementation Status

### ✅ Completed
- **Core Framework**: Configuration, logging, base classes, exception handling
- **PDF Processing**: Marker/PyPDF conversion with image extraction
- **Metadata Management**: YAML frontmatter generation with multi-source integration
- **Data Quality**: Standardization rules and comprehensive validation
- **Image Processing**: AI-powered description generation with Gemini
- **Pipeline Orchestration**: Complete paper processing workflow with parallel execution
- **CLI Interface**: Full command-line interface with subcommands and options

### 🚧 In Progress
- Data integration pipelines for merging multiple data sources
- Quality assurance workflows for automated QA processes
- Advanced error recovery mechanisms
- Performance optimization and caching

### 📋 Planned
- Web API interface for remote processing
- Real-time monitoring dashboard with metrics
- Advanced analytics and reporting capabilities
- Integration with existing HDM visualization tools
- Docker containerization for deployment

## Migration from Legacy Scripts

The refactored architecture replaces and improves upon these legacy scripts:

| Legacy Script | New Component | Improvements |
|---------------|---------------|--------------|
| `smart_converter.py` | `processors/pdf_converter.py` | Multi-backend, error recovery, parallel processing |
| `process_new_papers_batch.py` | `pipelines/paper_processing.py` | Modular design, checkpoint recovery, comprehensive reporting |
| Various metadata scripts | `processors/metadata_extractor.py` | Unified interface, multi-source support, validation |
| Manual validation processes | `processors/validator.py` | Automated quality checks, detailed reporting, configurable rules |
| Ad-hoc image processing | `processors/image_processor.py` | AI-powered descriptions, batch processing, index generation |

### Migration Steps
1. **Configuration**: Set up `config.yaml` with your existing paths and settings
2. **Testing**: Run new pipeline on small test set to verify compatibility
3. **Full Migration**: Process existing papers through new pipeline
4. **Verification**: Compare outputs and validate data integrity
5. **Legacy Cleanup**: Archive old scripts and update documentation

Legacy scripts are preserved in `/scripts/legacy/` for reference and fallback scenarios.
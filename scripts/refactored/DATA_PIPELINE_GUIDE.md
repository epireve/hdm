# HDM Data Pipeline Guide

This guide covers the comprehensive data pipeline architecture for the Human Digital Memory (HDM) project, including data integration, quality assurance, and orchestration capabilities.

## Overview

The HDM data pipeline provides a robust, scalable system for processing academic research papers from raw PDFs to a fully integrated knowledge graph. The pipeline consists of multiple stages with automatic error recovery, quality validation, and comprehensive monitoring.

## Pipeline Architecture

### 1. Pipeline Stages

The complete data pipeline consists of seven main stages:

1. **Initialization** - Environment validation and setup
2. **Paper Processing** - PDF conversion and metadata extraction
3. **Data Integration** - Multi-source data merging and deduplication
4. **Quality Assurance** - Comprehensive data validation and reporting
5. **Knowledge Graph Generation** - Graph construction and relationship extraction
6. **Visualization Update** - Update visualization data and interfaces
7. **Finalization** - Cleanup and reporting

### 2. Core Components

#### Data Integration Pipeline (`data_integration.py`)
- **Purpose**: Merge multiple data sources with conflict resolution
- **Features**: Fuzzy matching, exact matching, append-only modes
- **Capabilities**: Duplicate detection, data lineage tracking, comprehensive reporting

#### Quality Assurance Pipeline (`quality_assurance.py`)
- **Purpose**: Automated data quality validation and monitoring
- **Features**: 12+ built-in quality checks, customizable thresholds, alert generation
- **Capabilities**: Statistical analysis, outlier detection, schema validation

#### Data Flow Orchestrator (`data_flow_orchestrator.py`)
- **Purpose**: End-to-end pipeline execution and monitoring
- **Features**: Stage dependencies, retry logic, parallel execution
- **Capabilities**: Real-time status tracking, execution reports, failure recovery

## Usage Examples

### 1. Complete Pipeline Execution

Run the entire HDM data pipeline with all stages:

```bash
# Basic pipeline execution
python -m scripts.refactored.cli.main run-pipeline

# With custom trigger and configuration
python -m scripts.refactored.cli.main run-pipeline \
  --trigger "scheduled_daily" \
  --config config.yaml
```

### 2. Data Integration

Merge multiple data sources with various strategies:

```bash
# Fuzzy matching integration (default)
python -m scripts.refactored.cli.main integrate-data \
  --sources research_papers_complete.csv missing_papers.json \
  --output integrated_papers.csv \
  --strategy fuzzy_match \
  --threshold 0.85

# Exact matching integration
python -m scripts.refactored.cli.main integrate-data \
  --sources papers_v1.csv papers_v2.csv \
  --output merged_papers.csv \
  --strategy exact_match \
  --key-field cite_key

# Append-only integration (no deduplication)
python -m scripts.refactored.cli.main integrate-data \
  --sources old_papers.csv new_papers.csv \
  --output all_papers.csv \
  --strategy append_only
```

### 3. Quality Assurance

Run comprehensive data quality checks:

```bash
# Full quality assessment
python -m scripts.refactored.cli.main quality-assurance \
  research_papers_complete.csv \
  --report quality_report.json

# Specific quality checks
python -m scripts.refactored.cli.main quality-assurance \
  data.csv \
  --checks required_fields_present duplicate_detection \
  --report focused_qa_report.json
```

### 4. Pipeline Monitoring

Monitor pipeline execution status:

```bash
# List all active pipeline executions
python -m scripts.refactored.cli.main pipeline-status

# Check specific execution
python -m scripts.refactored.cli.main pipeline-status \
  --execution-id exec_20250712_143022_a1b2c3d4
```

## Configuration

### Pipeline Configuration

Create a pipeline configuration file (`pipeline_config.yaml`):

```yaml
stages:
  initialization:
    enabled: true
    timeout_seconds: 300
    parameters:
      validate_environment: true
  
  paper_processing:
    enabled: true
    timeout_seconds: 3600
    parallel_execution: true
    max_workers: 4
    parameters:
      process_new_papers: true
      force_reconvert: false
      include_images: true
  
  data_integration:
    enabled: true
    timeout_seconds: 1800
    parameters:
      merge_strategy: "fuzzy_match"
      similarity_threshold: 0.85
  
  quality_assurance:
    enabled: true
    timeout_seconds: 600
    parameters:
      run_all_checks: true
```

### Data Integration Configuration

Configure data sources programmatically:

```python
from scripts.refactored.pipelines import DataIntegrationPipeline, DataSource, MergeStrategy
from scripts.refactored.core import Config

config = Config.load('config.yaml')
pipeline = DataIntegrationPipeline(config)

# Add data sources
pipeline.add_data_source(DataSource(
    name="primary_research_data",
    file_path=Path("research_papers_complete.csv"),
    file_type="csv",
    key_field="cite_key",
    priority=10
))

pipeline.add_data_source(DataSource(
    name="supplementary_data",
    file_path=Path("missing_papers.json"),
    file_type="json",
    key_field="cite_key",
    priority=5
))

# Configure merge strategy
merge_strategy = MergeStrategy(
    strategy_type="fuzzy_match",
    match_threshold=0.85,
    conflict_resolution="merge",
    duplicate_handling="keep_first"
)

# Execute integration
result = pipeline.process_item(merge_strategy)
```

## Data Integration Strategies

### 1. Exact Match Strategy

- **Use Case**: Clean, consistent data with reliable key fields
- **Method**: Direct key field matching
- **Conflict Resolution**: Priority-based or merge-based
- **Performance**: Fastest, O(n) complexity

```python
MergeStrategy(
    strategy_type="exact_match",
    conflict_resolution="priority",  # or "merge"
    duplicate_handling="keep_first"
)
```

### 2. Fuzzy Match Strategy

- **Use Case**: Inconsistent data with potential typos or variations
- **Method**: String similarity matching using SequenceMatcher
- **Threshold**: Configurable similarity threshold (0.0-1.0)
- **Performance**: Moderate, O(n²) complexity

```python
MergeStrategy(
    strategy_type="fuzzy_match",
    match_threshold=0.85,  # 85% similarity required
    conflict_resolution="merge",
    duplicate_handling="keep_first"
)
```

### 3. Append-Only Strategy

- **Use Case**: Temporal data updates where duplicates are acceptable
- **Method**: Simple concatenation with source tracking
- **Performance**: Fastest, O(n) complexity
- **Result**: All records preserved with source metadata

```python
MergeStrategy(
    strategy_type="append_only",
    duplicate_handling="keep_all"
)
```

## Quality Assurance Framework

### Built-in Quality Checks

1. **Data Completeness**
   - Required fields presence
   - Overall completeness rate
   - Field coverage analysis

2. **Data Validity**
   - Year range validation
   - DOI format checking
   - URL accessibility testing

3. **Business Rules**
   - Duplicate detection
   - Cite key uniqueness
   - Relevancy consistency

4. **Schema Validation**
   - Schema compliance checking
   - Data type consistency
   - Field format validation

5. **Statistical Analysis**
   - Outlier detection
   - Distribution analysis
   - Trend identification

### Quality Thresholds

Configure quality thresholds for automated monitoring:

```python
from scripts.refactored.pipelines import QualityThreshold

thresholds = [
    QualityThreshold("completeness_rate", min_value=0.8),
    QualityThreshold("duplicate_rate", max_value=0.05),
    QualityThreshold("error_rate", max_value=0.02),
    QualityThreshold("schema_compliance_rate", min_value=0.95)
]
```

### Custom Quality Checks

Create custom quality checks:

```python
from scripts.refactored.pipelines import QualityCheck

custom_check = QualityCheck(
    name="publication_venue_validation",
    description="Validate publication venue formats",
    check_type="business_rule",
    check_function="validate_publication_venues",
    parameters={"allowed_venues": ["arXiv", "IEEE", "ACM"]},
    severity="warning"
)
```

## Error Handling and Recovery

### Checkpoint-Based Recovery

The pipeline automatically creates checkpoints at key stages:

- **Individual Record Level**: Track processing status for each paper
- **Stage Level**: Record completion status for each pipeline stage
- **Execution Level**: Maintain overall pipeline execution state

### Retry Logic

Configurable retry mechanisms for transient failures:

```python
StageConfig(
    stage=PipelineStage.PAPER_PROCESSING,
    retry_count=3,
    retry_delay=5.0,  # seconds
    timeout_seconds=3600
)
```

### Graceful Degradation

The pipeline continues execution even when non-critical stages fail:

- **Critical Stages**: Initialization, Paper Processing, Data Integration
- **Non-Critical Stages**: Quality Assurance, Visualization Update
- **Failure Handling**: Log errors, mark stages as failed, continue with remaining stages

## Monitoring and Reporting

### Execution Reports

Each pipeline execution generates comprehensive reports:

```json
{
  "execution_id": "exec_20250712_143022_a1b2c3d4",
  "start_time": "2025-07-12T14:30:22.123456",
  "end_time": "2025-07-12T15:45:33.987654",
  "duration_seconds": 4511.864,
  "overall_status": "completed",
  "stages": {
    "total": 7,
    "completed": 6,
    "failed": 1,
    "completed_list": ["initialization", "paper_processing", "data_integration", "quality_assurance", "visualization_update", "finalization"],
    "failed_list": ["knowledge_graph_generation"]
  }
}
```

### Quality Reports

Quality assurance generates detailed reports:

```json
{
  "timestamp": "2025-07-12T15:30:22.123456",
  "quality_score": 0.847,
  "data_summary": {
    "total_records": 1430,
    "total_fields": 21,
    "avg_field_coverage": 0.892
  },
  "check_summary": {
    "total_checks": 12,
    "passed_checks": 10,
    "failed_checks": 2
  },
  "alert_summary": {
    "total_alerts": 5,
    "error_alerts": 1,
    "warning_alerts": 4
  }
}
```

### Integration Reports

Data integration provides detailed merge analysis:

```json
{
  "integration_summary": {
    "total_input_records": 1500,
    "merged_records": 1430,
    "duplicate_reduction": 70,
    "conflicts_detected": 12,
    "data_reduction_rate": 0.047
  },
  "sources": {
    "research_papers_complete": {
      "records_loaded": 1200,
      "standardization_rate": 0.95
    },
    "missing_papers": {
      "records_loaded": 300,
      "standardization_rate": 0.87
    }
  }
}
```

## Performance Optimization

### Parallel Processing

Enable parallel processing for CPU-intensive operations:

```bash
# Enable parallel processing with 8 workers
python -m scripts.refactored.cli.main run-pipeline \
  --config config.yaml \
  --parallel \
  --workers 8
```

### Memory Management

For large datasets, configure batch processing:

```yaml
processing:
  batch_size: 50  # Process 50 records at a time
  max_workers: 4
  checkpoint_enabled: true  # Enable checkpointing
```

### Caching

Implement caching for expensive operations:

- **PDF Conversion**: Cache converted markdown files
- **Metadata Extraction**: Cache extracted metadata
- **Quality Checks**: Cache check results for unchanged data

## Best Practices

### 1. Data Source Management

- **Version Control**: Track data source versions and changes
- **Schema Evolution**: Document schema changes and migration paths
- **Data Lineage**: Maintain traceability from source to final output

### 2. Quality Assurance

- **Regular Monitoring**: Run quality checks on schedule
- **Threshold Tuning**: Adjust quality thresholds based on data characteristics
- **Alert Management**: Configure appropriate alert channels and escalation

### 3. Pipeline Operations

- **Incremental Processing**: Process only new or changed data when possible
- **Rollback Capability**: Maintain ability to rollback to previous versions
- **Monitoring**: Set up comprehensive monitoring and alerting

### 4. Testing

- **Unit Tests**: Test individual pipeline components
- **Integration Tests**: Test end-to-end pipeline execution
- **Data Quality Tests**: Validate output data quality

## Troubleshooting

### Common Issues

1. **Memory Errors**
   - Reduce batch size in configuration
   - Enable memory profiling
   - Check for memory leaks in custom processors

2. **Timeout Errors**
   - Increase timeout values for slow operations
   - Enable parallel processing
   - Optimize query performance

3. **Data Quality Issues**
   - Review quality check results
   - Adjust quality thresholds
   - Implement data cleaning steps

4. **Integration Conflicts**
   - Review merge strategy configuration
   - Adjust similarity thresholds
   - Implement custom conflict resolution

### Debugging

Enable debug logging for detailed troubleshooting:

```bash
python -m scripts.refactored.cli.main run-pipeline \
  --log-level DEBUG \
  --config config.yaml
```

Check execution logs:

```bash
# View recent pipeline executions
cat logs/pipeline_executions.json | jq '.executions[-5:]'

# View specific processor logs
tail -f logs/data_integration_20250712.log
```

## Advanced Usage

### Custom Processors

Create custom processors by extending the base classes:

```python
from scripts.refactored.core import BaseProcessor, ProcessingResult, ProcessingStatus

class CustomDataProcessor(BaseProcessor):
    def process_item(self, item, **kwargs):
        # Custom processing logic
        return ProcessingResult(
            status=ProcessingStatus.COMPLETED,
            message="Custom processing completed",
            data={'processed_item': item}
        )
```

### Custom Pipeline Stages

Add custom stages to the pipeline:

```python
from scripts.refactored.pipelines import DataFlowOrchestrator, StageConfig, PipelineStage

# Define custom stage
class CustomStage(Enum):
    CUSTOM_PROCESSING = "custom_processing"

# Add to orchestrator
orchestrator = DataFlowOrchestrator(config)
orchestrator.stage_configs[CustomStage.CUSTOM_PROCESSING] = StageConfig(
    stage=CustomStage.CUSTOM_PROCESSING,
    enabled=True,
    dependencies=[PipelineStage.DATA_INTEGRATION],
    timeout_seconds=600
)
```

### API Integration

Integrate with external APIs:

```python
from scripts.refactored.processors import MetadataExtractorProcessor

class APIEnhancedMetadataExtractor(MetadataExtractorProcessor):
    def __init__(self, config, api_client):
        super().__init__(config)
        self.api_client = api_client
    
    def process_item(self, markdown_path, **kwargs):
        # Enhanced processing with API calls
        result = super().process_item(markdown_path, **kwargs)
        
        if result.status == ProcessingStatus.COMPLETED:
            # Enhance with API data
            enhanced_data = self.api_client.enhance_metadata(result.data)
            result.data.update(enhanced_data)
        
        return result
```

## Migration Guide

### From Legacy Scripts

To migrate from legacy processing scripts:

1. **Identify Current Workflows**: Map existing scripts to pipeline stages
2. **Data Mapping**: Ensure data compatibility with new schema
3. **Testing**: Run parallel processing to validate results
4. **Gradual Migration**: Migrate one stage at a time
5. **Validation**: Compare outputs to ensure consistency

### Legacy Script Mapping

| Legacy Script | New Component | Migration Notes |
|---------------|---------------|-----------------|
| `smart_converter.py` | `PDFConverterProcessor` | Configuration updates required |
| `process_new_papers_batch.py` | `PaperProcessingPipeline` | Batch size and checkpoint settings |
| Various data merging scripts | `DataIntegrationPipeline` | Merge strategy configuration |
| Manual QA processes | `QualityAssurancePipeline` | Custom check implementation |

This comprehensive data pipeline provides a robust foundation for scaling HDM data processing to handle larger datasets and more complex integration scenarios while maintaining data quality and operational reliability.
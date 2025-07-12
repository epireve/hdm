#!/usr/bin/env python3
"""
Command-line interface for HDM processing pipeline.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from ..core import Config, setup_logger
from ..pipelines import (
    PaperProcessingPipeline, PipelineConfig,
    DataIntegrationPipeline, DataSource, MergeStrategy,
    QualityAssurancePipeline,
    DataFlowOrchestrator
)
from ..processors import (
    PDFConverterProcessor,
    MetadataExtractorProcessor,
    DataStandardizerProcessor,
    DataValidatorProcessor,
    ImageProcessor
)
from ..utils import CleanupHelper


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="HDM Paper Processing Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Process all PDFs in new_papers directory
  python -m scripts.refactored.cli.main process-papers new_papers/
  
  # Convert PDFs only
  python -m scripts.refactored.cli.main convert-pdf new_papers/ --output markdown_papers/
  
  # Extract metadata for existing markdown files
  python -m scripts.refactored.cli.main extract-metadata markdown_papers/
  
  # Validate data quality
  python -m scripts.refactored.cli.main validate-data research_papers_complete.csv
  
  # Full pipeline with custom config
  python -m scripts.refactored.cli.main process-papers new_papers/ --config config.yaml --parallel --workers 8
        '''
    )
    
    # Global options
    parser.add_argument(
        '--config', '-c',
        type=Path,
        help='Configuration file path (YAML format)'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without executing'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress non-error output'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Full data pipeline command
    pipeline_parser = subparsers.add_parser(
        'run-pipeline',
        help='Run complete HDM data pipeline (all stages)'
    )
    pipeline_parser.add_argument(
        '--trigger',
        default='manual',
        help='Pipeline trigger event (default: manual)'
    )
    pipeline_parser.add_argument(
        '--stages',
        nargs='+',
        help='Specific stages to run (default: all enabled stages)'
    )
    pipeline_parser.add_argument(
        '--config-file',
        type=Path,
        help='Pipeline configuration file'
    )
    
    # Process papers command (single stage)
    process_parser = subparsers.add_parser(
        'process-papers',
        help='Run paper processing pipeline (single stage)'
    )
    process_parser.add_argument(
        'input_dir',
        type=Path,
        help='Directory containing PDF files to process'
    )
    process_parser.add_argument(
        '--force-reconvert',
        action='store_true',
        help='Force reconversion of existing markdown files'
    )
    process_parser.add_argument(
        '--skip-images',
        action='store_true',
        help='Skip image processing step'
    )
    process_parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip data validation step'
    )
    process_parser.add_argument(
        '--parallel',
        action='store_true',
        help='Enable parallel processing'
    )
    process_parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    process_parser.add_argument(
        '--report',
        type=Path,
        help='Output file for processing report'
    )
    
    # Convert PDF command
    convert_parser = subparsers.add_parser(
        'convert-pdf',
        help='Convert PDF files to markdown'
    )
    convert_parser.add_argument(
        'input_dir',
        type=Path,
        help='Directory containing PDF files'
    )
    convert_parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output directory for markdown files'
    )
    convert_parser.add_argument(
        '--tool',
        choices=['marker', 'pypdf'],
        default='marker',
        help='PDF conversion tool (default: marker)'
    )
    convert_parser.add_argument(
        '--force',
        action='store_true',
        help='Force reconversion of existing files'
    )
    
    # Extract metadata command
    metadata_parser = subparsers.add_parser(
        'extract-metadata',
        help='Extract and add metadata to markdown files'
    )
    metadata_parser.add_argument(
        'input_dir',
        type=Path,
        help='Directory containing markdown files'
    )
    metadata_parser.add_argument(
        '--sources',
        nargs='+',
        help='Metadata source files (JSON, CSV)'
    )
    
    # Process images command
    images_parser = subparsers.add_parser(
        'process-images',
        help='Process images in paper directories'
    )
    images_parser.add_argument(
        'papers_dir',
        type=Path,
        help='Directory containing paper directories'
    )
    images_parser.add_argument(
        '--model',
        choices=['gemini', 'fallback'],
        default='gemini',
        help='Description generation model (default: gemini)'
    )
    images_parser.add_argument(
        '--index',
        type=Path,
        help='Generate image index file'
    )
    
    # Standardize data command
    standardize_parser = subparsers.add_parser(
        'standardize-data',
        help='Standardize data formats and values'
    )
    standardize_parser.add_argument(
        'input_file',
        type=Path,
        help='Input CSV file to standardize'
    )
    standardize_parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output file for standardized data'
    )
    standardize_parser.add_argument(
        '--rules',
        type=Path,
        help='Custom standardization rules file (JSON)'
    )
    
    # Validate data command
    validate_parser = subparsers.add_parser(
        'validate-data',
        help='Validate data quality and completeness'
    )
    validate_parser.add_argument(
        'input_file',
        type=Path,
        help='Input CSV file to validate'
    )
    validate_parser.add_argument(
        '--report', '-r',
        type=Path,
        help='Output file for validation report'
    )
    validate_parser.add_argument(
        '--rules',
        type=Path,
        help='Custom validation rules file (JSON)'
    )
    
    # Data integration command
    integrate_parser = subparsers.add_parser(
        'integrate-data',
        help='Integrate multiple data sources'
    )
    integrate_parser.add_argument(
        '--sources',
        nargs='+',
        type=Path,
        required=True,
        help='Data source files to integrate'
    )
    integrate_parser.add_argument(
        '--output', '-o',
        type=Path,
        required=True,
        help='Output file for integrated data'
    )
    integrate_parser.add_argument(
        '--strategy',
        choices=['exact_match', 'fuzzy_match', 'append_only'],
        default='fuzzy_match',
        help='Merge strategy (default: fuzzy_match)'
    )
    integrate_parser.add_argument(
        '--threshold',
        type=float,
        default=0.85,
        help='Similarity threshold for fuzzy matching (default: 0.85)'
    )
    integrate_parser.add_argument(
        '--key-field',
        default='cite_key',
        help='Field to use for matching records (default: cite_key)'
    )
    
    # Quality assurance command
    qa_parser = subparsers.add_parser(
        'quality-assurance',
        help='Run comprehensive quality assurance checks'
    )
    qa_parser.add_argument(
        'input_file',
        type=Path,
        help='Data file to analyze'
    )
    qa_parser.add_argument(
        '--report', '-r',
        type=Path,
        help='Output file for QA report'
    )
    qa_parser.add_argument(
        '--checks',
        nargs='+',
        help='Specific quality checks to run'
    )
    
    # Pipeline status command
    status_parser = subparsers.add_parser(
        'pipeline-status',
        help='Check status of running pipelines'
    )
    status_parser.add_argument(
        '--execution-id',
        help='Specific execution ID to check'
    )
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser(
        'cleanup',
        help='Analyze and clean up redundant files'
    )
    cleanup_parser.add_argument(
        '--analyze-only',
        action='store_true',
        help='Only analyze, do not execute cleanup'
    )
    cleanup_parser.add_argument(
        '--risk-level',
        choices=['low', 'medium', 'high'],
        default='low',
        help='Maximum risk level for cleanup execution (default: low)'
    )
    cleanup_parser.add_argument(
        '--report',
        type=Path,
        help='Output file for cleanup report'
    )
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Setup logging
    log_level = 'ERROR' if args.quiet else args.log_level
    logger = setup_logger(__name__)
    
    try:
        # Load configuration
        config = Config.load(args.config)
        
        # Override config with CLI arguments
        if args.dry_run:
            config.processing.dry_run = True
        if hasattr(args, 'log_level'):
            config.logging.level = log_level
        
        # Execute command
        if args.command == 'run-pipeline':
            return cmd_run_pipeline(args, config, logger)
        elif args.command == 'process-papers':
            return cmd_process_papers(args, config, logger)
        elif args.command == 'convert-pdf':
            return cmd_convert_pdf(args, config, logger)
        elif args.command == 'extract-metadata':
            return cmd_extract_metadata(args, config, logger)
        elif args.command == 'process-images':
            return cmd_process_images(args, config, logger)
        elif args.command == 'standardize-data':
            return cmd_standardize_data(args, config, logger)
        elif args.command == 'validate-data':
            return cmd_validate_data(args, config, logger)
        elif args.command == 'integrate-data':
            return cmd_integrate_data(args, config, logger)
        elif args.command == 'quality-assurance':
            return cmd_quality_assurance(args, config, logger)
        elif args.command == 'pipeline-status':
            return cmd_pipeline_status(args, config, logger)
        elif args.command == 'cleanup':
            return cmd_cleanup(args, config, logger)
        else:
            parser.print_help()
            return 1
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.log_level == 'DEBUG':
            import traceback
            traceback.print_exc()
        return 1


def cmd_process_papers(args, config: Config, logger) -> int:
    """Run complete paper processing pipeline."""
    if not args.input_dir.exists():
        logger.error(f"Input directory not found: {args.input_dir}")
        return 1
    
    # Configure pipeline
    pipeline_config = PipelineConfig(
        force_reconvert=args.force_reconvert,
        process_images=not args.skip_images,
        validate_data=not args.skip_validation,
        parallel_processing=args.parallel,
        max_workers=args.workers
    )
    
    # Run pipeline
    pipeline = PaperProcessingPipeline(config, pipeline_config)
    logger.info(f"Starting paper processing pipeline for {args.input_dir}")
    
    results = pipeline.process_directory(args.input_dir)
    
    # Generate report
    report = pipeline.generate_pipeline_report(results, args.report)
    
    # Print summary
    summary = report.get('summary', {})
    logger.info(f"Pipeline completed:")
    logger.info(f"  Total papers: {summary.get('total_papers', 0)}")
    logger.info(f"  Successful: {summary.get('successful', 0)}")
    logger.info(f"  Failed: {summary.get('failed', 0)}")
    logger.info(f"  Success rate: {summary.get('success_rate', 0):.1%}")
    
    return 0 if summary.get('failed', 0) == 0 else 1


def cmd_convert_pdf(args, config: Config, logger) -> int:
    """Convert PDF files to markdown."""
    if not args.input_dir.exists():
        logger.error(f"Input directory not found: {args.input_dir}")
        return 1
    
    # Override output directory if specified
    if args.output:
        config.paths.markdown_dir = args.output
    
    # Run conversion
    converter = PDFConverterProcessor(config, conversion_tool=args.tool)
    logger.info(f"Converting PDFs from {args.input_dir}")
    
    results = converter.batch_convert(args.input_dir, force_reconvert=args.force)
    
    # Print summary
    successful = sum(1 for r in results if r.status.value == 'completed')
    failed = sum(1 for r in results if r.status.value == 'failed')
    
    logger.info(f"Conversion completed: {successful} successful, {failed} failed")
    
    return 0 if failed == 0 else 1


def cmd_extract_metadata(args, config: Config, logger) -> int:
    """Extract metadata for markdown files."""
    if not args.input_dir.exists():
        logger.error(f"Input directory not found: {args.input_dir}")
        return 1
    
    # Configure metadata sources
    sources = args.sources if args.sources else None
    
    # Run metadata extraction
    extractor = MetadataExtractorProcessor(config, metadata_sources=sources)
    logger.info(f"Extracting metadata for files in {args.input_dir}")
    
    results = extractor.batch_process_directory(args.input_dir)
    
    # Print summary
    successful = sum(1 for r in results if r.status.value == 'completed')
    failed = sum(1 for r in results if r.status.value == 'failed')
    
    logger.info(f"Metadata extraction completed: {successful} successful, {failed} failed")
    
    return 0 if failed == 0 else 1


def cmd_process_images(args, config: Config, logger) -> int:
    """Process images in paper directories."""
    if not args.papers_dir.exists():
        logger.error(f"Papers directory not found: {args.papers_dir}")
        return 1
    
    # Run image processing
    processor = ImageProcessor(config, description_model=args.model)
    logger.info(f"Processing images in {args.papers_dir}")
    
    results = processor.batch_process_papers(args.papers_dir)
    
    # Generate index if requested
    if args.index:
        index_result = processor.generate_image_index(args.papers_dir, args.index)
        logger.info(f"Image index: {index_result.message}")
    
    # Print summary
    successful = sum(1 for r in results if r.status.value == 'completed')
    failed = sum(1 for r in results if r.status.value == 'failed')
    
    logger.info(f"Image processing completed: {successful} successful, {failed} failed")
    
    return 0 if failed == 0 else 1


def cmd_standardize_data(args, config: Config, logger) -> int:
    """Standardize data formats."""
    if not args.input_file.exists():
        logger.error(f"Input file not found: {args.input_file}")
        return 1
    
    # Run standardization
    standardizer = DataStandardizerProcessor(config, rules_file=args.rules)
    logger.info(f"Standardizing data in {args.input_file}")
    
    result = standardizer.standardize_csv_file(args.input_file, args.output)
    
    logger.info(f"Standardization: {result.message}")
    
    return 0 if result.status.value == 'completed' else 1


def cmd_validate_data(args, config: Config, logger) -> int:
    """Validate data quality."""
    if not args.input_file.exists():
        logger.error(f"Input file not found: {args.input_file}")
        return 1
    
    # Load data
    import pandas as pd
    df = pd.read_csv(args.input_file)
    data_list = df.to_dict('records')
    
    # Run validation
    validator = DataValidatorProcessor(config)
    logger.info(f"Validating data in {args.input_file}")
    
    result = validator.validate_dataset(data_list)
    
    # Export report if requested
    if args.report and result.status.value == 'completed':
        validator.export_validation_report(result, args.report)
    
    # Print summary
    if result.data:
        summary = result.data.get('summary', {})
        logger.info(f"Validation completed:")
        logger.info(f"  Total records: {result.data.get('total_records', 0)}")
        logger.info(f"  Average quality: {result.data.get('average_quality', 0):.3f}")
        logger.info(f"  Error records: {result.data.get('error_records', 0)}")
        logger.info(f"  Total issues: {summary.get('total_issues', 0)}")
    
    return 0 if result.status.value == 'completed' else 1


def cmd_run_pipeline(args, config: Config, logger) -> int:
    """Run complete HDM data pipeline."""
    # Create orchestrator
    orchestrator = DataFlowOrchestrator(config)
    
    logger.info("Starting complete HDM data pipeline")
    
    # Run pipeline
    result = orchestrator.process_item(trigger_event=args.trigger)
    
    # Print results
    if result.data:
        execution_report = result.data.get('execution_report', {})
        stages = execution_report.get('stages', {})
        
        logger.info(f"Pipeline execution completed:")
        logger.info(f"  Execution ID: {result.data.get('execution_id', 'unknown')}")
        logger.info(f"  Status: {result.status.value}")
        logger.info(f"  Stages completed: {stages.get('completed', 0)}/{stages.get('total', 0)}")
        logger.info(f"  Duration: {execution_report.get('duration_seconds', 0):.1f} seconds")
        
        if stages.get('failed', 0) > 0:
            failed_stages = execution_report.get('stages', {}).get('failed_list', [])
            logger.warning(f"  Failed stages: {', '.join(failed_stages)}")
    
    return 0 if result.status.value == 'completed' else 1


def cmd_integrate_data(args, config: Config, logger) -> int:
    """Integrate multiple data sources."""
    # Create integration pipeline
    pipeline = DataIntegrationPipeline(config)
    
    # Add data sources
    for i, source_file in enumerate(args.sources):
        if not source_file.exists():
            logger.error(f"Source file not found: {source_file}")
            return 1
        
        pipeline.add_data_source(DataSource(
            name=f"source_{i+1}",
            file_path=source_file,
            file_type=source_file.suffix[1:],  # Remove dot
            key_field=args.key_field,
            priority=len(args.sources) - i  # First file has highest priority
        ))
    
    # Configure merge strategy
    merge_strategy = MergeStrategy(
        strategy_type=args.strategy,
        match_threshold=args.threshold,
        conflict_resolution='merge',
        duplicate_handling='keep_first'
    )
    
    logger.info(f"Integrating {len(args.sources)} data sources using {args.strategy} strategy")
    
    # Run integration
    result = pipeline.process_item(merge_strategy)
    
    if result.status.value == 'completed' and result.data:
        # Export merged data
        merged_data = result.data.get('merged_data', [])
        export_result = pipeline.export_merged_data(merged_data, args.output)
        
        # Print summary
        integration_report = result.data.get('integration_report', {})
        summary = integration_report.get('integration_summary', {})
        
        logger.info(f"Data integration completed:")
        logger.info(f"  Input records: {summary.get('total_input_records', 0)}")
        logger.info(f"  Merged records: {summary.get('merged_records', 0)}")
        logger.info(f"  Duplicates removed: {summary.get('duplicate_reduction', 0)}")
        logger.info(f"  Output file: {args.output}")
        
        return 0
    else:
        logger.error(f"Data integration failed: {result.message}")
        return 1


def cmd_quality_assurance(args, config: Config, logger) -> int:
    """Run quality assurance checks."""
    if not args.input_file.exists():
        logger.error(f"Input file not found: {args.input_file}")
        return 1
    
    # Create QA pipeline
    qa_pipeline = QualityAssurancePipeline(config)
    
    logger.info(f"Running quality assurance on {args.input_file}")
    
    # Run QA
    result = qa_pipeline.process_item(args.input_file)
    
    # Export report if requested
    if args.report and result.data:
        quality_report = result.data.get('quality_report')
        if quality_report:
            qa_pipeline.export_quality_report(quality_report, args.report)
            logger.info(f"QA report exported to {args.report}")
    
    # Print summary
    if result.data:
        quality_report = result.data.get('quality_report', {})
        data_summary = result.data.get('data_summary', {})
        alerts = result.data.get('alerts', [])
        
        logger.info(f"Quality assurance completed:")
        logger.info(f"  Records analyzed: {data_summary.get('total_records', 0)}")
        logger.info(f"  Quality score: {quality_report.get('quality_score', 0):.3f}")
        logger.info(f"  Alerts generated: {len(alerts)}")
        
        # Show alerts by severity
        error_alerts = [a for a in alerts if a.get('severity') == 'error']
        warning_alerts = [a for a in alerts if a.get('severity') == 'warning']
        
        if error_alerts:
            logger.error(f"  Error alerts: {len(error_alerts)}")
        if warning_alerts:
            logger.warning(f"  Warning alerts: {len(warning_alerts)}")
    
    return 0 if result.status.value == 'completed' else 1


def cmd_pipeline_status(args, config: Config, logger) -> int:
    """Check pipeline execution status."""
    # Create orchestrator to check status
    orchestrator = DataFlowOrchestrator(config)
    
    if args.execution_id:
        # Check specific execution
        status = orchestrator.get_execution_status(args.execution_id)
        if status:
            logger.info(f"Execution {args.execution_id}:")
            logger.info(f"  Status: {status['status']}")
            logger.info(f"  Current stage: {status.get('current_stage', 'None')}")
            logger.info(f"  Completed stages: {', '.join(status['completed_stages'])}")
            if status['failed_stages']:
                logger.info(f"  Failed stages: {', '.join(status['failed_stages'])}")
        else:
            logger.error(f"Execution {args.execution_id} not found")
            return 1
    else:
        # List all active executions
        active_executions = orchestrator.list_active_executions()
        if active_executions:
            logger.info(f"Active pipeline executions: {len(active_executions)}")
            for execution in active_executions:
                logger.info(f"  {execution['execution_id']}: {execution['status']} ({execution.get('current_stage', 'unknown')})")
        else:
            logger.info("No active pipeline executions")
    
    return 0


def cmd_cleanup(args, config: Config, logger) -> int:
    """Analyze and clean up redundant files."""
    # Create cleanup helper
    cleanup_helper = CleanupHelper(config)
    
    logger.info("Analyzing project for cleanup opportunities...")
    
    # Run analysis
    analysis_result = cleanup_helper.analyze_project()
    
    if analysis_result.status.value != 'completed':
        logger.error(f"Analysis failed: {analysis_result.message}")
        return 1
    
    # Print analysis results
    data = analysis_result.data
    logger.info(f"Analysis completed:")
    logger.info(f"  Files scanned: {data.get('total_files_scanned', 0)}")
    logger.info(f"  Duplicate groups: {data.get('duplicate_groups', 0)}")
    logger.info(f"  Large files: {data.get('large_files', 0)}")
    logger.info(f"  Redundant scripts: {data.get('redundant_scripts', 0)}")
    logger.info(f"  Temp files: {data.get('temp_files', 0)}")
    logger.info(f"  Potential space saved: {data.get('potential_space_saved_mb', 0):.1f}MB")
    logger.info(f"  Cleanup suggestions: {len(data.get('cleanup_suggestions', []))}")
    
    # Generate report if requested
    if args.report:
        cleanup_helper.generate_cleanup_report(analysis_result, args.report)
        logger.info(f"Detailed report saved to {args.report}")
    
    # Execute cleanup if not analyze-only
    if not args.analyze_only:
        suggestions = [
            type('Suggestion', (), s) for s in data.get('cleanup_suggestions', [])
        ]
        
        if suggestions:
            logger.info(f"Executing cleanup with risk level: {args.risk_level}")
            cleanup_result = cleanup_helper.execute_cleanup(suggestions, args.risk_level)
            
            if cleanup_result.status.value == 'completed':
                cleanup_data = cleanup_result.data
                logger.info(f"Cleanup completed:")
                logger.info(f"  Executed suggestions: {cleanup_data.get('executed_suggestions', 0)}")
                logger.info(f"  Space saved: {cleanup_data.get('space_saved_mb', 0):.1f}MB")
            else:
                logger.error(f"Cleanup failed: {cleanup_result.message}")
                return 1
        else:
            logger.info("No cleanup suggestions to execute")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
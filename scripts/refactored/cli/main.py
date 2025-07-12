#!/usr/bin/env python3
"""
Command-line interface for HDM processing pipeline.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from ..core import Config, setup_logger
from ..pipelines import PaperProcessingPipeline, PipelineConfig
from ..processors import (
    PDFConverterProcessor,
    MetadataExtractorProcessor,
    DataStandardizerProcessor,
    DataValidatorProcessor,
    ImageProcessor
)


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
    
    # Process papers command (full pipeline)
    process_parser = subparsers.add_parser(
        'process-papers',
        help='Run complete paper processing pipeline'
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
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Setup logging
    log_level = 'ERROR' if args.quiet else args.log_level
    logger = setup_logger(__name__, level=log_level)
    
    try:
        # Load configuration
        config = Config.load(args.config)
        
        # Override config with CLI arguments
        if args.dry_run:
            config.processing.dry_run = True
        if hasattr(args, 'log_level'):
            config.logging.level = log_level
        
        # Execute command
        if args.command == 'process-papers':
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


if __name__ == '__main__':
    sys.exit(main())
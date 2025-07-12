"""
Complete paper processing pipeline from PDF to standardized markdown.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from ..core import BaseProcessor, ProcessingResult, ProcessingStatus, Config
from ..processors import (
    PDFConverterProcessor,
    MetadataExtractorProcessor,
    ImageProcessor,
    DataStandardizerProcessor,
    DataValidatorProcessor
)


@dataclass
class PipelineConfig:
    """Configuration for paper processing pipeline."""
    skip_existing: bool = True
    force_reconvert: bool = False
    process_images: bool = True
    validate_data: bool = True
    backup_enabled: bool = True
    parallel_processing: bool = True
    max_workers: int = 4


class PaperProcessingPipeline(BaseProcessor):
    """Complete pipeline for processing papers from PDF to standardized output."""
    
    def __init__(self, config: Config, pipeline_config: Optional[PipelineConfig] = None):
        super().__init__(config, "PaperProcessingPipeline")
        self.pipeline_config = pipeline_config or PipelineConfig()
        
        # Initialize processors
        self.pdf_converter = PDFConverterProcessor(config)
        self.metadata_extractor = MetadataExtractorProcessor(config)
        self.image_processor = ImageProcessor(config)
        self.standardizer = DataStandardizerProcessor(config)
        self.validator = DataValidatorProcessor(config)
        
        # Pipeline steps
        self.steps = [
            ("pdf_conversion", self.pdf_converter),
            ("metadata_extraction", self.metadata_extractor),
            ("image_processing", self.image_processor),
            ("data_standardization", self.standardizer),
            ("data_validation", self.validator)
        ]
    
    def process_item(self, pdf_path: Path, **kwargs) -> ProcessingResult:
        """Process a single PDF through the complete pipeline."""
        try:
            paper_id = pdf_path.stem
            self.logger.info(f"Starting pipeline for {paper_id}")
            
            pipeline_results = {}
            errors = []
            
            # Step 1: PDF Conversion
            self.logger.info(f"Step 1: Converting PDF {pdf_path.name}")
            conversion_result = self.pdf_converter.process_item(
                pdf_path, 
                force_reconvert=self.pipeline_config.force_reconvert
            )
            pipeline_results["pdf_conversion"] = conversion_result
            
            if conversion_result.status == ProcessingStatus.FAILED:
                errors.append(f"PDF conversion failed: {conversion_result.message}")
                return self._create_pipeline_result(paper_id, pipeline_results, errors)
            
            if conversion_result.status == ProcessingStatus.SKIPPED:
                self.logger.info(f"PDF conversion skipped for {paper_id}")
                
            # Get markdown path for subsequent steps
            markdown_path = None
            if conversion_result.data and 'markdown_path' in conversion_result.data:
                markdown_path = Path(conversion_result.data['markdown_path'])
            else:
                # Look for existing markdown
                markdown_dir = self.config.paths.markdown_dir / paper_id.replace(' ', '_').replace('-', '_').lower()
                if markdown_dir.exists():
                    markdown_path = markdown_dir / "paper.md"
            
            if not markdown_path or not markdown_path.exists():
                errors.append("No markdown file available for processing")
                return self._create_pipeline_result(paper_id, pipeline_results, errors)
            
            # Step 2: Metadata Extraction
            self.logger.info(f"Step 2: Extracting metadata for {paper_id}")
            metadata_result = self.metadata_extractor.process_item(markdown_path)
            pipeline_results["metadata_extraction"] = metadata_result
            
            if metadata_result.status == ProcessingStatus.FAILED:
                errors.append(f"Metadata extraction failed: {metadata_result.message}")
            
            # Step 3: Image Processing (optional)
            if self.pipeline_config.process_images:
                self.logger.info(f"Step 3: Processing images for {paper_id}")
                paper_dir = markdown_path.parent
                image_result = self.image_processor.process_item(paper_dir)
                pipeline_results["image_processing"] = image_result
                
                if image_result.status == ProcessingStatus.FAILED:
                    errors.append(f"Image processing failed: {image_result.message}")
            
            # Step 4: Data Standardization
            if metadata_result.data and 'metadata' in metadata_result.data:
                self.logger.info(f"Step 4: Standardizing data for {paper_id}")
                metadata = metadata_result.data['metadata']
                standardization_result = self.standardizer.process_item(metadata)
                pipeline_results["data_standardization"] = standardization_result
                
                if standardization_result.status == ProcessingStatus.FAILED:
                    errors.append(f"Data standardization failed: {standardization_result.message}")
            
            # Step 5: Data Validation (optional)
            if self.pipeline_config.validate_data and metadata_result.data:
                self.logger.info(f"Step 5: Validating data for {paper_id}")
                metadata = metadata_result.data.get('metadata', {})
                validation_result = self.validator.process_item(metadata)
                pipeline_results["data_validation"] = validation_result
                
                if validation_result.status == ProcessingStatus.FAILED:
                    errors.append(f"Data validation failed: {validation_result.message}")
            
            return self._create_pipeline_result(paper_id, pipeline_results, errors)
            
        except Exception as e:
            self.logger.error(f"Pipeline failed for {pdf_path}: {str(e)}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Pipeline error: {str(e)}",
                error=e
            )
    
    def _create_pipeline_result(self, paper_id: str, results: Dict[str, ProcessingResult], errors: List[str]) -> ProcessingResult:
        """Create final pipeline result."""
        # Determine overall status
        if errors:
            overall_status = ProcessingStatus.FAILED
            message = f"Pipeline completed with {len(errors)} errors"
        else:
            completed_steps = sum(1 for r in results.values() if r.status == ProcessingStatus.COMPLETED)
            total_steps = len(results)
            if completed_steps == total_steps:
                overall_status = ProcessingStatus.COMPLETED
                message = f"Pipeline completed successfully ({completed_steps}/{total_steps} steps)"
            else:
                overall_status = ProcessingStatus.COMPLETED  # Partial success
                message = f"Pipeline completed ({completed_steps}/{total_steps} steps successful)"
        
        # Compile result data
        result_data = {
            'paper_id': paper_id,
            'steps_completed': len([r for r in results.values() if r.status == ProcessingStatus.COMPLETED]),
            'total_steps': len(results),
            'errors': errors,
            'step_results': {step: result.to_dict() for step, result in results.items()}
        }
        
        return ProcessingResult(
            status=overall_status,
            message=message,
            data=result_data
        )
    
    def process_directory(self, pdf_directory: Path, **kwargs) -> List[ProcessingResult]:
        """Process all PDFs in a directory through the pipeline."""
        if not pdf_directory.exists():
            raise FileNotFoundError(f"Directory not found: {pdf_directory}")
        
        # Find all PDF files
        pdf_files = list(pdf_directory.glob("*.pdf")) + list(pdf_directory.glob("*.PDF"))
        
        if not pdf_files:
            self.logger.warning(f"No PDF files found in {pdf_directory}")
            return []
        
        self.logger.info(f"Starting pipeline for {len(pdf_files)} PDFs")
        
        # Process in batches or parallel if configured
        if self.pipeline_config.parallel_processing:
            return self._process_parallel(pdf_files, **kwargs)
        else:
            return self.process_batch(pdf_files, **kwargs)
    
    def _process_parallel(self, pdf_files: List[Path], **kwargs) -> List[ProcessingResult]:
        """Process files in parallel using thread pool."""
        import concurrent.futures
        
        results = []
        max_workers = min(self.pipeline_config.max_workers, len(pdf_files))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_pdf = {
                executor.submit(self.process_item, pdf_file, **kwargs): pdf_file 
                for pdf_file in pdf_files
            }
            
            # Collect results
            for future in concurrent.futures.as_completed(future_to_pdf):
                pdf_file = future_to_pdf[future]
                try:
                    result = future.result()
                    results.append(result)
                    self.logger.info(f"Completed processing {pdf_file.name}")
                except Exception as e:
                    self.logger.error(f"Failed to process {pdf_file.name}: {e}")
                    results.append(ProcessingResult(
                        status=ProcessingStatus.FAILED,
                        message=f"Parallel processing error: {str(e)}",
                        error=e
                    ))
        
        return results
    
    def generate_pipeline_report(self, results: List[ProcessingResult], output_file: Optional[Path] = None) -> Dict[str, Any]:
        """Generate comprehensive pipeline processing report."""
        try:
            # Calculate statistics
            total_papers = len(results)
            successful = sum(1 for r in results if r.status == ProcessingStatus.COMPLETED)
            failed = sum(1 for r in results if r.status == ProcessingStatus.FAILED)
            skipped = sum(1 for r in results if r.status == ProcessingStatus.SKIPPED)
            
            # Analyze step performance
            step_stats = {}
            for result in results:
                if result.data and 'step_results' in result.data:
                    for step_name, step_result in result.data['step_results'].items():
                        if step_name not in step_stats:
                            step_stats[step_name] = {'completed': 0, 'failed': 0, 'skipped': 0}
                        
                        status = step_result.get('status', 'unknown')
                        if status in step_stats[step_name]:
                            step_stats[step_name][status] += 1
            
            # Collect common errors
            all_errors = []
            for result in results:
                if result.data and 'errors' in result.data:
                    all_errors.extend(result.data['errors'])
            
            error_counts: Dict[str, int] = {}
            for error in all_errors:
                error_counts[error] = error_counts.get(error, 0) + 1
            
            # Calculate processing times
            total_time = sum(r.processing_time for r in results if r.processing_time)
            avg_time = total_time / len(results) if results else 0
            
            report = {
                'timestamp': self._get_timestamp(),
                'summary': {
                    'total_papers': total_papers,
                    'successful': successful,
                    'failed': failed,
                    'skipped': skipped,
                    'success_rate': successful / total_papers if total_papers > 0 else 0,
                    'total_processing_time': total_time,
                    'average_processing_time': avg_time
                },
                'step_performance': step_stats,
                'common_errors': dict(sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
                'configuration': {
                    'skip_existing': self.pipeline_config.skip_existing,
                    'force_reconvert': self.pipeline_config.force_reconvert,
                    'process_images': self.pipeline_config.process_images,
                    'validate_data': self.pipeline_config.validate_data,
                    'parallel_processing': self.pipeline_config.parallel_processing,
                    'max_workers': self.pipeline_config.max_workers
                }
            }
            
            # Save report if output file specified
            if output_file:
                import json
                with open(output_file, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
                self.logger.info(f"Pipeline report saved to {output_file}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate pipeline report: {e}")
            return {'error': str(e)}
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def resume_failed_processing(self, previous_results: List[ProcessingResult], pdf_directory: Path) -> List[ProcessingResult]:
        """Resume processing for previously failed papers."""
        failed_papers = []
        
        for result in previous_results:
            if result.status == ProcessingStatus.FAILED and result.data:
                paper_id = result.data.get('paper_id')
                if paper_id:
                    # Find corresponding PDF file
                    pdf_file = pdf_directory / f"{paper_id}.pdf"
                    if pdf_file.exists():
                        failed_papers.append(pdf_file)
        
        if failed_papers:
            self.logger.info(f"Resuming processing for {len(failed_papers)} failed papers")
            return self.process_batch(failed_papers)
        else:
            self.logger.info("No failed papers to resume")
            return []
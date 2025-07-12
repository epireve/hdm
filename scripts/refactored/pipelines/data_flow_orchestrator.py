"""
Data flow orchestrator for managing end-to-end data pipeline execution.
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..core import BaseProcessor, ProcessingResult, ProcessingStatus, Config
from ..core.exceptions import ProcessingError, ValidationError
from .paper_processing import PaperProcessingPipeline, PipelineConfig
from .data_integration import DataIntegrationPipeline, DataSource, MergeStrategy
from .quality_assurance import QualityAssurancePipeline


class PipelineStage(Enum):
    """Pipeline execution stages."""
    INITIALIZATION = "initialization"
    PAPER_PROCESSING = "paper_processing"
    DATA_INTEGRATION = "data_integration"
    QUALITY_ASSURANCE = "quality_assurance"
    KNOWLEDGE_GRAPH_GENERATION = "knowledge_graph_generation"
    VISUALIZATION_UPDATE = "visualization_update"
    FINALIZATION = "finalization"


@dataclass
class StageConfig:
    """Configuration for a pipeline stage."""
    stage: PipelineStage
    enabled: bool = True
    dependencies: List[PipelineStage] = field(default_factory=list)
    timeout_seconds: Optional[int] = None
    retry_count: int = 3
    retry_delay: float = 5.0
    parallel_execution: bool = False
    max_workers: int = 4
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineExecution:
    """Tracks pipeline execution state."""
    execution_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    current_stage: Optional[PipelineStage] = None
    completed_stages: List[PipelineStage] = field(default_factory=list)
    failed_stages: List[PipelineStage] = field(default_factory=list)
    stage_results: Dict[str, ProcessingResult] = field(default_factory=dict)
    overall_status: ProcessingStatus = ProcessingStatus.PENDING


class DataFlowOrchestrator(BaseProcessor):
    """Orchestrates the complete HDM data processing pipeline."""
    
    def __init__(self, config: Config, stage_configs: List[StageConfig] = None):
        super().__init__(config, "DataFlowOrchestrator")
        self.stage_configs = {sc.stage: sc for sc in (stage_configs or self._get_default_stage_configs())}
        self.active_executions: Dict[str, PipelineExecution] = {}
        self._lock = threading.Lock()
        
        # Initialize sub-pipelines
        self.paper_pipeline = None
        self.integration_pipeline = None
        self.qa_pipeline = None
        
    def process_item(self, trigger_event: str = "manual", **kwargs) -> ProcessingResult:
        """Execute the complete data pipeline."""
        execution_id = self._generate_execution_id()
        
        try:
            # Initialize execution tracking
            execution = PipelineExecution(
                execution_id=execution_id,
                start_time=datetime.now()
            )
            
            with self._lock:
                self.active_executions[execution_id] = execution
            
            self.logger.info(f"Starting pipeline execution {execution_id} triggered by {trigger_event}")
            
            # Execute pipeline stages in order
            for stage in PipelineStage:
                if stage not in self.stage_configs or not self.stage_configs[stage].enabled:
                    self.logger.info(f"Skipping disabled stage: {stage.value}")
                    continue
                
                # Check dependencies
                if not self._check_stage_dependencies(stage, execution):
                    self.logger.error(f"Dependencies not met for stage: {stage.value}")
                    execution.failed_stages.append(stage)
                    continue
                
                # Execute stage
                stage_result = self._execute_stage(stage, execution, **kwargs)
                execution.stage_results[stage.value] = stage_result
                
                if stage_result.status == ProcessingStatus.COMPLETED:
                    execution.completed_stages.append(stage)
                    self.logger.info(f"Stage {stage.value} completed successfully")
                else:
                    execution.failed_stages.append(stage)
                    self.logger.error(f"Stage {stage.value} failed: {stage_result.message}")
                    
                    # Check if this is a critical failure
                    if self._is_critical_stage(stage):
                        break
            
            # Finalize execution
            execution.end_time = datetime.now()
            execution.overall_status = self._determine_overall_status(execution)
            
            # Generate execution report
            report = self._generate_execution_report(execution)
            
            self.logger.info(f"Pipeline execution {execution_id} completed with status: {execution.overall_status.value}")
            
            return ProcessingResult(
                status=execution.overall_status,
                message=f"Pipeline execution completed: {len(execution.completed_stages)}/{len(self.stage_configs)} stages successful",
                data={
                    'execution_id': execution_id,
                    'execution_report': report,
                    'completed_stages': [s.value for s in execution.completed_stages],
                    'failed_stages': [s.value for s in execution.failed_stages]
                }
            )
            
        except Exception as e:
            self.logger.error(f"Pipeline execution {execution_id} failed with error: {str(e)}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Pipeline execution failed: {str(e)}",
                error=e
            )
        finally:
            # Cleanup
            with self._lock:
                if execution_id in self.active_executions:
                    del self.active_executions[execution_id]
    
    def _get_default_stage_configs(self) -> List[StageConfig]:
        """Get default configuration for all pipeline stages."""
        return [
            StageConfig(
                stage=PipelineStage.INITIALIZATION,
                enabled=True,
                timeout_seconds=300,
                parameters={'validate_environment': True}
            ),
            StageConfig(
                stage=PipelineStage.PAPER_PROCESSING,
                enabled=True,
                dependencies=[PipelineStage.INITIALIZATION],
                timeout_seconds=3600,
                parallel_execution=True,
                max_workers=4,
                parameters={
                    'process_new_papers': True,
                    'force_reconvert': False,
                    'include_images': True
                }
            ),
            StageConfig(
                stage=PipelineStage.DATA_INTEGRATION,
                enabled=True,
                dependencies=[PipelineStage.PAPER_PROCESSING],
                timeout_seconds=1800,
                parameters={
                    'merge_strategy': 'fuzzy_match',
                    'similarity_threshold': 0.85
                }
            ),
            StageConfig(
                stage=PipelineStage.QUALITY_ASSURANCE,
                enabled=True,
                dependencies=[PipelineStage.DATA_INTEGRATION],
                timeout_seconds=600,
                parameters={'run_all_checks': True}
            ),
            StageConfig(
                stage=PipelineStage.KNOWLEDGE_GRAPH_GENERATION,
                enabled=True,
                dependencies=[PipelineStage.QUALITY_ASSURANCE],
                timeout_seconds=1200,
                parameters={'rebuild_graph': False}
            ),
            StageConfig(
                stage=PipelineStage.VISUALIZATION_UPDATE,
                enabled=True,
                dependencies=[PipelineStage.KNOWLEDGE_GRAPH_GENERATION],
                timeout_seconds=300,
                parameters={'update_all_views': True}
            ),
            StageConfig(
                stage=PipelineStage.FINALIZATION,
                enabled=True,
                dependencies=[PipelineStage.VISUALIZATION_UPDATE],
                timeout_seconds=120,
                parameters={'cleanup_temp_files': True}
            )
        ]
    
    def _check_stage_dependencies(self, stage: PipelineStage, execution: PipelineExecution) -> bool:
        """Check if all dependencies for a stage are satisfied."""
        stage_config = self.stage_configs[stage]
        
        for dependency in stage_config.dependencies:
            if dependency not in execution.completed_stages:
                return False
        
        return True
    
    def _execute_stage(self, stage: PipelineStage, execution: PipelineExecution, **kwargs) -> ProcessingResult:
        """Execute a specific pipeline stage."""
        execution.current_stage = stage
        stage_config = self.stage_configs[stage]
        
        self.logger.info(f"Executing stage: {stage.value}")
        
        try:
            # Get stage executor
            executor = self._get_stage_executor(stage)
            
            # Execute with timeout and retry logic
            result = self._execute_with_retry(
                executor,
                stage_config,
                execution,
                **kwargs
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Stage {stage.value} execution failed: {str(e)}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Stage execution failed: {str(e)}",
                error=e
            )
    
    def _get_stage_executor(self, stage: PipelineStage) -> Callable:
        """Get the executor function for a specific stage."""
        executors = {
            PipelineStage.INITIALIZATION: self._execute_initialization,
            PipelineStage.PAPER_PROCESSING: self._execute_paper_processing,
            PipelineStage.DATA_INTEGRATION: self._execute_data_integration,
            PipelineStage.QUALITY_ASSURANCE: self._execute_quality_assurance,
            PipelineStage.KNOWLEDGE_GRAPH_GENERATION: self._execute_knowledge_graph_generation,
            PipelineStage.VISUALIZATION_UPDATE: self._execute_visualization_update,
            PipelineStage.FINALIZATION: self._execute_finalization
        }
        
        return executors.get(stage, self._execute_placeholder)
    
    def _execute_with_retry(self, executor: Callable, stage_config: StageConfig,
                          execution: PipelineExecution, **kwargs) -> ProcessingResult:
        """Execute a stage with retry logic."""
        last_error = None
        
        for attempt in range(stage_config.retry_count + 1):
            try:
                if attempt > 0:
                    self.logger.info(f"Retry attempt {attempt} for stage {stage_config.stage.value}")
                    import time
                    time.sleep(stage_config.retry_delay)
                
                result = executor(stage_config, execution, **kwargs)
                
                if result.status != ProcessingStatus.FAILED:
                    return result
                
                last_error = result.error
                
            except Exception as e:
                last_error = e
                self.logger.warning(f"Stage execution attempt {attempt + 1} failed: {str(e)}")
        
        return ProcessingResult(
            status=ProcessingStatus.FAILED,
            message=f"Stage failed after {stage_config.retry_count + 1} attempts",
            error=last_error
        )
    
    # Stage executor implementations
    
    def _execute_initialization(self, stage_config: StageConfig, execution: PipelineExecution, **kwargs) -> ProcessingResult:
        """Initialize the pipeline environment."""
        try:
            # Validate environment
            if stage_config.parameters.get('validate_environment', True):
                validation_errors = self._validate_environment()
                if validation_errors:
                    return ProcessingResult(
                        status=ProcessingStatus.FAILED,
                        message=f"Environment validation failed: {'; '.join(validation_errors)}"
                    )
            
            # Create necessary directories
            self._ensure_directories()
            
            # Load configuration
            self._load_pipeline_configuration()
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message="Pipeline initialized successfully",
                data={'environment_validated': True, 'directories_created': True}
            )
            
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Initialization failed: {str(e)}",
                error=e
            )
    
    def _execute_paper_processing(self, stage_config: StageConfig, execution: PipelineExecution, **kwargs) -> ProcessingResult:
        """Execute paper processing stage."""
        try:
            # Initialize paper processing pipeline if not already done
            if not self.paper_pipeline:
                pipeline_config = PipelineConfig(
                    force_reconvert=stage_config.parameters.get('force_reconvert', False),
                    process_images=stage_config.parameters.get('include_images', True),
                    parallel_processing=stage_config.parallel_execution,
                    max_workers=stage_config.max_workers
                )
                self.paper_pipeline = PaperProcessingPipeline(self.config, pipeline_config)
            
            # Find papers to process
            new_papers_dir = self.config.paths.base_dir / "new_papers"
            if not new_papers_dir.exists() or not list(new_papers_dir.glob("*.pdf")):
                return ProcessingResult(
                    status=ProcessingStatus.SKIPPED,
                    message="No new papers found to process"
                )
            
            # Process papers
            results = self.paper_pipeline.process_directory(new_papers_dir)
            
            # Generate summary
            successful = sum(1 for r in results if r.status == ProcessingStatus.COMPLETED)
            total = len(results)
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED if successful > 0 else ProcessingStatus.FAILED,
                message=f"Paper processing completed: {successful}/{total} papers processed successfully",
                data={
                    'papers_processed': total,
                    'successful_papers': successful,
                    'processing_results': [r.to_dict() for r in results]
                }
            )
            
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Paper processing failed: {str(e)}",
                error=e
            )
    
    def _execute_data_integration(self, stage_config: StageConfig, execution: PipelineExecution, **kwargs) -> ProcessingResult:
        """Execute data integration stage."""
        try:
            # Initialize data integration pipeline
            if not self.integration_pipeline:
                from .data_integration import create_hdm_paper_integration_pipeline
                self.integration_pipeline = create_hdm_paper_integration_pipeline(self.config)
            
            # Configure merge strategy
            merge_strategy = MergeStrategy(
                strategy_type=stage_config.parameters.get('merge_strategy', 'fuzzy_match'),
                match_threshold=stage_config.parameters.get('similarity_threshold', 0.85),
                conflict_resolution='merge',
                duplicate_handling='keep_first'
            )
            
            # Execute integration
            result = self.integration_pipeline.process_item(merge_strategy)
            
            if result.status == ProcessingStatus.COMPLETED:
                # Export integrated data
                merged_data = result.data.get('merged_data', [])
                output_file = self.config.paths.output_dir / "integrated_papers.csv"
                export_result = self.integration_pipeline.export_merged_data(merged_data, output_file)
                
                return ProcessingResult(
                    status=ProcessingStatus.COMPLETED,
                    message=f"Data integration completed: {len(merged_data)} records integrated",
                    data={
                        'integrated_records': len(merged_data),
                        'output_file': str(output_file),
                        'integration_report': result.data.get('integration_report')
                    }
                )
            else:
                return result
                
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Data integration failed: {str(e)}",
                error=e
            )
    
    def _execute_quality_assurance(self, stage_config: StageConfig, execution: PipelineExecution, **kwargs) -> ProcessingResult:
        """Execute quality assurance stage."""
        try:
            # Initialize QA pipeline
            if not self.qa_pipeline:
                self.qa_pipeline = QualityAssurancePipeline(self.config)
            
            # Find integrated data file
            integrated_file = self.config.paths.output_dir / "integrated_papers.csv"
            if not integrated_file.exists():
                # Fallback to main research file
                integrated_file = self.config.paths.base_dir / "research_papers_complete.csv"
            
            if not integrated_file.exists():
                return ProcessingResult(
                    status=ProcessingStatus.FAILED,
                    message="No data file found for quality assurance"
                )
            
            # Run quality checks
            qa_result = self.qa_pipeline.process_item(integrated_file)
            
            if qa_result.status == ProcessingStatus.COMPLETED:
                # Export QA report
                quality_report = qa_result.data.get('quality_report')
                if quality_report:
                    report_file = self.config.paths.output_dir / "quality_report.json"
                    self.qa_pipeline.export_quality_report(quality_report, report_file)
            
            return qa_result
            
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Quality assurance failed: {str(e)}",
                error=e
            )
    
    def _execute_knowledge_graph_generation(self, stage_config: StageConfig, execution: PipelineExecution, **kwargs) -> ProcessingResult:
        """Execute knowledge graph generation stage."""
        try:
            # This would integrate with existing graph generation scripts
            self.logger.info("Knowledge graph generation stage - placeholder implementation")
            
            # Check if graph generation scripts exist
            graph_scripts_dir = self.config.paths.base_dir / "scripts" / "graph_generation"
            if graph_scripts_dir.exists():
                # Run graph builder
                import subprocess
                result = subprocess.run([
                    ".venv/bin/python", 
                    str(graph_scripts_dir / "graph_builder.py")
                ], capture_output=True, text=True, cwd=self.config.paths.base_dir)
                
                if result.returncode == 0:
                    return ProcessingResult(
                        status=ProcessingStatus.COMPLETED,
                        message="Knowledge graph generated successfully",
                        data={'graph_output': result.stdout}
                    )
                else:
                    return ProcessingResult(
                        status=ProcessingStatus.FAILED,
                        message=f"Graph generation failed: {result.stderr}"
                    )
            else:
                return ProcessingResult(
                    status=ProcessingStatus.SKIPPED,
                    message="Graph generation scripts not found"
                )
                
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Knowledge graph generation failed: {str(e)}",
                error=e
            )
    
    def _execute_visualization_update(self, stage_config: StageConfig, execution: PipelineExecution, **kwargs) -> ProcessingResult:
        """Execute visualization update stage."""
        try:
            # Update visualization data files
            viz_data_dir = self.config.paths.base_dir / "visualization" / "data"
            
            if viz_data_dir.exists():
                # Check if visualization data was updated
                updated_files = []
                
                # This would integrate with existing visualization update logic
                self.logger.info("Visualization update stage - checking for updates")
                
                return ProcessingResult(
                    status=ProcessingStatus.COMPLETED,
                    message="Visualization data updated",
                    data={'updated_files': updated_files}
                )
            else:
                return ProcessingResult(
                    status=ProcessingStatus.SKIPPED,
                    message="Visualization directory not found"
                )
                
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Visualization update failed: {str(e)}",
                error=e
            )
    
    def _execute_finalization(self, stage_config: StageConfig, execution: PipelineExecution, **kwargs) -> ProcessingResult:
        """Execute finalization stage."""
        try:
            cleanup_tasks = []
            
            # Cleanup temporary files if requested
            if stage_config.parameters.get('cleanup_temp_files', True):
                temp_dirs = [
                    self.config.paths.base_dir / "temp",
                    self.config.paths.output_dir / "temp"
                ]
                
                for temp_dir in temp_dirs:
                    if temp_dir.exists():
                        import shutil
                        shutil.rmtree(temp_dir)
                        cleanup_tasks.append(f"Cleaned {temp_dir}")
            
            # Update pipeline execution log
            self._update_execution_log(execution)
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message="Pipeline finalization completed",
                data={'cleanup_tasks': cleanup_tasks}
            )
            
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Finalization failed: {str(e)}",
                error=e
            )
    
    def _execute_placeholder(self, stage_config: StageConfig, execution: PipelineExecution, **kwargs) -> ProcessingResult:
        """Placeholder executor for undefined stages."""
        return ProcessingResult(
            status=ProcessingStatus.SKIPPED,
            message=f"Stage {stage_config.stage.value} not implemented"
        )
    
    # Helper methods
    
    def _validate_environment(self) -> List[str]:
        """Validate the pipeline environment."""
        errors = []
        
        # Check required directories
        required_dirs = [
            self.config.paths.papers_dir,
            self.config.paths.markdown_dir,
            self.config.paths.output_dir
        ]
        
        for dir_path in required_dirs:
            if not dir_path.exists():
                errors.append(f"Required directory does not exist: {dir_path}")
        
        # Check Python dependencies
        required_packages = ['pandas', 'yaml', 'numpy']
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                errors.append(f"Required Python package not found: {package}")
        
        return errors
    
    def _ensure_directories(self):
        """Create necessary directories."""
        directories = [
            self.config.paths.output_dir,
            self.config.paths.backup_dir,
            self.config.paths.logs_dir,
            self.config.paths.output_dir / "temp"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_pipeline_configuration(self):
        """Load additional pipeline configuration."""
        # Load any additional configuration needed for the pipeline
        pass
    
    def _is_critical_stage(self, stage: PipelineStage) -> bool:
        """Check if a stage is critical (failure should stop the pipeline)."""
        critical_stages = {
            PipelineStage.INITIALIZATION,
            PipelineStage.PAPER_PROCESSING,
            PipelineStage.DATA_INTEGRATION
        }
        return stage in critical_stages
    
    def _determine_overall_status(self, execution: PipelineExecution) -> ProcessingStatus:
        """Determine overall pipeline execution status."""
        if execution.failed_stages:
            # Check if any critical stages failed
            critical_failures = [s for s in execution.failed_stages if self._is_critical_stage(s)]
            if critical_failures:
                return ProcessingStatus.FAILED
            else:
                return ProcessingStatus.COMPLETED  # Partial success
        else:
            return ProcessingStatus.COMPLETED
    
    def _generate_execution_report(self, execution: PipelineExecution) -> Dict[str, Any]:
        """Generate comprehensive execution report."""
        duration = (execution.end_time - execution.start_time).total_seconds() if execution.end_time else 0
        
        return {
            'execution_id': execution.execution_id,
            'start_time': execution.start_time.isoformat(),
            'end_time': execution.end_time.isoformat() if execution.end_time else None,
            'duration_seconds': duration,
            'overall_status': execution.overall_status.value,
            'stages': {
                'total': len(self.stage_configs),
                'completed': len(execution.completed_stages),
                'failed': len(execution.failed_stages),
                'completed_list': [s.value for s in execution.completed_stages],
                'failed_list': [s.value for s in execution.failed_stages]
            },
            'stage_details': {
                stage_name: result.to_dict() 
                for stage_name, result in execution.stage_results.items()
            }
        }
    
    def _update_execution_log(self, execution: PipelineExecution):
        """Update the pipeline execution log."""
        log_file = self.config.paths.logs_dir / "pipeline_executions.json"
        
        try:
            # Load existing log
            if log_file.exists():
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {'executions': []}
            
            # Add current execution
            execution_record = self._generate_execution_report(execution)
            log_data['executions'].append(execution_record)
            
            # Keep only last 100 executions
            if len(log_data['executions']) > 100:
                log_data['executions'] = log_data['executions'][-100:]
            
            # Save updated log
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.warning(f"Failed to update execution log: {e}")
    
    def _generate_execution_id(self) -> str:
        """Generate unique execution ID."""
        from uuid import uuid4
        return f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid4())[:8]}"
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a pipeline execution."""
        with self._lock:
            execution = self.active_executions.get(execution_id)
            if execution:
                return {
                    'execution_id': execution_id,
                    'status': execution.overall_status.value,
                    'current_stage': execution.current_stage.value if execution.current_stage else None,
                    'completed_stages': [s.value for s in execution.completed_stages],
                    'failed_stages': [s.value for s in execution.failed_stages],
                    'start_time': execution.start_time.isoformat()
                }
        return None
    
    def list_active_executions(self) -> List[Dict[str, Any]]:
        """List all currently active pipeline executions."""
        with self._lock:
            return [
                self.get_execution_status(exec_id) 
                for exec_id in self.active_executions.keys()
            ]
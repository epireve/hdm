"""
Base classes for HDM processing pipeline.
"""

import time
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .config import Config
from .logger import LoggerMixin
from .exceptions import ProcessingError


class ProcessingStatus(Enum):
    """Processing status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ProcessingResult:
    """Result of a processing operation."""
    status: ProcessingStatus
    message: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[Exception] = None
    processing_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'status': self.status.value,
            'message': self.message,
            'data': self.data,
            'error': str(self.error) if self.error else None,
            'processing_time': self.processing_time,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProcessingResult':
        """Create result from dictionary."""
        return cls(
            status=ProcessingStatus(data['status']),
            message=data.get('message', ''),
            data=data.get('data', {}),
            error=Exception(data['error']) if data.get('error') else None,
            processing_time=data.get('processing_time', 0.0),
            timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else datetime.now()
        )


class CheckpointManager:
    """Manages processing checkpoints for recovery."""
    
    def __init__(self, checkpoint_file: Path):
        self.checkpoint_file = checkpoint_file
        self.data = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load checkpoint data from file."""
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file) as f:
                    return json.load(f)
            except Exception:
                pass
        return {'completed': [], 'failed': [], 'progress': {}}
    
    def save(self):
        """Save checkpoint data to file."""
        try:
            self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.checkpoint_file, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            # Don't fail processing if checkpoint save fails
            pass
    
    def mark_completed(self, item_id: str):
        """Mark an item as completed."""
        if item_id not in self.data['completed']:
            self.data['completed'].append(item_id)
        if item_id in self.data['failed']:
            self.data['failed'].remove(item_id)
        self.save()
    
    def mark_failed(self, item_id: str, error: str = ""):
        """Mark an item as failed."""
        if item_id not in self.data['failed']:
            self.data['failed'].append(item_id)
        if item_id in self.data['completed']:
            self.data['completed'].remove(item_id)
        self.data['progress'][item_id] = {'status': 'failed', 'error': error}
        self.save()
    
    def is_completed(self, item_id: str) -> bool:
        """Check if an item is already completed."""
        return item_id in self.data['completed']
    
    def is_failed(self, item_id: str) -> bool:
        """Check if an item has failed."""
        return item_id in self.data['failed']
    
    def get_progress(self, item_id: str) -> Dict[str, Any]:
        """Get progress info for an item."""
        return self.data['progress'].get(item_id, {})
    
    def update_progress(self, item_id: str, progress_info: Dict[str, Any]):
        """Update progress info for an item."""
        self.data['progress'][item_id] = progress_info
        self.save()


class BaseProcessor(ABC, LoggerMixin):
    """Base class for all processors."""
    
    def __init__(self, config: Config, name: Optional[str] = None):
        super().__init__()
        self.config = config
        self.name = name or self.__class__.__name__
        self.setup_logging(config.logging)
        
        # Setup checkpoint manager if enabled
        self.checkpoint_manager = None
        if config.processing.checkpoint_enabled:
            checkpoint_file = config.paths.output_dir / f"{self.name.lower()}_checkpoint.json"
            self.checkpoint_manager = CheckpointManager(checkpoint_file)
    
    @abstractmethod
    def process_item(self, item: Any, **kwargs) -> ProcessingResult:
        """Process a single item. Must be implemented by subclasses."""
        pass
    
    def process_batch(self, items: List[Any], **kwargs) -> List[ProcessingResult]:
        """Process a batch of items."""
        results = []
        
        for item in items:
            item_id = self._get_item_id(item)
            
            # Skip if already completed and checkpointing is enabled
            if self.checkpoint_manager and self.checkpoint_manager.is_completed(item_id):
                self.logger.info(f"Skipping {item_id} - already completed")
                result = ProcessingResult(
                    status=ProcessingStatus.SKIPPED,
                    message=f"Already completed: {item_id}"
                )
                results.append(result)
                continue
            
            # Process item with timing
            start_time = time.time()
            try:
                result = self.process_item(item, **kwargs)
                result.processing_time = time.time() - start_time
                
                # Update checkpoint
                if self.checkpoint_manager:
                    if result.status == ProcessingStatus.COMPLETED:
                        self.checkpoint_manager.mark_completed(item_id)
                    elif result.status == ProcessingStatus.FAILED:
                        self.checkpoint_manager.mark_failed(item_id, result.message)
                
                results.append(result)
                
            except Exception as e:
                processing_time = time.time() - start_time
                result = ProcessingResult(
                    status=ProcessingStatus.FAILED,
                    message=f"Processing failed: {str(e)}",
                    error=e,
                    processing_time=processing_time
                )
                
                if self.checkpoint_manager:
                    self.checkpoint_manager.mark_failed(item_id, str(e))
                
                results.append(result)
                self.logger.error(f"Failed to process {item_id}: {e}")
        
        return results
    
    def _get_item_id(self, item: Any) -> str:
        """Get unique identifier for an item. Override in subclasses if needed."""
        if isinstance(item, (str, Path)):
            return str(item)
        elif hasattr(item, 'name'):
            return item.name
        elif hasattr(item, 'id'):
            return str(item.id)
        else:
            return str(hash(str(item)))
    
    def validate_prerequisites(self) -> List[str]:
        """Validate prerequisites for processing. Return list of error messages."""
        errors = []
        
        # Check required directories
        if not self.config.paths.base_dir.exists():
            errors.append(f"Base directory does not exist: {self.config.paths.base_dir}")
        
        return errors
    
    def create_backup(self, source_path: Path, backup_suffix: Optional[str] = None) -> Optional[Path]:
        """Create a backup of a file or directory."""
        if not self.config.processing.backup_enabled:
            return None
        
        backup_dir = self.config.paths.backup_dir
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if backup_suffix:
            backup_name = f"{source_path.name}_{backup_suffix}_{timestamp}"
        else:
            backup_name = f"{source_path.name}_{timestamp}"
        
        backup_path = backup_dir / backup_name
        
        try:
            if source_path.is_file():
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                import shutil
                shutil.copy2(source_path, backup_path)
            elif source_path.is_dir():
                import shutil
                shutil.copytree(source_path, backup_path)
            
            self.logger.info(f"Created backup: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.warning(f"Failed to create backup for {source_path}: {e}")
            return None


class PipelineStep(BaseProcessor):
    """Base class for pipeline steps."""
    
    def __init__(self, config: Config, step_name: str):
        super().__init__(config, step_name)
        self.step_name = step_name
    
    @abstractmethod
    def execute(self, input_data: Any, **kwargs) -> ProcessingResult:
        """Execute this pipeline step."""
        pass
    
    def process_item(self, item: Any, **kwargs) -> ProcessingResult:
        """Implement BaseProcessor interface."""
        return self.execute(item, **kwargs)
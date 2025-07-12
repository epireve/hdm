"""
Unit tests for base processor functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.refactored.core import BaseProcessor, ProcessingResult, ProcessingStatus
from scripts.refactored.core.exceptions import FileProcessingError


class MockProcessor(BaseProcessor):
    """Mock processor for testing base functionality."""
    
    def process_item(self, item, **kwargs):
        """Mock implementation."""
        if item == "error":
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message="Mock error",
                error=Exception("Test error")
            )
        return ProcessingResult(
            status=ProcessingStatus.COMPLETED,
            message="Mock success"
        )


class TestBaseProcessor:
    """Test base processor functionality."""
    
    def test_processor_initialization(self, sample_config):
        """Test processor initialization."""
        processor = MockProcessor(sample_config, "TestProcessor")
        
        assert processor.config == sample_config
        assert processor.name == "TestProcessor"
        assert processor.logger is not None
    
    def test_successful_processing(self, sample_config):
        """Test successful item processing."""
        processor = MockProcessor(sample_config, "TestProcessor")
        
        result = processor.process_item("test_item")
        
        assert result.status == ProcessingStatus.COMPLETED
        assert result.message == "Mock success"
        assert result.error is None
    
    def test_failed_processing(self, sample_config):
        """Test failed item processing."""
        processor = MockProcessor(sample_config, "TestProcessor")
        
        result = processor.process_item("error")
        
        assert result.status == ProcessingStatus.FAILED
        assert result.message == "Mock error"
        assert result.error is not None
    
    def test_batch_processing(self, sample_config):
        """Test batch processing functionality."""
        processor = MockProcessor(sample_config, "TestProcessor")
        
        items = ["item1", "item2", "error", "item3"]
        results = processor.process_batch(items)
        
        assert len(results) == 4
        assert sum(1 for r in results if r.status == ProcessingStatus.COMPLETED) == 3
        assert sum(1 for r in results if r.status == ProcessingStatus.FAILED) == 1
    
    def test_validation_errors(self, sample_config):
        """Test configuration validation."""
        processor = MockProcessor(sample_config, "TestProcessor")
        
        # Should not raise errors with valid config
        errors = processor.validate_environment()
        assert isinstance(errors, list)
    
    def test_create_backup(self, sample_config, temp_dir):
        """Test backup creation functionality."""
        processor = MockProcessor(sample_config, "TestProcessor")
        
        # Create a test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        # Create backup
        backup_path = processor.create_backup(test_file)
        
        if sample_config.processing.backup_enabled:
            assert backup_path is not None
            assert backup_path.exists()
        else:
            assert backup_path is None
    
    @patch('scripts.refactored.core.base.BaseProcessor.logger')
    def test_error_handling_with_logging(self, mock_logger, sample_config):
        """Test error handling includes proper logging."""
        processor = MockProcessor(sample_config, "TestProcessor")
        
        result = processor.process_item("error")
        
        assert result.status == ProcessingStatus.FAILED
        # Verify that logging occurred (exact call depends on implementation)
        assert mock_logger.error.called or mock_logger.warning.called
    
    def test_processing_result_creation(self):
        """Test ProcessingResult creation and properties."""
        # Test successful result
        success_result = ProcessingResult(
            status=ProcessingStatus.COMPLETED,
            message="Success",
            data={"key": "value"}
        )
        
        assert success_result.status == ProcessingStatus.COMPLETED
        assert success_result.message == "Success"
        assert success_result.data == {"key": "value"}
        assert success_result.error is None
        
        # Test failed result
        error = Exception("Test error")
        failed_result = ProcessingResult(
            status=ProcessingStatus.FAILED,
            message="Failed",
            error=error
        )
        
        assert failed_result.status == ProcessingStatus.FAILED
        assert failed_result.error == error
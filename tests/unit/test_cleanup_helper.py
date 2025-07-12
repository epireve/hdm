"""
Unit tests for cleanup helper functionality.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.refactored.utils import CleanupHelper
from scripts.refactored.core import ProcessingStatus


class TestCleanupHelper:
    """Test cleanup helper functionality."""
    
    def test_cleanup_helper_initialization(self, sample_config):
        """Test cleanup helper initialization."""
        helper = CleanupHelper(sample_config)
        
        assert helper.config == sample_config
        assert helper.name == "CleanupHelper"
        assert isinstance(helper.ignore_patterns, set)
        assert '.pyc' in helper.ignore_patterns
        assert '__pycache__' in helper.ignore_patterns
    
    def test_should_ignore_patterns(self, sample_config):
        """Test file ignore pattern matching."""
        helper = CleanupHelper(sample_config)
        
        # Should ignore common patterns
        assert helper._should_ignore("test.pyc") is True
        assert helper._should_ignore("__pycache__") is True
        assert helper._should_ignore(".DS_Store") is True
        assert helper._should_ignore("temp.tmp") is True
        
        # Should not ignore regular files
        assert helper._should_ignore("script.py") is False
        assert helper._should_ignore("data.csv") is False
        assert helper._should_ignore("README.md") is False
    
    def test_file_type_detection(self, sample_config):
        """Test file type detection from extensions."""
        helper = CleanupHelper(sample_config)
        
        assert helper._get_file_type(Path("script.py")) == "python"
        assert helper._get_file_type(Path("data.csv")) == "csv_data"
        assert helper._get_file_type(Path("config.json")) == "json_data"
        assert helper._get_file_type(Path("README.md")) == "markdown"
        assert helper._get_file_type(Path("unknown.xyz")) == "other"
    
    def test_base_name_extraction(self, sample_config):
        """Test base name extraction for redundant script detection."""
        helper = CleanupHelper(sample_config)
        
        # Test version suffix removal
        assert helper._extract_base_name("script_v1.py") == "script"
        assert helper._extract_base_name("process_final.py") == "process"
        assert helper._extract_base_name("data_new.py") == "data"
        assert helper._extract_base_name("backup_old.py") == "backup"
        
        # Test normal files unchanged
        assert helper._extract_base_name("normal_script.py") == "normal_script"
    
    def test_duplicate_detection(self, sample_config, temp_dir):
        """Test duplicate file detection."""
        helper = CleanupHelper(sample_config)
        
        # Create test files with same content
        file1 = temp_dir / "file1.txt"
        file2 = temp_dir / "file2.txt"
        file3 = temp_dir / "different.txt"
        
        file1.write_text("identical content")
        file2.write_text("identical content")
        file3.write_text("different content")
        
        # Mock the file scanning to return our test files
        from scripts.refactored.utils.cleanup_helper import FileInfo
        test_files = [
            FileInfo(
                path=file1,
                size=file1.stat().st_size,
                hash=helper._calculate_file_hash(file1),
                type="text",
                last_modified=file1.stat().st_mtime
            ),
            FileInfo(
                path=file2,
                size=file2.stat().st_size,
                hash=helper._calculate_file_hash(file2),
                type="text",
                last_modified=file2.stat().st_mtime
            ),
            FileInfo(
                path=file3,
                size=file3.stat().st_size,
                hash=helper._calculate_file_hash(file3),
                type="text",
                last_modified=file3.stat().st_mtime
            )
        ]
        
        duplicates = helper._find_duplicates(test_files)
        
        # Should find one group of duplicates (file1 and file2)
        assert len(duplicates) == 1
        assert len(duplicates[0]) == 2
    
    def test_analyze_project_with_mock_files(self, sample_config, temp_dir):
        """Test project analysis with mocked file system."""
        helper = CleanupHelper(sample_config)
        
        # Create some test files
        (temp_dir / "script.py").write_text("print('hello')")
        (temp_dir / "script_old.py").write_text("print('old version')")
        (temp_dir / "data.csv").write_text("header1,header2\nval1,val2")
        
        # Run analysis
        result = helper.analyze_project(temp_dir)
        
        assert result.status == ProcessingStatus.COMPLETED
        assert result.data is not None
        assert 'total_files_scanned' in result.data
        assert 'cleanup_suggestions' in result.data
    
    def test_cleanup_suggestion_generation(self, sample_config):
        """Test cleanup suggestion generation."""
        helper = CleanupHelper(sample_config)
        
        from scripts.refactored.utils.cleanup_helper import FileInfo
        
        # Create mock duplicate files
        file1 = FileInfo(
            path=Path("/test/file1.txt"),
            size=100,
            hash="abc123",
            type="text",
            last_modified=1000.0
        )
        file2 = FileInfo(
            path=Path("/test/file2.txt"),
            size=100,
            hash="abc123",
            type="text",
            last_modified=2000.0  # newer
        )
        
        duplicates = [[file1, file2]]
        large_files = []
        redundant_scripts = []
        temp_files = []
        
        suggestions = helper._generate_suggestions(
            duplicates, large_files, redundant_scripts, temp_files
        )
        
        assert len(suggestions) == 1
        assert suggestions[0].action == "archive"
        assert len(suggestions[0].files) == 1  # Only archive the older file
        assert suggestions[0].files[0] == file1.path
        assert suggestions[0].risk_level == "low"
    
    def test_generate_cleanup_report(self, sample_config, temp_dir):
        """Test cleanup report generation."""
        helper = CleanupHelper(sample_config)
        
        # Create a mock analysis result
        from scripts.refactored.core import ProcessingResult, ProcessingStatus
        
        mock_result = ProcessingResult(
            status=ProcessingStatus.COMPLETED,
            message="Analysis complete",
            data={
                'total_files_scanned': 100,
                'duplicate_groups': 5,
                'large_files': 2,
                'redundant_scripts': 3,
                'temp_files': 1,
                'potential_space_saved_mb': 25.5,
                'cleanup_suggestions': []
            }
        )
        
        # Generate report
        report_file = temp_dir / "test_report.json"
        result_path = helper.generate_cleanup_report(mock_result, report_file)
        
        assert result_path == report_file
        assert report_file.exists()
        
        # Verify report content
        with open(report_file) as f:
            report_data = json.load(f)
        
        assert 'timestamp' in report_data
        assert 'analysis_summary' in report_data
        assert 'recommendations' in report_data
        assert report_data['analysis_summary']['total_files_scanned'] == 100
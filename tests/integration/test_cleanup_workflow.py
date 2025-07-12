"""
Integration tests for complete cleanup workflow.
"""

import pytest
from pathlib import Path

from scripts.refactored.utils import CleanupHelper
from scripts.refactored.core import ProcessingStatus


class TestCleanupWorkflow:
    """Test complete cleanup workflow integration."""
    
    def test_full_cleanup_analysis_workflow(self, sample_config, temp_dir):
        """Test complete cleanup analysis workflow."""
        # Create a realistic file structure
        self._create_test_file_structure(temp_dir)
        
        # Initialize cleanup helper
        helper = CleanupHelper(sample_config)
        
        # Run analysis
        analysis_result = helper.analyze_project(temp_dir)
        
        # Verify analysis completed successfully
        assert analysis_result.status == ProcessingStatus.COMPLETED
        assert analysis_result.data is not None
        
        # Check analysis data structure
        data = analysis_result.data
        assert 'total_files_scanned' in data
        assert 'duplicate_groups' in data
        assert 'cleanup_suggestions' in data
        
        # Should find some files to clean up
        assert data['total_files_scanned'] > 0
        
        # Generate report
        report_file = temp_dir / "cleanup_report.json"
        report_path = helper.generate_cleanup_report(analysis_result, report_file)
        
        assert report_path.exists()
        assert report_path == report_file
    
    def test_cleanup_execution_workflow(self, sample_config, temp_dir):
        """Test cleanup execution workflow with low-risk operations."""
        # Create test structure with duplicates
        self._create_test_duplicates(temp_dir)
        
        helper = CleanupHelper(sample_config)
        
        # Run analysis
        analysis_result = helper.analyze_project(temp_dir)
        assert analysis_result.status == ProcessingStatus.COMPLETED
        
        # Get suggestions
        suggestions_data = analysis_result.data.get('cleanup_suggestions', [])
        
        if suggestions_data:
            # Convert dict suggestions back to objects for execution
            from scripts.refactored.utils.cleanup_helper import CleanupSuggestion
            suggestions = [
                CleanupSuggestion(
                    action=s['action'],
                    files=[Path(f) for f in s['files']],
                    reason=s['reason'],
                    space_saved=s['space_saved'],
                    risk_level=s['risk_level']
                )
                for s in suggestions_data
            ]
            
            # Execute low-risk cleanup
            cleanup_result = helper.execute_cleanup(suggestions, "low")
            
            # Verify execution completed
            assert cleanup_result.status == ProcessingStatus.COMPLETED
            assert cleanup_result.data is not None
            
            # Check that archive directory was created
            archive_dir = sample_config.paths.base_dir / "archive" / "automated_cleanup"
            if cleanup_result.data['executed_suggestions'] > 0:
                assert archive_dir.exists()
    
    def _create_test_file_structure(self, base_dir: Path):
        """Create a realistic test file structure."""
        # Create directories
        (base_dir / "scripts").mkdir()
        (base_dir / "data").mkdir()
        (base_dir / "temp").mkdir()
        
        # Create Python scripts (some redundant)
        scripts_dir = base_dir / "scripts"
        (scripts_dir / "processor.py").write_text("# Main processor\nprint('processing')")
        (scripts_dir / "processor_old.py").write_text("# Old processor\nprint('old processing')")
        (scripts_dir / "processor_backup.py").write_text("# Backup processor\nprint('backup')")
        (scripts_dir / "utils.py").write_text("# Utilities\ndef helper(): pass")
        
        # Create data files (some large)
        data_dir = base_dir / "data"
        (data_dir / "small.csv").write_text("col1,col2\nval1,val2")
        (data_dir / "large.csv").write_text("col1,col2\n" + "val,val\n" * 10000)  # Large file
        
        # Create temporary files
        temp_dir = base_dir / "temp"
        (temp_dir / "cache.tmp").write_text("temporary data")
        (temp_dir / "backup.temp").write_text("temp backup")
        
        # Create log files
        (base_dir / "debug.log").write_text("debug info")
        (base_dir / "error.log").write_text("error info")
    
    def _create_test_duplicates(self, base_dir: Path):
        """Create test files with duplicates."""
        # Create identical files
        content = "This is identical content for testing duplicates."
        
        (base_dir / "file1.txt").write_text(content)
        (base_dir / "file2.txt").write_text(content)
        (base_dir / "copy_of_file1.txt").write_text(content)
        
        # Create different file
        (base_dir / "different.txt").write_text("This is different content.")
        
        # Create backup copies
        backup_dir = base_dir / "backups"
        backup_dir.mkdir()
        (backup_dir / "file1_backup.txt").write_text(content)
    
    def test_CLI_integration(self, sample_config, temp_dir):
        """Test integration with CLI interface."""
        # This would test the CLI cleanup command
        # For now, just verify the helper can be created with CLI-like parameters
        helper = CleanupHelper(sample_config)
        
        # Test analysis (CLI --analyze-only equivalent)
        result = helper.analyze_project(temp_dir)
        assert result.status == ProcessingStatus.COMPLETED
        
        # Test report generation (CLI --report equivalent)
        report_file = temp_dir / "cli_test_report.json"
        report_path = helper.generate_cleanup_report(result, report_file)
        assert report_path.exists()
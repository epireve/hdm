"""
Unit tests for configuration management.
"""

import pytest
import tempfile
import yaml
from pathlib import Path

from scripts.refactored.core import Config, ConfigurationError


class TestConfig:
    """Test configuration loading and validation."""
    
    def test_default_config_creation(self):
        """Test creating default configuration."""
        config = Config()
        
        assert config.paths.base_dir == Path.cwd()
        assert config.processing.backup_enabled is True
        assert config.processing.max_workers == 4
        assert config.logging.level == "INFO"
    
    def test_config_from_dict(self):
        """Test creating configuration from dictionary."""
        config_data = {
            "paths": {
                "base_dir": "/test/path"
            },
            "processing": {
                "max_workers": 8,
                "backup_enabled": False
            }
        }
        
        config = Config._from_dict(config_data)
        
        assert config.paths.base_dir == Path("/test/path")
        assert config.processing.max_workers == 8
        assert config.processing.backup_enabled is False
    
    def test_config_load_yaml(self, temp_dir: Path):
        """Test loading configuration from YAML file."""
        config_file = temp_dir / "test_config.yaml"
        config_data = {
            "paths": {
                "base_dir": str(temp_dir),
                "markdown_dir": str(temp_dir / "markdown")
            },
            "processing": {
                "max_workers": 6
            }
        }
        
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        config = Config.load(config_file)
        
        assert config.paths.base_dir == temp_dir
        assert config.paths.markdown_dir == temp_dir / "markdown"
        assert config.processing.max_workers == 6
    
    def test_config_validation_errors(self):
        """Test configuration validation catches errors."""
        # Test invalid base directory
        config_data = {
            "paths": {
                "base_dir": "/nonexistent/path/that/should/not/exist"
            }
        }
        
        config = Config._from_dict(config_data)
        errors = config.validate()
        
        assert len(errors) > 0
        assert any("does not exist" in error for error in errors)
    
    def test_config_backup_settings(self):
        """Test backup configuration settings."""
        config = Config()
        
        # Test default backup settings
        assert config.processing.backup_enabled is True
        
        # Test custom backup settings
        config_data = {
            "processing": {
                "backup_enabled": False
            }
        }
        
        config = Config._from_dict(config_data)
        assert config.processing.backup_enabled is False
    
    def test_missing_config_file(self):
        """Test handling of missing configuration file."""
        nonexistent_file = Path("/nonexistent/config.yaml")
        
        # Should return default config when file doesn't exist
        config = Config.load(nonexistent_file)
        assert config.paths.base_dir == Path.cwd()
        assert config.processing.max_workers == 4
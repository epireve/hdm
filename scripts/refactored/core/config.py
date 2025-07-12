"""
Centralized configuration management for HDM processing pipeline.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from .exceptions import ConfigurationError


@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str = ""
    auth_token: str = ""
    timeout: int = 30


@dataclass
class APIConfig:
    """API configuration for external services."""
    kilocode_token: str = ""
    gemini_api_key: str = ""
    timeout: int = 60
    max_retries: int = 3
    retry_delay: float = 1.0


@dataclass
class PathsConfig:
    """File and directory paths configuration."""
    base_dir: Path = field(default_factory=lambda: Path.cwd())
    papers_dir: Path = field(default_factory=lambda: Path('papers'))
    markdown_dir: Path = field(default_factory=lambda: Path('markdown_papers'))
    output_dir: Path = field(default_factory=lambda: Path('output'))
    backup_dir: Path = field(default_factory=lambda: Path('backups'))
    logs_dir: Path = field(default_factory=lambda: Path('logs'))
    
    def __post_init__(self):
        """Convert relative paths to absolute paths based on base_dir."""
        for attr_name in ['papers_dir', 'markdown_dir', 'output_dir', 'backup_dir', 'logs_dir']:
            path = getattr(self, attr_name)
            if not path.is_absolute():
                setattr(self, attr_name, self.base_dir / path)


@dataclass
class ProcessingConfig:
    """Processing behavior configuration."""
    batch_size: int = 10
    max_workers: int = 4
    test_mode: bool = False
    test_papers_count: int = 5
    dry_run: bool = False
    backup_enabled: bool = True
    checkpoint_enabled: bool = True


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_enabled: bool = True
    console_enabled: bool = True


@dataclass
class Config:
    """Main configuration class containing all settings."""
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    api: APIConfig = field(default_factory=APIConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> 'Config':
        """Load configuration from file and environment variables."""
        config = cls()
        
        # Load from YAML file if provided
        if config_path and config_path.exists():
            try:
                with open(config_path) as f:
                    yaml_config = yaml.safe_load(f)
                config = cls._from_dict(yaml_config)
            except Exception as e:
                raise ConfigurationError(f"Failed to load config from {config_path}: {e}")
        
        # Override with environment variables
        config._load_from_env()
        
        # Validate configuration
        config._validate()
        
        return config
    
    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create Config instance from dictionary."""
        config = cls()
        
        if 'database' in data:
            config.database = DatabaseConfig(**data['database'])
        
        if 'api' in data:
            config.api = APIConfig(**data['api'])
        
        if 'paths' in data:
            # Convert string paths to Path objects
            paths_data = data['paths'].copy()
            for key, value in paths_data.items():
                if isinstance(value, str):
                    paths_data[key] = Path(value)
            config.paths = PathsConfig(**paths_data)
        
        if 'processing' in data:
            config.processing = ProcessingConfig(**data['processing'])
        
        if 'logging' in data:
            config.logging = LoggingConfig(**data['logging'])
        
        return config
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Database
        if os.getenv('TURSO_DATABASE_URL'):
            self.database.url = os.getenv('TURSO_DATABASE_URL')
        if os.getenv('TURSO_AUTH_TOKEN'):
            self.database.auth_token = os.getenv('TURSO_AUTH_TOKEN')
        
        # API
        if os.getenv('KILOCODE_API_TOKEN'):
            self.api.kilocode_token = os.getenv('KILOCODE_API_TOKEN')
        if os.getenv('GOOGLE_API_KEY'):
            self.api.gemini_api_key = os.getenv('GOOGLE_API_KEY')
        
        # Processing
        if os.getenv('TEST_MODE'):
            self.processing.test_mode = os.getenv('TEST_MODE').lower() == 'true'
        if os.getenv('DRY_RUN'):
            self.processing.dry_run = os.getenv('DRY_RUN').lower() == 'true'
        
        # Logging
        if os.getenv('LOG_LEVEL'):
            self.logging.level = os.getenv('LOG_LEVEL')
    
    def _validate(self):
        """Validate configuration."""
        # Ensure required directories exist or can be created
        for dir_path in [self.paths.output_dir, self.paths.backup_dir, self.paths.logs_dir]:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise ConfigurationError(f"Cannot create directory {dir_path}: {e}")
        
        # Validate batch size
        if self.processing.batch_size <= 0:
            raise ConfigurationError("batch_size must be positive")
        
        # Validate max workers
        if self.processing.max_workers <= 0:
            raise ConfigurationError("max_workers must be positive")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'database': {
                'url': self.database.url,
                'auth_token': self.database.auth_token,
                'timeout': self.database.timeout,
            },
            'api': {
                'kilocode_token': self.api.kilocode_token,
                'gemini_api_key': self.api.gemini_api_key,
                'timeout': self.api.timeout,
                'max_retries': self.api.max_retries,
                'retry_delay': self.api.retry_delay,
            },
            'paths': {
                'base_dir': str(self.paths.base_dir),
                'papers_dir': str(self.paths.papers_dir),
                'markdown_dir': str(self.paths.markdown_dir),
                'output_dir': str(self.paths.output_dir),
                'backup_dir': str(self.paths.backup_dir),
                'logs_dir': str(self.paths.logs_dir),
            },
            'processing': {
                'batch_size': self.processing.batch_size,
                'max_workers': self.processing.max_workers,
                'test_mode': self.processing.test_mode,
                'test_papers_count': self.processing.test_papers_count,
                'dry_run': self.processing.dry_run,
                'backup_enabled': self.processing.backup_enabled,
                'checkpoint_enabled': self.processing.checkpoint_enabled,
            },
            'logging': {
                'level': self.logging.level,
                'format': self.logging.format,
                'file_enabled': self.logging.file_enabled,
                'console_enabled': self.logging.console_enabled,
            }
        }
    
    def save(self, config_path: Path):
        """Save configuration to YAML file."""
        try:
            with open(config_path, 'w') as f:
                yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)
        except Exception as e:
            raise ConfigurationError(f"Failed to save config to {config_path}: {e}")
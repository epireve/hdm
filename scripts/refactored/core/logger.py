"""
Unified logging configuration for HDM processing pipeline.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from .config import LoggingConfig


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


def setup_logger(
    name: str,
    config: Optional[LoggingConfig] = None,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Set up a logger with consistent formatting and output options.
    
    Args:
        name: Logger name (typically __name__ or module name)
        config: Logging configuration
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    if config is None:
        config = LoggingConfig()
    
    logger = logging.getLogger(name)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Set level
    log_level = getattr(logging, config.level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create formatters
    detailed_formatter = logging.Formatter(config.format)
    simple_formatter = logging.Formatter('%(levelname)s: %(message)s')
    colored_formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console handler
    if config.console_enabled:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        # Use colored formatter for console if terminal supports it
        if sys.stdout.isatty():
            console_handler.setFormatter(colored_formatter)
        else:
            console_handler.setFormatter(simple_formatter)
        
        logger.addHandler(console_handler)
    
    # File handler
    if config.file_enabled and log_file:
        try:
            # Ensure log directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(detailed_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # If file logging fails, at least log to console
            logger.warning(f"Failed to setup file logging: {e}")
    
    return logger


def get_log_file_path(base_dir: Path, module_name: str) -> Path:
    """Generate a log file path for a module."""
    timestamp = datetime.now().strftime("%Y%m%d")
    log_filename = f"{module_name}_{timestamp}.log"
    return base_dir / "logs" / log_filename


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = None
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        if self._logger is None:
            self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        return self._logger
    
    def setup_logging(self, config: Optional[LoggingConfig] = None, log_file: Optional[Path] = None):
        """Setup logging for this class."""
        self._logger = setup_logger(
            f"{self.__class__.__module__}.{self.__class__.__name__}",
            config,
            log_file
        )
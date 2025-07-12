"""
Core processing framework for HDM paper processing pipeline.
"""

from .base import BaseProcessor, ProcessingResult, ProcessingStatus
from .config import Config
from .logger import setup_logger
from .exceptions import ProcessingError, ConfigurationError, ValidationError

__all__ = [
    'BaseProcessor',
    'ProcessingResult',
    'ProcessingStatus',
    'Config',
    'setup_logger',
    'ProcessingError',
    'ConfigurationError',
    'ValidationError'
]
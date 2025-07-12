"""
Custom exceptions for the HDM processing pipeline.
"""

class ProcessingError(Exception):
    """Base exception for processing errors."""
    
    def __init__(self, message: str, context: dict = None, recoverable: bool = True):
        super().__init__(message)
        self.message = message
        self.context = context or {}
        self.recoverable = recoverable


class ConfigurationError(ProcessingError):
    """Configuration-related errors."""
    
    def __init__(self, message: str, config_key: str = None):
        super().__init__(message, {'config_key': config_key}, recoverable=False)
        self.config_key = config_key


class ValidationError(ProcessingError):
    """Data validation errors."""
    
    def __init__(self, message: str, field: str = None, value=None):
        super().__init__(message, {'field': field, 'value': value}, recoverable=False)
        self.field = field
        self.value = value


class NetworkError(ProcessingError):
    """Network-related errors (API calls, downloads, etc.)."""
    
    def __init__(self, message: str, url: str = None, status_code: int = None):
        super().__init__(message, {'url': url, 'status_code': status_code}, recoverable=True)
        self.url = url
        self.status_code = status_code


class FileProcessingError(ProcessingError):
    """File processing errors."""
    
    def __init__(self, message: str, file_path: str = None, operation: str = None):
        super().__init__(message, {'file_path': file_path, 'operation': operation}, recoverable=True)
        self.file_path = file_path
        self.operation = operation
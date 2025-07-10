"""
Simplified Kilocode API Configuration Loader without python-dotenv dependency
"""

import os
import sys
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
from dataclasses import dataclass, field
from functools import lru_cache

@dataclass
class KilocodeConfig:
    """Configuration class for Kilocode API settings"""

    # Authentication
    token: str
    auth_source: str = "web"

    # API Configuration
    base_url: str = "https://kilocode.ai"
    api_version: str = "v1"
    openrouter_path: str = "/api/openrouter"

    # Default Model Settings
    default_model: str = "google/gemini-2.5-pro-preview"
    default_temperature: float = 0.7
    default_max_tokens: int = 1000
    default_top_p: Optional[float] = None

    # Headers Configuration
    http_referer: str = "https://kilocode.ai"
    x_title: str = "Kilo Code"
    version: str = "1.0.0"

    # Development/Debug
    debug: bool = False
    log_level: str = "INFO"
    retry_attempts: int = 3
    retry_delay: float = 1.0
    request_timeout: int = 120

    @property
    def openrouter_url(self) -> str:
        """Get the full OpenRouter API URL"""
        return f"{self.base_url}{self.openrouter_path}"

    @property
    def headers(self) -> Dict[str, str]:
        """Get default headers for API requests"""
        return {
            "Authorization": f"Bearer {self.token}",
            "HTTP-Referer": self.http_referer,
            "X-Title": self.x_title,
            "X-KiloCode-Version": self.version,
            "Content-Type": "application/json",
        }


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing"""
    pass


def load_env_file(env_path: Path) -> Dict[str, str]:
    """Simple .env file loader"""
    env_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    env_vars[key.strip()] = value
    return env_vars


@lru_cache(maxsize=1)
def load_config(env_file: Optional[str] = None, validate: bool = True) -> KilocodeConfig:
    """
    Load configuration from environment variables and .env file

    Args:
        env_file: Path to .env file (optional)
        validate: Whether to validate required fields

    Returns:
        KilocodeConfig instance

    Raises:
        ConfigurationError: If required configuration is missing
    """
    # Load .env file
    if env_file:
        env_path = Path(env_file)
    else:
        # Try to find .env in current directory or parent directories
        current_dir = Path.cwd()
        env_path = None
        for parent in [current_dir] + list(current_dir.parents):
            test_path = parent / ".env"
            if test_path.exists():
                env_path = test_path
                break
    
    # Load env vars from file
    if env_path:
        env_vars = load_env_file(env_path)
        # Set environment variables
        for key, value in env_vars.items():
            if key not in os.environ:
                os.environ[key] = value

    # Load token (required)
    token = os.getenv("KILOCODE_TOKEN")
    if validate and not token:
        raise ConfigurationError(
            "KILOCODE_TOKEN is required. "
            "Get your token from https://kilocode.ai/auth/signin"
        )

    # Create configuration with minimal settings
    config = KilocodeConfig(
        token=token or "",
        auth_source=os.getenv("KILOCODE_AUTH_SOURCE", "web"),
        base_url=os.getenv("KILOCODE_BASE_URL", "https://kilocode.ai"),
        api_version=os.getenv("KILOCODE_API_VERSION", "v1"),
        openrouter_path=os.getenv("KILOCODE_OPENROUTER_PATH", "/api/openrouter"),
        default_model=os.getenv("KILOCODE_DEFAULT_MODEL", "google/gemini-2.5-pro-preview"),
        default_temperature=float(os.getenv("KILOCODE_DEFAULT_TEMPERATURE", "0.7")),
        default_max_tokens=int(os.getenv("KILOCODE_DEFAULT_MAX_TOKENS", "1000")),
        http_referer=os.getenv("KILOCODE_HTTP_REFERER", "https://kilocode.ai"),
        x_title=os.getenv("KILOCODE_X_TITLE", "Kilo Code"),
        version=os.getenv("KILOCODE_VERSION", "1.0.0"),
        debug=os.getenv("KILOCODE_DEBUG", "false").lower() in ("true", "1", "yes", "on"),
        log_level=os.getenv("KILOCODE_LOG_LEVEL", "INFO").upper(),
        retry_attempts=int(os.getenv("KILOCODE_RETRY_ATTEMPTS", "3")),
        retry_delay=float(os.getenv("KILOCODE_RETRY_DELAY", "1.0")),
        request_timeout=int(os.getenv("KILOCODE_REQUEST_TIMEOUT", "120")),
    )

    return config


# Convenience function for quick access
def get_config() -> KilocodeConfig:
    """Get the current configuration (cached)"""
    return load_config()


# Example usage and validation
if __name__ == "__main__":
    try:
        config = load_config()
        print("Configuration loaded successfully!")
        print(f"Token: {config.token[:10]}..." if config.token else "No token")
        print(f"Base URL: {config.base_url}")
        print(f"OpenRouter URL: {config.openrouter_url}")
        print(f"Default Model: {config.default_model}")
        print(f"Debug Mode: {config.debug}")

    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
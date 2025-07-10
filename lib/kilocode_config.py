"""
Kilocode API Configuration Loader

This module provides a configuration management system for the Kilocode API,
loading settings from environment variables and .env files.
"""

import os
import sys
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
from dataclasses import dataclass, field
from functools import lru_cache

# Try to import python-dotenv, provide instructions if not available
try:
    from dotenv import load_dotenv
except ImportError:
    print("python-dotenv not installed. Install with: pip install python-dotenv")
    sys.exit(1)


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

    # Feature Flags
    enable_streaming: bool = True
    include_usage: bool = True
    use_transforms: bool = True
    enable_reasoning: bool = True
    enable_caching: bool = True

    # Headers Configuration
    http_referer: str = "https://kilocode.ai"
    x_title: str = "Kilo Code"
    version: str = "1.0.0"

    # Advanced Settings
    provider_order: List[str] = field(default_factory=list)
    allow_fallbacks: bool = True
    cache_models: bool = True
    cache_ttl: int = 3600

    # Development/Debug
    debug: bool = False
    log_level: str = "INFO"
    retry_attempts: int = 3
    retry_delay: float = 1.0
    request_timeout: int = 120

    # Profile/Balance Monitoring
    check_balance: bool = False
    balance_warning_threshold: float = 10.0

    # Rate Limiting
    rate_limit_rpm: Optional[int] = None
    rate_limit_tpm: Optional[int] = None

    # Legacy Model Support
    enable_legacy_models: bool = True
    custom_model_mappings: Dict[str, str] = field(default_factory=dict)

    # Proxy Settings
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None
    no_proxy: List[str] = field(default_factory=list)

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

    @property
    def openai_client_args(self) -> Dict[str, Any]:
        """Get arguments for OpenAI client initialization"""
        return {
            "base_url": self.openrouter_url,
            "api_key": self.token,
            "default_headers": {
                "HTTP-Referer": self.http_referer,
                "X-Title": self.x_title,
                "X-KiloCode-Version": self.version,
            },
            "timeout": self.request_timeout,
            "max_retries": self.retry_attempts,
        }

    def get_model_id(self, model: Optional[str] = None) -> str:
        """Get model ID with legacy mapping support"""
        model = model or self.default_model

        # Legacy mappings
        legacy_mappings = {
            "gemini25": "google/gemini-2.5-pro-preview",
            "gpt41": "openai/gpt-4.1",
            "gemini25flashpreview": "google/gemini-2.5-flash-preview",
            "claude37": "anthropic/claude-3.7-sonnet",
        }

        # Check custom mappings first
        if model in self.custom_model_mappings:
            return self.custom_model_mappings[model]

        # Check legacy mappings if enabled
        if self.enable_legacy_models and model in legacy_mappings:
            return legacy_mappings[model]

        return model

    def setup_logging(self):
        """Setup logging based on configuration"""
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format=log_format,
            handlers=[logging.StreamHandler(sys.stdout)],
        )

        if self.debug:
            # Enable debug logging for HTTP requests
            import http.client as http_client

            http_client.HTTPConnection.debuglevel = 1

            # Enable urllib3 debugging
            logging.getLogger("urllib3").setLevel(logging.DEBUG)


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing"""

    pass


def parse_bool(value: str) -> bool:
    """Parse string to boolean"""
    return value.lower() in ("true", "1", "yes", "on")


def parse_list(value: str, delimiter: str = ",") -> List[str]:
    """Parse comma-separated string to list"""
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter) if item.strip()]


def parse_dict(
    value: str, pair_delimiter: str = ",", key_value_delimiter: str = ":"
) -> Dict[str, str]:
    """Parse string to dictionary"""
    if not value:
        return {}

    result = {}
    pairs = value.split(pair_delimiter)
    for pair in pairs:
        if key_value_delimiter in pair:
            key, value = pair.split(key_value_delimiter, 1)
            result[key.strip()] = value.strip()
    return result


@lru_cache(maxsize=1)
def load_config(
    env_file: Optional[str] = None, validate: bool = True
) -> KilocodeConfig:
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
        load_dotenv(env_file)
    else:
        # Try to find .env in current directory or parent directories
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents):
            env_path = parent / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                break

    # Load token (required)
    token = os.getenv("KILOCODE_TOKEN")
    if validate and not token:
        raise ConfigurationError(
            "KILOCODE_TOKEN is required. "
            "Get your token from https://kilocode.ai/auth/signin"
        )

    # Create configuration
    config = KilocodeConfig(
        # Authentication
        token=token or "",
        auth_source=os.getenv("KILOCODE_AUTH_SOURCE", "web"),
        # API Configuration
        base_url=os.getenv("KILOCODE_BASE_URL", "https://kilocode.ai"),
        api_version=os.getenv("KILOCODE_API_VERSION", "v1"),
        openrouter_path=os.getenv("KILOCODE_OPENROUTER_PATH", "/api/openrouter"),
        # Default Model Settings
        default_model=os.getenv(
            "KILOCODE_DEFAULT_MODEL", "google/gemini-2.5-pro-preview"
        ),
        default_temperature=float(os.getenv("KILOCODE_DEFAULT_TEMPERATURE", "0.7")),
        default_max_tokens=int(os.getenv("KILOCODE_DEFAULT_MAX_TOKENS", "1000")),
        default_top_p=(
            float(os.getenv("KILOCODE_DEFAULT_TOP_P"))
            if os.getenv("KILOCODE_DEFAULT_TOP_P")
            else None
        ),
        # Feature Flags
        enable_streaming=parse_bool(os.getenv("KILOCODE_ENABLE_STREAMING", "true")),
        include_usage=parse_bool(os.getenv("KILOCODE_INCLUDE_USAGE", "true")),
        use_transforms=parse_bool(os.getenv("KILOCODE_USE_TRANSFORMS", "true")),
        enable_reasoning=parse_bool(os.getenv("KILOCODE_ENABLE_REASONING", "true")),
        enable_caching=parse_bool(os.getenv("KILOCODE_ENABLE_CACHING", "true")),
        # Headers Configuration
        http_referer=os.getenv("KILOCODE_HTTP_REFERER", "https://kilocode.ai"),
        x_title=os.getenv("KILOCODE_X_TITLE", "Kilo Code"),
        version=os.getenv("KILOCODE_VERSION", "1.0.0"),
        # Advanced Settings
        provider_order=parse_list(os.getenv("KILOCODE_PROVIDER_ORDER", "")),
        allow_fallbacks=parse_bool(os.getenv("KILOCODE_ALLOW_FALLBACKS", "true")),
        cache_models=parse_bool(os.getenv("KILOCODE_CACHE_MODELS", "true")),
        cache_ttl=int(os.getenv("KILOCODE_CACHE_TTL", "3600")),
        # Development/Debug
        debug=parse_bool(os.getenv("KILOCODE_DEBUG", "false")),
        log_level=os.getenv("KILOCODE_LOG_LEVEL", "INFO").upper(),
        retry_attempts=int(os.getenv("KILOCODE_RETRY_ATTEMPTS", "3")),
        retry_delay=float(os.getenv("KILOCODE_RETRY_DELAY", "1.0")),
        request_timeout=int(os.getenv("KILOCODE_REQUEST_TIMEOUT", "120")),
        # Profile/Balance Monitoring
        check_balance=parse_bool(os.getenv("KILOCODE_CHECK_BALANCE", "false")),
        balance_warning_threshold=float(
            os.getenv("KILOCODE_BALANCE_WARNING_THRESHOLD", "10.0")
        ),
        # Rate Limiting
        rate_limit_rpm=(
            int(os.getenv("KILOCODE_RATE_LIMIT_RPM"))
            if os.getenv("KILOCODE_RATE_LIMIT_RPM")
            else None
        ),
        rate_limit_tpm=(
            int(os.getenv("KILOCODE_RATE_LIMIT_TPM"))
            if os.getenv("KILOCODE_RATE_LIMIT_TPM")
            else None
        ),
        # Legacy Model Support
        enable_legacy_models=parse_bool(
            os.getenv("KILOCODE_ENABLE_LEGACY_MODELS", "true")
        ),
        custom_model_mappings=parse_dict(
            os.getenv("KILOCODE_CUSTOM_MODEL_MAPPINGS", "")
        ),
        # Proxy Settings
        http_proxy=os.getenv("HTTP_PROXY"),
        https_proxy=os.getenv("HTTPS_PROXY"),
        no_proxy=parse_list(os.getenv("NO_PROXY", "")),
    )

    # Auto-detect development environment from token
    if config.token:
        try:
            import base64
            import json

            # Parse JWT payload
            payload_string = config.token.split(".")[1]
            # Add padding if needed
            payload_string += "=" * (4 - len(payload_string) % 4)
            payload = json.loads(base64.b64decode(payload_string))

            # Override base URL for development
            if (
                payload.get("env") == "development"
                and config.base_url == "https://kilocode.ai"
            ):
                config.base_url = "http://localhost:3000"
                if config.debug:
                    logging.info("Detected development token, using localhost:3000")
        except Exception:
            # Ignore token parsing errors
            pass

    # Setup logging if requested
    if config.debug:
        config.setup_logging()

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

        # Test model mapping
        test_models = ["gemini25", "gpt41", "claude37", "gpt-4"]
        print("\nModel Mappings:")
        for model in test_models:
            mapped = config.get_model_id(model)
            if model != mapped:
                print(f"  {model} -> {mapped}")
            else:
                print(f"  {model} (no mapping)")

    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
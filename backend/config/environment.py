"""Environment configuration."""

import os
from typing import Any, Dict


class Environment:
    """Environment configuration management."""

    _config: Dict[str, Any] = None

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration values."""
        if cls._config is None:
            # Check all required variables first
            required_vars = ["JWT_SECRET_KEY", "GOOGLE_CLIENT_ID", "APPLE_CLIENT_ID"]
            missing = [var for var in required_vars if not os.getenv(var)]

            if missing:
                raise ValueError("Required environment variables not set: " + ", ".join(missing))

            cls._config = {
                "ENVIRONMENT": cls.get("ENVIRONMENT", "development"),
                "JWT_SECRET_KEY": cls.get_required("JWT_SECRET_KEY"),
                "GOOGLE_CLIENT_ID": cls.get_required("GOOGLE_CLIENT_ID"),
                "APPLE_CLIENT_ID": cls.get_required("APPLE_CLIENT_ID"),
            }
        return cls._config

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get environment variable with default."""
        return os.getenv(key, default)

    @staticmethod
    def get_required(key: str) -> str:
        """Get required environment variable."""
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Required environment variable {key} not set")
        return value

    @staticmethod
    def is_testing() -> bool:
        """Check if running in test environment."""
        return Environment.get("ENVIRONMENT") == "test"

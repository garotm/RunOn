"""Environment configuration."""

import os
from typing import Optional


class Environment:
    """Environment configuration management."""

    @staticmethod
    def get(key: str) -> Optional[str]:
        """Get environment variable value."""
        return os.getenv(key)

    @staticmethod
    def get_required(key: str) -> str:
        """Get required environment variable value."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} not set")
        return value

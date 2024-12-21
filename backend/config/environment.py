import os
from typing import Dict, Any


class Environment:
    """Environment configuration management."""
    
    _config = None  # Class variable to store configuration
    
    @staticmethod
    def get_required(key: str) -> str:
        """Get required environment variable."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f'Required environment variable {key} not set')
        return value
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration values."""
        if cls._config is None:
            # First check required variables
            required_vars = ['GOOGLE_CLIENT_ID', 'APPLE_CLIENT_ID', 'JWT_SECRET_KEY']
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            
            if missing_vars:
                raise ValueError(f'Required environment variables not set: {", ".join(missing_vars)}')
            
            cls._config = {
                'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
                'APPLE_CLIENT_ID': os.getenv('APPLE_CLIENT_ID'),
                'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY'),
                'ENVIRONMENT': os.getenv('ENVIRONMENT', 'development')  # Default to 'development'
            }
        return cls._config
    
    @classmethod
    def initialize(cls, testing: bool = False) -> None:
        """Initialize configuration."""
        if testing:
            cls._config = {
                'GOOGLE_CLIENT_ID': 'test-google-id',
                'APPLE_CLIENT_ID': 'test-apple-id',
                'JWT_SECRET_KEY': 'test-secret-key',
                'ENVIRONMENT': 'development'  # Changed from 'test' to 'development'
            }
        else:
            cls._config = None  # Force reloading of config
"""Security configuration."""

from dataclasses import dataclass


@dataclass
class SecurityConfig:
    """Security configuration settings."""

    jwt_secret_key: str = "default-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expiry: int = 3600
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    def __post_init__(self):
        """Validate configuration values."""
        if self.jwt_expiry <= 0:
            raise ValueError("JWT expiry must be positive")
        if self.rate_limit_requests <= 0:
            raise ValueError("Rate limit requests must be positive")
        if self.rate_limit_window <= 0:
            raise ValueError("Rate limit window must be positive")

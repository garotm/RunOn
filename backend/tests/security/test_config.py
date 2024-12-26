"""Tests for security configuration."""

import pytest

from security.config import SecurityConfig


def test_security_config_defaults():
    """Test default security configuration values."""
    config = SecurityConfig()
    assert config.jwt_secret_key is not None
    assert config.jwt_algorithm == "HS256"
    assert config.jwt_expiry == 3600
    assert config.rate_limit_requests == 100
    assert config.rate_limit_window == 60


def test_security_config_custom_values():
    """Test custom security configuration values."""
    config = SecurityConfig(
        jwt_secret_key="custom-secret",
        jwt_algorithm="RS256",
        jwt_expiry=7200,
        rate_limit_requests=50,
        rate_limit_window=30,
    )
    assert config.jwt_secret_key == "custom-secret"
    assert config.jwt_algorithm == "RS256"
    assert config.jwt_expiry == 7200
    assert config.rate_limit_requests == 50
    assert config.rate_limit_window == 30


def test_security_config_validation():
    """Test security configuration validation."""
    with pytest.raises(ValueError):
        SecurityConfig(jwt_expiry=-1)

    with pytest.raises(ValueError):
        SecurityConfig(rate_limit_requests=0)

    with pytest.raises(ValueError):
        SecurityConfig(rate_limit_window=0)

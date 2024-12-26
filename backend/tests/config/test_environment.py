"""Tests for environment configuration."""

from unittest.mock import patch

import pytest

from config.environment import Environment


def test_get_required_existing():
    """Test getting required environment variable that exists."""
    with patch.dict("os.environ", {"TEST_VAR": "test-value"}, clear=True):
        value = Environment.get_required("TEST_VAR")
        assert value == "test-value"


def test_get_required_missing():
    """Test getting required environment variable that's missing."""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError) as exc:
            Environment.get_required("TEST_VAR")
        assert "Required environment variable TEST_VAR not set" in str(exc.value)


def test_get_config():
    """Test getting all configuration values."""
    mock_env = {
        "GOOGLE_CLIENT_ID": "google-id",
        "APPLE_CLIENT_ID": "apple-id",
        "JWT_SECRET_KEY": "secret-key",
        "ENVIRONMENT": "test",
    }

    with patch.dict("os.environ", mock_env, clear=True):
        Environment._config = None  # Reset config
        config = Environment.get_config()
        assert config["GOOGLE_CLIENT_ID"] == "google-id"
        assert config["APPLE_CLIENT_ID"] == "apple-id"
        assert config["JWT_SECRET_KEY"] == "secret-key"
        assert config["ENVIRONMENT"] == "test"


def test_get_config_default_environment():
    """Test getting config with default environment."""
    mock_env = {
        "GOOGLE_CLIENT_ID": "google-id",
        "APPLE_CLIENT_ID": "apple-id",
        "JWT_SECRET_KEY": "secret-key",
    }

    with patch.dict("os.environ", mock_env, clear=True):
        Environment._config = None  # Reset config
        config = Environment.get_config()
        assert config["ENVIRONMENT"] == "development"


def test_get_config_missing_required():
    """Test config fails with missing required variables."""
    mock_env = {
        "GOOGLE_CLIENT_ID": "google-id"
        # Missing APPLE_CLIENT_ID and JWT_SECRET_KEY
    }

    with patch.dict("os.environ", mock_env, clear=True):
        Environment._config = None  # Reset config
        with pytest.raises(ValueError) as exc:
            Environment.get_config()
        assert "Required environment variables not set:" in str(exc.value)
        assert "JWT_SECRET_KEY" in str(exc.value)
        assert "APPLE_CLIENT_ID" in str(exc.value)


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset Environment configuration before each test."""
    Environment._config = None
    yield
    Environment._config = None

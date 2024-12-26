"""Test configuration and fixtures."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables."""
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("STACKDRIVER_PROJECT_ID", "test-project")
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "test-project")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("GOOGLE_SEARCH_API_KEY", "test-api-key")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "test-credentials.json")
    monkeypatch.setenv("GOOGLE_SEARCH_ENGINE_ID", "test-engine-id")


@pytest.fixture(autouse=True)
def mock_monitoring():
    """Mock monitoring client."""
    with patch("google.cloud.monitoring_v3.MetricServiceClient") as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_redis():
    """Mock Redis client."""
    with patch("redis.Redis") as mock:
        mock_client = MagicMock()
        mock.from_url.return_value = mock_client
        yield mock_client

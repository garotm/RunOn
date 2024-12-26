"""Test fixtures and configuration."""
import os

import pytest


@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment."""
    os.environ["ENVIRONMENT"] = "test"
    os.environ["JWT_SECRET_KEY"] = "test-key"
    os.environ["GOOGLE_SEARCH_API_KEY"] = "test-search-key"
    os.environ["GOOGLE_SEARCH_ENGINE_ID"] = "test-engine-id"
    yield
    os.environ.pop("ENVIRONMENT", None)
    os.environ.pop("JWT_SECRET_KEY", None)
    os.environ.pop("GOOGLE_SEARCH_API_KEY", None)
    os.environ.pop("GOOGLE_SEARCH_ENGINE_ID", None)

"""Shared test fixtures."""
from unittest.mock import MagicMock

import pytest
from google.oauth2.credentials import Credentials


@pytest.fixture
def mock_credentials():
    """Mock Google OAuth credentials."""
    return MagicMock(spec=Credentials)

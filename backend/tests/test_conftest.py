"""Tests for conftest fixtures."""
from unittest.mock import MagicMock

from google.oauth2.credentials import Credentials


def test_mock_credentials_fixture(mock_credentials):
    """Test mock_credentials fixture."""
    # Verify it's a MagicMock
    assert isinstance(mock_credentials, MagicMock)

    # Verify it mocks Credentials
    assert isinstance(mock_credentials, MagicMock)
    assert mock_credentials._spec_class == Credentials

    # Test some common Credentials methods
    assert hasattr(mock_credentials, "valid")
    assert hasattr(mock_credentials, "expired")
    assert hasattr(mock_credentials, "refresh")

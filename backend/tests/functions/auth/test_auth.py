"""Tests for authentication functionality."""

from unittest.mock import patch

import pytest

from functions.auth import verify_google_id_token


@pytest.fixture
def mock_environment():
    """Mock environment variables."""
    with patch("config.environment.Environment.get_required") as mock:
        mock.return_value = "test-client-id"
        yield mock


@pytest.fixture
def mock_id_token():
    """Mock Google ID token verification."""
    with patch("google.oauth2.id_token.verify_oauth2_token") as mock:
        mock.return_value = {"sub": "123", "email": "test@example.com"}
        yield mock


def test_verify_google_id_token_success(mock_environment, mock_id_token):
    """Test successful token verification."""
    token = "valid-token"
    result = verify_google_id_token(token)

    assert result["sub"] == "123"
    assert result["email"] == "test@example.com"
    mock_id_token.assert_called_once()


def test_verify_google_id_token_invalid(mock_environment, mock_id_token):
    """Test invalid token handling."""
    mock_id_token.side_effect = ValueError("Invalid token")

    with pytest.raises(ValueError) as exc:
        verify_google_id_token("invalid-token")

    assert "Invalid token" in str(exc.value)

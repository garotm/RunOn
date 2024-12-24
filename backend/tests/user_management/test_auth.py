"""Tests for authentication functionality."""

from unittest.mock import patch

import pytest

from functions.user_management.auth import (
    create_session_token,
    verify_google_token,
    verify_session_token,
)


def test_verify_google_token_valid():
    """Test Google token verification with valid token."""
    mock_info = {"sub": "123", "email": "test@example.com", "name": "Test User"}

    with patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_info):
        with patch("google.auth.transport.requests.Request") as mock_request:
            result = verify_google_token("valid-token")
            assert result == mock_info
            mock_request.assert_called_once()


def test_verify_google_token_invalid():
    """Test Google token verification with invalid token."""
    with patch(
        "google.oauth2.id_token.verify_oauth2_token", side_effect=ValueError("Invalid token")
    ):
        with pytest.raises(ValueError) as exc:
            verify_google_token("invalid-token")
        assert "Invalid token" in str(exc.value)


def test_create_session_token():
    """Test session token creation."""
    user_data = {"id": "123", "email": "test@example.com"}
    token = create_session_token(user_data)
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_session_token_valid():
    """Test session token verification with valid token."""
    user_data = {"id": "123", "email": "test@example.com"}
    token = create_session_token(user_data)
    result = verify_session_token(token)
    assert result["sub"] == user_data["id"]
    assert result["email"] == user_data["email"]


def test_verify_session_token_invalid():
    """Test session token verification with invalid token."""
    with pytest.raises(ValueError):
        verify_session_token("invalid-token")

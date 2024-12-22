from unittest.mock import Mock, patch

import jwt
import pytest

from functions.user_management.auth import (
    create_session_token,
    verify_google_token,
    verify_session_token,
)


def test_verify_google_token():
    """Test Google token verification."""
    mock_token = "google-token"
    mock_user_info = {
        "sub": "google123",
        "email": "test@gmail.com",
        "name": "Test User",
    }

    with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.return_value = mock_user_info
        result = verify_google_token(mock_token)

        assert result == mock_user_info
        mock_verify.assert_called_once()


def test_create_session_token():
    """Test session token creation."""
    mock_user = Mock(
        id="user123", email="test@example.com", name="Test User"
    )

    with patch("jwt.encode") as mock_encode:
        mock_encode.return_value = "session-token"
        result = create_session_token(mock_user)

        assert result == "session-token"
        mock_encode.assert_called_once()


def test_verify_session_token():
    """Test session token verification."""
    mock_token = "valid-token"
    mock_payload = {"sub": "user123", "email": "test@example.com"}

    with patch("jwt.decode") as mock_decode:
        mock_decode.return_value = mock_payload
        result = verify_session_token(mock_token)

        assert result == mock_payload
        mock_decode.assert_called_once()


def test_verify_session_token_invalid():
    """Test session token verification with invalid token."""
    mock_token = "invalid-token"

    with patch("jwt.decode") as mock_decode:
        mock_decode.side_effect = jwt.InvalidTokenError()
        result = verify_session_token(mock_token)

        assert result is None
        mock_decode.assert_called_once()
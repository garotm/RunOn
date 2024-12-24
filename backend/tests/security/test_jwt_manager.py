"""Tests for JWT manager."""
from security.jwt_manager import verify_token


def test_verify_token_invalid():
    """Test token verification with invalid token."""
    assert not verify_token("invalid-token")

"""Authentication functionality."""

from typing import Any, Dict

from google.auth.transport import requests
from google.oauth2 import id_token

from security.jwt_manager import create_token, verify_token


def verify_google_token(token: str) -> Dict[str, Any]:
    """Verify Google OAuth token."""
    try:
        return id_token.verify_oauth2_token(token, requests.Request())
    except ValueError as e:
        raise ValueError(f"Invalid token: {str(e)}")


def create_session_token(user: Dict[str, Any]) -> str:
    """Create a session token for the user.

    Args:
        user: User data dictionary

    Returns:
        str: JWT session token
    """
    payload = {"sub": user["id"], "email": user["email"], "name": user.get("name", "")}
    return create_token(payload)


def verify_session_token(token: str) -> Dict[str, Any]:
    """Verify session token.

    Args:
        token: JWT token string

    Returns:
        Dict: Token payload if valid

    Raises:
        ValueError: If token is invalid
    """
    payload = verify_token(token)
    if not payload:
        raise ValueError("Invalid token")
    return payload

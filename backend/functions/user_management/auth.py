import os
from typing import Any, Dict, Optional

import jwt
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token


def verify_google_token(token: str) -> Dict[str, Any]:
    """Verify Google OAuth token."""
    return id_token.verify_oauth2_token(
        token, google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
    )


def create_session_token(user: Any) -> str:
    """Create a session token for the user.

    Args:
        user: User object

    Returns:
        str: JWT session token
    """
    payload = {"sub": user.id, "email": user.email, "name": user.name}

    return jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")


def verify_session_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify a session token.

    Args:
        token: JWT token to verify

    Returns:
        Dict containing user information or None if invalid
    """
    try:
        return jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None

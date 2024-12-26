"""JWT token management."""

from typing import Any, Dict, Optional

import jwt

from config import Environment


def create_token(payload: Dict[str, Any]) -> str:
    """Create a JWT token.

    Args:
        payload: Data to encode in the token

    Returns:
        str: Encoded JWT token
    """
    return jwt.encode(payload, Environment.get_required("JWT_SECRET_KEY"), algorithm="HS256")


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify a JWT token.

    Args:
        token: JWT token to verify

    Returns:
        Dict: Token payload if valid, None if invalid
    """
    try:
        return jwt.decode(token, Environment.get_required("JWT_SECRET_KEY"), algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None

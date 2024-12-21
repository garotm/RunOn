import os
from typing import Any, Dict, Optional

import jwt
import requests
from cachetools import TTLCache, cached
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

# Cache Apple's public keys for 24 hours
APPLE_KEY_CACHE = TTLCache(maxsize=100, ttl=86400)


def verify_google_token(token: str) -> Dict[str, Any]:
    """Verify Google OAuth token."""
    return id_token.verify_oauth2_token(
        token, google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
    )


@cached(cache=APPLE_KEY_CACHE)
def get_apple_public_key(kid: str) -> Dict[str, Any]:
    """Fetch Apple's public key for token verification."""
    response = requests.get("https://appleid.apple.com/auth/keys")
    keys = response.json()["keys"]

    # Find the key matching the kid (Key ID)
    for key in keys:
        if key["kid"] == kid:
            return key
    raise ValueError(f"Key ID {kid} not found in Apple public keys")


def verify_apple_token(token: str) -> Dict[str, Any]:
    """Verify Apple Sign In token."""
    # Decode the JWT header without verification to get the key ID
    header = jwt.get_unverified_header(token)
    kid = header["kid"]

    # Get Apple's public key
    public_key = get_apple_public_key(kid)

    # Verify and decode the token
    try:
        payload = jwt.decode(
            token,
            jwt.algorithms.RSAAlgorithm.from_jwk(public_key),
            algorithms=["RS256"],
            audience=os.getenv("APPLE_CLIENT_ID"),
            issuer="https://appleid.apple.com",
        )

        # Convert to standard claims format
        return {
            "sub": payload["sub"],  # Apple's unique user ID
            "email": payload.get("email"),
            "name": payload.get("name", {}).get("firstName", "")
            + " "
            + payload.get("name", {}).get("lastName", ""),
            "email_verified": payload.get("email_verified", False),
        }

    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid Apple token: {str(e)}")


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

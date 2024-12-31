"""Authentication functionality."""

import logging

from google.auth.transport import requests
from google.oauth2 import id_token

from config.environment import Environment

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def verify_google_id_token(token: str) -> dict:
    """Verify Google ID token and return payload.

    Args:
        token: The Google ID token to verify

    Returns:
        dict: The decoded token payload

    Raises:
        ValueError: If token is invalid
    """
    try:
        client_id = Environment.get_required("RUNON_CLIENT_ID")
        logger.debug(f"Using client_id: {client_id[:10]}...")
        logger.debug(f"Token received: {token[:10]}...")

        request = requests.Request()
        idinfo = id_token.verify_oauth2_token(token, request, client_id)
        logger.debug(f"Token verification successful: {str(idinfo)[:100]}...")
        return idinfo
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        logger.error(f"Token: {token[:10]}...")
        logger.error(f"Client ID: {client_id[:10]}...")
        raise ValueError(f"Invalid token: {str(e)}")

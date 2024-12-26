"""Security middleware."""

from functools import wraps

from flask import request
from werkzeug.exceptions import Unauthorized

from security.jwt_manager import verify_token


def require_auth(f):
    """Require authentication decorator."""

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise Unauthorized("No authorization header")

        try:
            token = auth_header.split(" ")[1]
            verify_token(token)
        except Exception as e:
            raise Unauthorized(str(e))

        return f(*args, **kwargs)

    return decorated

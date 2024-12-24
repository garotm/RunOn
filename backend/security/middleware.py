"""Security middleware package."""

from functools import wraps
from typing import Callable

from flask import abort, request


def require_auth(f: Callable) -> Callable:
    """Require authentication decorator."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            abort(401)
        return f(*args, **kwargs)

    return decorated

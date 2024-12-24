"""Rate limiting functionality."""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List


class RateLimiter:
    """Rate limiter implementation."""

    def __init__(self, window_size: int = 60, max_requests: int = 100):
        """Initialize rate limiter."""
        self._window_size = timedelta(seconds=window_size)
        self._max_requests = max_requests
        self._request_logs: Dict[str, List[datetime]] = defaultdict(list)

    def check_rate_limit(self, user_id: str) -> None:
        """Check if user has exceeded rate limit."""
        now = datetime.utcnow()
        user_requests = self._request_logs[user_id]

        while user_requests and now - user_requests[0] > self._window_size:
            user_requests.pop(0)

        if len(user_requests) >= self._max_requests:
            raise Exception("Rate limit exceeded")

        user_requests.append(now)

    def clear(self) -> None:
        """Clear all rate limit data."""
        self._request_logs.clear()


_rate_limiter = RateLimiter()


def check_rate_limit(user_id: str) -> None:
    """Check rate limit for user."""
    _rate_limiter.check_rate_limit(user_id)


def get_rate_limiter() -> RateLimiter:
    """Get rate limiter instance."""
    return _rate_limiter

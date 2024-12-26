"""Tests for rate limiter."""

import time

import pytest

from security.rate_limiter import RateLimiter


@pytest.fixture
def rate_limiter():
    """Create a test rate limiter."""
    limiter = RateLimiter(window_size=1, max_requests=2)
    yield limiter
    limiter.clear()


def test_rate_limit_not_exceeded(rate_limiter):
    """Test rate limit within bounds."""
    rate_limiter.check_rate_limit("test-user")
    rate_limiter.check_rate_limit("test-user")


def test_rate_limit_exceeded(rate_limiter):
    """Test rate limit exceeded."""
    rate_limiter.check_rate_limit("test-user")
    rate_limiter.check_rate_limit("test-user")

    with pytest.raises(Exception) as exc:
        rate_limiter.check_rate_limit("test-user")
    assert "Rate limit exceeded" in str(exc.value)


def test_rate_limit_window_reset():
    """Test rate limit window reset."""
    limiter = RateLimiter(window_size=1, max_requests=1)
    limiter.check_rate_limit("test-user")

    time.sleep(1.1)
    limiter.check_rate_limit("test-user")

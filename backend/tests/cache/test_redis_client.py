"""Tests for Redis cache client."""

import json
from unittest.mock import patch

from cache.redis_client import cache_key, get_cache, invalidate_cache, set_cache


def test_cache_key():
    """Test cache key generation."""
    assert cache_key("prefix", 123, "test") == "prefix:123:test"
    assert cache_key("user", "profile", 456) == "user:profile:456"
    assert cache_key() == ""


@patch("cache.redis_client.redis_client")
def test_set_cache(mock_client):
    """Test setting cache values."""
    data = {"test": "value"}
    set_cache("test_key", data)
    mock_client.set.assert_called_once_with("test_key", json.dumps(data))

    mock_client.reset_mock()
    set_cache("test_key", data, ttl=60)
    mock_client.setex.assert_called_once_with("test_key", 60, json.dumps(data))


@patch("cache.redis_client.redis_client")
def test_get_cache(mock_client):
    """Test getting cache values."""
    mock_client.get.return_value = '{"test": "value"}'
    result = get_cache("test_key")
    assert result == {"test": "value"}
    mock_client.get.assert_called_once_with("test_key")

    mock_client.reset_mock()
    mock_client.get.return_value = None
    result = get_cache("missing_key")
    assert result is None


@patch("cache.redis_client.redis_client")
def test_invalidate_cache(mock_client):
    """Test cache invalidation."""
    invalidate_cache("test_key")
    mock_client.delete.assert_called_once_with("test_key")

"""Redis cache client configuration."""

import json
from typing import Any, Optional

import redis

from config import Environment

# Initialize Redis client with error handling
try:
    redis_client = redis.Redis.from_url(
        Environment.get("REDIS_URL", "redis://localhost:6379/0"),
        decode_responses=True,
    )
except Exception as e:
    print(f"Redis connection error: {e}")
    redis_client = None


def cache_key(*args: Any) -> str:
    """Generate cache key from arguments."""
    return ":".join(str(arg) for arg in args)


def set_cache(key: str, value: Any, ttl: Optional[int] = None) -> None:
    """Set cache value with optional TTL."""
    try:
        serialized = json.dumps(value)
        if ttl:
            redis_client.setex(key, ttl, serialized)
        else:
            redis_client.set(key, serialized)
    except Exception as e:
        print(f"Cache set error: {e}")


def get_cache(key: str) -> Optional[Any]:
    """Get cached value."""
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except Exception as e:
        print(f"Cache get error: {e}")
        return None


def invalidate_cache(key: str) -> None:
    """Remove cached value."""
    try:
        redis_client.delete(key)
    except Exception as e:
        print(f"Cache invalidate error: {e}")

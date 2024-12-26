"""Cache decorators."""

from functools import wraps
from typing import Any, Callable, Optional

from .redis_client import cache_key, get_cache, invalidate_cache, set_cache


def cached(prefix: str, ttl: Optional[int] = None) -> Callable:
    """Cache function results."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate cache key
            key = cache_key(prefix, *args, *kwargs.values())

            # Try to get from cache
            cached_value = get_cache(key)
            if cached_value is not None:
                return cached_value

            # Execute function and cache result
            result = await func(*args, **kwargs)
            set_cache(key, result, ttl)
            return result

        return wrapper

    return decorator


def invalidate_on_update(prefix: str) -> Callable:
    """Invalidate cache after function execution."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Execute function
            result = await func(*args, **kwargs)

            # Invalidate cache
            key = cache_key(prefix, *args, *kwargs.values())
            invalidate_cache(key)

            return result

        return wrapper

    return decorator

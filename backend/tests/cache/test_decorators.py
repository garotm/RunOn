"""Tests for cache decorators."""

from unittest.mock import AsyncMock, patch

import pytest

from cache.decorators import cached, invalidate_on_update


@pytest.mark.asyncio
async def test_cached_decorator():
    """Test cached decorator."""
    mock_function = AsyncMock(return_value={"data": "test"})

    # Apply decorator
    decorated = cached("test")(mock_function)

    with patch("cache.decorators.get_cache") as mock_get, patch(
        "cache.decorators.set_cache"
    ) as mock_set:
        # Test cache miss
        mock_get.return_value = None
        result = await decorated("arg1", kwarg1="value1")

        assert result == {"data": "test"}
        mock_get.assert_called_once()
        mock_set.assert_called_once()
        mock_function.assert_called_once()

        # Test cache hit
        mock_get.return_value = {"data": "cached"}
        mock_function.reset_mock()

        result = await decorated("arg1", kwarg1="value1")
        assert result == {"data": "cached"}
        mock_function.assert_not_called()


@pytest.mark.asyncio
async def test_invalidate_on_update_decorator():
    """Test invalidate_on_update decorator."""
    mock_function = AsyncMock(return_value={"data": "updated"})

    # Apply decorator
    decorated = invalidate_on_update("test")(mock_function)

    with patch("cache.decorators.invalidate_cache") as mock_invalidate:
        # Test cache invalidation
        result = await decorated("arg1", kwarg1="value1")

        assert result == {"data": "updated"}
        mock_function.assert_called_once()
        mock_invalidate.assert_called_once()

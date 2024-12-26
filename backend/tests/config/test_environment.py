"""Tests for environment configuration."""
import os
from unittest.mock import patch

import pytest

from config.environment import Environment


def test_get_environment_variable():
    """Test getting environment variable."""
    with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
        assert Environment.get("TEST_VAR") == "test_value"
        assert Environment.get("NONEXISTENT") is None


def test_get_required_environment_variable():
    """Test getting required environment variable."""
    with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
        assert Environment.get_required("TEST_VAR") == "test_value"

    with pytest.raises(ValueError):
        Environment.get_required("NONEXISTENT")

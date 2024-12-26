"""Tests for monitoring logger."""

from unittest.mock import Mock, patch

from monitoring.logger import setup_monitoring


def test_setup_monitoring():
    """Test monitoring setup configuration."""
    with patch("logging.basicConfig") as mock_logging:
        with patch("opencensus.trace.tracer.Tracer") as mock_tracer:
            with patch("google.auth.default", return_value=(Mock(), "test-project")):
                tracer = setup_monitoring()
                mock_logging.assert_called_once()
                mock_tracer.assert_called_once()
                assert tracer is not None


def test_logging_format():
    """Test logging format configuration."""
    with patch("logging.basicConfig") as mock_logging:
        with patch("google.auth.default", return_value=(Mock(), "test-project")):
            setup_monitoring()
            call_args = mock_logging.call_args[1]
            assert "format" in call_args
            assert "%(asctime)s" in call_args["format"]
            assert "%(levelname)s" in call_args["format"]

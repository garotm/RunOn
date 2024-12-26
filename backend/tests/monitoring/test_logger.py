"""Tests for monitoring logger."""

from unittest.mock import MagicMock, patch

import pytest

from monitoring.logger import create_metric, record_metric, setup_monitoring, trace_function


@patch("monitoring.logger.logging")
@patch("monitoring.logger.trace_exporter.StackdriverExporter")
def test_setup_monitoring(mock_exporter, mock_logging):
    """Test monitoring setup."""
    tracer = setup_monitoring()
    assert tracer is not None
    mock_logging.basicConfig.assert_called_once()


@patch("monitoring.logger.monitoring_v3")
@patch("monitoring.logger.client")
def test_create_metric(mock_client, mock_monitoring):
    """Test metric creation."""
    mock_descriptor = MagicMock()
    mock_monitoring.MetricDescriptor.return_value = mock_descriptor

    create_metric("test_metric", "Test description")

    mock_client.create_metric_descriptor.assert_called_once()
    assert mock_descriptor.type == "custom.googleapis.com/runon/test_metric"


@patch("monitoring.logger.monitoring_v3")
@patch("monitoring.logger.client")
@patch("monitoring.logger.time")
def test_record_metric(mock_time, mock_client, mock_monitoring):
    """Test metric recording."""
    mock_time.time.return_value = 1234567890
    mock_point = MagicMock()
    mock_monitoring.Point.return_value = mock_point
    mock_point.interval.end_time.seconds = 1234567890

    record_metric("test_metric", 1, {"label": "value"})

    mock_client.create_time_series.assert_called_once()


@pytest.mark.asyncio
@patch("monitoring.logger.setup_monitoring")
async def test_trace_function(mock_setup):
    """Test function tracing."""
    mock_tracer = MagicMock()
    mock_setup.return_value = mock_tracer
    mock_span = MagicMock()
    mock_tracer.span.return_value.__enter__.return_value = mock_span

    @trace_function("test_function")
    async def test_func():
        return "success"

    result = await test_func()
    assert result == "success"
    mock_span.add_attribute.assert_called_with("status", "success")

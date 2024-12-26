"""Tests for monitoring metrics."""

from unittest.mock import MagicMock, patch

import pytest

from monitoring.metrics import (
    MetricDescriptor,
    MetricKind,
    MetricsClient,
    create_metric_descriptor,
    record_metric,
)


@pytest.fixture
def mock_monitoring_client():
    """Create mock monitoring client."""
    with patch("monitoring.metrics.monitoring_v3.MetricServiceClient") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_create_metric_descriptor(mock_monitoring_client):
    """Test metric descriptor creation."""
    descriptor = MetricDescriptor(
        name="test_metric",
        description="Test metric description",
        kind=MetricKind.GAUGE,
    )

    create_metric_descriptor(descriptor)

    assert mock_monitoring_client.create_metric_descriptor.called


def test_record_metric(mock_monitoring_client):
    """Test metric recording."""
    name = "test_metric"
    value = 42
    labels = {"label1": "value1"}

    record_metric(name, value, labels)

    assert mock_monitoring_client.create_time_series.called


def test_metrics_client_initialization():
    """Test metrics client initialization."""
    with patch("monitoring.metrics.Environment.get") as mock_env:
        mock_env.return_value = "test-project"
        client = MetricsClient()
        assert client.project_id == "test-project"


def test_metrics_client_validation():
    """Test metrics client validation."""
    with patch("monitoring.metrics.Environment.get") as mock_env:
        mock_env.return_value = None
        with pytest.raises(ValueError):
            MetricsClient()

    with pytest.raises(ValueError):
        record_metric("test", -1, {})

    with pytest.raises(ValueError):
        create_metric_descriptor(None)

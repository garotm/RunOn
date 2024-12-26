"""Monitoring metrics configuration."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional

from google.cloud import monitoring_v3

from config import Environment


class MetricKind(Enum):
    """Metric kinds."""

    GAUGE = auto()
    COUNTER = auto()
    TIMER = auto()


@dataclass
class MetricDescriptor:
    """Metric descriptor configuration."""

    name: str
    description: str
    kind: MetricKind


class MetricsClient:
    """Metrics client for Google Cloud Monitoring."""

    def __init__(self, project_id: Optional[str] = None):
        """Initialize metrics client."""
        self.project_id = project_id or Environment.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Project ID is required")

        self.client = monitoring_v3.MetricServiceClient()


def create_metric_descriptor(descriptor: MetricDescriptor) -> None:
    """Create a custom metric descriptor."""
    if not descriptor:
        raise ValueError("Metric descriptor is required")

    client = MetricsClient()
    project_path = f"projects/{client.project_id}"

    descriptor_dict = {
        "name": descriptor.name,
        "type": f"custom.googleapis.com/runon/{descriptor.name}",
        "description": descriptor.description,
        "metric_kind": "GAUGE" if descriptor.kind == MetricKind.GAUGE else "CUMULATIVE",
        "value_type": "INT64",
    }

    client.client.create_metric_descriptor(
        name=project_path,
        metric_descriptor=descriptor_dict,
    )


def record_metric(name: str, value: int, labels: Dict[str, str]) -> None:
    """Record a metric value."""
    if value < 0:
        raise ValueError("Metric value must be non-negative")

    client = MetricsClient()
    project_path = f"projects/{client.project_id}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = f"custom.googleapis.com/runon/{name}"
    series.metric.labels.update(labels)

    point = monitoring_v3.Point()
    point.value.int64_value = value
    series.points.append(point)

    client.client.create_time_series(
        name=project_path,
        time_series=[series],
    )

"""Monitoring configuration."""

import logging
import time
from functools import wraps
from typing import Any, Callable, Dict, Optional

from google.cloud import monitoring_v3
from opencensus.ext.stackdriver import trace_exporter
from opencensus.trace import tracer as tracer_module
from opencensus.trace.span import SpanKind

from config import Environment

# Initialize monitoring client
try:
    client = monitoring_v3.MetricServiceClient()
    project_path = f"projects/{Environment.get('STACKDRIVER_PROJECT_ID')}"
except Exception:
    client = None
    project_path = None


def setup_monitoring() -> Any:
    """Setup monitoring and return tracer."""
    # Configure structured logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=Environment.get("LOG_LEVEL", "INFO"),
    )

    # Setup distributed tracing
    return tracer_module.Tracer(
        exporter=trace_exporter.StackdriverExporter(),
        sampler=tracer_module.samplers.AlwaysOnSampler(),
    )


def create_metric(name: str, description: str) -> None:
    """Create a custom metric."""
    if not client:
        return

    descriptor = monitoring_v3.MetricDescriptor()
    descriptor.type = f"custom.googleapis.com/runon/{name}"
    descriptor.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.GAUGE
    descriptor.value_type = monitoring_v3.MetricDescriptor.ValueType.INT64
    descriptor.description = description

    client.create_metric_descriptor(
        name=project_path,
        metric_descriptor=descriptor,
    )


def record_metric(name: str, value: int, labels: Optional[Dict[str, str]] = None) -> None:
    """Record a metric value."""
    if not client:
        return

    series = monitoring_v3.TimeSeries()
    series.metric.type = f"custom.googleapis.com/runon/{name}"
    if labels:
        series.metric.labels.update(labels)

    point = monitoring_v3.Point()
    point.value.int64_value = value
    point.interval.end_time.seconds = int(time.time())
    series.points = [point]

    client.create_time_series(
        name=project_path,
        time_series=[series],
    )


def trace_function(name: Optional[str] = None) -> Callable:
    """Decorator to trace function execution."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracer = setup_monitoring()
            with tracer.span(name=name or func.__name__) as span:
                span.span_kind = SpanKind.SERVER
                try:
                    result = func(*args, **kwargs)
                    span.add_attribute("status", "success")
                    return result
                except Exception as e:
                    span.add_attribute("status", "error")
                    span.add_attribute("error.message", str(e))
                    raise

        return wrapper

    return decorator

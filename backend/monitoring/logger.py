"""Monitoring configuration."""

import logging
from typing import Any

from opencensus.ext.stackdriver import trace_exporter
from opencensus.trace import tracer as tracer_module


def setup_monitoring() -> Any:
    """Setup monitoring and return tracer."""
    # Configure structured logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    # Setup distributed tracing
    return tracer_module.Tracer(
        exporter=trace_exporter.StackdriverExporter(),
        sampler=tracer_module.samplers.AlwaysOnSampler(),
    )

"""Tests for event discovery search."""

from datetime import datetime

from functions.event_discovery.search import search_running_events
from models.event import Event


def test_search_running_events():
    """Test searching for running events."""
    location = "New York"

    events = search_running_events(location)

    assert isinstance(events, list)
    assert len(events) > 0
    assert isinstance(events[0], Event)
    assert events[0].location == location


def test_search_running_events_returns_valid_event():
    """Test that returned event has required fields."""
    events = search_running_events("Boston")

    event = events[0]
    assert event.name
    assert isinstance(event.date, datetime)
    assert event.location

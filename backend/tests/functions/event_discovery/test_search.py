"""Tests for event discovery search."""

from unittest.mock import MagicMock, patch

import pytest

from functions.event_discovery.search import search_running_events
from models.event import Event


@pytest.fixture
def mock_environment():
    """Mock environment variables."""
    with patch("config.environment.Environment.get_required") as mock:
        mock.side_effect = ["test-api-key", "test-search-engine-id"]
        yield mock


@pytest.fixture
def mock_requests():
    """Mock requests library."""
    with patch("requests.get") as mock:
        mock.return_value = MagicMock(
            json=lambda: {
                "items": [
                    {
                        "title": "Test Run Event",
                        "snippet": "A test running event",
                        "link": "https://example.com/event",
                    }
                ]
            }
        )
        yield mock


def test_search_running_events_success(mock_environment, mock_requests):
    """Test successful event search."""
    location = "New York"
    events = search_running_events(location)

    assert len(events) == 1
    assert isinstance(events[0], Event)
    assert events[0].name == "Test Run Event"
    assert events[0].location == location
    assert events[0].description == "A test running event"
    assert events[0].url == "https://example.com/event"


def test_search_running_events_api_error(mock_environment, mock_requests):
    """Test handling of API errors."""
    mock_requests.side_effect = Exception("API Error")

    events = search_running_events("Boston")
    assert len(events) == 0


def test_search_running_events_no_results(mock_environment, mock_requests):
    """Test handling of no search results."""
    mock_requests.return_value = MagicMock(json=lambda: {"items": []})

    events = search_running_events("Remote Location")
    assert len(events) == 0

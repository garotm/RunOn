"""Tests for event discovery functionality."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
import requests

from functions.event_discovery.search import search_running_events


@pytest.fixture
def mock_environment():
    """Mock environment variables."""
    with patch("functions.event_discovery.search.Environment") as mock_env:
        mock_env.get_required.side_effect = lambda x: {
            "RUNON_API_KEY": "test-api-key",
            "RUNON_SEARCH_ENGINE_ID": "test-search-engine-id",
        }[x]
        yield mock_env


@pytest.fixture
def mock_requests(mock_search_response):
    """Mock requests.get for Google Custom Search API."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_search_response
        mock_get.return_value = mock_response
        yield mock_get


def test_search_running_events_success(mock_environment, mock_requests):
    """Test successful event search."""
    location = "New York"
    events = search_running_events(location)

    assert len(events) == 1
    event = events[0]
    assert event.name == "5K Run on March 15, 2024"
    assert event.date == datetime(2024, 3, 15)
    assert event.location == location
    assert event.url == "https://example.com/event1"
    assert event.distance == 5.0


def test_search_running_events_api_error(mock_environment, mock_requests):
    """Test handling of API errors."""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "API Error"
    mock_requests.return_value = mock_response

    events = search_running_events("Boston")
    assert len(events) == 0


def test_search_running_events_with_location(mock_environment, mock_requests):
    """Test search with location parameter."""
    location = "Boston"
    events = search_running_events("marathon", location=location)

    assert len(events) == 1
    event = events[0]
    assert event.location == location

    # Verify location was added to search terms
    call_args = mock_requests.call_args[1]
    assert location in call_args["params"]["q"]


def test_search_running_events_request_exception(mock_environment):
    """Test handling of request exceptions."""
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        events = search_running_events("marathon")
        assert len(events) == 0

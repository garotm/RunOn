"""Tests for event discovery functionality."""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
import requests

from functions.event_discovery.search import (
    CACHE_TTL,
    _cache,
    _get_cache_key,
    extract_date_from_text,
    extract_distance_from_text,
    search_running_events,
)


def test_extract_date_from_text_month_dd_yyyy():
    """Test extracting date in Month DD, YYYY format."""
    text = "Join us on March 15, 2024 for the annual run"
    result = extract_date_from_text(text)
    assert result == datetime(2024, 3, 15)


def test_extract_date_from_text_dd_month_yyyy():
    """Test extracting date in DD Month YYYY format."""
    text = "The race is on 15 March 2024"
    result = extract_date_from_text(text)
    assert result == datetime(2024, 3, 15)


def test_extract_date_from_text_mm_dd_yyyy():
    """Test extracting date in MM/DD/YYYY format."""
    text = "Race date: 03/15/2024"
    result = extract_date_from_text(text)
    assert result == datetime(2024, 3, 15)


def test_extract_date_from_text_yyyy_mm_dd():
    """Test extracting date in YYYY-MM-DD format."""
    text = "Event scheduled for 2024-03-15"
    result = extract_date_from_text(text)
    assert result == datetime(2024, 3, 15)


def test_extract_date_from_text_invalid():
    """Test handling invalid date text."""
    text = "No date here"
    result = extract_date_from_text(text)
    assert result is None


def test_extract_date_from_text_no_date():
    """Test handling text with no valid date."""
    text = "Join us for a great run!"
    result = extract_date_from_text(text)
    assert result is None


def test_extract_date_from_text_invalid_date():
    """Test handling text with invalid date format."""
    text = "The race is on 35/15/2024"  # Invalid date
    result = extract_date_from_text(text)
    assert result is None


def test_extract_distance_from_text_5k():
    """Test extracting 5K distance."""
    text = "Join our 5K run"
    result = extract_distance_from_text(text)
    assert result == 5.0


def test_extract_distance_from_text_10k():
    """Test extracting 10K distance."""
    text = "Annual 10K race"
    result = extract_distance_from_text(text)
    assert result == 10.0


def test_extract_distance_from_text_half_marathon():
    """Test extracting half marathon distance."""
    text = "City Half Marathon"
    result = extract_distance_from_text(text)
    assert result == 21.1


def test_extract_distance_from_text_marathon():
    """Test extracting marathon distance."""
    text = "Full Marathon Event"
    result = extract_distance_from_text(text)
    assert result == 42.2


def test_extract_distance_from_text_invalid():
    """Test handling text without distance."""
    text = "Fun Run Event"
    result = extract_distance_from_text(text)
    assert result is None


@pytest.fixture
def mock_env_vars():
    """Mock environment variables."""
    with patch("functions.event_discovery.search.Environment") as mock_env:
        mock_env.get_required.side_effect = lambda x: {
            "RUNON_API_KEY": "test_api_key",
            "RUNON_SEARCH_ENGINE_ID": "test_search_engine_id",
        }[x]
        yield mock_env


@pytest.fixture
def mock_search_response():
    """Mock Google Custom Search API response."""
    return {
        "items": [
            {
                "title": "5K Run on March 15, 2024",
                "snippet": "Join us for a 5K run through Central Park. Distance: 5K",
                "link": "https://example.com/event1",
                "pagemap": {
                    "metatags": [
                        {
                            "og:description": "5K run through Central Park",
                            "og:title": "5K Run on March 15, 2024",
                        }
                    ]
                },
            }
        ]
    }


@pytest.fixture
def mock_requests(mock_search_response):
    """Mock requests.get for Google Custom Search API."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_search_response
        mock_get.return_value = mock_response
        yield mock_get


def test_search_running_events_success(mock_env_vars, mock_requests):
    """Test successful event search."""
    location = "New York"

    # First call should hit the API
    events1 = search_running_events(location)
    assert len(events1) == 1
    mock_requests.assert_called_once()

    # Second call should use cache
    events2 = search_running_events(location)
    assert len(events2) == 1
    assert mock_requests.call_count == 1  # No additional API calls

    # Results should be the same
    assert events1 == events2


def test_search_running_events_api_error(mock_env_vars):
    """Test handling API errors."""
    # Clear the cache
    _cache.clear()

    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError("API Error")
        events = search_running_events("New York")
        assert len(events) == 0


def test_search_running_events_with_location(mock_env_vars, mock_requests):
    """Test search with location parameter."""
    location = "Boston"
    events = search_running_events("marathon", location=location)

    # Verify location was added to search terms
    call_args = mock_requests.call_args[1]
    assert location in call_args["params"]["q"]
    assert len(events) == 1


def test_search_running_events_caching(mock_env_vars, mock_requests):
    """Test that search results are cached."""
    # Clear the cache first
    _cache.clear()

    location = "New York"

    # First call should hit the API
    events1 = search_running_events(location)
    assert len(events1) == 1
    mock_requests.assert_called_once()

    # Second call should use cache
    events2 = search_running_events(location)
    assert len(events2) == 1
    assert mock_requests.call_count == 1  # No additional API calls

    # Results should be the same
    assert events1 == events2


def test_search_running_events_cache_expiry(mock_env_vars, mock_requests):
    """Test that cache expires after TTL."""
    # Clear the cache first
    _cache.clear()

    location = "New York"

    # First call should hit the API
    events1 = search_running_events(location)
    assert len(events1) == 1
    mock_requests.assert_called_once()

    # Simulate cache expiry
    cache_key = _get_cache_key(location)
    _cache[cache_key] = (_cache[cache_key][0], datetime.now() - CACHE_TTL - timedelta(seconds=1))

    # Second call should hit API again due to expired cache
    events2 = search_running_events(location)
    assert len(events2) == 1
    assert mock_requests.call_count == 2  # Additional API call made

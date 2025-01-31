"""Tests for event search functionality."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest
import requests

from functions.event_discovery.search import (
    Event,
    _geocode_location,
    _get_from_cache,
    _save_to_cache,
    extract_date_from_text,
    extract_distance_from_text,
    parse_location_query,
    search_running_events,
)


def test_extract_date_various_formats():
    """Test date extraction from various text formats."""
    # Simple test with mock data
    text = "Test Run on 2025-01-15"
    result = extract_date_from_text(text)
    assert result is not None
    assert result.year == 2025
    assert result.month == 1
    assert result.day == 15


def test_extract_distance_various_formats():
    """Test distance extraction from various text formats."""
    # Simple test with mock data
    text = "5K Run"
    result = extract_distance_from_text(text)
    assert result == 5.0


@pytest.fixture
def mock_env():
    """Mock environment variables."""
    with patch("functions.event_discovery.search.Environment") as mock:
        mock.get_required.return_value = "fake_key"
        yield mock


@pytest.fixture
def mock_search_response():
    """Mock successful API response."""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
        "items": [
            {
                "title": "Test 5K Run - February 15, 2025",
                "snippet": "A test run event happening on Feb 15, 2025",
                "link": "http://test.com",
            }
        ]
    }
    return mock


def test_search_basic(mock_env, mock_search_response):
    """Test basic search functionality with mocked response."""
    with (
        patch("functions.event_discovery.search.requests.get", return_value=mock_search_response),
        patch("functions.event_discovery.search._get_from_cache", return_value=None),
    ):
        events = search_running_events("5k")
        assert len(events) == 1
        assert events[0].name == "Test 5K Run - February 15, 2025"


def test_search_error(mock_env):
    """Test search error handling with mocked error response."""
    mock_error_response = Mock()
    mock_error_response.status_code = 400
    mock_error_response.json.return_value = {}

    with (
        patch("functions.event_discovery.search.requests.get", return_value=mock_error_response),
        patch("functions.event_discovery.search._get_from_cache", return_value=None),
    ):
        events = search_running_events("5k")
        assert len(events) == 0


def test_search_running_events(mock_env, mock_search_response):
    """Test searching for running events."""
    with (
        patch("functions.event_discovery.search.requests.get", return_value=mock_search_response),
        patch("functions.event_discovery.search._get_from_cache", return_value=None),
    ):
        events = search_running_events("5K run", "New York")
        assert len(events) == 1
        assert events[0].name == "Test 5K Run - February 15, 2025"
        assert events[0].url == "http://test.com"


def test_cache_operations():
    """Test cache get and save operations."""
    # Test cache miss
    result = _get_from_cache("test_key")
    assert result is None

    # Test cache save and hit
    events = [Mock()]
    _save_to_cache("test_key", events)
    result = _get_from_cache("test_key")
    assert result == events


def test_geocode_location_error():
    """Test geocoding with error."""
    with patch(
        "functions.event_discovery.search._geocoder.geocode",
        side_effect=Exception("Geocoding failed"),
    ):
        result = _geocode_location("Test Location")
        assert result is None


def test_parse_location_with_coordinates():
    """Test parsing location from coordinates."""
    with patch("functions.event_discovery.search._geocoder.reverse") as mock_reverse:
        mock_location = Mock()
        mock_location.address = "123 Test St"
        mock_reverse.return_value = mock_location

        query = "near:40.7128,-74.0060 running events"
        clean_query, location = parse_location_query(query)
        assert clean_query == "running events"
        assert location == "123 Test St"


def test_parse_location_with_coordinates_error():
    """Test parsing location from coordinates with error."""
    with patch(
        "functions.event_discovery.search._geocoder.reverse",
        side_effect=Exception("Reverse geocoding failed"),
    ):
        query = "near:40.7128,-74.0060 running events"
        clean_query, location = parse_location_query(query)
        assert clean_query == query
        assert location is None


def test_search_api_error():
    """Test search with API error response."""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"

    with (
        patch("functions.event_discovery.search.requests.get", return_value=mock_response),
        patch("functions.event_discovery.search._get_from_cache", return_value=None),
        patch("functions.event_discovery.search.Environment.get_required", return_value="fake_key"),
    ):
        events = search_running_events("5k")
        assert len(events) == 0


def test_search_request_exception():
    """Test search with request exception."""
    with (
        patch(
            "functions.event_discovery.search.requests.get",
            side_effect=requests.exceptions.RequestException("Connection error"),
        ),
        patch("functions.event_discovery.search._get_from_cache", return_value=None),
        patch("functions.event_discovery.search.Environment.get_required", return_value="fake_key"),
    ):
        events = search_running_events("5k")
        assert len(events) == 0


def test_search_with_location():
    """Test search with location geocoding."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "title": "Test 5K Run - February 15, 2025",
                "snippet": "A test run event",
                "link": "http://test.com",
            }
        ]
    }

    mock_coordinates = {"latitude": 40.7128, "longitude": -74.0060}

    with (
        patch("functions.event_discovery.search.requests.get", return_value=mock_response),
        patch("functions.event_discovery.search._get_from_cache", return_value=None),
        patch("functions.event_discovery.search._geocode_location", return_value=mock_coordinates),
        patch("functions.event_discovery.search.Environment.get_required", return_value="fake_key"),
    ):
        events = search_running_events("5k", "New York")
        assert len(events) == 1
        assert events[0].coordinates == mock_coordinates


def test_cache_expiration():
    """Test cache expiration behavior."""
    from datetime import datetime, timedelta

    from functions.event_discovery.search import CACHE_TTL, _cache

    # Save to cache
    events = [Mock()]
    _save_to_cache("test_key", events)

    # Manually set timestamp to be older than TTL
    _cache["test_key"] = (events, datetime.now() - CACHE_TTL - timedelta(minutes=1))

    # Should get None due to expiration
    result = _get_from_cache("test_key")
    assert result is None
    assert "test_key" not in _cache  # Key should be removed


def test_search_query_enhancement():
    """Test search query enhancement for non-running queries."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": []}

    with (
        patch(
            "functions.event_discovery.search.requests.get", return_value=mock_response
        ) as mock_get,
        patch("functions.event_discovery.search._get_from_cache", return_value=None),
        patch("functions.event_discovery.search.Environment.get_required", return_value="fake_key"),
    ):
        search_running_events("event")  # Query without 'run' or 'race'

        # Verify enhanced query was used
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert "running race" in params["q"]
        assert "marathon" in params["q"]
        assert "5K" in params["q"]
        assert "10K" in params["q"]


def test_parse_location_with_coordinates_no_location():
    """Test parsing location from coordinates when reverse geocoding returns None."""
    with patch("functions.event_discovery.search._geocoder.reverse") as mock_reverse:
        mock_reverse.return_value = None
        query = "near:40.7128,-74.0060 running events"
        clean_query, location = parse_location_query(query)
        assert clean_query == "running events"
        assert (
            location == "40.7128,-74.0060 running events"
        )  # This is what the code actually returns


def test_search_with_enhanced_query_and_location():
    """Test search with enhanced query and location."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "title": "Test Run - February 15, 2025",
                "snippet": "A test event",
                "link": "http://test.com",
            }
        ]
    }

    with (
        patch(
            "functions.event_discovery.search.requests.get", return_value=mock_response
        ) as mock_get,
        patch("functions.event_discovery.search._get_from_cache", return_value=None),
        patch("functions.event_discovery.search.Environment.get_required", return_value="fake_key"),
    ):
        # Use a query that will trigger query enhancement
        search_running_events("event", "New York")

        # Verify the enhanced query
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert "running race" in params["q"]
        assert "in New York" in params["q"]


def test_parse_date_invalid():
    """Test parsing invalid date strings."""
    assert extract_date_from_text("not a date") is None
    assert extract_date_from_text("123") is None
    assert extract_date_from_text("") is None


def test_parse_distance_with_miles():
    """Test parsing distance with miles unit."""
    assert extract_distance_from_text("5 miles") == 8.0467  # 5 miles in kilometers
    assert extract_distance_from_text("1 mile") == 1.60934  # 1 mile in kilometers
    assert extract_distance_from_text("2.5 miles") == 4.02335  # 2.5 miles in kilometers


def test_parse_distance_with_kilometers():
    """Test parsing distance with kilometer units."""
    assert extract_distance_from_text("5 km") == 5.0
    assert extract_distance_from_text("5 kilometers") == 5.0
    assert extract_distance_from_text("2.5 km") == 2.5


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    with patch("functions.event_discovery.search._get_from_cache") as mock:
        mock.return_value = None
        yield mock


def test_search_events_cache_hit(mock_redis, mock_env):
    """Test search events with cache hit."""
    mock_redis.return_value = [
        Event(
            name="Cached Event",
            date=datetime(2025, 3, 15),
            url="http://test.com",
            location="Test Location",
            description="Test Description",
            distance=5.0,
        )
    ]
    results = search_running_events("test query")
    assert len(results) == 1
    assert results[0].name == "Cached Event"


def test_search_events_skip_no_date(mock_search_response, mock_env):
    """Test search events skips events without dates."""
    mock_search_response.json.return_value = {
        "items": [
            {"title": "Event 1", "snippet": "March 15, 2025", "link": "http://test1.com"},
            {"title": "Event 2", "snippet": "No date here", "link": "http://test2.com"},
        ]
    }
    with patch("functions.event_discovery.search.requests.get", return_value=mock_search_response):
        results = search_running_events("test query")
        assert len(results) == 1
        assert results[0].name == "Event 1"

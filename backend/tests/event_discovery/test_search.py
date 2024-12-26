"""Tests for event discovery search functionality."""

from unittest.mock import Mock, patch

from functions.event_discovery.search import (
    extract_event_details,
    format_search_query,
    search_running_events,
)


def test_format_search_query():
    """Test search query formatting."""
    location = "New York"
    radius = 50
    query = format_search_query(location, radius)
    assert "running events" in query.lower()
    assert "new york" in query.lower()
    assert "50km" in query.lower()


def test_extract_event_details():
    """Test event detail extraction."""
    search_result = {
        "title": "Marathon 2024",
        "link": "http://example.com",
        "snippet": "10K run on January 1st, 2024 at Central Park",
        "pagemap": {
            "metatags": [
                {
                    "og:description": "Annual marathon event",
                    "og:title": "City Marathon 2024",
                }
            ]
        },
    }

    event = extract_event_details(search_result)
    assert event["title"] == "Marathon 2024"
    assert event["url"] == "http://example.com"
    assert event["description"] == "10K run on January 1st, 2024 at Central Park"


def test_extract_event_details_missing_data():
    """Test event detail extraction with missing data."""
    search_result = {
        "title": "Marathon 2024",
        # Missing other fields
    }

    event = extract_event_details(search_result)
    assert event["title"] == "Marathon 2024"
    assert event["url"] == ""
    assert event["description"] == ""


@patch("functions.event_discovery.search.build")
def test_search_running_events(mock_build):
    """Test running event search."""
    # Mock the Google Custom Search API response
    mock_service = Mock()
    mock_build.return_value = mock_service

    mock_search = Mock()
    mock_service.cse.return_value = mock_search

    mock_list = Mock()
    mock_search.list.return_value = mock_list

    mock_execute = Mock(
        return_value={
            "items": [
                {
                    "title": "Test Event",
                    "link": "http://example.com",
                    "snippet": "Test description",
                }
            ]
        }
    )
    mock_list.execute = mock_execute

    events = search_running_events("New York", 50)

    assert len(events) > 0
    assert events[0]["title"] == "Test Event"
    mock_search.list.assert_called_once()


@patch("functions.event_discovery.search.build")
def test_search_running_events_no_results(mock_build):
    """Test search with no results."""
    mock_service = Mock()
    mock_build.return_value = mock_service

    mock_search = Mock()
    mock_service.cse.return_value = mock_search

    mock_list = Mock()
    mock_search.list.return_value = mock_list

    mock_execute = Mock(return_value={})  # Empty response
    mock_list.execute = mock_execute

    events = search_running_events("Remote Location", 50)
    assert len(events) == 0

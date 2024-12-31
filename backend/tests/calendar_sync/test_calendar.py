"""Tests for calendar sync functionality."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from functions.calendar_sync.calendar import add_event_to_calendar, create_events_from_search
from models.event import Event


@pytest.fixture
def mock_calendar_service():
    """Create mock calendar service."""
    with patch("functions.calendar_sync.calendar.build") as mock_build:
        service = MagicMock()
        mock_build.return_value = service
        yield service


@pytest.fixture
def mock_search():
    """Mock search functionality."""
    with patch("functions.calendar_sync.calendar.search_running_events") as mock:
        mock.return_value = [
            Event(
                name="Test Run",
                date=datetime.now(),
                location="Test Location",
                description="Test Description",
            )
        ]
        yield mock


def test_add_event_to_calendar_success(mock_calendar_service):
    """Test successfully adding event to calendar."""
    event = Event(
        name="Test Run",
        date=datetime.now(),
        location="Test Location",
        description="Test Description",
    )
    credentials = MagicMock()

    mock_calendar_service.events().insert().execute.return_value = {
        "id": "test123",
    }

    result = add_event_to_calendar(event, credentials)
    assert result == "test123"


def test_add_event_to_calendar_failure(mock_calendar_service):
    """Test handling calendar API errors."""
    event = Event(
        name="Test Run",
        date=datetime.now(),
        location="Test Location",
    )
    credentials = MagicMock()

    mock_calendar_service.events().insert().execute.side_effect = Exception("API Error")

    result = add_event_to_calendar(event, credentials)
    assert result is None


def test_create_events_from_search_success(mock_calendar_service, mock_search):
    """Test creating events from search results."""
    mock_calendar_service.events().insert().execute.return_value = {
        "id": "test123",
    }

    credentials = MagicMock()
    event_ids = create_events_from_search("New York", credentials)

    assert len(event_ids) == 1
    assert event_ids[0] == "test123"
    mock_search.assert_called_once_with("New York")


def test_create_events_from_search_no_results(mock_calendar_service, mock_search):
    """Test handling no search results."""
    mock_search.return_value = []

    credentials = MagicMock()
    event_ids = create_events_from_search("Remote Location", credentials)

    assert len(event_ids) == 0

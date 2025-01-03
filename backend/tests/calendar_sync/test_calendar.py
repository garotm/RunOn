"""Tests for calendar sync functionality."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from functions.calendar_sync.calendar import (
    add_event_to_calendar,
    get_calendar_service,
    get_upcoming_running_events,
    remove_event_from_calendar,
)
from models.event import Event


@pytest.fixture
def mock_calendar_service():
    """Create mock calendar service."""
    with patch("functions.calendar_sync.calendar.build") as mock_build:
        service = MagicMock()
        mock_build.return_value = service
        yield service


@pytest.fixture
def mock_event():
    """Create mock event."""
    return Event(
        name="Test Run",
        date=datetime.now(),
        location="Test Location",
        description="Test Description",
        url="https://test.com",
        distance=5.0,
    )


def test_get_calendar_service():
    """Test calendar service creation."""
    credentials = MagicMock()
    with patch("functions.calendar_sync.calendar.build") as mock_build:
        get_calendar_service(credentials)
        mock_build.assert_called_once_with("calendar", "v3", credentials=credentials)


def test_add_event_to_calendar_success(mock_calendar_service, mock_event):
    """Test successfully adding event to calendar."""
    credentials = MagicMock()

    mock_calendar_service.events().insert().execute.return_value = {
        "id": "test123",
    }

    result = add_event_to_calendar(mock_event, credentials)
    assert result == "test123"

    # Verify calendar event format
    calendar_event = mock_calendar_service.events().insert.call_args[1]["body"]
    assert calendar_event["summary"] == f"🏃 {mock_event.name}"
    assert calendar_event["location"] == mock_event.location
    assert mock_event.url in calendar_event["description"]
    assert str(mock_event.distance) in calendar_event["description"]


def test_add_event_to_calendar_existing(mock_calendar_service, mock_event):
    """Test handling existing calendar event."""
    credentials = MagicMock()
    mock_event.calendar_event_id = "existing123"

    mock_calendar_service.events().get().execute.return_value = {
        "id": "existing123",
    }

    result = add_event_to_calendar(mock_event, credentials)
    assert result == "existing123"
    mock_calendar_service.events().insert.assert_not_called()


def test_add_event_to_calendar_failure(mock_calendar_service, mock_event):
    """Test handling calendar API errors."""
    credentials = MagicMock()

    mock_calendar_service.events().insert().execute.side_effect = Exception("API Error")

    result = add_event_to_calendar(mock_event, credentials)
    assert result is None


def test_add_event_to_calendar_not_found(mock_calendar_service, mock_event):
    """Test handling 404 error when checking existing event."""
    credentials = MagicMock()
    mock_event.calendar_event_id = "missing123"

    # Mock 404 error when getting event
    from googleapiclient.errors import HttpError

    resp = MagicMock()
    resp.status = 404
    mock_calendar_service.events().get().execute.side_effect = HttpError(resp, b"Not found")

    # Mock successful event creation
    mock_calendar_service.events().insert().execute.return_value = {
        "id": "new123",
    }

    result = add_event_to_calendar(mock_event, credentials)
    assert result == "new123"

    # Verify that insert was called with the correct parameters
    mock_calendar_service.events().insert.assert_called_with(
        calendarId="primary",
        body=mock_event.to_calendar_event(),
    )


def test_add_event_to_calendar_http_error(mock_calendar_service, mock_event):
    """Test handling non-404 HTTP error when checking existing event."""
    credentials = MagicMock()
    mock_event.calendar_event_id = "error123"

    # Mock 500 error when getting event
    from googleapiclient.errors import HttpError

    resp = MagicMock()
    resp.status = 500
    mock_calendar_service.events().get().execute.side_effect = HttpError(resp, b"Server error")

    result = add_event_to_calendar(mock_event, credentials)
    assert result is None  # Function should return None on error


def test_remove_event_from_calendar_success(mock_calendar_service):
    """Test successfully removing event from calendar."""
    credentials = MagicMock()
    event_id = "test123"

    result = remove_event_from_calendar(event_id, credentials)
    assert result is True
    mock_calendar_service.events().delete.assert_called_once_with(
        calendarId="primary", eventId=event_id
    )


def test_remove_event_from_calendar_failure(mock_calendar_service):
    """Test handling calendar API errors during removal."""
    credentials = MagicMock()
    event_id = "test123"

    mock_calendar_service.events().delete().execute.side_effect = Exception("API Error")

    result = remove_event_from_calendar(event_id, credentials)
    assert result is False


def test_get_upcoming_running_events_success(mock_calendar_service):
    """Test successfully retrieving upcoming events."""
    credentials = MagicMock()
    mock_events = [{"id": "test123", "summary": "🏃 Test Run"}]
    mock_calendar_service.events().list().execute.return_value = {"items": mock_events}

    result = get_upcoming_running_events(credentials)
    assert result == mock_events

    # Verify search parameters
    list_args = mock_calendar_service.events().list.call_args[1]
    assert list_args["calendarId"] == "primary"
    assert list_args["maxResults"] == 10
    assert list_args["singleEvents"] is True
    assert list_args["orderBy"] == "startTime"
    assert list_args["q"] == "🏃"


def test_get_upcoming_running_events_failure(mock_calendar_service):
    """Test handling calendar API errors during event retrieval."""
    credentials = MagicMock()
    mock_calendar_service.events().list().execute.side_effect = Exception("API Error")

    result = get_upcoming_running_events(credentials)
    assert result == []

"""Tests for calendar sync functionality."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from google.auth.credentials import Credentials
from googleapiclient.errors import HttpError

from functions.calendar_sync.calendar import (
    add_event_to_calendar,
    create_calendar_event,
    get_upcoming_running_events,
    remove_event_from_calendar,
)
from models.event import Event


@pytest.fixture
def mock_service():
    """Create mock Google Calendar service."""
    service = Mock()
    events = service.events.return_value

    # For insert operations
    insert = events.insert.return_value
    insert.execute.return_value = {"id": "test123"}

    # For delete operations
    delete = events.delete.return_value
    delete.execute.return_value = {}

    # For list operations
    list_events = events.list.return_value
    list_events.execute.return_value = {"items": []}

    # For get operations
    get = events.get.return_value
    get.execute.return_value = {"id": "test123", "summary": "Test Run"}

    return service


@pytest.fixture
def mock_event():
    """Create mock event with test data."""
    return Event(
        name="Test Run",
        date=datetime(2025, 1, 15),  # Use fixed date for predictability
        location="Test Location",
        description="Test Description",
        url="http://test.com",
        distance=5.0,
    )


def test_add_event_success(mock_service, mock_event):
    """Test adding event with mocked service."""
    with patch("functions.calendar_sync.calendar.build", return_value=mock_service):
        result = add_event_to_calendar(mock_event, Mock())
        assert result == "test123"

        # Verify the correct calendar event was created
        mock_service.events.return_value.insert.assert_called_once()
        call_args = mock_service.events.return_value.insert.call_args
        assert call_args[1]["calendarId"] == "primary"
        assert call_args[1]["body"] == create_calendar_event(mock_event)


def test_add_event_error(mock_service, mock_event):
    """Test adding event with mocked error."""
    with patch("functions.calendar_sync.calendar.build", return_value=mock_service):
        mock_service.events.return_value.insert.return_value.execute.side_effect = Exception(
            "API Error"
        )
        result = add_event_to_calendar(mock_event, Mock())
        assert result is None


def test_remove_event_success(mock_service):
    """Test removing event with mocked service."""
    with patch("functions.calendar_sync.calendar.build", return_value=mock_service):
        result = remove_event_from_calendar("test123", Mock())
        assert result is True


def test_get_events_success(mock_service):
    """Test getting events with mocked service."""
    mock_events = [{"id": "test123", "summary": "🏃 Test Run"}]
    mock_service.events().list().execute.return_value = {"items": mock_events}

    with patch("functions.calendar_sync.calendar.build", return_value=mock_service):
        result = get_upcoming_running_events(Mock())
        assert result == mock_events


def test_add_event_existing_event_not_found():
    """Test adding event when existing event is not found."""
    mock_creds = Mock(spec=Credentials)
    mock_service = Mock()
    mock_events = Mock()
    mock_service.events.return_value = mock_events

    # Mock HTTP 404 error when checking existing event
    mock_resp = Mock()
    mock_resp.status = 404
    mock_error = HttpError(mock_resp, b"Not Found")
    mock_events.get.return_value.execute.side_effect = mock_error

    # Mock successful event creation
    mock_events.insert.return_value.execute.return_value = {"id": "new123"}

    event = Event(
        name="Test Run",
        date=datetime(2025, 2, 8, 9, 0),
        location="Test Location",
        description="Test Description",
        url="http://test.com",
        calendar_event_id="test123",
    )

    with patch("functions.calendar_sync.calendar.get_calendar_service", return_value=mock_service):
        result = add_event_to_calendar(event, mock_creds)
        assert result == "new123"


def test_add_event_existing_event_error():
    """Test adding event when checking existing event fails."""
    mock_creds = Mock(spec=Credentials)
    mock_service = Mock()
    mock_events = Mock()
    mock_service.events.return_value = mock_events

    # Mock HTTP error when checking existing event
    mock_resp = Mock()
    mock_resp.status = 500
    mock_error = HttpError(mock_resp, b"Server error")
    mock_events.get.return_value.execute.side_effect = mock_error

    event = Event(
        name="Test Run",
        date=datetime(2025, 2, 8, 9, 0),
        location="Test Location",
        description="Test Description",
        url="http://test.com",
        calendar_event_id="test123",
    )

    with patch("functions.calendar_sync.calendar.get_calendar_service", return_value=mock_service):
        result = add_event_to_calendar(event, mock_creds)
        assert result is None


def test_add_event_no_event_id():
    """Test adding event when no event ID is returned."""
    mock_creds = Mock(spec=Credentials)
    mock_service = Mock()
    mock_events = Mock()
    mock_service.events.return_value = mock_events

    # Mock successful event creation but without ID
    mock_events.insert.return_value.execute.return_value = {}

    event = Event(
        name="Test Run",
        date=datetime(2025, 2, 8, 9, 0),
        location="Test Location",
        description="Test Description",
        url="http://test.com",
    )

    with patch("functions.calendar_sync.calendar.get_calendar_service", return_value=mock_service):
        result = add_event_to_calendar(event, mock_creds)
        assert result is None


def test_remove_event_error():
    """Test removing event with error."""
    mock_creds = Mock(spec=Credentials)
    mock_service = Mock()
    mock_events = Mock()
    mock_service.events.return_value = mock_events

    # Mock error during event deletion
    mock_events.delete.return_value.execute.side_effect = Exception("Delete failed")

    with patch("functions.calendar_sync.calendar.get_calendar_service", return_value=mock_service):
        result = remove_event_from_calendar("test123", mock_creds)
        assert result is False


def test_get_upcoming_events_error():
    """Test getting upcoming events with error."""
    mock_creds = Mock(spec=Credentials)
    mock_service = Mock()
    mock_events = Mock()
    mock_service.events.return_value = mock_events

    # Mock error during event listing
    mock_events.list.return_value.execute.side_effect = Exception("List failed")

    with patch("functions.calendar_sync.calendar.get_calendar_service", return_value=mock_service):
        result = get_upcoming_running_events(mock_creds)
        assert result == []


def test_add_event_existing_event_other_http_error():
    """Test adding event when checking existing event fails with non-404 error."""
    mock_creds = Mock(spec=Credentials)
    mock_service = Mock()
    mock_events = Mock()
    mock_service.events.return_value = mock_events

    # Mock HTTP error when checking existing event
    mock_resp = Mock()
    mock_resp.status = 403  # Forbidden error
    mock_error = HttpError(mock_resp, b"Forbidden")
    mock_events.get.return_value.execute.side_effect = mock_error

    event = Event(
        name="Test Run",
        date=datetime(2025, 2, 8, 9, 0),
        location="Test Location",
        description="Test Description",
        url="http://test.com",
        calendar_event_id="test123",
    )

    with patch("functions.calendar_sync.calendar.get_calendar_service", return_value=mock_service):
        result = add_event_to_calendar(event, mock_creds)
        assert result is None


def test_add_event_existing_event_other_error(mock_credentials):
    """Test adding event when checking existing event returns non-404 error."""
    from googleapiclient.errors import HttpError

    # Create a simple mock response
    mock_resp = Mock()
    mock_resp.status = 403
    mock_resp.reason = "Forbidden"
    mock_error = HttpError(resp=mock_resp, content=b"Forbidden")

    # Mock the calendar service to raise our error
    mock_service = Mock()
    mock_service.events().get().execute.side_effect = mock_error

    with patch("functions.calendar_sync.calendar.build", return_value=mock_service):
        event = Event(
            name="Test Run",
            date=datetime.now(),
            location="Test Location",
            description="Test Description",
            url="http://test.com",
            calendar_event_id="test_id",
        )

        result = add_event_to_calendar(event, mock_credentials)
        assert result is None  # Should return None for non-404 errors


def test_add_event_existing_event_found(mock_credentials):
    """Test adding event when the event already exists in calendar."""
    # Mock the calendar service to return an existing event
    mock_service = Mock()
    mock_service.events().get().execute.return_value = {"id": "existing123"}

    with patch("functions.calendar_sync.calendar.build", return_value=mock_service):
        event = Event(
            name="Test Run",
            date=datetime.now(),
            location="Test Location",
            description="Test Description",
            url="http://test.com",
            calendar_event_id="existing123",
        )

        result = add_event_to_calendar(event, mock_credentials)
        assert result == "existing123"  # Should return the existing event ID

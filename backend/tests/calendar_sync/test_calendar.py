"""Tests for calendar sync functionality."""

from unittest.mock import Mock, patch

from functions.calendar_sync.calendar import (
    add_event_to_calendar,
    get_calendar_service,
    list_synced_events,
    remove_event_from_calendar,
)


def test_get_calendar_service():
    """Test calendar service initialization."""
    mock_creds = Mock()
    with patch("functions.calendar_sync.calendar.build") as mock_build:
        get_calendar_service(mock_creds)
        mock_build.assert_called_once_with("calendar", "v3", credentials=mock_creds)


def test_add_event_to_calendar():
    """Test adding event to calendar."""
    mock_service = Mock()
    event_data = {
        "title": "Test Run",
        "location": {"address": "Test Location"},
        "description": "Test Description",
        "date": "2024-01-01T10:00:00Z",
    }

    add_event_to_calendar(mock_service, event_data)
    mock_service.events().insert.assert_called_once()


def test_remove_event_from_calendar():
    """Test removing event from calendar."""
    mock_service = Mock()
    event_id = "test-123"

    remove_event_from_calendar(mock_service, event_id)
    mock_service.events().delete.assert_called_once_with(calendarId="primary", eventId=event_id)


def test_list_synced_events():
    """Test listing synced events."""
    mock_service = Mock()
    mock_events = Mock()
    mock_list = Mock()
    mock_execute = Mock(return_value={"items": []})

    # Setup mock chain
    mock_service.events.return_value = mock_events
    mock_events.list.return_value = mock_list
    mock_list.execute = mock_execute

    events = list_synced_events(mock_service)
    assert isinstance(events, list)
    mock_events.list.assert_called_once()

"""Tests for calendar sync functionality."""
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from functions.calendar_sync.calendar import add_event_to_calendar
from models.event import Event


@pytest.fixture
def mock_calendar_service():
    """Create mock calendar service."""
    with patch("functions.calendar_sync.calendar.build") as mock_build:
        service = MagicMock()
        mock_build.return_value = service
        yield service


def test_add_event_to_calendar(mock_calendar_service):
    """Test adding event to calendar."""
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

"""Tests for Event model."""
from datetime import datetime

from models.event import Event


def test_event_to_calendar_event():
    """Test conversion of Event to Google Calendar event format."""
    event = Event(
        name="Test Event",
        date=datetime.now(),
        location="Test Location",
        description="Test Description",
    )

    calendar_event = event.to_calendar_event()

    assert calendar_event["summary"] == event.name
    assert calendar_event["location"] == event.location
    assert calendar_event["description"] == event.description
    assert "dateTime" in calendar_event["start"]
    assert "dateTime" in calendar_event["end"]

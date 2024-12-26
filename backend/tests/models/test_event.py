from datetime import datetime

import pytest

from models.event import Event


def test_event_creation():
    """Test creating an event with valid data."""
    event_data = {
        "id": "test-123",
        "title": "Test Marathon",
        "description": "Test event description",
        "date": datetime.utcnow(),
        "location": {"address": "Test Location", "coordinates": {"lat": 40.7829, "lng": -73.9654}},
        "distance": 42.195,
        "event_type": "marathon",
        "organizer_id": "user-123",
    }

    event = Event(**event_data)
    assert event.id == "test-123"
    assert event.title == "Test Marathon"
    assert event.distance == 42.195


def test_event_validation():
    """Test event validation rules."""
    with pytest.raises(ValueError):
        Event(
            id="test-123",
            title="",  # Empty title should fail
            date=datetime.utcnow(),
            location={"address": "Test"},
            event_type="marathon",
            organizer_id="user-123",
        )


def test_event_defaults():
    """Test default values for event fields."""
    event = Event(
        id="test-123",
        title="Test Event",
        date=datetime.utcnow(),
        location={"address": "Test"},
        event_type="marathon",
        organizer_id="user-123",
    )

    assert event.current_participants == 0
    assert event.status == "scheduled"
    assert isinstance(event.tags, list)
    assert event.created_at is not None
    assert event.updated_at is not None

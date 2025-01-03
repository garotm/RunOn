"""Tests for Event model."""

from datetime import datetime, timedelta

from models.event import Event


def test_event_initialization():
    """Test event initialization with all fields."""
    event = Event(
        name="Test Run",
        date=datetime(2024, 3, 15),
        location="Test Location",
        description="Test Description",
        url="https://test.com",
        distance=5.0,
        id="test123",
        calendar_event_id="cal123",
    )

    assert event.name == "Test Run"
    assert event.date == datetime(2024, 3, 15)
    assert event.location == "Test Location"
    assert event.description == "Test Description"
    assert event.url == "https://test.com"
    assert event.distance == 5.0
    assert event.id == "test123"
    assert event.calendar_event_id == "cal123"


def test_event_initialization_minimal():
    """Test event initialization with minimal fields."""
    event = Event(
        name="Test Run",
        date=datetime(2024, 3, 15),
        location="Test Location",
        description="Test Description",
        url="https://test.com",
    )

    assert event.name == "Test Run"
    assert event.date == datetime(2024, 3, 15)
    assert event.location == "Test Location"
    assert event.description == "Test Description"
    assert event.url == "https://test.com"
    assert event.distance == 0.0
    assert event.id is not None  # Auto-generated
    assert event.calendar_event_id is None


def test_to_calendar_event_with_distance():
    """Test calendar event conversion with distance."""
    event = Event(
        name="5K Run",
        date=datetime(2024, 3, 15, 9, 0),  # 9:00 AM
        location="Central Park",
        description="Annual 5K run",
        url="https://test.com",
        distance=5.0,
    )

    calendar_event = event.to_calendar_event()

    assert calendar_event["summary"] == "🏃 5K Run"
    assert calendar_event["location"] == "Central Park"
    assert "Annual 5K run" in calendar_event["description"]
    assert "Distance: 5.0km" in calendar_event["description"]
    assert "https://test.com" in calendar_event["description"]

    # Check duration calculation (5km * 8 min/km = 40 minutes)
    start_time = datetime.fromisoformat(calendar_event["start"]["dateTime"])
    end_time = datetime.fromisoformat(calendar_event["end"]["dateTime"])
    assert end_time - start_time == timedelta(minutes=40)


def test_to_calendar_event_without_distance():
    """Test calendar event conversion without distance."""
    event = Event(
        name="Fun Run",
        date=datetime(2024, 3, 15, 9, 0),
        location="Central Park",
        description="Annual fun run",
        url="https://test.com",
    )

    calendar_event = event.to_calendar_event()

    # Check default duration (120 minutes)
    start_time = datetime.fromisoformat(calendar_event["start"]["dateTime"])
    end_time = datetime.fromisoformat(calendar_event["end"]["dateTime"])
    assert end_time - start_time == timedelta(minutes=120)


def test_to_dict():
    """Test dictionary conversion."""
    event = Event(
        name="Test Run",
        date=datetime(2024, 3, 15),
        location="Test Location",
        description="Test Description",
        url="https://test.com",
        distance=5.0,
        id="test123",
        calendar_event_id="cal123",
    )

    event_dict = event.to_dict()

    assert event_dict["name"] == "Test Run"
    assert event_dict["date"] == "2024-03-15T00:00:00"
    assert event_dict["location"] == "Test Location"
    assert event_dict["description"] == "Test Description"
    assert event_dict["url"] == "https://test.com"
    assert event_dict["distance"] == 5.0
    assert event_dict["id"] == "test123"
    assert event_dict["calendar_event_id"] == "cal123"


def test_from_dict():
    """Test creating event from dictionary."""
    event_dict = {
        "name": "Test Run",
        "date": "2024-03-15T00:00:00",
        "location": "Test Location",
        "description": "Test Description",
        "url": "https://test.com",
        "distance": 5.0,
        "id": "test123",
        "calendar_event_id": "cal123",
    }

    event = Event.from_dict(event_dict)

    assert event.name == "Test Run"
    assert event.date == datetime(2024, 3, 15)
    assert event.location == "Test Location"
    assert event.description == "Test Description"
    assert event.url == "https://test.com"
    assert event.distance == 5.0
    assert event.id == "test123"
    assert event.calendar_event_id == "cal123"

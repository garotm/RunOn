"""Tests for Event model."""

from datetime import datetime

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
    )

    assert event.name == "Test Run"
    assert event.date == datetime(2024, 3, 15)
    assert event.location == "Test Location"
    assert event.description == "Test Description"
    assert event.url == "https://test.com"
    assert event.distance == 5.0
    assert event.id == "test123"


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
    )

    event_dict = event.to_dict()

    assert event_dict["name"] == "Test Run"
    assert event_dict["date"] == "2024-03-15T00:00:00"
    assert event_dict["location"] == "Test Location"
    assert event_dict["description"] == "Test Description"
    assert event_dict["url"] == "https://test.com"
    assert event_dict["distance"] == 5.0
    assert event_dict["id"] == "test123"
    assert event_dict["coordinates"] is None

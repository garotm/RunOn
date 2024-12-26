"""Event discovery using Google Search."""
from datetime import datetime
from typing import List

from models.event import Event


def search_running_events(location: str) -> List[Event]:
    """Search for running events in a given location."""
    # Simplified implementation
    events = []

    # Process results into Event objects
    events.append(
        Event(
            name="Sample Running Event",
            date=datetime.now(),
            location=location,
            description="A running event near you",
            url="https://example.com",
        )
    )

    return events

"""Event model for running events."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    """Running event details."""

    name: str
    date: datetime
    location: str
    description: Optional[str] = None
    url: Optional[str] = None

    def to_calendar_event(self) -> dict:
        """Convert to Google Calendar event format."""
        return {
            "summary": self.name,
            "location": self.location,
            "description": self.description or "",
            "start": {
                "dateTime": self.date.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": self.date.isoformat(),
                "timeZone": "UTC",
            },
        }

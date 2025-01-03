"""Event model."""
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class Event(BaseModel):
    """Running event model."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "5K Fun Run",
                "date": "2024-03-15T09:00:00",
                "location": "Central Park",
                "description": "Annual charity run",
                "url": "https://example.com/event",
                "distance": 5.0,
            }
        }
    )

    id: str = Field(default_factory=lambda: "")
    name: str
    date: datetime
    location: str
    description: str
    url: str
    distance: float = Field(default=0.0)
    calendar_event_id: Optional[str] = None

    def __init__(self, **data):
        """Initialize event with auto-generated ID if not provided."""
        if "id" not in data:
            data["id"] = str(hash(f"{data['name']}{data['date']}{data['location']}"))
        super().__init__(**data)

    def to_calendar_event(self) -> Dict:
        """Convert to Google Calendar event format.

        Returns:
            Dict: Calendar event data
        """
        # Estimate event duration based on distance
        # Rough estimate: 1km = 8 minutes for average runner
        duration_minutes = int(self.distance * 8) if self.distance > 0 else 120

        end_time = self.date + timedelta(minutes=duration_minutes)

        description = (
            f"{self.description}\n\n" f"Distance: {self.distance}km\n" f"Registration: {self.url}"
        )

        return {
            "summary": f"🏃 {self.name}",
            "location": self.location,
            "description": description,
            "start": {
                "dateTime": self.date.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "UTC",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},  # 1 day before
                    {"method": "popup", "minutes": 60},  # 1 hour before
                ],
            },
            "source": {
                "url": self.url,
                "title": "RunOn App",
            },
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Event":
        """Create from dictionary.

        Args:
            data: Event data

        Returns:
            Event: New event instance
        """
        if isinstance(data.get("date"), str):
            data["date"] = datetime.fromisoformat(data["date"])
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.isoformat() if self.date else None,
            "location": self.location,
            "description": self.description,
            "url": self.url,
            "distance": self.distance,
            "calendar_event_id": self.calendar_event_id,
        }

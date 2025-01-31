"""Event model."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class Event(BaseModel):
    """Running event model."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Lockport 10",
                "date": "2025-02-08T09:00:00",
                "location": "Palace Theatre, 2 East Ave, Lockport, NY",
                "description": "Annual 10-mile race",
                "url": "https://example.com/event",
                "distance": 16.1,  # 10 miles in km
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
    coordinates: Optional[Dict[str, float]] = None  # {"latitude": float, "longitude": float}
    calendar_event_id: Optional[str] = None

    def __init__(self, **data):
        """Initialize event with auto-generated ID if not provided."""
        if "id" not in data:
            data["id"] = str(hash(f"{data['name']}{data['date']}{data['location']}"))
        super().__init__(**data)

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
            "coordinates": self.coordinates,
            "calendar_event_id": self.calendar_event_id,
        }

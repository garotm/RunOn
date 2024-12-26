from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Event(BaseModel):
    """Running event model."""

    id: str = Field(..., description="Unique event identifier")
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    date: datetime
    location: Dict[str, Any] = Field(..., description="Event location details")
    distance: Optional[float] = Field(None, description="Event distance in kilometers")
    event_type: str = Field(..., description="Type of running event")
    organizer_id: str = Field(..., description="Event organizer's user ID")
    max_participants: Optional[int] = None
    current_participants: int = Field(default=0)
    status: str = Field(default="scheduled")
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "title": "City Marathon 2024",
                "description": "Annual city marathon event",
                "date": "2024-04-15T08:00:00Z",
                "location": {
                    "address": "Central Park, New York",
                    "coordinates": {"lat": 40.7829, "lng": -73.9654},
                },
                "distance": 42.195,
                "event_type": "marathon",
            }
        }

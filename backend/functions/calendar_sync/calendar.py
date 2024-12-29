"""Calendar sync functionality."""

from typing import Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from models.event import Event


def add_event_to_calendar(
    event: Event,
    credentials: Credentials,
) -> Optional[str]:
    """Add event to user's Google Calendar."""
    service = build(
        "calendar",
        "v3",
        credentials=credentials,
    )

    calendar_event = event.to_calendar_event()

    try:
        result = (
            service.events()
            .insert(
                calendarId="primary",
                body=calendar_event,
            )
            .execute()
        )
        return result.get("id")
    except Exception as e:
        print(f"Error adding event to calendar: {e}")
        return None

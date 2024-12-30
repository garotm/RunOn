"""Calendar sync functionality."""

from typing import List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from functions.event_discovery.search import search_running_events
from models.event import Event


def add_event_to_calendar(
    event: Event,
    credentials: Credentials,
) -> Optional[str]:
    """Add event to user's Google Calendar.

    Args:
        event: Event to add to calendar
        credentials: Google OAuth credentials

    Returns:
        Optional[str]: Event ID if successful, None otherwise
    """
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


def create_events_from_search(
    search_query: str,
    credentials: Credentials,
) -> List[str]:
    """Create calendar events from search results.

    Args:
        search_query: Location or search query
        credentials: Google OAuth credentials

    Returns:
        List[str]: List of created event IDs
    """
    events = search_running_events(search_query)
    event_ids = []

    for event in events:
        event_id = add_event_to_calendar(event, credentials)
        if event_id:
            event_ids.append(event_id)

    return event_ids

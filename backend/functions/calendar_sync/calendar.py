"""Calendar sync functionality."""

from datetime import datetime
from typing import Dict, List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from models.event import Event


def get_calendar_service(credentials: Credentials):
    """Get Google Calendar service.

    Args:
        credentials: Google OAuth credentials

    Returns:
        Calendar service instance
    """
    return build("calendar", "v3", credentials=credentials)


def create_calendar_event(event: Event) -> Dict:
    """Create a Google Calendar event from a RunOn event."""
    return {
        "summary": f"🏃 {event.name}",
        "location": event.location,
        "description": f"{event.description}\n\nDistance: {event.distance}km\n\nMore info: {event.url}",
        "start": {"dateTime": event.date.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": event.date.isoformat(), "timeZone": "UTC"},
    }


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
    try:
        service = get_calendar_service(credentials)
        calendar_event = create_calendar_event(event)

        # Check if event already exists
        if event.calendar_event_id:
            try:
                existing_event = (
                    service.events()
                    .get(calendarId="primary", eventId=event.calendar_event_id)
                    .execute()
                )
                print(f"Event already exists in calendar: {existing_event['id']}")
                return existing_event["id"]
            except HttpError as e:
                if e.resp.status != 404:  # If error is not "Not Found"
                    print(f"Error checking existing event: {str(e)}")
                    return None

        # Create new event
        result = (
            service.events()
            .insert(
                calendarId="primary",
                body=calendar_event,
            )
            .execute()
        )

        event_id = result.get("id")
        if not event_id:
            print("No event ID returned from calendar API")
            return None

        print(f"Created calendar event: {event_id}")
        return event_id

    except Exception as e:
        print(f"Error adding event to calendar: {str(e)}")
        return None


def remove_event_from_calendar(
    event_id: str,
    credentials: Credentials,
) -> bool:
    """Remove event from user's Google Calendar.

    Args:
        event_id: Calendar event ID
        credentials: Google OAuth credentials

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        service = get_calendar_service(credentials)
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print(f"Removed calendar event: {event_id}")
        return True
    except Exception as e:
        print(f"Error removing event from calendar: {str(e)}")
        return False


def get_upcoming_running_events(
    credentials: Credentials, time_min: Optional[datetime] = None, max_results: int = 10
) -> List[Dict]:
    """Get upcoming running events from calendar.

    Args:
        credentials: Google OAuth credentials
        time_min: Minimum time for events (default: now)
        max_results: Maximum number of events to return

    Returns:
        List[Dict]: List of calendar events
    """
    try:
        service = get_calendar_service(credentials)

        if not time_min:
            time_min = datetime.utcnow()

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=time_min.isoformat() + "Z",
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
                q="🏃",  # Search for our running event emoji
            )
            .execute()
        )

        return events_result.get("items", [])
    except Exception as e:
        print(f"Error getting upcoming running events: {str(e)}")
        return []

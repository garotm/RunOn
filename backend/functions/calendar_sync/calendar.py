from datetime import datetime
from typing import Any, Dict, List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_calendar_service(credentials: Credentials):
    """Initialize Google Calendar API client.

    Args:
        credentials: OAuth2 credentials

    Returns:
        googleapiclient.discovery.Resource: Google Calendar API client
    """
    return build("calendar", "v3", credentials=credentials)


def add_event_to_calendar(service, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a running event to Google Calendar.

    Args:
        service: Google Calendar API service
        event_data: Event details

    Returns:
        Dict: Created calendar event
    """
    calendar_event = {
        "summary": event_data["title"],
        "location": event_data["location"]["address"],
        "description": f"Running event: {event_data.get('description', '')}",
        "start": {"dateTime": event_data["date"], "timeZone": "UTC"},
        "end": {
            "dateTime": event_data["date"],  # TODO: Calculate end time based on distance
            "timeZone": "UTC",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 60},
            ],
        },
    }

    return service.events().insert(calendarId="primary", body=calendar_event).execute()


def remove_event_from_calendar(service, event_id: str) -> None:
    """Remove an event from Google Calendar.

    Args:
        service: Google Calendar API service
        event_id: Calendar event ID
    """
    service.events().delete(calendarId="primary", eventId=event_id).execute()


def list_synced_events(service) -> List[Dict[str, Any]]:
    """List all synced running events from Google Calendar.

    Args:
        service: Google Calendar API service

    Returns:
        List[Dict]: List of calendar events
    """
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=datetime.utcnow().isoformat() + "Z",
            maxResults=100,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    return events_result.get("items", [])

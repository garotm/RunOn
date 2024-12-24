"""Event discovery search functionality."""

from typing import Any, Dict, List

from googleapiclient.discovery import build

from config import Environment


def format_search_query(location: str, radius: int) -> str:
    """Format search query for running events."""
    return f"running events near {location} within {radius}km"


def extract_event_details(search_result: Dict[str, Any]) -> Dict[str, str]:
    """Extract relevant event details from search result."""
    return {
        "title": search_result.get("title", ""),
        "url": search_result.get("link", ""),
        "description": search_result.get("snippet", ""),
    }


def search_running_events(location: str, radius: int = 50) -> List[Dict[str, Any]]:
    """Search for running events near a location."""
    service = build(
        "customsearch",
        "v1",
        developerKey=Environment.get_required("GOOGLE_SEARCH_API_KEY"),
    )

    query = format_search_query(location, radius)

    try:
        result = (
            service.cse()
            .list(
                q=query,
                cx=Environment.get_required("GOOGLE_SEARCH_ENGINE_ID"),
                num=10,
            )
            .execute()
        )

        events = []
        if "items" in result:
            for item in result["items"]:
                event = extract_event_details(item)
                events.append(event)

        return events

    except Exception as e:
        # Log error and return empty list
        print(f"Error searching for events: {e}")
        return []

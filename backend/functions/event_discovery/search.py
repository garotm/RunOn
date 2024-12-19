import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_google_search_client():
    """Initialize Google Custom Search API client.

    Returns:
        googleapiclient.discovery.Resource: Google Custom Search API client
    """
    # Get credentials from environment or service account
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/cse"]
    )

    return build("customsearch", "v1", credentials=credentials)


def search_running_events(location: str, radius: int = 50) -> List[Dict[str, Any]]:
    """Search for running events using Google Custom Search API.

    Args:
        location: Location string (e.g., "Seattle, WA")
        radius: Search radius in kilometers

    Returns:
        List[Dict]: List of event objects
    """
    try:
        service = get_google_search_client()

        # Construct search query
        query = f"running race events near {location}"

        # Execute search
        result = (
            service.cse()
            .list(
                q=query,
                cx=os.getenv("GOOGLE_CUSTOM_SEARCH_CX"),
                dateRestrict="m3",  # Last 3 months
                num=10,
            )
            .execute()
        )

        # Parse and format results
        events = []
        for item in result.get("items", []):
            event = {
                "id": item["link"],
                "title": item["title"],
                "description": item.get("snippet", ""),
                "url": item["link"],
                "location": {
                    "address": location,
                    "coordinates": extract_coordinates(item),
                },
                "date": extract_date(item),
                "type": "running",
                "distance": extract_distance(item),
            }
            events.append(event)

        return events

    except Exception as e:
        raise Exception(f"Failed to search events: {str(e)}")


def extract_coordinates(item: Dict) -> Dict[str, float]:
    """Extract coordinates from search result if available."""
    # TODO: Implement coordinate extraction
    return {"lat": 0, "lng": 0}


def extract_date(item: Dict) -> str:
    """Extract event date from search result."""
    # TODO: Implement date extraction using NLP
    return (datetime.now() + timedelta(days=30)).isoformat()


def extract_distance(item: Dict) -> str:
    """Extract race distance from search result."""
    # TODO: Implement distance extraction using regex
    return "5K"

"""Event discovery using Google Search."""

from datetime import datetime
from typing import List

import requests

from config.environment import Environment
from models.event import Event


def search_running_events(location: str) -> List[Event]:
    """Search for running events in a given location using Google Custom Search.

    Args:
        location: Location to search for events

    Returns:
        List[Event]: List of running events found
    """
    api_key = Environment.get_required("RUNON_API_KEY")
    search_engine_id = Environment.get_required("RUNON_SEARCH_ENGINE_ID")

    base_url = "https://www.googleapis.com/customsearch/v1"
    query = f"running events races {location}"

    params = {"key": api_key, "cx": search_engine_id, "q": query, "num": 10}  # Number of results

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        search_results = response.json()

        events = []
        for item in search_results.get("items", []):
            event = Event(
                name=item.get("title", "Unknown Event"),
                date=datetime.now(),  # Default to now, would parse from result in production
                location=location,
                description=item.get("snippet", ""),
                url=item.get("link", ""),
            )
            events.append(event)

        return events
    except Exception as e:
        print(f"Search error: {str(e)}")
        return []

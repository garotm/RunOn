"""Event discovery using Google Search."""

from datetime import datetime
from typing import List

import requests

from config.environment import Environment
from models.event import Event


def search_running_events(query: str) -> List[Event]:
    """Search for running events using Google Custom Search.

    Args:
        query: Search query for running events

    Returns:
        List[Event]: List of running events found
    """
    api_key = Environment.get_required("RUNON_API_KEY")
    search_engine_id = Environment.get_required("RUNON_SEARCH_ENGINE_ID")

    print(f"Using API Key: {api_key[:10]}... (truncated)")
    print(f"Using Search Engine ID: {search_engine_id}")

    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": search_engine_id, "q": query, "num": 10}

    try:
        print(f"Making request to Google Custom Search API with query: {query}")
        response = requests.get(base_url, params=params)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error response body: {response.text}")
        
        response.raise_for_status()
        search_results = response.json()

        events = []
        for item in search_results.get("items", []):
            event = Event(
                name=item.get("title", "Unknown Event"),
                date=datetime.now(),  # Default to now, would parse from result in production
                location=query,  # Using query as location for now
                description=item.get("snippet", ""),
                url=item.get("link", ""),
            )
            events.append(event)

        return events
    except requests.exceptions.HTTPError as e:
        print(f"Search error: {str(e)}")
        if e.response.status_code == 403:
            print("API key or search engine ID may be invalid or quota exceeded")
            print(f"Full error response: {e.response.text}")
        return []
    except Exception as e:
        print(f"Unexpected error during search: {str(e)}")
        return []

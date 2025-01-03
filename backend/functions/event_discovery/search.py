"""Event discovery using Google Search."""

import re
from datetime import datetime
from typing import List, Optional

import requests
from dateutil import parser as date_parser

from config.environment import Environment
from models.event import Event


def extract_date_from_text(text: str) -> Optional[datetime]:
    """Extract date from text using various patterns.

    Args:
        text: Text containing potential date information

    Returns:
        Optional[datetime]: Parsed date if found, None otherwise
    """
    # Common date patterns in running event descriptions
    date_patterns = [
        # Month DD, YYYY
        r"\b(?:January|February|March|April|May|June|July|August|September|"
        r"October|November|December)\s+\d{1,2},?\s+\d{4}\b",
        # DD Month YYYY
        r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|"
        r"September|October|November|December)\s+\d{4}\b",
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",  # MM/DD/YYYY
        r"\b\d{4}-\d{2}-\d{2}\b",  # YYYY-MM-DD
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return date_parser.parse(match.group())
            except (ValueError, TypeError):
                continue

    return None


def extract_distance_from_text(text: str) -> Optional[float]:
    """Extract race distance from text.

    Args:
        text: Text containing potential distance information

    Returns:
        Optional[float]: Distance in kilometers if found, None otherwise
    """
    # Common race distance patterns (5K, 10K, half marathon, marathon)
    distance_patterns = {
        r"\b5k\b": 5.0,
        r"\b10k\b": 10.0,
        r"\bhalf\s*marathon\b": 21.1,
        r"\bmarathon\b": 42.2,
    }

    text = text.lower()
    for pattern, distance in distance_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return distance

    return None


def search_running_events(query: str, location: Optional[str] = None) -> List[Event]:
    """Search for running events using Google Custom Search.

    Args:
        query: Search query for running events
        location: Optional location to filter events

    Returns:
        List[Event]: List of running events found
    """
    api_key = Environment.get_required("RUNON_API_KEY")
    search_engine_id = Environment.get_required("RUNON_SEARCH_ENGINE_ID")

    # Enhance query with running event specific terms
    search_terms = [query, "running race", "marathon", "5K", "10K", "registration"]
    if location:
        search_terms.append(location)

    enhanced_query = " ".join(search_terms)

    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": enhanced_query,
        "num": 10,
        "sort": "date",  # Prioritize recent content
    }

    try:
        print(f"Making request to Google Custom Search API with query: {enhanced_query}")
        response = requests.get(base_url, params=params)
        print(f"Response status code: {response.status_code}")

        if response.status_code != 200:
            print(f"Error response body: {response.text}")
            return []

        search_results = response.json()

        events = []
        for item in search_results.get("items", []):
            # Combine title and snippet for better date/distance extraction
            full_text = f"{item.get('title', '')} {item.get('snippet', '')}"

            # Extract date from text or fall back to current date
            event_date = extract_date_from_text(full_text) or datetime.now()

            # Extract distance or default to 0
            distance = extract_distance_from_text(full_text) or 0.0

            event = Event(
                name=item.get("title", "Unknown Event"),
                date=event_date,
                location=location or query,
                description=item.get("snippet", ""),
                url=item.get("link", ""),
                distance=distance,
            )
            events.append(event)

        return events
    except requests.exceptions.RequestException as e:
        print(f"Search error: {str(e)}")
        return []

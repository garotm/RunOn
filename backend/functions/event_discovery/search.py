"""Event discovery using Google Search."""

import hashlib
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import requests
from dateutil import parser as date_parser
from geopy.geocoders import Nominatim

from config.environment import Environment
from models.event import Event

# Simple in-memory cache
_cache: Dict[str, tuple[List[Event], datetime]] = {}
CACHE_TTL = timedelta(hours=1)  # Reduced cache time for more frequent updates

# Initialize geocoder
_geocoder = Nominatim(user_agent="RunOn")


def _get_cache_key(query: str, location: Optional[str] = None) -> str:
    """Generate cache key from search parameters."""
    key = f"{query}:{location if location else ''}"
    return hashlib.md5(key.encode()).hexdigest()


def _get_from_cache(cache_key: str) -> Optional[List[Event]]:
    """Get results from cache if available and not expired."""
    if cache_key in _cache:
        results, timestamp = _cache[cache_key]
        if datetime.now() - timestamp < CACHE_TTL:
            print(f"Cache hit for key: {cache_key}")
            return results
        else:
            print(f"Cache expired for key: {cache_key}")
            del _cache[cache_key]
    return None


def _save_to_cache(cache_key: str, results: List[Event]):
    """Save results to cache."""
    _cache[cache_key] = (results, datetime.now())
    print(f"Saved to cache: {cache_key}")


def _geocode_location(location: str) -> Optional[Dict[str, float]]:
    """Get coordinates for a location string."""
    try:
        location_data = _geocoder.geocode(location)
        if location_data:
            return {
                "latitude": location_data.latitude,
                "longitude": location_data.longitude,
            }
    except Exception as e:
        print(f"Geocoding error for {location}: {str(e)}")
    return None


def extract_date_from_text(text: str) -> Optional[datetime]:
    """Extract date from text using various patterns."""
    # Common date patterns in running event descriptions
    date_patterns = [
        # Feb 8, 2025 9:00 AM
        (
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
            r"\s+\d{1,2},?\s+\d{4}\s+\d{1,2}(?::\d{2})?\s*(?:AM|PM)\b"
        ),
        # February 8, 2025
        (
            r"\b(?:January|February|March|April|May|June|July|August|"
            r"September|October|November|December)\s+\d{1,2},?\s+\d{4}\b"
        ),
        # 2025-02-08
        r"\b\d{4}-\d{2}-\d{2}\b",
        # 08/02/2025
        r"\b\d{2}/\d{2}/\d{4}\b",
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
    """Extract race distance from text."""
    # Common race distance patterns with metric conversions
    distance_patterns = {
        r"\b5k\b": 5.0,
        r"\b10k\b": 10.0,
        r"\bhalf\s*marathon\b": 21.1,
        r"\bmarathon\b": 42.2,
        r"\b10\s*mile\b": 16.1,
        r"\b5\s*mile\b": 8.05,
        r"\b15k\b": 15.0,
        r"\b30k\b": 30.0,
    }

    text = text.lower()
    for pattern, distance in distance_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return distance

    # Try to find numeric distances
    distance_match = re.search(r"(\d+(?:\.\d+)?)\s*(km|kilometers|miles?)", text, re.IGNORECASE)
    if distance_match:
        value = float(distance_match.group(1))
        unit = distance_match.group(2).lower()
        if "mile" in unit:
            return value * 1.60934  # Convert miles to kilometers
        return value

    return None


def parse_location_query(query: str) -> Tuple[str, Optional[str]]:
    """Parse location from query string."""
    # Check for "near:" prefix with coordinates
    location_match = re.match(r"near:([\d\.-]+),([\d\.-]+)", query)
    if location_match:
        lat, lon = map(float, location_match.groups())
        try:
            location = _geocoder.reverse((lat, lon))
            if location:
                # Remove the location part from query
                clean_query = re.sub(r"near:[\d\.-]+,[\d\.-]+", "", query).strip()
                return clean_query, location.address
        except Exception as e:
            print(f"Reverse geocoding error: {str(e)}")
            return query, None

    # Check for "near:" prefix with location name
    location_match = re.match(r"near:(.+)", query)
    if location_match:
        location = location_match.group(1).strip()
        clean_query = re.sub(r"near:.+", "", query).strip()
        return clean_query or "running events", location

    return query, None


def search_running_events(query: str, location: Optional[str] = None) -> List[Event]:
    """Search for running events using Google Custom Search."""
    # Parse location from query if present
    clean_query, parsed_location = parse_location_query(query)
    location = location or parsed_location

    # Check cache first
    cache_key = _get_cache_key(clean_query, location)
    cached_results = _get_from_cache(cache_key)
    if cached_results is not None:
        return cached_results

    api_key = Environment.get_required("RUNON_API_KEY")
    search_engine_id = Environment.get_required("RUNON_SEARCH_ENGINE_ID")

    # Enhance query with running event specific terms
    search_terms = [clean_query]
    if "run" not in clean_query.lower() and "race" not in clean_query.lower():
        search_terms.extend(["running race", "marathon", "5K", "10K"])
    if location:
        search_terms.append(f"in {location}")

    enhanced_query = " ".join(search_terms)

    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": enhanced_query,
        "num": 10,
        "sort": "date",
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
            # Extract event details
            event_date = extract_date_from_text(
                item.get("title", "") + " " + item.get("snippet", "")
            )
            if not event_date:
                continue  # Skip events without a clear date

            distance = (
                extract_distance_from_text(item.get("title", "") + " " + item.get("snippet", ""))
                or 0.0
            )

            # Get coordinates for location
            coordinates = None
            if location:
                coordinates = _geocode_location(location)

            event = Event(
                name=item.get("title", ""),  # Use the full title
                date=event_date,
                location=location or "Location TBD",
                description=item.get("snippet", ""),
                url=item.get("link", ""),
                distance=distance,
                coordinates=coordinates,
            )
            events.append(event)

        # Cache successful results
        _save_to_cache(cache_key, events)
        return events

    except requests.exceptions.RequestException as e:
        print(f"Search error: {str(e)}")
        return []

from datetime import datetime, timedelta
from typing import Any, Dict, List


def search_running_events(location: str, radius: int = 50) -> List[Dict[str, Any]]:
    """Search for running events using Google Search API.

    Args:
        location: Location string (e.g., "Seattle, WA")
        radius: Search radius in kilometers

    Returns:
        List[Dict]: List of event objects
    """
    # TODO: Implement actual Google Search API call
    # This is a placeholder for now
    return [
        {
            "id": "sample-event-1",
            "title": "Sample Running Event",
            "date": (datetime.now() + timedelta(days=30)).isoformat(),
            "location": {
                "address": f"Sample Location near {location}",
                "coordinates": {"lat": 0, "lng": 0},
            },
            "type": "running",
            "distance": "5K",
            "url": "https://example.com/event",
        }
    ]

from typing import Any, Dict, Tuple

import functions_framework
from flask import jsonify

from .search import search_running_events


@functions_framework.http
def discover_events(request) -> Tuple[Dict[str, Any], int]:
    """HTTP Cloud Function for discovering running events.

    Args:
        request (flask.Request): The request object

    Returns:
        Tuple[dict, int]: The response object and status code
    """
    # Parse request parameters
    request_json = request.get_json(silent=True)
    request_args = request.args

    location = (
        request_json.get("location") if request_json else request_args.get("location")
    )
    radius = (
        request_json.get("radius", 50)
        if request_json
        else request_args.get("radius", 50)
    )

    if not location:
        return jsonify({"error": "location parameter is required", "status": 400}), 400

    try:
        events = search_running_events(location, radius)
        return (
            jsonify(
                {"events": events, "metadata": {"location": location, "radius": radius}}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e), "status": 500}), 500

import os
from typing import Any, Dict, Tuple

import functions_framework
from flask import jsonify
from google.auth.transport import requests
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials

from .calendar import (add_event_to_calendar, get_calendar_service,
                       list_synced_events, remove_event_from_calendar)


@functions_framework.http
def sync_calendar(request) -> Tuple[Dict[str, Any], int]:
    """HTTP Cloud Function for syncing running events with Google Calendar.

    Args:
        request (flask.Request): The request object

    Returns:
        Tuple[dict, int]: The response object and status code
    """
    # Verify authentication
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return (
            jsonify(
                {"error": "Missing or invalid authorization header", "status": 401}
            ),
            401,
        )

    try:
        # Verify the ID token
        token = auth_header.split("Bearer ")[1]
        try:
            user_info = id_token.verify_oauth2_token(
                token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
            )
            if not user_info.get("sub"):
                return jsonify({"error": "Invalid user token", "status": 401}), 401
        except ValueError as e:
            return jsonify({"error": str(e), "status": 401}), 401

        # Get request parameters
        request_json = request.get_json(silent=True)
        if not request_json:
            return jsonify({"error": "No JSON data provided", "status": 400}), 400

        action = request_json.get("action")
        event_data = request_json.get(
            "event", {}
        )  # Make event optional for 'list' action

        if not action:
            return (
                jsonify({"error": "Missing required action parameter", "status": 400}),
                400,
            )

        if action not in ["add", "remove", "list"]:
            return jsonify({"error": f"Invalid action: {action}", "status": 400}), 400

        if action in ["add", "remove"] and not event_data:
            return jsonify({"error": "Missing required event data", "status": 400}), 400

        # Create credentials from the token
        credentials = Credentials(
            token=token, scopes=["https://www.googleapis.com/auth/calendar"]
        )

        # Get calendar service
        service = get_calendar_service(credentials)

        # Process the request based on action
        if action == "add":
            result = add_event_to_calendar(service, event_data)
            return jsonify({"status": "success", "event": result}), 200

        elif action == "remove":
            result = remove_event_from_calendar(service, event_data["id"])
            return jsonify({"status": "success", "message": "Event removed"}), 200

        elif action == "list":
            events = list_synced_events(service)
            return jsonify({"status": "success", "events": events}), 200

        else:
            return jsonify({"error": f"Invalid action: {action}", "status": 400}), 400

    except Exception as e:
        return jsonify({"error": str(e), "status": 500}), 500

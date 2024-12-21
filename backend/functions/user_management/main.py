from typing import Any, Dict, Tuple

import functions_framework
from flask import Request, jsonify

from .auth import (
    create_session_token,
    verify_apple_token,
    verify_google_token,
    verify_session_token,
)
from .models import create_user_profile, get_user_profile, update_user_profile


@functions_framework.http
def manage_user(request: Request) -> Tuple[Dict[str, Any], int]:
    """HTTP Cloud Function for user management operations.

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
        # Get the operation from the path
        path = request.path
        method = request.method

        # Handle authentication
        if path.endswith("/auth/login"):
            return handle_login(request)

        # For all other operations, verify the session token
        token = auth_header.split("Bearer ")[1]
        user_info = verify_session_token(token)

        if not user_info:
            return jsonify({"error": "Invalid token", "status": 401}), 401

        # Handle user operations
        if path.endswith("/user/profile"):
            if method == "GET":
                return get_profile(user_info["sub"])
            elif method == "PUT":
                return update_profile(user_info["sub"], request)

        return jsonify({"error": "Invalid endpoint", "status": 404}), 404

    except Exception as e:
        return jsonify({"error": str(e), "status": 500}), 500


def handle_login(request: Request) -> Tuple[Dict[str, Any], int]:
    """Handle user login with various providers."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No credentials provided", "status": 400}), 400

        provider = data.get("provider", "").lower()
        token = data.get("token")

        if not provider or not token:
            return jsonify({"error": "Missing provider or token", "status": 400}), 400

        # Verify token based on provider
        if provider == "google":
            user_info = verify_google_token(token)
        elif provider == "apple":
            user_info = verify_apple_token(token)
        else:
            return (
                jsonify({"error": f"Unsupported provider: {provider}", "status": 400}),
                400,
            )

        # Get or create user profile
        user_id = user_info["sub"]
        user = get_user_profile(user_id)

        if not user:
            user = create_user_profile(
                user_id=user_id,
                email=user_info.get("email"),
                name=user_info.get("name"),
                provider=provider,
            )

        # Generate session token
        session_token = create_session_token(user)

        return (
            jsonify(
                {"status": "success", "token": session_token, "user": user.to_dict()}
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e), "status": 401}), 401


def get_profile(user_id: str) -> Tuple[Dict[str, Any], int]:
    """Get user profile."""
    try:
        user = get_user_profile(user_id)
        if not user:
            return jsonify({"error": "User not found", "status": 404}), 404

        return jsonify({"status": "success", "profile": user.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": str(e), "status": 500}), 500


def update_profile(user_id: str, request: Request) -> Tuple[Dict[str, Any], int]:
    """Update user profile."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No update data provided", "status": 400}), 400

        user = update_user_profile(user_id, data)
        return jsonify({"status": "success", "profile": user.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": str(e), "status": 500}), 500

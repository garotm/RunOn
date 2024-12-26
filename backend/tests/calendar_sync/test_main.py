from unittest.mock import Mock, patch

import pytest
from flask import Flask

from functions.calendar_sync.main import sync_calendar


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    return app


def test_sync_calendar_unreachable_action(app):
    """Test unreachable action case."""

    def get_json(silent=None):
        # Use an action that's not in ["add", "remove", "list"]
        return {"action": "update"}

    request = Mock(
        headers={"Authorization": "Bearer valid-token"}, get_json=get_json, path="/calendar/sync"
    )

    with app.test_request_context():
        with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.return_value = {"sub": "user123"}
            response, status_code = sync_calendar(request)
            assert status_code == 400
            assert "Invalid action: update" in response.get_json()["error"]


def test_sync_calendar_remove_missing_event_data(app):
    """Test remove action with missing event data."""

    def get_json(silent=None):
        return {"action": "remove"}  # Missing event data

    request = Mock(
        headers={"Authorization": "Bearer valid-token"}, get_json=get_json, path="/calendar/sync"
    )

    with app.test_request_context():
        with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.return_value = {"sub": "user123"}
            response, status_code = sync_calendar(request)
            assert status_code == 400
            assert "Missing required event data" in response.get_json()["error"]

from unittest.mock import Mock, patch

import pytest
from flask import Flask

from functions.calendar_sync.main import sync_calendar


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    return app


@pytest.fixture
def mock_credentials():
    """Mock Google OAuth2 credentials."""
    return Mock()


@pytest.fixture
def mock_calendar_service():
    """Mock Google Calendar service."""
    return Mock()


def test_sync_calendar_missing_auth(app):
    """Test sync_calendar with missing authorization header."""
    with app.app_context():
        request = Mock()
        request.headers = {}

        response, status_code = sync_calendar(request)
        assert status_code == 401
        assert "error" in response.get_json()


def test_sync_calendar_invalid_token(app):
    """Test sync_calendar with invalid token."""
    with app.app_context():
        request = Mock()
        request.headers = {"Authorization": "Bearer invalid_token"}

        with patch("functions.calendar_sync.main.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.side_effect = ValueError("Invalid token")

            response, status_code = sync_calendar(request)
            assert status_code == 401
            assert "error" in response.get_json()


def test_sync_calendar_add_event(app, mock_credentials, mock_calendar_service):
    """Test adding an event to calendar."""
    with app.app_context():
        request = Mock()
        request.headers = {"Authorization": "Bearer valid_token"}
        request.get_json.return_value = {
            "action": "add",
            "event": {
                "title": "Test Run",
                "date": "2024-03-15T10:00:00Z",
                "location": {"address": "Test Location"},
            },
        }

        # Mock the verification and service creation
        with patch("functions.calendar_sync.main.id_token.verify_oauth2_token") as mock_verify:
            with patch("functions.calendar_sync.main.get_calendar_service") as mock_get_service:
                mock_verify.return_value = {"sub": "user123"}
                mock_get_service.return_value = mock_calendar_service

                # Mock the calendar operation
                mock_calendar_service.events().insert().execute.return_value = {
                    "id": "event123",
                    "status": "confirmed",
                }

                response, status_code = sync_calendar(request)
                assert status_code == 200
                data = response.get_json()
                assert data["status"] == "success"
                assert "event" in data


def test_sync_calendar_remove_event(app, mock_credentials, mock_calendar_service):
    """Test removing an event from calendar."""
    with app.app_context():
        request = Mock()
        request.headers = {"Authorization": "Bearer valid_token"}
        request.get_json.return_value = {"action": "remove", "event": {"id": "event123"}}

        with patch("functions.calendar_sync.main.id_token.verify_oauth2_token") as mock_verify:
            with patch("functions.calendar_sync.main.get_calendar_service") as mock_get_service:
                mock_verify.return_value = {"sub": "user123"}
                mock_get_service.return_value = mock_calendar_service

                response, status_code = sync_calendar(request)
                assert status_code == 200
                data = response.get_json()
                assert data["status"] == "success"
                assert data["message"] == "Event removed"


def test_sync_calendar_list_events(app, mock_credentials, mock_calendar_service):
    """Test listing calendar events."""
    with app.app_context():
        request = Mock()
        request.headers = {"Authorization": "Bearer valid_token"}
        request.get_json.return_value = {"action": "list"}

        with patch("functions.calendar_sync.main.id_token.verify_oauth2_token") as mock_verify:
            with patch("functions.calendar_sync.main.get_calendar_service") as mock_get_service:
                mock_verify.return_value = {"sub": "user123"}
                mock_get_service.return_value = mock_calendar_service

                mock_calendar_service.events().list().execute.return_value = {
                    "items": [{"id": "event123"}]
                }

                response, status_code = sync_calendar(request)
                assert status_code == 200
                data = response.get_json()
                assert data["status"] == "success"
                assert "events" in data


def test_sync_calendar_invalid_action(app, mock_credentials):
    """Test sync_calendar with invalid action."""
    with app.app_context():
        request = Mock()
        request.headers = {"Authorization": "Bearer valid_token"}
        request.get_json.return_value = {"action": "invalid"}

        with patch("functions.calendar_sync.main.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.return_value = {"sub": "user123"}

            response, status_code = sync_calendar(request)
            assert status_code == 400
            assert "error" in response.get_json()


def test_sync_calendar_missing_json(app):
    """Test handling of missing JSON data."""
    with app.app_context():
        request = Mock()
        request.headers = {"Authorization": "Bearer valid_token"}
        request.get_json.return_value = None

        with patch("functions.calendar_sync.main.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.return_value = {"sub": "user123"}

            response, status_code = sync_calendar(request)
            assert status_code == 400
            assert response.get_json()["error"] == "No JSON data provided"


def test_sync_calendar_missing_action(app):
    """Test handling of missing action parameter."""
    with app.app_context():
        request = Mock()
        request.headers = {"Authorization": "Bearer valid_token"}
        request.get_json.return_value = {"event": {}}

        with patch("functions.calendar_sync.main.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.return_value = {"sub": "user123"}

            response, status_code = sync_calendar(request)
            assert status_code == 400
            assert response.get_json()["error"] == "Missing required action parameter"


def test_sync_calendar_missing_event_data(app):
    """Test handling of missing event data for add/remove actions."""
    with app.app_context():
        request = Mock()
        request.headers = {"Authorization": "Bearer valid_token"}
        request.get_json.return_value = {"action": "add"}

        with patch("functions.calendar_sync.main.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.return_value = {"sub": "user123"}

            response, status_code = sync_calendar(request)
            assert status_code == 400
            assert response.get_json()["error"] == "Missing required event data"


def test_sync_calendar_invalid_user_token(app):
    """Test handling of invalid user token (missing sub claim)."""
    with app.app_context():
        request = Mock()
        request.headers = {"Authorization": "Bearer valid_token"}

        with patch("functions.calendar_sync.main.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.return_value = {}  # Empty token info (no 'sub' claim)

            response, status_code = sync_calendar(request)
            assert status_code == 401
            assert response.get_json()["error"] == "Invalid user token"


def test_sync_calendar_credentials_error(app):
    """Test handling of credentials creation error."""
    with app.app_context():
        request = Mock()
        request.headers = {"Authorization": "Bearer valid_token"}
        request.get_json.return_value = {"action": "list"}

        with patch("functions.calendar_sync.main.id_token.verify_oauth2_token") as mock_verify:
            with patch("functions.calendar_sync.main.Credentials") as mock_creds:
                mock_verify.return_value = {"sub": "user123"}
                mock_creds.side_effect = Exception("Failed to create credentials")

                response, status_code = sync_calendar(request)
                assert status_code == 500
                assert "Failed to create credentials" in response.get_json()["error"]

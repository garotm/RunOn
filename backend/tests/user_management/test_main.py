from unittest.mock import Mock, patch

import pytest
from flask import Flask

from functions.user_management.main import get_profile, handle_login, manage_user, update_profile


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    return app


@pytest.fixture
def mock_user():
    """Create a mock user object."""
    return Mock(
        id="user123",
        email="test@example.com",
        name="Test User",
        to_dict=lambda: {"id": "user123", "email": "test@example.com", "name": "Test User"},
    )


def test_manage_user_missing_auth(app):
    """Test manage_user with missing authorization header."""
    with app.test_request_context():
        request = Mock(headers={})
        response, status_code = manage_user(request)

        assert status_code == 401
        assert "Missing or invalid authorization header" in response.get_json()["error"]


def test_manage_user_login_success(app, mock_user):
    """Test successful user login."""
    with app.test_request_context(path="/auth/login"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"},
            path="/auth/login",
            get_json=lambda: {"provider": "google", "token": "google-token"},
        )

        mock_user_info = {"sub": "user123", "email": "test@example.com", "name": "Test User"}

        with patch("functions.user_management.main.verify_google_token") as mock_verify:
            with patch("functions.user_management.main.get_user_profile") as mock_get_user:
                with patch(
                    "functions.user_management.main.create_session_token"
                ) as mock_create_token:
                    mock_verify.return_value = mock_user_info
                    mock_get_user.return_value = mock_user
                    mock_create_token.return_value = "session-token"

                    response, status_code = manage_user(request)

                    assert status_code == 200
                    data = response.get_json()
                    assert data["status"] == "success"
                    assert data["token"] == "session-token"
                    assert "user" in data


def test_manage_user_get_profile(app, mock_user):
    """Test getting user profile."""
    with app.test_request_context(path="/user/profile"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"}, path="/user/profile", method="GET"
        )

        with patch("functions.user_management.main.verify_session_token") as mock_verify:
            with patch("functions.user_management.main.get_user_profile") as mock_get_user:
                mock_verify.return_value = {"sub": "user123"}
                mock_get_user.return_value = mock_user

                response, status_code = manage_user(request)

                assert status_code == 200
                data = response.get_json()
                assert data["status"] == "success"
                assert data["profile"]["id"] == "user123"


def test_manage_user_update_profile(app, mock_user):
    """Test updating user profile."""
    with app.test_request_context(path="/user/profile", method="PUT"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"},
            path="/user/profile",
            method="PUT",
            get_json=lambda: {"name": "Updated Name"},
        )

        with patch("functions.user_management.main.verify_session_token") as mock_verify:
            with patch("functions.user_management.main.update_user_profile") as mock_update:
                mock_verify.return_value = {"sub": "user123"}
                mock_update.return_value = mock_user

                response, status_code = manage_user(request)

                assert status_code == 200
                data = response.get_json()
                assert data["status"] == "success"
                assert "profile" in data


def test_manage_user_invalid_endpoint(app):
    """Test invalid endpoint."""
    with app.test_request_context(path="/invalid"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"}, path="/invalid", method="GET"
        )

        with patch("functions.user_management.main.verify_session_token") as mock_verify:
            mock_verify.return_value = {"sub": "user123"}

            response, status_code = manage_user(request)

            assert status_code == 404
            assert "Invalid endpoint" in response.get_json()["error"]


def test_manage_user_invalid_json(app):
    """Test manage_user with invalid JSON."""
    with app.test_request_context(path="/auth/login"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"},
            path="/auth/login",
            get_json=lambda: None,
        )

        response, status_code = manage_user(request)
        assert status_code == 400
        assert "No credentials provided" in response.get_json()["error"]


def test_manage_user_missing_token(app):
    """Test manage_user with missing token."""
    with app.test_request_context(path="/auth/login"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"},
            path="/auth/login",
            get_json=lambda: {"provider": "google"},
        )

        response, status_code = manage_user(request)
        assert status_code == 400
        assert "Missing provider or token" in response.get_json()["error"]


def test_manage_user_unsupported_provider(app):
    """Test manage_user with unsupported provider."""
    with app.test_request_context(path="/auth/login"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"},
            path="/auth/login",
            get_json=lambda: {"provider": "unsupported", "token": "token"},
        )

        response, status_code = manage_user(request)
        assert status_code == 400
        assert "Unsupported provider" in response.get_json()["error"]


def test_manage_user_profile_not_found(app):
    """Test getting non-existent profile."""
    with app.test_request_context(path="/user/profile"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"}, path="/user/profile", method="GET"
        )

        with patch("functions.user_management.main.verify_session_token") as mock_verify:
            with patch("functions.user_management.main.get_user_profile") as mock_get_user:
                mock_verify.return_value = {"sub": "user123"}
                mock_get_user.return_value = None

                response, status_code = manage_user(request)
                assert status_code == 404
                assert "User not found" in response.get_json()["error"]


def test_manage_user_update_profile_no_data(app):
    """Test updating profile with no data."""
    with app.test_request_context(path="/user/profile", method="PUT"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"},
            path="/user/profile",
            method="PUT",
            get_json=lambda: None,
        )

        with patch("functions.user_management.main.verify_session_token") as mock_verify:
            mock_verify.return_value = {"sub": "user123"}

            response, status_code = manage_user(request)
            assert status_code == 400
            assert "No update data provided" in response.get_json()["error"]


def test_handle_login_no_json(app):
    """Test login with no JSON data."""
    with app.test_request_context(path="/auth/login"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"},
            path="/auth/login",
            get_json=lambda: None,  # This covers line 49
        )

        response, status_code = handle_login(request)
        assert status_code == 400
        assert "No credentials provided" in response.get_json()["error"]


def test_handle_login_user_not_found(app):
    """Test login when user profile doesn't exist."""
    with app.test_request_context(path="/auth/login"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"},
            path="/auth/login",
            get_json=lambda: {"provider": "google", "token": "valid-token"},
        )

        with patch("functions.user_management.main.verify_google_token") as mock_verify:
            mock_verify.side_effect = Exception("Invalid token")

            response, status_code = handle_login(request)
            assert status_code == 401
            assert "Invalid token" in response.get_json()["error"]


def test_update_profile_invalid_data(app):
    """Test profile update with invalid data."""
    with app.test_request_context(path="/user/profile", method="PUT"):
        request = Mock(
            headers={"Authorization": "Bearer valid-token"},
            path="/user/profile",
            method="PUT",
            get_json=lambda: {"invalid_field": "value"},
        )

        with patch("functions.user_management.main.update_user_profile") as mock_update:
            mock_update.return_value = Mock(to_dict=lambda: {"id": "user123"})

            _, status_code = update_profile("user123", request)
            assert status_code == 200
            mock_update.assert_called_once()


def test_get_profile_error(app):
    """Test get profile with database error."""
    with app.test_request_context():
        with patch("functions.user_management.main.get_user_profile") as mock_get:
            mock_get.side_effect = Exception("Database error")

            response, status_code = get_profile("user123")
            assert status_code == 500
            assert "Database error" in response.get_json()["error"]


def test_manage_user_invalid_token(app):
    """Test manage_user with invalid session token."""
    with app.test_request_context():
        request = Mock(headers={"Authorization": "Bearer invalid-token"}, path="/profile")

        with patch("functions.user_management.main.verify_session_token") as mock_verify:
            mock_verify.return_value = None  # Simulate invalid token
            response, status_code = manage_user(request)

            assert status_code == 401
            assert "Invalid token" in response.get_json()["error"]


def test_handle_login_general_error(app):
    """Test handle_login with unexpected error."""
    with app.test_request_context():

        def get_json(silent=None):
            return {"provider": "google", "token": "valid.google.token"}  # Format like a JWT

        request = Mock(
            headers={"Authorization": "Bearer valid-token"}, path="/auth/login", get_json=get_json
        )

        with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.side_effect = Exception("Test error")
            response, status_code = manage_user(request)

            assert status_code == 401
            assert "Test error" in response.get_json()["error"]


def test_manage_user_general_error(app):
    """Test general error handling in manage_user."""
    with app.test_request_context():

        def get_json(silent=None):
            return {"some": "data"}

        request = Mock(
            headers={"Authorization": "Bearer valid-token"},
            path="/user/profile",  # Use a path that requires session token
            method="GET",
            get_json=get_json,
        )

        with patch("functions.user_management.main.verify_session_token") as mock_verify:
            mock_verify.side_effect = Exception("Test error")
            response, status_code = manage_user(request)

            assert status_code == 500  # This one should be 500
            assert "Test error" in response.get_json()["error"]


def test_handle_login_unsupported_provider(app):
    """Test login with unsupported provider."""
    with app.test_request_context():

        def get_json(silent=None):
            return {"provider": "facebook", "token": "valid.token"}  # Unsupported provider

        request = Mock(
            headers={"Authorization": "Bearer valid-token"}, path="/auth/login", get_json=get_json
        )

        response, status_code = manage_user(request)

        assert status_code == 400
        assert "Unsupported provider: facebook" in response.get_json()["error"]

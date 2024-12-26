"""Tests for security middleware."""

from unittest.mock import patch

import pytest
from flask import Flask
from werkzeug.exceptions import Unauthorized

from security.middleware import require_auth


@pytest.fixture
def app():
    """Create test Flask app."""
    return Flask(__name__)


def test_require_auth_no_token(app):
    """Test authentication middleware with missing token."""
    with app.test_request_context():

        @require_auth
        def test_route():
            return "OK"

        with pytest.raises(Unauthorized) as exc:
            test_route()
        assert exc.value.code == 401


@patch("security.middleware.verify_token")
def test_require_auth_valid_token(mock_verify, app):
    """Test authentication middleware with valid token."""
    mock_verify.return_value = {"user_id": "123"}

    with app.test_request_context(headers={"Authorization": "Bearer valid-token"}):

        @require_auth
        def test_route():
            return "OK"

        response = test_route()
        assert response == "OK"
        mock_verify.assert_called_once_with("valid-token")

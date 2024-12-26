from unittest.mock import Mock

import pytest
from flask import Flask

from security.middleware import require_auth


@pytest.fixture
def app():
    return Flask(__name__)


def test_require_auth_no_token(app):
    """Test authentication middleware with missing token."""
    with app.test_request_context():

        @require_auth
        def test_route():
            return "OK"

        with pytest.raises(Exception) as exc:
            test_route()
        assert exc.value.code == 401


def test_require_auth_valid_token(app):
    """Test authentication middleware with valid token."""
    with app.test_request_context(headers={"Authorization": "Bearer valid-token"}):

        @require_auth
        def test_route():
            return "OK"

        # Mock the verify_token function
        from security import jwt_manager

        jwt_manager.verify_token = Mock(return_value=True)

        response = test_route()
        assert response == "OK"

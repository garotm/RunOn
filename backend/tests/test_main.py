"""Tests for main FastAPI application."""

from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from models.event import Event


@pytest.fixture
def client():
    """Create a test client."""
    from main import app

    return TestClient(app)


@pytest.fixture
def mock_env():
    """Mock environment variables."""

    def mock_get_required(key: str) -> str:
        return {
            "RUNON_CLIENT_ID": "test_client_id",
            "RUNON_API_KEY": "test_api_key",
            "RUNON_SEARCH_ENGINE_ID": "test_search_engine_id",
        }[key]

    with patch("config.environment.Environment.get_required", mock_get_required):
        yield mock_get_required


@pytest.fixture
def mock_search_events():
    """Mock search events function."""
    mock_events = [
        Event(
            name="Test Run 1",
            date=datetime(2024, 3, 15),
            location="Test Location",
            description="Test Description",
            url="https://test.com/event1",
            distance=5.0,
        ),
        Event(
            name="Test Run 2",
            date=datetime(2024, 4, 1),
            location="Test Location",
            description="Test Description",
            url="https://test.com/event2",
            distance=10.0,
        ),
    ]

    with patch("main.search_running_events", return_value=mock_events):
        yield mock_events


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_search_events_no_auth(client, mock_env):
    """Test search events endpoint without authentication."""
    response = client.post("/events/search?query=test")
    assert response.status_code == 401


def test_search_events_invalid_auth(client, mock_env):
    """Test search events endpoint with invalid authentication."""
    response = client.post(
        "/events/search?query=test",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401


def test_search_events_valid_auth(client, mock_env, mock_search_events):
    """Test search events endpoint with valid authentication."""
    response = client.post(
        "/events/search?query=test",
        headers={"Authorization": "Bearer test_client_id"},
    )
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 2
    assert events[0]["name"] == "Test Run 1"
    assert events[1]["name"] == "Test Run 2"


def test_search_events_missing_query(client, mock_env):
    """Test search events endpoint with missing query."""
    response = client.post(
        "/events/search",
        headers={"Authorization": "Bearer test_client_id"},
    )
    assert response.status_code == 422


def test_search_events_server_error(client, mock_env):
    """Test search events endpoint with server error."""
    with patch("main.search_running_events", side_effect=Exception("Search failed")):
        response = client.post(
            "/events/search?query=test",
            headers={"Authorization": "Bearer test_client_id"},
        )
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_verify_token_missing():
    """Test token verification with missing token."""
    from fastapi import HTTPException

    from main import verify_token

    with pytest.raises(HTTPException) as exc_info:
        await verify_token(None)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Authorization header required"


@pytest.mark.asyncio
async def test_verify_token_invalid(mock_env):
    """Test token verification with invalid token."""
    from fastapi import HTTPException

    from main import verify_token

    with pytest.raises(HTTPException) as exc_info:
        await verify_token("invalid_token")
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid credentials"


@pytest.mark.asyncio
async def test_verify_token_valid(mock_env):
    """Test token verification with valid token."""
    from main import verify_token

    result = await verify_token("Bearer test_client_id")
    assert result is True


@pytest.fixture
def mock_env_error():
    """Mock environment variables with error."""

    def mock_get_required(key: str) -> str:
        raise Exception("Configuration error")

    with patch("config.environment.Environment.get_required", mock_get_required):
        yield mock_get_required


@pytest.mark.asyncio
async def test_verify_token_config_error(mock_env_error):
    """Test token verification with configuration error."""
    from fastapi import HTTPException

    from main import verify_token

    with pytest.raises(HTTPException) as exc_info:
        await verify_token("test_token")
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Server configuration error"

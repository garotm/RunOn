"""Tests for main FastAPI application."""

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a test client."""
    from main import app

    client = TestClient(app)
    return client


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables."""

    def mock_get_required(key: str) -> str:
        return "test_client_id"

    from config.environment import Environment

    monkeypatch.setattr(Environment, "get_required", mock_get_required)
    return mock_get_required


@pytest.fixture
def mock_env_error(monkeypatch):
    """Mock environment variables with error."""

    def mock_get_required(key: str) -> str:
        raise Exception("Configuration error")

    from config.environment import Environment

    monkeypatch.setattr(Environment, "get_required", mock_get_required)
    return mock_get_required


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_search_events_no_auth(client):
    """Test search events endpoint without authentication."""
    response = client.post("/events/search?query=test")
    assert response.status_code == 401
    assert response.json() == {"detail": "Authorization header required"}


def test_search_events_invalid_auth(client, mock_env):
    """Test search events endpoint with invalid authentication."""
    response = client.post(
        "/events/search?query=test",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_search_events_valid_auth(client, mock_env):
    """Test search events endpoint with valid authentication."""
    response = client.post(
        "/events/search?query=test",
        headers={"Authorization": "Bearer test_client_id"},
    )
    assert response.status_code == 200
    assert response.json() == ["event1", "event2"]


def test_search_events_missing_query(client, mock_env):
    """Test search events endpoint without query parameter."""
    response = client.post(
        "/events/search",
        headers={"Authorization": "Bearer test_client_id"},
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_verify_token_missing():
    """Test token verification with missing token."""
    from main import verify_token

    with pytest.raises(HTTPException) as exc:
        await verify_token(None)
    assert exc.value.detail == "Authorization header required"
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_verify_token_invalid(mock_env):
    """Test token verification with invalid token."""
    from main import verify_token

    with pytest.raises(HTTPException) as exc:
        await verify_token("Bearer invalid_token")
    assert exc.value.detail == "Invalid credentials"
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_verify_token_valid(mock_env):
    """Test token verification with valid token."""
    from main import verify_token

    result = await verify_token("Bearer test_client_id")
    assert result is True


@pytest.mark.asyncio
async def test_verify_token_config_error(mock_env_error):
    """Test token verification with configuration error."""
    from main import verify_token

    with pytest.raises(HTTPException) as exc:
        await verify_token("Bearer any_token")
    assert exc.value.detail == "Server configuration error"
    assert exc.value.status_code == 500


def test_search_events_server_error(client, mock_env, monkeypatch):
    """Test search events endpoint with server error."""

    def mock_get_events():
        raise Exception("Search failed")

    monkeypatch.setattr("main.get_mock_events", mock_get_events)

    response = client.post(
        "/events/search?query=test",
        headers={"Authorization": "Bearer test_client_id"},
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Search failed"

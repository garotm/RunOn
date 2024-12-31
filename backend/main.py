"""Main FastAPI application."""

from typing import List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException

from config.environment import Environment

app = FastAPI(title="RunOn API")


async def verify_token(authorization: Optional[str] = Header(None)):
    """Verify the authorization token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    # Remove 'Bearer ' prefix if present
    token = authorization.replace("Bearer ", "")

    # For development/testing, if the token matches our client ID, we'll allow it
    try:
        client_id = Environment.get_required("RUNON_CLIENT_ID")
    except Exception:
        raise HTTPException(status_code=500, detail="Server configuration error")

    if token == client_id:
        return True

    raise HTTPException(status_code=401, detail="Invalid credentials")


def get_mock_events() -> List[str]:
    """Get mock events for testing."""
    return ["event1", "event2"]


@app.post("/events/search")
async def search_and_create_events(
    query: str, authorized: bool = Depends(verify_token)
) -> List[str]:
    """Search for events and create them in calendar."""
    try:
        # For now, return a mock response
        return get_mock_events()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

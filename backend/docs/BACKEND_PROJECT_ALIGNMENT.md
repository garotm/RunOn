# Backend Project Alignment

## MVP

**Observations:**

1.  **Backend Framework:** The backend is built using **FastAPI**, which is excellent! It aligns with my earlier recommendation.
2.  **Existing Functionality:** The backend already has a significant amount of code related to:
    *   **Google Calendar Interaction:** The `src/backend/app/routers/calendar.py` file contains code for creating and managing calendar events.
    *   **Google Search Integration:** The `src/backend/app/routers/search.py` file contains code for interacting with a Google Search API (or a placeholder for it).
    *   **Database (SQLite):** The `src/backend/app/database.py` file suggests that you were planning to use SQLite to store some data locally.
    *   **Utility Functions:** The `src/backend/app/utils.py` file contains various utility functions.
3.  **Testing:** The `tests/` directory has a good set of unit tests, which is great for ensuring code quality.
4.  **Authentication (TODO):** While there's a placeholder for authentication (`src/backend/app/auth.py`), it's not fully implemented. This is something we'll need to address.

**Proposed Approach (Revised):**

Given the existing backend code, I will adapt it to fit the MVP goals, rather than starting from scratch. This will save a lot of time and effort.

1.  **Authentication:**
    *   **Implement Google ID Token Verification:** Modify the backend to receive the Google ID token from the Android app and verify it using the Google Auth Library for Python. This will go in `src/backend/app/auth.py` or a similar authentication-related module.
    *   **Temporary Simplification:** For the MVP, I'll consider a simplified authentication flow where we don't require a complete user login/registration process on the backend. We can rely solely on verifying the Google ID token for now. This can be enhanced later.

2.  **Calendar Endpoint:**
    *   **Refine Existing Endpoint:** Use and refine the existing `/calendar/event` endpoint (or a similar one) in `src/backend/app/routers/calendar.py`.
    *   **Focus on Event Creation:** Ensure this endpoint can create basic calendar events based on the search query received from the Android app.

3.  **Search Endpoint (Simplified):**
    *   **Placeholder for MVP:** Temporarily simplify or even remove the `/search` endpoint for the MVP. The initial focus is on getting the calendar integration working. We can revisit search functionality later.
    *   **Direct Calendar Interaction:** The Android app will primarily interact with the calendar endpoint, passing the search query as a parameter for event creation.

4.  **Database (Optional for MVP):**
    *   **Minimal Usage:** We might not need to use the database at all for the MVP if we're just creating calendar events based on searches. We can decide whether to keep the SQLite integration or remove it temporarily.

5.  **Frontend-Backend Communication:**
    *   The Android app will make HTTP POST requests (using Retrofit) to the refined calendar endpoint, passing the Google ID token in the header and the search query in the request body.

**Actionable Steps:**

1.  **Code Review and Refinement:** Review the existing backend code in the `full-featured-backend` branch, focusing on `calendar.py`, `auth.py`, and `main.py`. Make specific modifications to align it with the MVP.
2.  **Authentication Implementation:** Implement Google ID token verification in your FastAPI backend.
3.  **Environment Setup:** We'll ensure you can run the backend locally. This will likely involve:
    *   Creating a virtual environment (if not already done).
    *   Installing dependencies using `pip install -r requirements.txt`.
    *   Running the FastAPI application using `uvicorn`.

**Questions/Requirements[unfulfilled]:**

1.  **Google Search API:** Create an API key for a Google Search API (e.g., the Custom Search JSON API).
2.  **Database:** Database will be SQLite unless we remove it for the MVP.
3.  **Local Development:** The ability to run the backend code on your local machine currently.

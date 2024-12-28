# MVP

I have adjusted the plan to incorporate the Python backend as using a backend, even for an MVP, is a good practice for security and scalability in the long run. 
It also allows for more flexibility if I decide to add more complex features later.

**Revised Development Plan (MVP with Backend):**

1.  **Project Setup (Modified):**
    *   We'll still create a **new** Android Studio project with an "Empty Compose Activity" to keep the frontend focused.
    *   We will also need to get your **existing Python backend** set up and running locally.

2.  **Google Sign-In (Frontend):**
    *   Implement Google Sign-In in your Android app as before.
    *   **Important Difference:** Instead of directly accessing the Google Calendar API from the app, the app will send the user's Google ID token (obtained after successful sign-in) to your backend.

3.  **Backend (Python):**
    *   **Authentication:** Your backend will be responsible for:
        *   Receiving the Google ID token from the Android app.
        *   Verifying the token's authenticity with Google. This ensures that the user is who they say they are.
    *   **Google Calendar API Interaction:**
        *   The backend will use the Google API Client Library for Python to interact with the Google Calendar API on behalf of the user.
            *   **Caveat:** Making API calls directly from a mobile app has security implications (e.g., handling API keys). I want the backend to act as an intermediary for a public release. Still, for an MVP to gather early feedback, it might be acceptable to do it directly from the app if you are careful about security.
        *   Implement an endpoint (e.g., `/create_event`) that the Android app can call to create calendar events. This endpoint will:
            *   Receive the user's search query from the app.
            *   Create a calendar event using the Calendar API.
            *   Return a success/failure response to the app.

4.  **Frontend-Backend Communication:**
    *   **Network Requests:** Use a library like Retrofit in your Android app to make HTTP requests to your backend endpoints.
    *   **Data Format:** Use a standard format like JSON to exchange data between the app and the backend.

5.  **UI (Frontend):**
    *   The UI remains largely the same: a sign-in screen, a search input screen, and feedback mechanisms.

6.  **Testing:**
    *   Test the entire flow: Sign-in, search, event creation.
    *   Use the Android emulator or a physical device.
    *   Make sure your backend is running locally and accessible to the emulator/device.

**Technology Choices:**

*   **Frontend (Android/Kotlin):**
    *   **Google Sign-In for Android:** As before.
    *   **Retrofit:** For making network requests to your backend.
    *   **Jetpack Compose:** For the UI.
    *   **Google API Client Library for Java:** You might still need this for handling date/time objects or other utilities related to the Calendar API, even though the primary interaction will be through your backend.

*   **Backend (Python):**
    *   **Flask or FastAPI:** Choose one of these frameworks to create your backend API. They are both relatively easy to use for this kind of project. (If your existing backend already uses one of these, stick with it).
    *   **Google API Client Library for Python:** To interact with the Google Calendar API.
    *   **Requests:** (Likely already in your backend) For making HTTP requests to verify the Google ID token.

**Advantages of Using the Backend:**

*   **Security:** API keys and user tokens are handled server-side, which is more secure.
*   **Scalability:** Easier to add more complex features or handle a larger number of users.
*   **Flexibility:** You have more control over the logic and data processing on the backend.

**Challenges:**

*   **Slightly Increased Complexity:** Adds the overhead of managing a separate backend.
*   **Deployment:** You'll eventually need to deploy your backend to a server (e.g., Heroku, Google Cloud Run, AWS, etc.), but this can be done after the MVP is working.

Project: RunOn (`main` branch)

Goal: Implement MVP backend for an app that creates Google Calendar events from user search queries, leveraging Google APIs and no database.

Instructions:

1.  Context:
    *   This hybrid project uses Cursor IDE and Android Studio.
        *   Once all of the code has been taken as far as it can in the IDE and is ready to be imported into the Andriod Studio, a new project will be created within the Android Studio application from which all subsequent testing and emulation will be carried out and the final deployment to the Google Play Store will be completed.
    *   Review the following URLs:
        * Project WIKI - https://github.com/fleXRPL/RunOn/wiki
        *   Main repository `main` branch - https://github.com/fleXRPL/RunOn
            *   All tests currently pass in this branch - https://github.com/fleXRPL/RunOn/pull/35#issue-2761370315
    *   The project's current working directory is `/Users/garotconklin/garotm/fleXRPL/RunOn`
        *   Within this directory, there is a `.env` file containing all of the Variables referenced below and additional project data.
        *   The backend will be built in the Google Public Cloud.
        *   It is safe to assume that everything required in GCP is set up in GCP based on the Variable requirements.
    *   To ensure a consistent workflow, NOTHING will be merged into the `main` branch until all tests pass and the build is verified to work locally.
        *   This will require the creation of `feature` branches for all code changes.
     
3.  Authentication:
    *   Modify `auth.py` to include a function `verify_google_id_token(token: str) -> dict`.
    *   This function should use the `google-auth` library to verify the Google ID token passed from the Android app.
    *   Verify the token against our Google Cloud Project's client ID (get this from the environment variable `RUNON_CLIENT_ID`).
    *   Return the decoded token payload (a dictionary) if the token is valid.
    *   If the token is invalid, raise a `ValueError`.
    *   (We are simplifying authentication for the MVP; no user registration/login on the backend is needed for now).

4.  Search Integration:
    *   Create a new function (in `app.py`, `search.py`, or a new file if appropriate) called `search_with_google(query: str) -> list`.
    *   This function will use the Custom Search JSON API to perform a web search based on the user's query.
    *   Use the environment variables `GOOGLE_API_KEY` and `SEARCH_ENGINE_ID` for API authentication and the Search Engine ID.
    *   Return a list of search result items (or a simplified representation).

5.  Calendar Event Creation:
    *   Modify the `create_calendar_event` function (or create a new, appropriately named function) in `calendar.py`.
    *   This function should accept a search query parameter (string).
    *   If a search query is provided:
        *   Call the `search_with_google` function to get search results.
        *   Use the search results to create a more informative Google Calendar event. For example, the event title could include the search query, and the description could include snippets from the search results.
        *   If no search query is provided, create a basic calendar event.
    *   Use the Google Calendar API (via the `google-api-python-client` library) to create the event on the user's calendar.
    *   Ensure the function interacts correctly with the Google Sign-In flow (using the verified user's credentials).

6.  Database Removal:
    *   Remove or comment out any code related to the SQLite database (in `database.py` and any references to it in other files). We are not using a database for the MVP.

7.  Environment Variables:
    *   Make sure the code uses the following environment variables:
        *   `RUNON_CLIENT_ID`
        *   `RUNON_API_KEY`
        *   `RUNON_SEARCH_ENGINE_ID`

8.  Error Handling:
    *   Implement appropriate error handling in each function (e.g., for invalid tokens, API errors, network issues).
    *   Ensure that all linting and coverage tests pass.

9.  Testing:
    *   It is okay to comment out or remove tests that are no longer relevant due to database removal or other changes. We will write new tests later.
    *   Ensure that all remaining or newly created linting and coverage tests pass.

10.  Documentation:
    *  Amend or create new, comprehensive documentation in the existing WIKI - https://github.com/fleXRPL/RunOn/wiki


# Local Environment Testing Guide

This guide provides detailed instructions for setting up and testing the RunOn backend in a local development environment.

## Prerequisites

- Python 3.9 or higher
- Google Cloud Platform account with the following APIs enabled:
  - Google Calendar API
  - Google Custom Search API
  - Google OAuth 2.0
- macOS, Linux, or WSL for Windows users

## Environment Setup

### 1. Google Cloud Configuration

1. **Access Google Cloud Console**
   - Navigate to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one

2. **Enable Required APIs**
   - In the left sidebar, go to "APIs & Services" > "Library"
   - Search for and enable:
     - Google Calendar API
     - Google Custom Search API

3. **Create OAuth Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - If prompted, configure the OAuth consent screen:
     - User Type: External
     - App name: RunOn
     - User support email: your email
     - Developer contact information: your email
   - For application type, select "Web application"
   - Add authorized redirect URIs:
     - `http://localhost:8000/auth/callback`
   - Save your Client ID and Client Secret

### 2. Local Environment Configuration

1. **Environment Variables**
   Create a `.env` file in the project root:

   ```bash
   # Required OAuth credentials
   RUNON_CLIENT_ID=your_client_id_here
   RUNON_API_KEY=your_api_key_here
   RUNON_SEARCH_ENGINE_ID=your_search_engine_id_here
   ```

2. **Verify File Permissions**

   ```bash
   chmod 600 .env  # Restrict access to owner only
   ```

## Running the Backend

### 1. Initial Setup

```bash
# Navigate to backend directory
cd backend

# Make the run script executable
chmod +x scripts/run_local.sh
```

### 2. Start the Server

```bash
./scripts/run_local.sh
```

This script performs the following:

- Removes existing virtual environment (if any)
- Creates a new Python virtual environment
- Installs all required dependencies
- Sets up environment variables
- Starts the FastAPI server on port 8000

### 3. Testing Endpoints

#### Health Check

```bash
curl http://localhost:8000/health
```
Expected response:

```json
{"status": "healthy"}
```

#### Search Events

```bash
# In a new terminal:
cd /path/to/RunOn && \
while IFS= read -r line; do \
  [[ $line =~ ^#.*$ ]] && continue; \
  [[ -z $line ]] && continue; \
  export "$line"; \
done < <(grep -v '^#' .env | grep -v '^$') && \
curl -X POST "http://localhost:8000/events/search?query=Boston%20Marathon" \
-H "Authorization: Bearer $RUNON_CLIENT_ID" \
-H "Content-Type: application/json"
```

Expected response (development):

```json
["event1", "event2"]
```

## Troubleshooting

### Common Issues and Solutions

1. **Virtual Environment Issues**

   ```bash
   # Remove existing venv
   rm -rf backend/venv
   # Try running setup again
   ./scripts/run_local.sh
   ```

2. **Permission Denied for run_local.sh**

   ```bash
   chmod +x scripts/run_local.sh
   ```

3. **Environment Variables Not Loading**

   ```bash
   # Check .env file exists
   ls -la .env
   
   # Verify file contents (safely)
   grep -v '^#' .env | grep -v '^$'
   ```

4. **Authentication Errors**
   - Verify `RUNON_CLIENT_ID` matches Google Cloud Console
   - Check API enablement status in Google Cloud Console
   - Verify OAuth consent screen configuration

5. **Dependencies Installation Fails**
   - Check Python version:

     ```bash
     python3 --version  # Should be 3.9+
     ```

   - On macOS, ensure Xcode Command Line Tools:

     ```bash
     xcode-select --install
     ```

### Debug Mode

For more detailed logging:

1. **Enable Debug Logging**
   Add to `.env`:

   ```bash
   DEBUG=True
   ```

2. **View Logs**

   ```bash
   tail -f backend/logs/app.log
   ```

## Development Tips

### Testing Changes

1. **Auto-reload**
   The server automatically reloads when you modify Python files.

2. **Manual Restart**
   If needed:

   ```bash
   # Stop the server (Ctrl+C)
   # Restart
   ./scripts/run_local.sh
   ```

### Code Quality

Before committing changes:

```bash

# Run formatting and linting
bash scripts/format_and_lint.sh

# Run tests
python -m pytest
```

## Security Notes

- Never commit `.env` file
- Keep API keys secure
- Use environment variables for sensitive data
- Regularly update dependencies
- Monitor Google Cloud Console for suspicious activity

## Getting Help

- Check [GitHub Issues](https://github.com/fleXRPL/RunOn/issues)
- Review [Project Wiki](https://github.com/fleXRPL/RunOn/wiki)
- Join [Discussions](https://github.com/fleXRPL/RunOn/discussions)

## Next Steps

After successful local testing:

1. Review the main README.md for full project context
2. Check the Android app setup guide
3. Review contribution guidelines
4. Consider setting up CI/CD integration 
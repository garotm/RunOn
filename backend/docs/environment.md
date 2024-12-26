# Environment Variables

This document describes all environment variables required by the RunOn! backend.

## Required Variables

### Authentication
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `APPLE_CLIENT_ID`: Apple Sign In client ID

### Google APIs
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account JSON file
- `GOOGLE_SEARCH_API_KEY`: API key for Google Custom Search
- `GOOGLE_SEARCH_ENGINE_ID`: Custom Search Engine ID
- `GOOGLE_CLOUD_PROJECT`: Google Cloud project ID

### Monitoring
- `STACKDRIVER_PROJECT_ID`: Google Stackdriver project ID
- `LOG_LEVEL`: Logging level (default: INFO)

## Optional Variables

### Application Settings
- `ENVIRONMENT`: Deployment environment (development/staging/production)
- `DEFAULT_SEARCH_RADIUS`: Default radius for event search in km (default: 50)
- `MAX_SEARCH_RESULTS`: Maximum number of search results (default: 10)
- `SEARCH_DATE_RANGE`: Date range for event search (default: m3)

### Rate Limiting
- `RATE_LIMIT_WINDOW`: Rate limit window in seconds (default: 60)
- `RATE_LIMIT_MAX_REQUESTS`: Maximum requests per window (default: 100)

### Cache Settings
- `CACHE_TTL`: Cache time-to-live in seconds (default: 3600)
- `REDIS_URL`: Redis connection URL (if using Redis cache)

## Development Setup

1. Create a `.env` file in the backend directory
2. Copy the template below and fill in your values:

```bash
# Authentication
JWT_SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
APPLE_CLIENT_ID=your-apple-client-id

# Google APIs
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GOOGLE_SEARCH_API_KEY=your-search-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id
GOOGLE_CLOUD_PROJECT=your-project-id

# Environment
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

## Production Deployment

For production deployment, set these variables using your cloud provider's secrets management:

```bash
# GCP Secret Manager
gcloud secrets create runon-jwt-secret \
    --replication-policy="automatic" \
    --data-file="jwt-secret.txt"

# Set in Cloud Functions
gcloud functions deploy runon-api \
    --set-secrets=JWT_SECRET_KEY=runon-jwt-secret:latest
``` 
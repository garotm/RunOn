# RunOn Backend

Simple backend services for the RunOn Android application.

## Features

- Event discovery using Google Search API
- Google Calendar integration
- Simple configuration management

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

2. Set environment variables:
```bash
export GOOGLE_SEARCH_API_KEY=your_key
export GOOGLE_CALENDAR_CLIENT_ID=your_client_id
```

3. Run tests:
```bash
bash scripts/format_and_lint.sh
```

## Project Structure

```
backend/
├── config/              # Configuration management
├── functions/           # Core functionality
│   ├── event_discovery/ # Event search
│   └── calendar_sync/   # Calendar integration
├── models/             # Data models
└── tests/             # Test suite
```

## Testing

Run tests with coverage:
```bash
pytest --cov=.
```

## Contributing

1. Ensure tests pass
2. Follow PEP 8
3. Add tests for new features 
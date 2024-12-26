# RunOn Backend

Simple backend services for the RunOn Android application.

## Features

- Event discovery using Google Search API
- Google Calendar integration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
bash scripts/format_and_lint.sh
```

## Project Structure
```
backend/
├── functions/           # Core functionality
│   ├── event_discovery/ # Event search
│   └── calendar_sync/   # Calendar integration
├── models/             # Data models
└── tests/             # Test suite (100% coverage)
```

## Contributing

1. Ensure tests pass with 100% coverage
2. Follow PEP 8
3. Run format_and_lint.sh before committing

# RunOn Backend

A Python-based backend service for the RunOn application, providing event discovery, calendar synchronization, and user management functionality.

## Features

- Event Discovery
  - Search for running events near a location
  - Integration with Google Custom Search API
  - Event detail extraction and formatting

- Calendar Synchronization
  - Google Calendar integration
  - Add/remove running events
  - List synced events
  - OAuth2 authentication

- User Management
  - Google OAuth authentication
  - JWT-based session management
  - User profile management
  - Secure token validation

- Security
  - JWT token authentication
  - Rate limiting
  - Request validation middleware
  - Environment-based configuration

## Development Setup

### Prerequisites

- Python 3.9+
- pip
- virtualenv (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/garotm/fleXRPL.git
cd fleXRPL/RunOn/backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### Environment Configuration

Create a `.env` file in the backend directory:

```env
ENVIRONMENT=development
JWT_SECRET_KEY=your-secret-key
GOOGLE_SEARCH_API_KEY=your-google-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id
GOOGLE_CLIENT_ID=your-google-client-id
APPLE_CLIENT_ID=your-apple-client-id
```

### Running Tests

Run the test suite with coverage:

```bash
bash scripts/format_and_lint.sh
```

This will:
- Format code with Black
- Sort imports with isort
- Run flake8 linting
- Execute pytest with coverage reporting (current coverage: 98%)

### Code Quality

The project maintains:
- 98% test coverage
- Strict typing with mypy
- PEP 8 compliance via flake8
- Consistent formatting with Black
- Organized imports with isort

### CI/CD

Automated workflows include:
- GitHub Actions for CI/CD (`.github/workflows/`)
- SonarQube Cloud integration
- Dependabot security scanning
- Automated testing and deployment

## Project Structure

```
backend/
├── config/                     # Configuration management
│   ├── __init__.py
│   ├── environment.py          # Environment configuration
│   └── settings.py             # Application settings
├── docs/                       # Documentation
│   └── __init__.py
├── functions/                  # Core functionality
│   ├── calendar_sync/          # Calendar integration
│   │   ├── __init__.py
│   │   ├── calendar.py
│   │   └── main.py
│   ├── event_discovery/        # Event search
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── search.py
│   └── user_management/        # User handling
│       ├── __init__.py
│       ├── auth.py
│       ├── main.py
│       └── models.py
├── infrastructure/             # Infrastructure code
│   └── __init__.py
├── models/                     # Data models
│   ├── __init__.py
│   └── event.py
├── monitoring/                 # Logging and monitoring
│   ├── __init__.py
│   └── logger.py
├── security/                   # Security components
│   ├── __init__.py
│   ├── jwt_manager.py
│   ├── middleware.py
│   └── rate_limiter.py
├── tests/                      # Test suite
│   ├── calendar_sync/
│   ├── config/
│   ├── event_discovery/
│   ├── infrastructure/
│   ├── models/
│   ├── monitoring/
│   ├── security/
│   └── user_management/
├── scripts/                    # Utility scripts
│   ├── cleanup_env.sh
│   └── format_and_lint.sh
├── .env                        # Environment variables (not in repo)
├── README.md                   # This file
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Production dependencies
└── requirements-dev.txt        # Development dependencies
```

## Testing

The test suite is comprehensive and includes:
- Unit tests for all components
- Integration tests for API endpoints
- Mock testing for external services
- Coverage reporting

Run tests with:
```bash
# Full test suite with coverage
bash scripts/format_and_lint.sh

# Single test file
pytest tests/path/to/test_file.py -v

# Test with specific marker
pytest -m "marker_name" -v
```

## API Documentation

API documentation is available in the [docs](./docs) directory.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality (`bash scripts/format_and_lint.sh`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Submit a pull request

## License

[Your License Here]

## Contact

[Your Contact Information] 
<p align="center">
  <img src="https://raw.githubusercontent.com/wiki/fleXRPL/RunOn/images/runon-icon-notext.png" alt="RunOn Logo" width="200"/>
</p>

# RunOn

[![Build and Test](https://github.com/fleXRPL/RunOn/actions/workflows/build.yml/badge.svg)](https://github.com/fleXRPL/RunOn/actions/workflows/build.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_RunOn&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fleXRPL_RunOn)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_RunOn&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fleXRPL_RunOn)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_RunOn&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fleXRPL_RunOn)

A mobile app designed to be the ultimate tool for runners to discover and manage local running events.

## Project Overview

RunOn helps runners find and participate in local running events by providing:

- Event discovery based on location
- Calendar integration for event management
- User profiles and preferences
- Real-time event updates and notifications

## Architecture

### Backend

- **Framework**: Google Cloud Functions
- **Language**: Python 3.9+
- **APIs**: 
  - Google Search API for event discovery
  - Google Calendar API for event management
  - Custom REST APIs for user management

### Android App

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Architecture**: MVVM with Clean Architecture
- **Key Features**:
  - Native Android UI components
  - Offline support
  - Background sync services
  - Material Design 3 implementation

For detailed Android documentation, see our [Wiki](https://github.com/fleXRPL/RunOn/wiki):
- [Android Technical Stack](https://github.com/fleXRPL/RunOn/wiki/Android-Technical-Stack)
- [Android Architecture](https://github.com/fleXRPL/RunOn/wiki/Android-Architecture)
- [Development Guide](https://github.com/fleXRPL/RunOn/wiki/Android-Development-Guide)
- [Implementation Plan](https://github.com/fleXRPL/RunOn/wiki/Android-Implementation-Plan)

### Testing

- Unit tests with pytest
- 100% code coverage requirement
- Automated linting and formatting
- Android instrumentation tests
- UI automation tests

See our [Testing Strategy](https://github.com/fleXRPL/RunOn/wiki/Testing-Strategy) for detailed testing documentation.

## Development Setup

1. Clone the repository:

```bash
git clone https://github.com/fleXRPL/RunOn.git
cd RunOn
```

2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Run tests:

```bash
bash format_and_lint.sh
```

4. Android Setup:

```bash
cd ../android
./gradlew build
```

## Project Structure

```python
RunOn/backend/
.
├── README.md
├── config
│   ├── __init__.py
│   ├── environment.py
│   └── settings.py
├── coverage.xml
├── coveragerc
├── docs
│   ├── __init__.py
│   └── openapi.yaml
├── functions
│   ├── __init__.py
│   ├── calendar_sync
│   │   ├── __init__.py
│   │   ├── calendar.py
│   │   └── main.py
│   ├── event_discovery
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── search.py
│   └── user_management
│       ├── __init__.py
│       ├── auth.py
│       ├── function.yaml
│       ├── main.py
│       └── models.py
├── infrastructure
│   ├── __init__.py
│   └── terraform
│       ├── main.tf
│       ├── outputs.tf
│       └── variables.tf
├── models
│   ├── __init__.py
│   └── event.py
├── monitoring
│   ├── __init__.py
│   └── logger.py
├── pyproject.toml
├── pytest.ini
├── requirements-dev.txt
├── requirements.txt
├── scripts
│   ├── cleanup_env.sh
│   └── format_and_lint.sh
├── security
│   ├── __init__.py
│   ├── jwt_manager.py
│   ├── middleware.py
│   └── rate_limiter.py
└── tests
    ├── __init__.py
    ├── calendar_sync
    │   ├── __init__.py
    │   ├── test_calendar.py
    │   ├── test_calendar_sync.py
    │   └── test_main.py
    ├── config
    │   ├── __init__.py
    │   └── test_environment.py
    ├── conftest.py
    ├── event_discovery
    │   ├── __init__.py
    │   ├── test_event_discovery.py
    │   └── test_search.py
    ├── infrastructure
    │   ├── __init__.py
    │   └── test_terraform.py
    ├── models
    │   ├── __init__.py
    │   └── test_event.py
    ├── monitoring
    │   ├── __init__.py
    │   └── test_logger.py
    ├── security
    │   ├── __init__.py
    │   ├── test_jwt_manager.py
    │   ├── test_middleware.py
    │   └── test_rate_limiter.py
    ├── test_basic.py
    └── user_management
        ├── __init__.py
        ├── test_auth.py
        ├── test_main.py
        └── test_models.py

40 directories, 143 files
```

## Contributing

1. Ensure all tests pass with 100% coverage
2. Follow PEP 8 style guide
3. Run `format_and_lint.sh` before committing
4. Add tests for new functionality

## Documentation

- [Project Plan](docs/detail/IOS/RunOn!-Project_Plan.md)
- [Technical Project Plan](docs/detail/IOS/RunOn!-Technical_Project_Plan.md)
- [Competitive Analysis](docs/detail/IOS/RunOn!-Competitive_Analysis.md)
- [Business Prospectus](docs/detail/IOS/RunOn!-Prospectus.md)

## License

This project is licensed under the terms of the license file in the root directory.

---
Maintained by the fleXRP team

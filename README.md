<p align="center">
  <img src="https://raw.githubusercontent.com/wiki/fleXRPL/RunOn/images/runon-icon-notext.png" alt="RunOn Logo" width="200"/>
</p>

# RunOn

[![Build and Test](https://github.com/fleXRPL/RunOn/actions/workflows/build.yml/badge.svg)](https://github.com/fleXRPL/RunOn/actions)
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

### Testing
- Unit tests with pytest
- 100% code coverage requirement
- Automated linting and formatting

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

## Project Structure
```
RunOn/
├── backend/
│   ├── functions/
│   │   ├── event_discovery/    # Event discovery service
│   │   ├── calendar_sync/      # Calendar integration
│   │   └── user_management/    # User profile management
│   ├── tests/                  # Test suites
│   └── config/                 # Configuration files
└── docs/
    ├── detail/                 # Detailed documentation
    └── summary/                # Summary documentation
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

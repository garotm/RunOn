<p align="center">
  <img src="https://raw.githubusercontent.com/wiki/fleXRPL/RunOn/images/runon-icon-notext.png" alt="RunOn Logo" width="200"/>
</p>

# RunOn

## Project Status

[![Build and Test](https://github.com/fleXRPL/RunOn/actions/workflows/build.yml/badge.svg)](https://github.com/fleXRPL/RunOn/actions/workflows/build.yml)
[![Android CI](https://github.com/fleXRPL/RunOn/actions/workflows/android.yml/badge.svg)](https://github.com/fleXRPL/RunOn/actions/workflows/android.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_RunOn&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fleXRPL_RunOn)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_RunOn&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fleXRPL_RunOn)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_RunOn&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fleXRPL_RunOn)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_RunOn&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=fleXRPL_RunOn)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_RunOn&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=fleXRPL_RunOn)

A mobile app designed to help runners discover and manage local running events.

## Project Overview

RunOn helps runners find and participate in local running events by providing:

- Event discovery based on location
- Simple Google Calendar integration
- Google Sign-in authentication

## Architecture

### Backend

- **APIs**: 
  - Google Search API for event discovery
  - Google Calendar API for event management
- **Testing**:
  - 100% test coverage
  - Automated linting and formatting
  - SonarCloud quality gates

### Android App

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Key Features**:
  - Material Design 3 implementation
  - Direct Google Calendar integration
  - Google Sign-in

## Project Structure

```bash
RunOn/
├── .github/
│   └── workflows/
│       └── build.yml       # CI/CD pipeline
│       └── android.yml     # Android CI/CD pipeline
├── android/                # Android mobile app
│   ├── app/                # Main Android application
│   └── docs/               # Android documentation
├── backend/                # Core functionality
│   ├── functions/          # Business logic
│   ├── models/             # Data models
│   ├── tests/              # Test suite
│   └── scripts/            # Development tools
```

## Development Setup

### Android Setup

```bash
# Clone repository
git clone https://github.com/fleXRPL/RunOn.git
cd RunOn/android

# Run Android setup script
chmod +x scripts/setup.sh
bash scripts/setup.sh
```

### Backend Setup

```bash
# Clone repository
git clone https://github.com/fleXRPL/RunOn.git
cd RunOn/backend

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests and checks
bash scripts/format_and_lint.sh
```

## Branch Strategy

- `main`: Contains MVP implementation
- `full-featured`: Contains full implementation with advanced features

## Contributing

1. Ensure all tests pass with 100% coverage
2. Follow PEP 8 style guide
3. Run `format_and_lint.sh` before committing to backend
4. Run `format_and_lint.sh` before committing to android

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file.

---
Maintained by the fleXRP team

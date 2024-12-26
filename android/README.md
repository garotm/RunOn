# RunOn Android Application

## Overview

The RunOn Android application provides a native mobile interface for discovering and managing running events, with seamless calendar integration and user management features.

## Project Structure

```
android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/flexrpl/runon/
│   │   │   │   ├── activities/         # Main UI activities
│   │   │   │   ├── fragments/          # UI fragments
│   │   │   │   ├── models/             # Data models
│   │   │   │   ├── network/            # API client and services
│   │   │   │   ├── services/           # Background services
│   │   │   │   └── utils/              # Utility classes
│   │   │   └── res/                    # Resources
│   │   └── test/                       # Unit tests
│   ├── build.gradle                    # App-level build config
│   └── proguard-rules.pro              # ProGuard rules
├── gradle/                             # Gradle wrapper
├── build.gradle                        # Project-level build config
└── settings.gradle                     # Project settings
```

## Technology Stack

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Architecture**: MVVM with Clean Architecture
- **Dependencies**:
  - Android Architecture Components
  - Retrofit for API communication
  - Room for local storage
  - Hilt for dependency injection
  - Material Design 3

## Development Setup

1. Install Android Studio (latest version)
2. Install JDK 17 or later
3. Clone the repository
4. Open the project in Android Studio
5. Sync Gradle files
6. Run the application

## Building and Running

```bash
# Build debug variant
./gradlew assembleDebug

# Run tests
./gradlew test

# Install on connected device
./gradlew installDebug
```

## Testing

- Unit Tests: `./gradlew test`
- Instrumentation Tests: `./gradlew connectedAndroidTest`
- UI Tests: `./gradlew connectedCheck`

## CI/CD

The project uses GitHub Actions for continuous integration and deployment:

- Automated builds
- Unit test execution
- Code quality checks
- Release management

## Code Style

The project follows the official Kotlin style guide and Android best practices:

- Kotlin style guide
- Android architecture components patterns
- Material Design guidelines

## Security

- SSL pinning for API communication
- Secure storage for user credentials
- ProGuard optimization and obfuscation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[License details here]

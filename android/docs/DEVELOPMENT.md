# Android Development Guide

## Project Overview

RunOn is an Android application built with modern Android development tools and practices:

- Kotlin as the programming language
- Jetpack Compose for UI
- Coroutines and Flow for asynchronous operations
- Material3 for design

## Directory Structure

```bash
android/
├── app/                                # Main application module
│   ├── src/
│   │   ├── main/
│   │   │   ├── kotlin/                 # Kotlin source files
│   │   │   │   └── com/flexrpl/runon/
│   │   │   │       ├── data/           # Data layer (repositories)
│   │   │   │       ├── domain/         # Domain layer (models)
│   │   │   │       └── ui/             # UI layer (screens, viewmodels)
│   │   │   └── res/                    # Android resources
│   │   └── test/                       # Unit tests
│   └── build.gradle.kts                # App-level build configuration
├── gradle/                             # Gradle wrapper files
├── scripts/                            # Development scripts
└── build.gradle.kts                    # Project-level build configuration
```

## Setup Instructions

### Prerequisites

1. JDK 17
2. macOS (M1/ARM64 compatible)
3. Android Studio (for emulator and interactive development)
4. Git

### First-Time Setup

1. Clone and setup:

   ```bash
   git clone https://github.com/flexrpl/RunOn.git
   cd RunOn
   ./android/scripts/setup.sh    # Sets up build environment
   ```

2. Configure emulator in Android Studio:
   - Open Android Studio
   - Tools → Device Manager
   - Create Device (Pixel 5, API 34)
   - Start emulator

3. Build and install from command line:

   ```bash
   cd android
   ./gradlew installDebug
   ```

### Development Workflow

1. **Command Line Tasks**:
   - Building: `./gradlew build`
   - Testing: `./gradlew test`
   - Formatting: `./scripts/format_and_lint.sh`
   - Installing: `./gradlew installDebug`

2. **Android Studio Tasks**:
   - Code editing
   - Debugging
   - UI development
   - Resource management

### 1. Code Organization

- **data/repository/**: Data access layer
  - `EventRepository.kt`: Interface defining data operations
  - `EventRepositoryImpl.kt`: Implementation with mock data
- **domain/model/**: Business models
  - `Event.kt`: Core data model
- **ui/**: User interface components
  - `EventScreen.kt`: Main UI composition
  - `EventViewModel.kt`: Manages UI state

### 2. Making Changes

1. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Write code following our conventions:
   - Use Kotlin idioms
   - Follow Material3 design guidelines
   - Write tests for business logic

3. Format your code:

   ```bash
   ./scripts/format_and_lint.sh
   ```

   This runs:
   - ktlint for Kotlin style

4. Run tests:

   ```bash
   ./gradlew test
   ```

### 3. Testing

The project includes:

- Unit tests with JUnit and MockK
- Basic UI tests with Compose testing
- Coroutines testing utilities

### 4. Manual Testing

1. Start the emulator:

   ```bash
   $ANDROID_HOME/emulator/emulator -avd RunOnEmulator &
   ```

2. Install the app:

   ```bash
   cd android
   ./gradlew installDebug
   ```

## Troubleshooting

### Common Issues

1. **Emulator Issues**
   - First boot can take several minutes
   - Check nohup.out for emulator logs
   - Try rerunning dev_setup.sh

2. **Build Failures**
   - Check Java version: `java -version`
   - Verify ANDROID_HOME is set
   - Run `./gradlew clean build --info`

3. **Test Failures**
   - Check test logs in build/reports/tests
   - Run specific test: `./gradlew test --tests TestName`

### Getting Help

- Check existing GitHub issues
- Review this documentation
- Ask in team discussions

## Additional Resources

- [Kotlin Style Guide](https://kotlinlang.org/docs/coding-conventions.html)
- [Compose Documentation](https://developer.android.com/jetpack/compose)
- [Material3 Design](https://m3.material.io/)

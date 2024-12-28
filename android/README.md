# RunOn! Android App

## MVP Features

- Event discovery integration
- Google Calendar sync
- Clean architecture implementation

## Project Structure

```bash
android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── kotlin/
│   │   │   │   └── com/flexrpl/runon/
│   │   │   │       ├── data/         # Data layer
│   │   │   │       ├── domain/       # Business logic
│   │   │   │       └── ui/           # Presentation layer
│   │   │   └── res/                  # Resources
│   │   └── test/                     # Unit tests
│   └── build.gradle.kts
└── build.gradle.kts
```

## Development Setup

### Quick Start

```bash
# From project root
./android/scripts/setup.sh
```

The setup script will:

- Install required tools (via Homebrew)
- Initialize Gradle
- Set up permissions
- Run initial build

### Required Software

- Android Studio Hedgehog | 2023.1.1
- JDK 17

## Core Dependencies

```kotlin
dependencies {
    // Core Android
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    
    // UI
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation(platform("androidx.compose:compose-bom:2024.01.00"))
    
    // Testing
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
}
```

## Getting Started

1. Clone the repository
2. Open in Android Studio
3. Sync Gradle files
4. Run tests
5. Build and run

## Testing Requirements

- Unit tests for all business logic
- UI tests for critical paths
- Integration tests for API communication

## Code Style

- Follow Kotlin coding conventions
- Use Compose best practices
- Maintain clean architecture separation

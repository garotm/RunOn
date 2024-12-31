#!/bin/bash

# Set Java version for the session
export JAVA_HOME=$(/Users/garotconklin/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home)
export PATH="$JAVA_HOME/bin:$PATH"

# Run ktlint
echo "🧹 Running code formatting..."
echo "Running ktlint..."
./gradlew ktlintFormat

# Run the build
echo "🏗️ Building Android project..."
./gradlew build 
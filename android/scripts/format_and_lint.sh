#!/bin/bash

set -e

# Set Java version for the session
export JAVA_HOME=$(/Users/garotconklin/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home)
export PATH="$JAVA_HOME/bin:$PATH"

# Change to the android directory (parent of scripts directory)
cd "$(dirname "$0")/.."

echo "🧹 Running code formatting..."

# Run ktlint
echo "Running ktlint..."
./gradlew ktlintFormat

echo "✅ Code formatting complete!" 
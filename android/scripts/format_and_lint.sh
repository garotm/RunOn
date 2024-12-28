#!/bin/bash

set -e

# Change to the android directory (parent of scripts directory)
cd "$(dirname "$0")/.."

echo "🧹 Running code formatting..."

# Run ktlint
echo "Running ktlint..."
./gradlew ktlintFormat

echo "✅ Code formatting complete!" 
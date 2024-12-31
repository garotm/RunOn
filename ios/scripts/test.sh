#!/bin/bash

# Exit on error
set -e

echo "🧪 Running iOS tests..."

# Navigate to iOS project directory
cd "$(dirname "$0")/.."

# Run tests using xcodebuild
xcodebuild test \
    -scheme RunOn \
    -destination 'platform=iOS Simulator,name=iPhone 15,OS=17.2' \
    -enableCodeCoverage YES \
    | xcpretty

# Generate and open code coverage report
xcrun xccov view --report --files-for-target RunOn DerivedData/Logs/Test/*.xcresult

echo "✅ Tests completed!" 
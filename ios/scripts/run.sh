#!/bin/bash

# Exit on error
set -e

echo "🚀 Building and running RunOn..."

# Navigate to iOS project directory
cd "$(dirname "$0")/.."

# Build and run the app in the simulator
xcodebuild \
    -scheme RunOn \
    -destination 'platform=iOS Simulator,name=iPhone 15,OS=17.2' \
    -configuration Debug \
    build run \
    | xcpretty

echo "✅ App is running in simulator!" 
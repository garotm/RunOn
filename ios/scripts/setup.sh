#!/bin/bash

# Exit on error
set -e

echo "🔧 Setting up iOS development environment..."

# Check for Xcode installation
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ Xcode is not installed. Please install Xcode from the App Store."
    exit 1
fi

# Check Xcode version
XCODE_VERSION=$(xcodebuild -version | head -n1 | awk '{print $2}')
echo "✓ Using Xcode version: $XCODE_VERSION"

# Navigate to the correct iOS project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📍 Script directory: $SCRIPT_DIR"

# Check if we're in CI environment (GitHub Actions)
if [[ "$GITHUB_ACTIONS" == "true" ]]; then
    # For CI, navigate to the RunOn directory containing the xcodeproj
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")/RunOn"
else
    # Local development path
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")/RunOn"
fi

echo "📍 Target project directory: $PROJECT_DIR"
cd "$PROJECT_DIR"

echo "📍 Working directory: $(pwd)"
echo "📂 Directory contents:"
ls -la

# Verify Xcode project exists
if [ ! -d "RunOn.xcodeproj" ]; then
    echo "❌ RunOn.xcodeproj not found in $(pwd)"
    echo "Available files:"
    ls -la
    exit 1
fi

# Resolve Swift Package Manager dependencies
echo "📦 Resolving Swift Package Manager dependencies..."
xcodebuild -resolvePackageDependencies -project RunOn.xcodeproj

# Clean build folder
echo "🧹 Cleaning build folder..."
rm -rf build
rm -rf ~/Library/Developer/Xcode/DerivedData/*RunOn*

echo "✨ Setup complete!" 
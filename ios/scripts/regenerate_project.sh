#!/bin/bash

# Exit on error
set -e

echo "🔧 Regenerating Xcode project..."

# Check for xcodegen
if ! command -v xcodegen &> /dev/null; then
    echo "⚠️ xcodegen not found. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew is required to install xcodegen. Please install Homebrew first:"
        echo "https://brew.sh"
        exit 1
    fi
    brew install xcodegen
fi

# Navigate to the project directory
cd "$(dirname "$0")/../RunOn"

# Load .env file if it exists (local development)
if [ -f "../../.env" ]; then
    echo "📝 Loading environment variables from .env file..."
    export $(cat ../../.env | grep -v '^#' | xargs)
fi

# Debug environment variables
echo "📝 Environment variables:"
echo "RUNON_CLIENT_ID: ${RUNON_CLIENT_ID:-not set}"

# Ensure environment variables are set
if [ -z "$RUNON_CLIENT_ID" ]; then
    echo "⚠️ Required environment variable RUNON_CLIENT_ID is not set!"
    echo "Please ensure RUNON_CLIENT_ID is set in .env file (local) or GitHub Secrets (CI)"
    exit 1
fi

# Clean up any existing package resolution files
echo "🧹 Cleaning up package files..."
rm -f RunOn.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved
rm -rf .build

# Backup the old project file
if [ -f "RunOn.xcodeproj/project.pbxproj" ]; then
    echo "📦 Backing up old project file..."
    cp "RunOn.xcodeproj/project.pbxproj" "RunOn.xcodeproj/project.pbxproj.bak"
fi

# Create new project using xcodegen
echo "🛠 Creating new project..."
xcodegen generate

# Verify project generation
if [ ! -f "RunOn.xcodeproj/project.pbxproj" ]; then
    echo "❌ Project generation failed - project.pbxproj not created!"
    exit 1
fi

echo "✨ Project regenerated successfully!" 
#!/bin/bash

# Exit on error
set -e

echo "🔧 Regenerating Xcode project..."

# Navigate to the project directory
cd "$(dirname "$0")/../RunOn"

# Debug environment variables
echo "📝 Environment variables:"
echo "RUNON_CLIENT_ID: ${RUNON_CLIENT_ID:-not set}"

# Ensure environment variables are set
if [ -z "$RUNON_CLIENT_ID" ]; then
    echo "⚠️ Required environment variable RUNON_CLIENT_ID is not set!"
    echo "Please ensure RUNON_CLIENT_ID is set."
    exit 1
fi

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
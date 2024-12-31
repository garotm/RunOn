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

# Install/Update CocoaPods if needed
if ! command -v pod &> /dev/null; then
    echo "📦 Installing CocoaPods..."
    sudo gem install cocoapods
else
    echo "📦 Updating CocoaPods..."
    sudo gem update cocoapods
fi

# Navigate to iOS project directory
cd "$(dirname "$0")/.."

# Install dependencies if Podfile exists
if [ -f "Podfile" ]; then
    echo "📱 Installing iOS dependencies..."
    pod install
    echo "✅ Dependencies installed"
fi

echo "✨ Setup complete!" 
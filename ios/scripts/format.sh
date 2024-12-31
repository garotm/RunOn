#!/bin/bash

# Exit on error
set -e

echo "🎨 Formatting Swift code..."

# Check if SwiftFormat is installed
if ! command -v swiftformat &> /dev/null; then
    echo "📦 Installing SwiftFormat..."
    brew install swiftformat
fi

# Navigate to iOS project directory
cd "$(dirname "$0")/.."

# Format Swift files
swiftformat . \
    --indent 4 \
    --allman false \
    --stripunusedargs closure-only \
    --self remove \
    --disable redundantSelf \
    --disable redundantRawValues \
    --swiftversion 5.9

echo "✨ Formatting complete!" 
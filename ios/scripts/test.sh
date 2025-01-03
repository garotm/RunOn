#!/bin/bash

# Exit on error
set -e

echo "🧪 Running iOS tests..."

# Navigate to iOS project directory
cd "$(dirname "$0")/../RunOn"

# Clean build directory and derived data
echo "🧹 Cleaning build directory..."
rm -rf ~/Library/Developer/Xcode/DerivedData/RunOn-*
rm -rf ./DerivedData

echo "📦 Resolving Swift package dependencies..."
xcodebuild \
    -resolvePackageDependencies \
    -scheme RunOn \
    -clonedSourcePackagesDirPath ./DerivedData/SourcePackages

echo "🏗 Building and testing project..."
xcodebuild \
    -scheme RunOn \
    -destination 'platform=iOS Simulator,name=iPhone 16 Pro,OS=18.2' \
    -derivedDataPath ./DerivedData \
    -configuration Debug \
    clean build test \
    ONLY_ACTIVE_ARCH=YES \
    CODE_SIGN_IDENTITY="" \
    CODE_SIGNING_REQUIRED=NO \
    BUILD_LIBRARY_FOR_DISTRIBUTION=YES \
    ENABLE_TESTABILITY=YES \
    -verbose \
    | tee build.log

# Check if the build succeeded
BUILD_RESULT=${PIPESTATUS[0]}
if [ $BUILD_RESULT -eq 0 ]; then
    echo "✅ Tests completed successfully!"
    exit 0
else
    echo "❌ Tests failed with exit code $BUILD_RESULT"
    exit $BUILD_RESULT
fi 
#!/bin/bash

set -e

# Set Java version for the session
export JAVA_HOME=$(/Users/garotconklin/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home)
export PATH="$JAVA_HOME/bin:$PATH"

echo "🚀 Setting up development environment..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for cleanup flag
if [ "$1" = "--clean" ]; then
    echo "🧹 Cleaning up existing emulator..."
    rm -rf ~/.android/avd/RunOnEmulator*
    rm -f ~/.android/avd/RunOnEmulator.ini
    echo "✅ Cleanup complete"
    exit 0
fi

# Set ANDROID_HOME if not set
if [ -z "$ANDROID_HOME" ]; then
    export ANDROID_HOME="/Users/$USER/Library/Android/sdk"
    echo "Setting ANDROID_HOME to $ANDROID_HOME"
    echo "export ANDROID_HOME=$ANDROID_HOME" >> ~/.zshrc
fi

# Set ANDROID_SDK_ROOT (required by emulator)
if [ -z "$ANDROID_SDK_ROOT" ]; then
    export ANDROID_SDK_ROOT="$ANDROID_HOME"
    echo "Setting ANDROID_SDK_ROOT to $ANDROID_SDK_ROOT"
    echo "export ANDROID_SDK_ROOT=$ANDROID_SDK_ROOT" >> ~/.zshrc
fi

# Verify Android SDK location
if [ ! -d "$ANDROID_HOME" ]; then
    echo "Android SDK not found at $ANDROID_HOME, attempting to install..."
    if ! command_exists sdkmanager; then
        echo "Installing Android Command Line Tools..."
        brew install --cask android-commandlinetools
    fi
fi

# Add Android SDK tools to PATH
export PATH="$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/latest/bin"

echo "📱 Setting up Android emulator..."

# Install required packages
echo "Installing system images and emulator..."
yes | sdkmanager --licenses > /dev/null 2>&1
echo "Installing Android SDK components..."
echo "Installing platform tools..."
sdkmanager "platform-tools"

echo "Installing emulator..."
sdkmanager "emulator"

echo "Installing system image..."
mkdir -p "$ANDROID_SDK_ROOT/system-images/android-34/google_apis/arm64-v8a"
sdkmanager --verbose "system-images;android-34;google_apis;arm64-v8a"

echo "Installing platform and build tools..."
sdkmanager "platforms;android-34" "build-tools;34.0.0"

# Accept the system image license
yes | sdkmanager --licenses

# Verify system image installation
if [ ! -d "$ANDROID_SDK_ROOT/system-images/android-34/google_apis/arm64-v8a" ]; then
    echo "Checking system image installation..."
    sdkmanager --list_installed | grep "system-images;android-34"
    echo "❌ System image installation failed"
    exit 1
fi

# Create AVD if it doesn't exist
if ! avdmanager list avd | grep -q "RunOnEmulator"; then
    echo "Creating Android Virtual Device..."
    
    # Clean up any existing AVD files
    echo "Cleaning up any existing AVD files..."
    rm -rf ~/.android/avd/RunOnEmulator*
    rm -f ~/.android/avd/RunOnEmulator.ini
    
    # Create base config directory
    mkdir -p ~/.android/avd

    # Create AVD with minimal configuration
    echo "no" | avdmanager create avd \
        -n "RunOnEmulator" \
        -k "system-images;android-34;google_apis;arm64-v8a" \
        --force

    # Create a fresh config.ini specifically for M1
    cat > ~/.android/avd/RunOnEmulator.avd/config.ini << 'EOL'
hw.cpu.arch=arm64
hw.cpu.ncore=4
image.sysdir.1=system-images/android-34/google_apis/arm64-v8a/
tag.display=Google APIs
tag.id=google_apis
AvdId=RunOnEmulator
EOL

    # Create hardware config
    cat > ~/.android/avd/RunOnEmulator.avd/hardware-qemu.ini << 'EOL'
hw.ramSize=4096
hw.gpu.enabled=yes
hw.gpu.mode=auto
hw.keyboard=yes
EOL
else
    echo "✓ RunOnEmulator AVD already exists"
fi

# Check if emulator is running
if ! pgrep -f "RunOnEmulator" > /dev/null; then
    echo "Starting emulator..."
    # Start emulator in background
    nohup $ANDROID_HOME/emulator/emulator \
        -avd RunOnEmulator \
        -no-window \
        -gpu host \
        -accel auto &
    
    # Wait for emulator to boot
    echo "Waiting for emulator to boot..."
    echo "This might take a few minutes on first boot..."
    
    # Add timeout (5 minutes)
    TIMEOUT=300
    COUNTER=0
    
    $ANDROID_HOME/platform-tools/adb wait-for-device
    
    # Additional wait for full boot
    echo -n "Waiting for system boot: "
    while [ "$($ANDROID_HOME/platform-tools/adb shell getprop sys.boot_completed 2>/dev/null)" != "1" ]; do
        echo -n "."
        sleep 2
        COUNTER=$((COUNTER + 2))
        if [ $COUNTER -ge $TIMEOUT ]; then
            echo "\n❌ Emulator boot timed out after ${TIMEOUT} seconds"
            echo "Try running the script again or check the emulator logs"
            exit 1
        fi
    done
    echo " Done!"
else
    echo "✓ Emulator already running"
fi

echo "��� Building and installing app..."
cd "$(dirname "$0")/.."
./gradlew installDebug

echo "✅ Development environment setup complete!"
echo "The RunOn app should now be installed on the emulator"
echo ""
echo "To manually start the emulator in the future:"
echo "$ANDROID_HOME/emulator/emulator -avd RunOnEmulator &"
echo ""
echo "To reinstall the app:"
echo "cd android"
echo "./gradlew installDebug" 
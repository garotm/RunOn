#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up Android development environment..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Java version
echo "📝 Checking Java version..."
# Check if Java is installed and is version 17
if ! command_exists java || ! java -version 2>&1 | grep -q "version \"17"; then
    echo "Installing JDK 17..."
    brew install openjdk@17
    # Only create symlink if it doesn't exist
    if [ ! -L "/Library/Java/JavaVirtualMachines/openjdk-17.jdk" ]; then
        sudo ln -sfn $(brew --prefix)/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk
    fi
fi

# Check if Homebrew is installed
if ! command_exists brew; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install required tools
echo "📦 Installing required tools..."
if ! command_exists gradle; then
    echo "Installing Gradle..."
    brew install gradle
else
    echo "✓ Gradle already installed"
fi

if ! command_exists kotlin; then
    echo "Installing Kotlin..."
    brew install kotlin
else
    echo "✓ Kotlin already installed"
fi

# Ensure using Java 17
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
echo "Using Java from: $JAVA_HOME"

# Install Android Command Line Tools
echo "📱 Setting up Android SDK..."
if ! command_exists sdkmanager; then
    echo "Installing Android Command Line Tools..."
    brew install --cask android-commandlinetools
else
    echo "✓ Android Command Line Tools already installed"
fi

# Set ANDROID_HOME and ANDROID_SDK_ROOT
export ANDROID_HOME="/Users/$USER/Library/Android/sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
echo "export ANDROID_HOME=$ANDROID_HOME" >> ~/.zshrc
echo "export ANDROID_SDK_ROOT=$ANDROID_SDK_ROOT" >> ~/.zshrc
echo "export PATH=\$PATH:\$ANDROID_HOME/tools:\$ANDROID_HOME/platform-tools" >> ~/.zshrc

# Accept licenses and install required SDK components
yes | sdkmanager --licenses
echo "Installing Android SDK components..."
sdkmanager --install \
    "platform-tools" \
    "platforms;android-34" \
    "build-tools;34.0.0" \
    "emulator" \
    "system-images;android-34;google_apis;arm64-v8a"

# Verify installations
for component in "platform-tools" "platforms;android-34" "build-tools;34.0.0" "emulator" "system-images;android-34;google_apis;arm64-v8a"; do
    if ! sdkmanager --list | grep -q "$component"; then
        echo "❌ Failed to install $component"
        exit 1
    fi
done

# Create local.properties
echo "sdk.dir=$ANDROID_HOME" > android/local.properties

# Create gradle.properties with required settings
echo "android.useAndroidX=true" > android/gradle.properties
echo "org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8" >> android/gradle.properties
echo "kotlin.code.style=official" >> android/gradle.properties

# Simplify directory creation
mkdir -p android/app/src/main/res/{mipmap,values,drawable}
mkdir -p android/app/src/main/kotlin/com/flexrpl/runon/{data/repository,domain/model,ui}

# Generate debug keystore
if [ ! -f "android/keystore/debug.keystore" ]; then
    echo "🔐 Generating debug keystore..."
    keytool -genkey -v \
      -keystore android/keystore/debug.keystore \
      -storepass android \
      -alias androiddebugkey \
      -keypass android \
      -keyalg RSA \
      -keysize 2048 \
      -validity 10000 \
      -dname "CN=Android Debug,O=Android,C=US" \
      -noprompt
else
    echo "✓ Debug keystore already exists"
fi

# Create launcher icon
if [ ! -f "android/app/src/main/res/mipmap/ic_launcher.xml" ]; then
    cat > android/app/src/main/res/mipmap/ic_launcher.xml << 'EOL'
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
EOL
fi

if [ ! -f "android/app/src/main/res/values/colors.xml" ]; then
    cat > android/app/src/main/res/values/colors.xml << 'EOL'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="primary">#FF6200EE</color>
    <color name="background">#FFFFFF</color>
    <color name="ic_launcher_background">#FFFFFF</color>
</resources>
EOL
fi

# Navigate to android directory
cd "$(dirname "$0")/.."

# Initialize Gradle wrapper
echo "🔧 Setting up Gradle wrapper..."
gradle wrapper

# Make scripts executable
echo "🔑 Setting permissions..."
chmod +x gradlew
chmod +x scripts/*

# Create format_and_lint script if it doesn't exist
mkdir -p scripts
if [ ! -f "scripts/format_and_lint.sh" ]; then
    cat > scripts/format_and_lint.sh << 'EOL'
#!/bin/bash

set -e

# Change to the android directory (parent of scripts directory)
cd "$(dirname "$0")/.."

echo "🧹 Running code formatting..."

# Run ktlint
echo "Running ktlint..."
./gradlew ktlintFormat

echo "✅ Code formatting complete!"
EOL
fi

# Run formatting and linting first
echo "🧹 Running formatting..."
bash scripts/format_and_lint.sh

# Run initial setup
echo "🏗️  Running initial build..."
./gradlew build

echo "✅ Setup complete! You can now run:"
echo "cd android"
echo "./scripts/format_and_lint.sh" 

# Create basic project structure
echo "📁 Creating project structure..."

# Create Event model
if [ ! -f "android/app/src/main/kotlin/com/flexrpl/runon/domain/model/Event.kt" ]; then
    mkdir -p "android/app/src/main/kotlin/com/flexrpl/runon/domain/model"
    cat > "android/app/src/main/kotlin/com/flexrpl/runon/domain/model/Event.kt" << 'EOL'
package com.flexrpl.runon.domain.model

data class Event(
    val id: String,
    val title: String,
    val description: String,
    val date: String,
    val location: String
)
EOL
fi 
#!/bin/bash

# Exit on any error
set -e

# Change to the backend directory
cd "$(dirname "$0")/.."

# Function to check Python version
check_python_version() {
    local required_version="3.9"
    local python_cmd=$1
    local version=$($python_cmd -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    
    if [[ $version == $required_version* ]]; then
        echo "✅ Found compatible Python version: $version"
        return 0
    else
        echo "❌ Python version $version found, but version $required_version.x is required"
        return 1
    fi
}

# Find compatible Python version
echo "🔍 Looking for compatible Python version..."
PYTHON_CMD=""
for cmd in "python3.9" "python3" "python"; do
    if command -v $cmd >/dev/null 2>&1; then
        if check_python_version $cmd; then
            PYTHON_CMD=$cmd
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: Python 3.9.x is required but not found"
    echo "Please install Python 3.9 using one of these methods:"
    echo "  - brew install python@3.9"
    echo "  - arch -arm64 /opt/homebrew/bin/brew install python@3.9"
    exit 1
fi

# Check if venv exists and remove it
if [ -d "venv" ]; then
    echo "🗑️  Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "🔨 Creating new virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate

# Verify virtual environment Python version
if ! check_python_version "python"; then
    echo "❌ Virtual environment Python version mismatch"
    exit 1
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Set up Google Cloud credentials for development
if [ ! -f "$HOME/.config/gcloud/application_default_credentials.json" ]; then
    echo "🔑 Setting up Google Cloud credentials..."
    gcloud auth application-default login
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements-dev.txt

# Run format and lint
echo "🔍 Running format and lint checks..."
PYTHONPATH=$PYTHONPATH:$(pwd) bash scripts/format_and_lint.sh

echo "✅ Setup complete!" 
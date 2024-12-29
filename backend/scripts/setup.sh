#!/bin/bash

# Exit on any error
set -e

# Change to the backend directory
cd "$(dirname "$0")/.."

# Check if venv exists and remove it
if [ -d "venv" ]; then
    echo "🗑️  Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "🔨 Creating new virtual environment..."
python3.9 -m venv venv

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate

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
bash scripts/format_and_lint.sh

echo "✅ Setup complete!" 
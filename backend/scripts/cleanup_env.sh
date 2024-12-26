#!/bin/bash

# Exit on any error
set -e

# Change to the backend directory
cd "$(dirname "$0")/.."
BACKEND_DIR=$(pwd)

echo "🧹 Cleaning up Python environment..."

# Remove Python cache files
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete
find . -type f -name ".coverage" -delete
find . -type f -name "coverage.xml" -delete
find . -type d -name ".pytest_cache" -exec rm -rf {} +
find . -type d -name ".mypy_cache" -exec rm -rf {} +

echo "🗑️  Removing existing virtual environment..."
# Remove virtual environment if it exists
if [ -d "venv" ]; then
    rm -rf venv
fi

echo "🔧 Creating new virtual environment..."
# Create new virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

echo "📦 Clearing pip cache..."
pip cache purge

echo "⬇️  Installing dependencies..."
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements-dev.txt

echo "✨ Environment setup complete!"
echo "👉 Activate the virtual environment with: source venv/bin/activate"

# Print current git branch
BRANCH=$(git branch --show-current)
echo "📌 Current git branch: $BRANCH"

# Check if there are any uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes"
    git status
else
    echo "✅ Working directory is clean"
fi

echo "
🚀 Ready to start development!
Run the following commands to begin:

cd $BACKEND_DIR
source venv/bin/activate
bash scripts/format_and_lint.sh
" 
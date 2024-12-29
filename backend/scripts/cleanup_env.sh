#!/bin/bash

# Exit on any error
set -e

# Change to the backend directory
cd "$(dirname "$0")/.."

# Remove virtual environment
if [ -d "venv" ]; then
    echo "🗑️  Removing virtual environment..."
    rm -rf venv
fi

# Remove Python cache files
echo "🧹 Cleaning Python cache files..."
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

# Remove test cache and coverage files
echo "🧹 Cleaning test and coverage files..."
rm -rf .pytest_cache
rm -rf .coverage
rm -rf coverage.xml
rm -rf htmlcov

# Remove build artifacts
echo "🧹 Cleaning build artifacts..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

echo "✨ Cleanup complete!" 
#!/bin/bash

# Exit on any error
set -e

# Change to the backend directory
cd "$(dirname "$0")/.."

echo "Running Black formatter..."
black .

echo -e "\nRunning isort import sorter..."
isort .

echo -e "\nRunning flake8 linter..."
if [ -f config/.flake8 ]; then
    flake8 --config=config/.flake8 .
else
    flake8 .
fi

echo -e "\nRunning pytest with coverage..."
pytest \
    --verbose \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=xml \
    --cov-config=.coveragerc \
    tests/

# Check the exit code of pytest
if [ $? -eq 0 ]; then
    echo -e "\n✅ All tests passed!"
else
    echo -e "\n❌ Tests failed!"
    exit 1
fi

#!/bin/bash

# Exit on any error
set -e

# Change to the backend directory
cd "$(dirname "$0")/.."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if ! pip show black >/dev/null 2>&1; then
    echo "Installing development dependencies..."
    pip install -r requirements-dev.txt
fi

echo "Running Black formatter..."
python -m black .

echo "Running isort import sorter..."
python -m isort .

echo "Running flake8 linter..."
python -m flake8 .

echo "Running pytest with coverage..."
PYTHONPATH=$PYTHONPATH:$(pwd) python -m pytest --cov=. --cov-report=xml --cov-report=term-missing

# Deactivate virtual environment
deactivate

#!/bin/bash

# Exit on any error
set -e

# Change to the backend directory (one level up from scripts)
cd "$(dirname "$0")/.."

echo "Running Black formatter..."
black functions/

echo -e "\nRunning isort import sorter..."
isort functions/

echo -e "\nRunning flake8 linter..."
flake8 --config=config/.flake8 functions/

echo -e "\nRunning pytest with coverage..."
pytest tests/ -v --cov=functions/ --cov-report=term-missing --cov-report=xml

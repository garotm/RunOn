#!/bin/bash

# Exit on any error
set -e

# Change to the backend directory
cd "$(dirname "$0")/.."

echo "Running Black formatter..."
black .

echo "Running isort import sorter..."
isort .

echo "Running flake8 linter..."
flake8 .

echo "Running pytest with coverage..."
pytest

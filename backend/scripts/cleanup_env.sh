#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Uninstall all packages
pip freeze | xargs pip uninstall -y

# Reinstall from requirements
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Clean pip cache
pip cache purge

# Optional: Remove old .pyc files
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete 
"""Test suite for RunOn backend."""

import os
import sys
from pathlib import Path

# Get the absolute path to the backend directory
backend_dir = Path(__file__).parent.parent.absolute()

# Add the backend directory to Python path
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

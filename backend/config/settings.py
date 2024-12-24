import os
from pathlib import Path

# Google API Configuration
GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", str(Path(__file__).parent / "service-account.json")
)
GOOGLE_CUSTOM_SEARCH_CX = os.getenv("GOOGLE_CUSTOM_SEARCH_CX")

# Search Configuration
DEFAULT_SEARCH_RADIUS = 50  # kilometers
MAX_SEARCH_RESULTS = 10
SEARCH_DATE_RANGE = "m3"  # 3 months

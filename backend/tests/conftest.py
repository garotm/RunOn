"""Test configuration and fixtures."""
import os
import sys
from unittest.mock import MagicMock

import pytest
from google.oauth2.credentials import Credentials

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture
def mock_credentials():
    """Mock Google OAuth credentials."""
    return MagicMock(spec=Credentials)


@pytest.fixture
def mock_search_response():
    """Mock response for Google Custom Search API."""
    return {
        "items": [
            {
                "title": "5K Run on March 15, 2024",
                "snippet": "Join us for a 5K run through Central Park. Distance: 5K",
                "link": "https://example.com/event1",
                "pagemap": {
                    "metatags": [
                        {
                            "og:description": "5K run through Central Park",
                            "og:title": "5K Run on March 15, 2024",
                        }
                    ]
                },
            }
        ]
    }

import pytest
from unittest.mock import Mock, patch
from flask import Flask
from functions.event_discovery.main import discover_events


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


def test_discover_events_missing_location(app):
    with app.app_context():
        request = Mock()
        request.get_json.return_value = None
        request.args = {}
        
        response, status_code = discover_events(request)
        assert status_code == 400
        assert 'error' in response.get_json()


def test_discover_events_valid_request(app):
    with app.app_context():
        request = Mock()
        request.get_json.return_value = {
            'location': 'Seattle, WA',
            'radius': 50
        }
        
        # Mock the search_running_events function to return sample data
        mock_events = [{
            'id': 'test-event-1',
            'title': 'Test Event',
            'date': '2024-03-15T00:00:00',
            'location': {
                'address': 'Seattle, WA',
                'coordinates': {'lat': 0, 'lng': 0}
            }
        }]
        
        with patch('functions.event_discovery.main.search_running_events') as mock_search:
            mock_search.return_value = mock_events
            
            response, status_code = discover_events(request)
            assert status_code == 200
            data = response.get_json()
            assert 'events' in data
            assert 'metadata' in data
            assert data['metadata']['location'] == 'Seattle, WA'
            assert data['events'] == mock_events


def test_discover_events_error_handling(app):
    """Test error handling when search_running_events raises an exception."""
    with app.app_context():
        request = Mock()
        request.get_json.return_value = {
            'location': 'Seattle, WA',
            'radius': 50
        }
        
        # Mock the search_running_events function to raise an exception
        with patch('functions.event_discovery.main.search_running_events') as mock_search:
            mock_search.side_effect = Exception('Search API error')
            
            response, status_code = discover_events(request)
            assert status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Search API error'
            assert data['status'] == 500
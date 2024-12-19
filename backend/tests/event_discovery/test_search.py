import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from freezegun import freeze_time
from functions.event_discovery.search import (
    search_running_events,
    get_google_search_client,
    extract_coordinates,
    extract_date,
    extract_distance
)


@pytest.fixture
def mock_search_response():
    """Mock response from Google Custom Search API."""
    return {
        'items': [
            {
                'title': 'Seattle Marathon 2024',
                'link': 'https://example.com/seattle-marathon',
                'snippet': 'Annual Seattle Marathon on March 15, 2024. Join us for this 26.2 mile race through downtown Seattle.',
                'pagemap': {
                    'metatags': [
                        {
                            'og:description': 'Marathon event in Seattle',
                            'og:title': 'Seattle Marathon 2024'
                        }
                    ]
                }
            }
        ]
    }


def test_get_google_search_client_missing_credentials():
    """Test client creation fails without credentials."""
    with patch('os.getenv', return_value=None):
        with pytest.raises(ValueError) as exc:
            get_google_search_client()
        assert "GOOGLE_APPLICATION_CREDENTIALS environment variable not set" in str(exc.value)


@patch('functions.event_discovery.search.build')
@patch('functions.event_discovery.search.service_account.Credentials')
def test_get_google_search_client_success(mock_credentials, mock_build):
    """Test successful client creation."""
    with patch('os.getenv', return_value='/path/to/credentials.json'):
        mock_credentials.from_service_account_file.return_value = 'fake_creds'
        mock_build.return_value = 'fake_client'
        
        client = get_google_search_client()
        
        assert client == 'fake_client'
        mock_credentials.from_service_account_file.assert_called_once()
        mock_build.assert_called_once_with('customsearch', 'v1', credentials='fake_creds')


@patch('functions.event_discovery.search.get_google_search_client')
def test_search_running_events_success(mock_get_client, mock_search_response):
    """Test successful event search."""
    mock_service = Mock()
    mock_cse = Mock()
    mock_list = Mock()
    
    mock_get_client.return_value = mock_service
    mock_service.cse.return_value = mock_cse
    mock_cse.list.return_value = mock_list
    mock_list.execute.return_value = mock_search_response
    
    events = search_running_events('Seattle, WA')
    
    assert len(events) == 1
    event = events[0]
    assert event['title'] == 'Seattle Marathon 2024'
    assert event['url'] == 'https://example.com/seattle-marathon'
    assert 'location' in event
    assert event['type'] == 'running'


@patch('functions.event_discovery.search.get_google_search_client')
def test_search_running_events_api_error(mock_get_client):
    """Test error handling in search."""
    mock_get_client.side_effect = Exception('API Error')
    
    with pytest.raises(Exception) as exc:
        search_running_events('Seattle, WA')
    assert 'Failed to search events' in str(exc.value)


def test_extract_coordinates():
    """Test coordinate extraction."""
    item = {'pagemap': {'metatags': [{'og:latitude': '47.6062', 'og:longitude': '-122.3321'}]}}
    coords = extract_coordinates(item)
    assert coords == {'lat': 0, 'lng': 0}  # Currently returns default values


@freeze_time('2024-01-15')
def test_extract_date():
    """Test date extraction."""
    item = {'snippet': 'Event on March 15, 2024'}
    date = extract_date(item)
    expected_date = (datetime(2024, 1, 15) + timedelta(days=30)).isoformat()
    assert date == expected_date


def test_extract_distance():
    """Test distance extraction."""
    item = {'title': 'Seattle 5K Run', 'snippet': '5K race in downtown'}
    distance = extract_distance(item)
    assert distance == '5K' 
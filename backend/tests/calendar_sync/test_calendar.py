import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from freezegun import freeze_time
from functions.calendar_sync.calendar import (
    get_calendar_service,
    add_event_to_calendar,
    remove_event_from_calendar,
    list_synced_events
)


@pytest.fixture
def mock_credentials():
    """Mock Google OAuth2 credentials."""
    return Mock()


@pytest.fixture
def mock_service():
    """Mock Google Calendar service."""
    service = Mock()
    # Create proper mock chain
    events = Mock()
    service.events.return_value = events
    
    # Setup insert mock
    insert = Mock()
    events.insert.return_value = insert
    insert.execute.return_value = {'id': 'event123'}
    
    # Setup delete mock
    delete = Mock()
    events.delete.return_value = delete
    delete.execute.return_value = None
    
    # Setup list mock
    list_mock = Mock()
    events.list.return_value = list_mock
    list_mock.execute.return_value = {'items': [{'id': 'event123'}]}
    
    return service


def test_get_calendar_service(mock_credentials):
    """Test calendar service initialization."""
    with patch('functions.calendar_sync.calendar.build') as mock_build:
        mock_build.return_value = 'calendar_service'
        service = get_calendar_service(mock_credentials)
        assert service == 'calendar_service'
        mock_build.assert_called_once_with('calendar', 'v3', credentials=mock_credentials)


def test_add_event_to_calendar(mock_service):
    """Test adding event to calendar."""
    event_data = {
        'title': 'Test Run',
        'date': '2024-03-15T10:00:00Z',
        'location': {'address': 'Test Location'},
        'description': 'Test Description'
    }
    
    result = add_event_to_calendar(mock_service, event_data)
    assert result == {'id': 'event123'}
    
    mock_service.events.assert_called_once()
    mock_service.events().insert.assert_called_once()


def test_remove_event_from_calendar(mock_service):
    """Test removing event from calendar."""
    remove_event_from_calendar(mock_service, 'event123')
    
    mock_service.events.assert_called_once()
    mock_service.events().delete.assert_called_once()


@freeze_time('2024-01-15')
def test_list_synced_events(mock_service):
    """Test listing synced events."""
    events = list_synced_events(mock_service)
    assert events == [{'id': 'event123'}]
    
    mock_service.events.assert_called_once()
    mock_service.events().list.assert_called_once()
    assert 'timeMin' in mock_service.events().list.call_args[1] 
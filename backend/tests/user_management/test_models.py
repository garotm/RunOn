import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from functions.user_management.models import (
    User,
    create_user_profile,
    get_user_profile,
    update_user_profile,
    delete_user_profile
)


@pytest.fixture
def mock_firestore():
    """Create a mock Firestore client."""
    mock_client = Mock()
    mock_collection = Mock()
    mock_doc = Mock()
    
    mock_client.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_doc
    
    return {
        'client': mock_client,
        'collection': mock_collection,
        'doc': mock_doc
    }


@pytest.fixture
def sample_user_data():
    """Create sample user data."""
    return {
        'id': 'user123',
        'email': 'test@example.com',
        'name': 'Test User',
        'provider': 'google',
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'preferences': {
            'notifications': True,
            'email_updates': True,
            'distance_unit': 'km',
            'theme': 'light'
        }
    }


def test_user_to_dict(sample_user_data):
    """Test User.to_dict method."""
    user = User.from_dict(sample_user_data)
    result = user.to_dict()
    
    assert result['id'] == 'user123'
    assert result['email'] == 'test@example.com'
    assert 'created_at' in result
    assert 'updated_at' in result
    assert isinstance(result['created_at'], str)
    assert isinstance(result['updated_at'], str)


def test_user_from_dict(sample_user_data):
    """Test User.from_dict method."""
    user = User.from_dict(sample_user_data)
    
    assert user.id == 'user123'
    assert user.email == 'test@example.com'
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_create_user_profile(mock_firestore):
    """Test user profile creation."""
    with patch('functions.user_management.models.get_firestore_client') as mock_get_client:
        mock_get_client.return_value = mock_firestore['client']
        
        user = create_user_profile(
            user_id='user123',
            email='test@example.com',
            name='Test User',
            provider='google'
        )
        
        assert user.id == 'user123'
        assert user.email == 'test@example.com'
        mock_firestore['doc'].set.assert_called_once()


def test_get_user_profile(mock_firestore, sample_user_data):
    """Test getting user profile."""
    mock_firestore['doc'].get.return_value.exists = True
    mock_firestore['doc'].get.return_value.to_dict.return_value = sample_user_data
    
    with patch('functions.user_management.models.get_firestore_client') as mock_get_client:
        mock_get_client.return_value = mock_firestore['client']
        
        user = get_user_profile('user123')
        
        assert user.id == 'user123'
        assert user.email == 'test@example.com'
        mock_firestore['collection'].document.assert_called_with('user123')


def test_update_user_profile(mock_firestore, sample_user_data):
    """Test updating user profile."""
    mock_firestore['doc'].get.return_value.exists = True
    mock_firestore['doc'].get.return_value.to_dict.return_value = sample_user_data
    
    with patch('functions.user_management.models.get_firestore_client') as mock_get_client:
        mock_get_client.return_value = mock_firestore['client']
        
        update_data = {'name': 'Updated Name'}
        user = update_user_profile('user123', update_data)
        
        assert user.name == 'Updated Name'
        mock_firestore['doc'].update.assert_called_once()


def test_delete_user_profile(mock_firestore):
    """Test deleting user profile."""
    mock_firestore['doc'].get.return_value.exists = True
    
    with patch('functions.user_management.models.get_firestore_client') as mock_get_client:
        mock_get_client.return_value = mock_firestore['client']
        
        delete_user_profile('user123')
        
        mock_firestore['doc'].delete.assert_called_once()


def test_delete_user_profile_not_found(mock_firestore):
    """Test deleting non-existent user profile."""
    mock_firestore['doc'].get.return_value.exists = False
    
    with patch('functions.user_management.models.get_firestore_client') as mock_get_client:
        mock_get_client.return_value = mock_firestore['client']
        
        with pytest.raises(ValueError) as exc:
            delete_user_profile('nonexistent')
        assert 'User nonexistent not found' in str(exc.value)


def test_update_user_profile_not_found(mock_firestore):
    """Test updating non-existent user profile."""
    mock_firestore['doc'].get.return_value.exists = False
    
    with patch('functions.user_management.models.get_firestore_client') as mock_get_client:
        mock_get_client.return_value = mock_firestore['client']
        
        with pytest.raises(ValueError) as exc:
            update_user_profile('nonexistent', {'name': 'New Name'})
        assert 'User nonexistent not found' in str(exc.value)


def test_update_user_profile_no_changes(mock_firestore, sample_user_data):
    """Test updating profile with no valid fields."""
    mock_firestore['doc'].get.return_value.exists = True
    mock_firestore['doc'].get.return_value.to_dict.return_value = sample_user_data
    
    with patch('functions.user_management.models.get_firestore_client') as mock_get_client:
        mock_get_client.return_value = mock_firestore['client']
        
        user = update_user_profile('user123', {'invalid_field': 'value'})
        assert user.id == 'user123'
        mock_firestore['doc'].update.assert_not_called() 


def test_update_user_profile_no_valid_fields(mock_firestore, sample_user_data):
    """Test updating user profile with no valid fields."""
    mock_firestore['doc'].get.return_value.exists = True
    mock_firestore['doc'].get.return_value.to_dict.return_value = sample_user_data
    
    with patch('functions.user_management.models.get_firestore_client') as mock_get_client:
        mock_get_client.return_value = mock_firestore['client']
        
        # Try to update with only invalid fields
        update_data = {'invalid_field1': 'value1', 'invalid_field2': 'value2'}
        user = update_user_profile('user123', update_data)
        
        # Should return unchanged user without making Firestore call
        assert user.id == 'user123'
        mock_firestore['doc'].update.assert_not_called()
  
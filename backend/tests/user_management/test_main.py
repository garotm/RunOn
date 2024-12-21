import pytest
from unittest.mock import Mock, patch
from flask import Flask
from functions.user_management.main import manage_user


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    return app


@pytest.fixture
def mock_user():
    """Create a mock user object."""
    return Mock(
        id='user123',
        email='test@example.com',
        name='Test User',
        to_dict=lambda: {
            'id': 'user123',
            'email': 'test@example.com',
            'name': 'Test User'
        }
    )


def test_manage_user_missing_auth(app):
    """Test manage_user with missing authorization header."""
    with app.test_request_context():
        request = Mock(headers={})
        response, status_code = manage_user(request)
        
        assert status_code == 401
        assert 'Missing or invalid authorization header' in response.get_json()['error']


def test_manage_user_login_success(app, mock_user):
    """Test successful user login."""
    with app.test_request_context(path='/auth/login'):
        request = Mock(
            headers={'Authorization': 'Bearer valid-token'},
            path='/auth/login',
            get_json=lambda: {
                'provider': 'google',
                'token': 'google-token'
            }
        )
        
        mock_user_info = {
            'sub': 'user123',
            'email': 'test@example.com',
            'name': 'Test User'
        }
        
        with patch('functions.user_management.main.verify_google_token') as mock_verify:
            with patch('functions.user_management.main.get_user_profile') as mock_get_user:
                with patch('functions.user_management.main.create_session_token') as mock_create_token:
                    mock_verify.return_value = mock_user_info
                    mock_get_user.return_value = mock_user
                    mock_create_token.return_value = 'session-token'
                    
                    response, status_code = manage_user(request)
                    
                    assert status_code == 200
                    data = response.get_json()
                    assert data['status'] == 'success'
                    assert data['token'] == 'session-token'
                    assert 'user' in data


def test_manage_user_get_profile(app, mock_user):
    """Test getting user profile."""
    with app.test_request_context(path='/user/profile'):
        request = Mock(
            headers={'Authorization': 'Bearer valid-token'},
            path='/user/profile',
            method='GET'
        )
        
        with patch('functions.user_management.main.verify_session_token') as mock_verify:
            with patch('functions.user_management.main.get_user_profile') as mock_get_user:
                mock_verify.return_value = {'sub': 'user123'}
                mock_get_user.return_value = mock_user
                
                response, status_code = manage_user(request)
                
                assert status_code == 200
                data = response.get_json()
                assert data['status'] == 'success'
                assert data['profile']['id'] == 'user123'


def test_manage_user_update_profile(app, mock_user):
    """Test updating user profile."""
    with app.test_request_context(path='/user/profile', method='PUT'):
        request = Mock(
            headers={'Authorization': 'Bearer valid-token'},
            path='/user/profile',
            method='PUT',
            get_json=lambda: {'name': 'Updated Name'}
        )
        
        with patch('functions.user_management.main.verify_session_token') as mock_verify:
            with patch('functions.user_management.main.update_user_profile') as mock_update:
                mock_verify.return_value = {'sub': 'user123'}
                mock_update.return_value = mock_user
                
                response, status_code = manage_user(request)
                
                assert status_code == 200
                data = response.get_json()
                assert data['status'] == 'success'
                assert 'profile' in data


def test_manage_user_invalid_endpoint(app):
    """Test invalid endpoint."""
    with app.test_request_context(path='/invalid'):
        request = Mock(
            headers={'Authorization': 'Bearer valid-token'},
            path='/invalid',
            method='GET'
        )
        
        with patch('functions.user_management.main.verify_session_token') as mock_verify:
            mock_verify.return_value = {'sub': 'user123'}
            
            response, status_code = manage_user(request)
            
            assert status_code == 404
            assert 'Invalid endpoint' in response.get_json()['error'] 


def test_manage_user_invalid_json(app):
    """Test manage_user with invalid JSON."""
    with app.test_request_context(path='/auth/login'):
        request = Mock(
            headers={'Authorization': 'Bearer valid-token'},
            path='/auth/login',
            get_json=lambda: None
        )
        
        response, status_code = manage_user(request)
        assert status_code == 400
        assert 'No credentials provided' in response.get_json()['error']


def test_manage_user_missing_token(app):
    """Test manage_user with missing token."""
    with app.test_request_context(path='/auth/login'):
        request = Mock(
            headers={'Authorization': 'Bearer valid-token'},
            path='/auth/login',
            get_json=lambda: {'provider': 'google'}
        )
        
        response, status_code = manage_user(request)
        assert status_code == 400
        assert 'Missing provider or token' in response.get_json()['error']


def test_manage_user_unsupported_provider(app):
    """Test manage_user with unsupported provider."""
    with app.test_request_context(path='/auth/login'):
        request = Mock(
            headers={'Authorization': 'Bearer valid-token'},
            path='/auth/login',
            get_json=lambda: {
                'provider': 'unsupported',
                'token': 'token'
            }
        )
        
        response, status_code = manage_user(request)
        assert status_code == 400
        assert 'Unsupported provider' in response.get_json()['error']


def test_manage_user_profile_not_found(app):
    """Test getting non-existent profile."""
    with app.test_request_context(path='/user/profile'):
        request = Mock(
            headers={'Authorization': 'Bearer valid-token'},
            path='/user/profile',
            method='GET'
        )
        
        with patch('functions.user_management.main.verify_session_token') as mock_verify:
            with patch('functions.user_management.main.get_user_profile') as mock_get_user:
                mock_verify.return_value = {'sub': 'user123'}
                mock_get_user.return_value = None
                
                response, status_code = manage_user(request)
                assert status_code == 404
                assert 'User not found' in response.get_json()['error']


def test_manage_user_update_profile_no_data(app):
    """Test updating profile with no data."""
    with app.test_request_context(path='/user/profile', method='PUT'):
        request = Mock(
            headers={'Authorization': 'Bearer valid-token'},
            path='/user/profile',
            method='PUT',
            get_json=lambda: None
        )
        
        with patch('functions.user_management.main.verify_session_token') as mock_verify:
            mock_verify.return_value = {'sub': 'user123'}
            
            response, status_code = manage_user(request)
            assert status_code == 400
            assert 'No update data provided' in response.get_json()['error']
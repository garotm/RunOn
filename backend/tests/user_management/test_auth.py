import pytest
from unittest.mock import Mock, patch
import jwt
from datetime import datetime, timedelta
import json
import responses

from functions.user_management.auth import (
    verify_google_token,
    verify_apple_token,
    create_session_token,
    verify_session_token,
    get_apple_public_key
)


@pytest.fixture
def mock_user():
    """Create a mock user object."""
    class User:
        def __init__(self):
            self.id = 'user123'
            self.email = 'test@example.com'
            self.name = 'Test User'
    return User()


@pytest.fixture
def valid_jwt_token():
    """Create a valid JWT token for testing."""
    payload = {
        'sub': 'user123',
        'email': 'test@example.com',
        'name': 'Test User',
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, 'test-secret', algorithm='HS256')


def test_verify_google_token():
    """Test Google token verification."""
    mock_token = 'google-token'
    mock_user_info = {
        'sub': 'google123',
        'email': 'test@gmail.com',
        'name': 'Test Google'
    }
    
    with patch('google.oauth2.id_token.verify_oauth2_token') as mock_verify:
        mock_verify.return_value = mock_user_info
        
        result = verify_google_token(mock_token)
        
        assert result == mock_user_info
        mock_verify.assert_called_once()


def test_verify_apple_token():
    """Test Apple token verification."""
    mock_token = 'apple-token'
    mock_header = {'kid': 'key123'}
    mock_key = {
        'kty': 'RSA',
        'kid': 'key123',
        'n': 'test',
        'e': 'AQAB'
    }
    mock_payload = {
        'sub': 'apple123',
        'email': 'test@icloud.com',
        'name': {'firstName': 'Test', 'lastName': 'Apple'}
    }
    
    with patch('jwt.get_unverified_header') as mock_header_fn:
        with patch('functions.user_management.auth.get_apple_public_key') as mock_key_fn:
            with patch('jwt.decode') as mock_decode:
                mock_header_fn.return_value = mock_header
                mock_key_fn.return_value = mock_key
                mock_decode.return_value = mock_payload
                
                result = verify_apple_token(mock_token)
                
                assert result['sub'] == 'apple123'
                assert result['email'] == 'test@icloud.com'
                assert result['name'] == 'Test Apple'


def test_create_session_token(mock_user):
    """Test session token creation."""
    with patch('os.getenv', return_value='test-secret'):
        token = create_session_token(mock_user)
        
        # Verify token can be decoded
        payload = jwt.decode(token, 'test-secret', algorithms=['HS256'])
        assert payload['sub'] == 'user123'
        assert payload['email'] == 'test@example.com'
        assert payload['name'] == 'Test User'


def test_verify_session_token(valid_jwt_token):
    """Test session token verification."""
    with patch('os.getenv', return_value='test-secret'):
        result = verify_session_token(valid_jwt_token)
        
        assert result['sub'] == 'user123'
        assert result['email'] == 'test@example.com'
        assert result['name'] == 'Test User'


def test_verify_session_token_invalid():
    """Test invalid session token verification."""
    with patch('os.getenv', return_value='test-secret'):
        result = verify_session_token('invalid-token')
        assert result is None


def test_verify_apple_token_invalid_key():
    """Test Apple token verification with invalid key."""
    with patch('jwt.get_unverified_header') as mock_header:
        mock_header.return_value = {'kid': 'invalid-key'}
        
        with patch('functions.user_management.auth.get_apple_public_key') as mock_key:
            mock_key.side_effect = ValueError('Key not found')
            
            with pytest.raises(ValueError):
                verify_apple_token('invalid-token') 


@responses.activate
def test_get_apple_public_key_success():
    """Test successful Apple public key retrieval."""
    kid = 'test-kid'
    mock_key = {
        'kty': 'RSA',
        'kid': 'test-kid',
        'n': 'test',
        'e': 'AQAB'
    }
    mock_response = {
        'keys': [mock_key]
    }
    
    responses.add(
        responses.GET,
        'https://appleid.apple.com/auth/keys',
        json=mock_response,
        status=200
    )
    
    result = get_apple_public_key(kid)
    assert result == mock_key


@responses.activate
def test_get_apple_public_key_not_found():
    """Test Apple public key not found."""
    kid = 'missing-kid'
    mock_response = {
        'keys': [{
            'kid': 'other-kid'
        }]
    }
    
    responses.add(
        responses.GET,
        'https://appleid.apple.com/auth/keys',
        json=mock_response,
        status=200
    )
    
    with pytest.raises(ValueError) as exc:
        get_apple_public_key(kid)
    assert f'Key ID {kid} not found' in str(exc.value)


def test_verify_apple_token_invalid():
    """Test Apple token verification with invalid token."""
    # Create an invalid but properly base64-encoded JWT token with kid
    invalid_token = (
        'eyJhbGciOiJSUzI1NiIsImtpZCI6InRlc3Qta2lkIiwidHlwIjoiSldUIn0'  # header with kid
        '.'
        'eyJzdWIiOiIxMjM0NTY3ODkwIn0'  # payload
        '.'
        'aW52YWxpZC1zaWduYXR1cmU='  # base64 encoded "invalid-signature"
    )
    
    with pytest.raises(ValueError) as exc:
        verify_apple_token(invalid_token)
    assert 'Invalid Apple token' in str(exc.value)
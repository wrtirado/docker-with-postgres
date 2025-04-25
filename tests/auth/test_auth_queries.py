import pytest
from unittest.mock import MagicMock
from app.auth.auth_queries import (
    generate_auth_code,
    verify_auth_code,
    verify_refresh_token,
    delete_refresh_token,
    validate_token,
)
from fastapi import HTTPException
from datetime import timedelta, datetime, timezone
import jwt
from app.config import SECRET_KEY


@pytest.mark.auth_queries
def test_generate_auth_code(mocker):
    # Arrange: Mock the Redis client
    # patch the redis client to avoid actual Redis calls
    # and to control the behavior of the setex method
    # and set test email
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.setex = MagicMock()
    email = "test@example.com"

    # Act: Call the function
    auth_code = generate_auth_code(email)

    # Assert: Verify the behavior
    assert len(auth_code) == 6  # Ensure the code is 6 digits
    assert auth_code.isdigit()  # Ensure the code is numeric
    mock_redis.setex.assert_called_once_with(
        f"auth_code:{email}",  # Key
        mocker.ANY,  # Expiration time (mocked)
        auth_code,  # Value
    )


@pytest.mark.auth_queries
def test_verify_auth_code_valid(mocker):
    # Arrange: Mock the Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.get = MagicMock(return_value="123456")
    mock_redis.delete = MagicMock()
    email = "test@example.com"
    auth_code = "123456"

    # Act: Call the function
    result = verify_auth_code(email, auth_code)

    # Assert: Verify the behavior
    assert "access_token" in result
    assert "refresh_token" in result
    mock_redis.get.assert_called_once_with(f"auth_code:{email}")
    mock_redis.delete.assert_called_once_with(f"auth_code:{email}")


@pytest.mark.auth_queries
def test_verify_auth_code_invalid(mocker):
    # Arrange: Mock the Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.get = MagicMock(return_value=None)
    email = "test@example.com"
    auth_code = "123456"

    # Act: Call the function and expect an exception
    with pytest.raises(HTTPException) as excinfo:
        verify_auth_code(email, auth_code)

    # Assert: Verify the behavior
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Invalid or expired code"
    mock_redis.get.assert_called_once_with(f"auth_code:{email}")


@pytest.mark.auth_queries
def test_verify_refresh_token_valid(mocker):
    # Arrange: Encode a valid refresh token
    refresh_payload = {
        "sub": "test@example.com",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
        "token_type": "refresh",
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")
    # Arrange: Mock the Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.get = MagicMock(return_value=refresh_token)
    email = "test@example.com"

    # Act: Call the function
    result = verify_refresh_token(refresh_token)

    # Assert: Verify the behavior
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    mock_redis.get.assert_called_once_with(f"refresh_token:{email}")


@pytest.mark.auth_queries
def test_verify_refresh_token_expired(mocker):
    # Arrange: Encode a valid refresh token
    refresh_payload = {
        "sub": "test@example.com",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=10),
        "token_type": "refresh",
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")
    # Arrange: Mock the Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.get = MagicMock(return_value=refresh_token)
    email = "test@example.com"

    # Act: Call the function
    with pytest.raises(HTTPException) as excinfo:
        verify_refresh_token(refresh_token)

    # Assert: Verify the behavior
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Token has expired"


@pytest.mark.auth_queries
def test_verify_refresh_token_invalid(mocker):
    # Arrange: Encode a valid refresh token
    refresh_payload = {
        "sub": "test@example.com",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
        "token_type": "refresh",
    }
    refresh_token = jwt.encode(refresh_payload, "123456789", algorithm="HS256")
    # Arrange: Mock the Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.get = MagicMock(return_value=refresh_token)
    email = "test@example.com"

    # Act: Call the function
    with pytest.raises(HTTPException) as excinfo:
        verify_refresh_token(refresh_token)

    # Assert: Verify the behavior
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid token"


@pytest.mark.auth_queries
def test_delete_refresh_token_valid(mocker):
    # Arrange: Encode a valid refresh token
    refresh_payload = {
        "sub": "test@example.com",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
        "token_type": "refresh",
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")
    # Arrange: Mock the Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.get = MagicMock(return_value=refresh_token)
    mock_redis.delete = MagicMock()
    email = "test@example.com"

    # Act: Call the function
    result = delete_refresh_token(refresh_token)

    # Assert: Verify the behavior
    assert result["message"] == "Refresh token deleted successfully"
    mock_redis.get.assert_called_once_with(f"refresh_token:{email}")
    mock_redis.delete.assert_called_once_with(f"refresh_token:{email}")


@pytest.mark.auth_queries
def test_delete_refresh_token_expired(mocker):
    # Arrange: Encode a valid refresh token
    refresh_payload = {
        "sub": "test@example.com",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=10),
        "token_type": "refresh",
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")
    # Arrange: Mock the Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.get = MagicMock(return_value=refresh_token)
    mock_redis.delete = MagicMock()
    email = "test@example.com"

    # Act: Call the function
    with pytest.raises(HTTPException) as excinfo:
        delete_refresh_token(refresh_token)

    # Assert: Verify the behavior
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Token has expired"


@pytest.mark.auth_queries
def test_delete_refresh_token_invalid(mocker):
    # Arrange: Encode a valid refresh token
    refresh_payload = {
        "sub": "test@example.com",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
        "token_type": "refresh",
    }
    refresh_token = jwt.encode(refresh_payload, "123456789", algorithm="HS256")
    # Arrange: Mock the Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.get = MagicMock(return_value=refresh_token)
    email = "test@example.com"

    # Act: Call the function
    with pytest.raises(HTTPException) as excinfo:
        verify_refresh_token(refresh_token)

    # Assert: Verify the behavior
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid token"


import pytest
from unittest.mock import MagicMock
from app.auth.auth_queries import validate_token
from fastapi import HTTPException
from datetime import datetime, timedelta
import jwt
from app.config import SECRET_KEY


@pytest.mark.auth_queries
def test_validate_token_valid(mocker):
    # Arrange: Create a valid token
    payload = {
        "sub": "test@example.com",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
        "token_type": "access",
    }
    valid_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    authorization = f"Bearer {valid_token}"

    # Act: Call the function
    result = validate_token(authorization, "access")

    # Assert: Verify the behavior
    assert result == valid_token


@pytest.mark.auth_queries
def test_validate_token_invalid_header():
    # Arrange: Invalid Authorization header
    authorization = "InvalidHeader token"

    # Act & Assert: Expect an exception
    with pytest.raises(HTTPException) as excinfo:
        validate_token(authorization, "access")

    # Assert: Verify the exception details
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid Authorization header"


@pytest.mark.auth_queries
def test_validate_token_expired():
    # Arrange: Create an expired token
    payload = {
        "sub": "test@example.com",
        "exp": datetime.now(timezone.utc)
        - timedelta(minutes=10),  # Expired 10 minutes ago
        "token_type": "access",
    }
    expired_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    authorization = f"Bearer {expired_token}"

    # Act & Assert: Expect an exception
    with pytest.raises(HTTPException) as excinfo:
        validate_token(authorization, "access")

    # Assert: Verify the exception details
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Token has expired"


@pytest.mark.auth_queries
def test_validate_token_invalid_token():
    # Arrange: Malformed token
    authorization = "Bearer invalid.token.here"

    # Act & Assert: Expect an exception
    with pytest.raises(HTTPException) as excinfo:
        validate_token(authorization, "access")

    # Assert: Verify the exception details
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid token"


@pytest.mark.auth_queries
def test_validate_token_wrong_type():
    # Arrange: Create a token with the wrong type
    payload = {
        "sub": "test@example.com",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
        "token_type": "refresh",  # Wrong type
    }
    wrong_type_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    authorization = f"Bearer {wrong_type_token}"

    # Act & Assert: Expect an exception
    with pytest.raises(HTTPException) as excinfo:
        validate_token(authorization, "access")  # Expected type is "access"

    # Assert: Verify the exception details
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid token type"

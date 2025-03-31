import pytest
from unittest.mock import MagicMock
from app.auth.auth_queries import generate_auth_code, verify_auth_code
from fastapi import HTTPException


def test_generate_auth_code(mocker):
    # Mock Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.setex = MagicMock()

    # Call the function
    email = "test@example.com"
    auth_code = generate_auth_code(email)

    # Assertions
    assert len(auth_code) == 6
    assert auth_code.isdigit()
    mock_redis.setex.assert_called_once_with(
        f"auth_code:{email}", mocker.ANY, auth_code
    )


def test_verify_auth_code_valid(mocker):
    # Mock Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.get = MagicMock(return_value="123456")
    mock_redis.delete = MagicMock()

    # Call the function
    email = "test@example.com"
    auth_code = "123456"
    result = verify_auth_code(email, auth_code)

    # Assertions
    assert "access_token" in result
    assert "refresh_token" in result
    mock_redis.get.assert_called_once_with(f"auth_code:{email}")
    mock_redis.delete.assert_called_once_with(f"auth_code:{email}")


def test_verify_auth_code_invalid(mocker):
    # Mock Redis client
    mock_redis = mocker.patch("app.auth.auth_queries.redis_client")
    mock_redis.get = MagicMock(return_value=None)

    # Call the function and expect an exception
    email = "test@example.com"
    auth_code = "123456"
    with pytest.raises(HTTPException) as excinfo:
        verify_auth_code(email, auth_code)

    # Assertions
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Invalid or expired code"
    mock_redis.get.assert_called_once_with(f"auth_code:{email}")

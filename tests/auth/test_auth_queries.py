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

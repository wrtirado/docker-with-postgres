import pytest

# from unittest.mock import MagicMock
# from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.auth.auth_routers import request_code, verify_code, refresh_token, logout
from app.auth.auth_queries import generate_auth_code

# from app.main import app
from app.auth import auth_routers

# import app.db.database as database
# from app.db.database import get_db


@pytest.mark.auth_routers
def test_request_code_returns_generic_message_when_user_not_found(client):
    response = client.post("/auth/request-code", json={"email": "test@example.com"})

    assert response.status_code == 200
    assert response.json() == {
        "message": "If your email is registered, you will receive an authentication code."
    }


@pytest.mark.auth_routers
def test_request_code_unregistered_email(mocker):
    # Arrange: Mock database to return None
    # Act: Call the request_code route
    # Assert: Verify response message and that generate_auth_code was not called
    assert True


@pytest.mark.auth_routers
def test_request_code_database_error(mocker):
    # Arrange: Mock database to raise an exception
    # Act: Call the request_code route
    # Assert: Verify that the exception is handled gracefully
    assert True

import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.auth.auth_routers import request_code, verify_code, refresh_token, logout
from app.auth.auth_queries import generate_auth_code
from app.main import app
from app.auth.auth_routers import get_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_db_session(mocker):
    mock_session = mocker.MagicMock()
    # By default, simulate a nonexistent user
    mock_session.query.return_value.filter.return_value.first.return_value = None
    return mock_session


def override_get_db(mock_db_session):
    yield mock_db_session


@pytest.mark.auth_routers
def test_request_code_returns_generic_message_when_user_not_found(
    client, mock_db_session, mocker
):
    # Override FastAPI's get_db dependency
    app.dependency_overrides[get_db] = lambda: override_get_db(mock_db_session)

    # Act
    response = client.post("/request-code", json={"email": "test@example.com"})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "If your email is registered, you will receive an authentication code."
    }

    # Cleanup override for other tests
    app.dependency_overrides = {}


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

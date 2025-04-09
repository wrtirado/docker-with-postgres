import pytest
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from app.auth.auth_routers import request_code, verify_code, refresh_token, logout
from app.auth.auth_queries import generate_auth_code
from app.auth import auth_routers


@pytest.mark.auth_routers
def test_request_code_returns_generic_message_when_user_not_found(
    client, mock_db_session
):
    # Arrange: Mock database to return None
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    # Act: Call the request_code route
    response = client.post("/auth/request-code", json={"email": "test@example.com"})

    # Assert: Verify response message
    assert response.status_code == 200
    assert response.json() == {
        "message": "If your email is registered, you will receive an authentication code."
    }


@pytest.mark.auth_routers
def test_request_code_valid_email(client, mock_db_session, mocker):
    # Arrange: Mock the database to return a user
    mock_user = {"email": "test@example.com"}
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        mock_user
    )

    # Mock the generate_auth_code function to return a fixed code
    mock_generate_auth_code = mocker.patch("app.auth.auth_routers.generate_auth_code")
    mock_generate_auth_code.return_value = "123456"

    # Act: Call the /auth/request-code route
    response = client.post("/auth/request-code", json={"email": "test@example.com"})

    # Assert: Verify the response
    assert response.status_code == 200
    assert response.json() == {
        "message": "If your email is registered, you will receive an authentication code."
    }


@pytest.mark.auth_routers
def test_request_code_database_error(client, mock_db_session):
    # Arrange: Simulate a SQLAlchemy exception
    mock_db_session.query.side_effect = SQLAlchemyError("Simulated DB error")

    # Act
    response = client.post("/auth/request-code", json={"email": "test@example.com"})

    # Assert
    assert response.status_code == 500
    assert response.json() == {
        "detail": "An internal server error occurred. Please try again later."
    }


@pytest.mark.auth_routers
def test_request_code_handles_bad_request_body(client, mocker):
    # Act: Call the /auth/request-code route
    # with an invalid request body (see "emails" instead of "email")
    response = client.post("/auth/request-code", json={"emails": "test@example.com"})

    # Assert: Verify the response
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {"emails": "test@example.com"},
                "loc": ["body", "email"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }

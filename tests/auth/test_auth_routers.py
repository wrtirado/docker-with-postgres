import pytest
from fastapi import HTTPException
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


@pytest.mark.auth_routers
def test_verify_code_missing_fields(client):
    # Act: Call the /auth/verify-code route with an empty body
    response = client.post("/auth/verify-code", json={})

    # Assert: Verify the response
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "email"],
                "msg": "Field required",
                "type": "missing",
            },
            {
                "input": {},
                "loc": ["body", "auth_code"],
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }


@pytest.mark.auth_routers
def test_verify_code_invalid_email_format(client):
    # Act: Call the /auth/verify-code route with an invalid email
    response = client.post(
        "/auth/verify-code", json={"email": "invalid-email", "auth_code": "123456"}
    )

    # Assert: Verify the response
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "email"],
                "msg": "value is not a valid email address: An email address must have an @-sign.",
                "type": "value_error",
                "input": "invalid-email",
                "ctx": {"reason": "An email address must have an @-sign."},
            }
        ]
    }


@pytest.mark.auth_routers
def test_verify_code_valid_request(client, mocker):
    # Arrange: Mock the verify_auth_code function
    mock_verify_auth_code = mocker.patch("app.auth.auth_routers.verify_auth_code")
    mock_verify_auth_code.return_value = {
        "access_token": "access123",
        "refresh_token": "refresh123",
        "token_type": "bearer",
    }

    # Act: Call the /auth/verify-code route
    response = client.post(
        "/auth/verify-code", json={"email": "test@example.com", "auth_code": "123456"}
    )

    # Assert: Verify the response
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "access123",
        "refresh_token": "refresh123",
        "token_type": "bearer",
    }
    mock_verify_auth_code.assert_called_once_with("test@example.com", "123456")


@pytest.mark.auth_routers
def test_verify_code_invalid_code(client, mocker):
    # Arrange: Mock the verify_auth_code function to raise an exception
    mock_verify_auth_code = mocker.patch("app.auth.auth_routers.verify_auth_code")
    mock_verify_auth_code.side_effect = HTTPException(
        status_code=400, detail="Invalid or expired code"
    )

    # Act: Call the /auth/verify-code route
    response = client.post(
        "/auth/verify-code", json={"email": "test@example.com", "auth_code": "123456"}
    )

    # Assert: Verify the response
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid or expired code"}
    mock_verify_auth_code.assert_called_once_with("test@example.com", "123456")


@pytest.mark.auth_routers
def test_refresh_token_missing_authorization_header(client):
    # Act: Call the /auth/refresh-token route without an authorization header
    response = client.post("/auth/refresh-token")

    # Assert: Verify the response
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.auth_routers
def test_refresh_token_invalid_token(client, mocker):
    # Arrange: Mock the validate_token function to raise an exception
    mock_validate_token = mocker.patch("app.auth.auth_routers.validate_token")
    mock_validate_token.side_effect = HTTPException(
        status_code=401, detail="Invalid token"
    )

    # Act: Call the /auth/refresh-token route with an invalid token
    response = client.post(
        "/auth/refresh-token",
        headers={"Authorization": "Bearer invalid-token"},
    )

    # Assert: Verify the response
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
    mock_validate_token.assert_called_once_with("invalid-token", "refresh")


@pytest.mark.auth_routers
def test_refresh_token_expired_token(client, mocker):
    # Arrange: Mock the validate_token function to raise an exception for an expired token
    mock_validate_token = mocker.patch("app.auth.auth_routers.validate_token")
    mock_validate_token.side_effect = HTTPException(
        status_code=401, detail="Token has expired"
    )

    # Act: Call the /auth/refresh-token route with an expired token
    response = client.post(
        "/auth/refresh-token",
        headers={"Authorization": "Bearer expired-token"},
    )

    # Assert: Verify the response
    assert response.status_code == 401
    assert response.json() == {"detail": "Token has expired"}
    mock_validate_token.assert_called_once_with("expired-token", "refresh")


@pytest.mark.auth_routers
def test_refresh_token_success(client, mocker):
    # Arrange: Mock the validate_token and verify_refresh_token functions
    mock_validate_token = mocker.patch("app.auth.auth_routers.validate_token")
    mock_validate_token.return_value = "valid-refresh-token"

    mock_verify_refresh_token = mocker.patch(
        "app.auth.auth_routers.verify_refresh_token"
    )
    mock_verify_refresh_token.return_value = {
        "access_token": "new-access-token",
        "token_type": "bearer",
    }

    # Act: Call the /auth/refresh-token route with a valid token
    response = client.post(
        "/auth/refresh-token",
        headers={"Authorization": "Bearer valid-refresh-token"},
    )

    # Assert: Verify the response
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "new-access-token",
        "token_type": "bearer",
    }
    mock_validate_token.assert_called_once_with("valid-refresh-token", "refresh")
    mock_verify_refresh_token.assert_called_once_with("valid-refresh-token")

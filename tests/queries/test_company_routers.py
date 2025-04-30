import pytest
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import MagicMock
from uuid import uuid4


@pytest.mark.company_routers
def test_create_company(client, mock_db_session):

    # Define the request payload
    payload = {
        "name": "Test Company",
    }

    # Call the endpoint
    response = client.post("/companies/", json=payload)

    # Assertions
    assert response.status_code == 200
    assert response.json()["name"] == "Test Company"
    assert "id" in response.json()
    assert "created_at" in response.json()
    assert "name" in response.json()


@pytest.mark.company_routers
def test_create_company_invalid_data(client, mock_db_session):
    # Define the request payload with invalid data
    payload = {
        "name": 2,  # Invalid name
    }

    # Call the endpoint
    response = client.post("/companies/", json=payload)

    # Assertions
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": 2,
                "loc": ["body", "name"],
                "msg": "Input should be a valid string",
                "type": "string_type",
            }
        ]
    }


@pytest.mark.company_routers
def test_read_company(client, mock_db_session):
    # Arrange: Mock the database to return a valid Company object
    mock_company = MagicMock()
    mock_company.id = str(uuid4())  # UUID as a string
    mock_company.name = "Test Company"  # Valid string
    mock_company.created_at = "2025-04-29T12:00:00+00:00"  # Valid ISO 8601 string

    # Mock the query to return the mocked company
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        mock_company
    )

    # Act: Call the endpoint to read the company
    response = client.get(f"/companies/{mock_company.id}")

    # Assertions
    assert response.status_code == 200
    assert response.json()["name"] == "Test Company"
    assert response.json()["id"] == mock_company.id
    assert response.json()["created_at"] == mock_company.created_at


@pytest.mark.company_routers
def test_read_company_not_found(client, mock_db_session):
    # Arrange: Mock the database to return None for a non-existent company
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    # Act: Call the endpoint to read a non-existent company
    response = client.get(f"/companies/{str(uuid4())}")

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "Company not found"}

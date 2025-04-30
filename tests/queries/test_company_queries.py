import pytest
from unittest.mock import MagicMock
from app.queries.company_queries import create_company, get_company_by_id


@pytest.mark.company_queries
def test_create_company_success():
    # Mock the database session
    db = MagicMock()
    company_in = MagicMock()
    company_in.name = "Test Company"

    # Call the function
    result = create_company(db, company_in)

    # Assertions
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
    assert result.name == "Test Company"
    assert isinstance(result.created_at, str)


@pytest.mark.company_queries
def test_create_company_failure():
    # Mock the database session
    db = MagicMock()
    company_in = MagicMock()
    company_in.name = "Test Company"

    # Simulate a database error
    db.commit.side_effect = Exception("Database error")

    # Call the function and check for exception
    with pytest.raises(Exception):
        create_company(db, company_in)


@pytest.mark.company_queries
def test_get_company_by_id_success():
    # Mock the database session
    db = MagicMock()
    company_id = "12345"
    mock_company = MagicMock()
    db.query().filter().first.return_value = mock_company

    # Call the function
    result = get_company_by_id(db, company_id)

    # Assertions
    db.query().filter().first.assert_called_once()
    assert result == mock_company


@pytest.mark.company_queries
def test_get_company_by_id_not_found():
    # Mock the database session
    db = MagicMock()
    company_id = "12345"
    db.query().filter().first.return_value = None

    # Call the function
    result = get_company_by_id(db, company_id)

    # Assertions
    db.query().filter().first.assert_called_once()
    assert result is None

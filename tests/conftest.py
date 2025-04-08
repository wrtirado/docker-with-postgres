import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.db.database import get_db


# This runs once per testing session and sets the testing environment variable
@pytest.fixture(scope="session", autouse=True)
def set_testing_env():
    os.environ["TESTING_SUITE_ACTIVE"] = "true"


# Shared TestClient instance
@pytest.fixture
def client():
    return TestClient(app)


# Provides a fake DB session for tests
@pytest.fixture
def mock_db_session(mocker):
    return mocker.MagicMock()


# Automatically override the DB dependency for all tests that request 'client' + 'mock_db_session'
@pytest.fixture(autouse=True)
def override_get_db(mock_db_session):
    def _override():
        yield mock_db_session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()

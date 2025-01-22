"""Unit test fixtures for the Flask app"""

from unittest.mock import MagicMock
import pytest
import sqlalchemy
from flask.testing import FlaskClient
from backend.src.app import create_app
from backend.src.utils.helpers import metrics_logger

app = create_app()


@pytest.fixture(name="client")
def flask_client() -> FlaskClient:
    """Fixture to create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def mock_metrics_logger():
    """Fixture to mock the MetricsLogger"""
    metrics_logger.incr = MagicMock()
    metrics_logger.decr = MagicMock()
    metrics_logger.log_execution_time = MagicMock()
    metrics_logger.log_calculated_route_for_user = MagicMock()
    metrics_logger.incr_by_float = MagicMock()


@pytest.fixture(autouse=True)
def mock_db_session(mocker):
    """Fixture to mock the database session"""
    mock_session = MagicMock()

    # Simulate storing objects in the session
    db_store = {}

    def mock_add(obj):
        # Assign a mock ID and store the object
        if not hasattr(obj, "id"):
            obj.id = len(db_store) + 1  # Mock ID generation
        db_store[obj.id] = obj

    def mock_refresh(obj):
        # Ensure the object exists in the mock store
        if obj.id not in db_store:
            raise sqlalchemy.exc.InvalidRequestError(
                "Instance is not persistent within this Session"
            )
        for key, value in db_store[obj.id].__dict__.items():
            setattr(obj, key, value)

    mock_session.add.side_effect = mock_add
    mock_session.refresh.side_effect = mock_refresh
    mock_session.commit = MagicMock()

    # Patch `get_db_session` to return the mock session
    mocker.patch("backend.src.database.db_connection.get_db_session", return_value=mock_session)

    return mock_session

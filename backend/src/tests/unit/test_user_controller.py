"""
Tests for the user controller.
"""

from unittest.mock import patch, MagicMock
import pytest
from flask import Flask

from backend.src.web_backend.controller.user_controller import init_user_routes


@pytest.fixture
def client():
    """
    Fixture to create a test client for the Flask app.
    """
    app = Flask(__name__)
    init_user_routes(app)
    with app.test_client() as client:  # pylint: disable=redefined-outer-name
        yield client


@patch("backend.src.web_backend.controller.user_controller.UserDao")
@patch("backend.src.web_backend.controller.user_controller.get_db_session")
def test_register_user_success(
    mock_get_db_session, mock_user_dao, client
):  # pylint: disable=redefined-outer-name
    """
    Test registering a new user successfully.
    """
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_user_dao.user_exists_by_username.return_value = False

    def mock_save_user(user, session):  # pylint: disable=unused-argument
        user.id = 1
        return user

    mock_user_dao.save_user.side_effect = mock_save_user

    response = client.post("/auth/register", json={"username": "testuser"})
    assert response.status_code == 201
    assert response.json == {
        "message": "User testuser registered successfully.",
        "user": {"username": "testuser", "id": 1},
    }
    mock_user_dao.save_user.assert_called_once()


@patch("backend.src.web_backend.controller.user_controller.UserDao")
@patch("backend.src.web_backend.controller.user_controller.get_db_session")
def test_register_user_missing_username(
    mock_get_db_session,  # pylint: disable=unused-argument
    mock_user_dao,
    client,  # pylint: disable=redefined-outer-name
):
    """
    Test registering a new user without a username.
    """
    response = client.post("/auth/register", json={})
    assert response.status_code == 400
    assert response.json == {"error": "Username is required"}
    mock_user_dao.save_user.assert_not_called()

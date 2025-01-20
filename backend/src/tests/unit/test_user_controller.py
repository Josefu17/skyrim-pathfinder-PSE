"""Tests for user_controller.py"""

from unittest.mock import patch, MagicMock
import pytest
from flask import Flask
from backend.src.web_backend.controller.user_controller import init_user_routes


@pytest.fixture
def app():
    """Create a test Flask application."""
    app = Flask(__name__)
    init_user_routes(app)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@patch("backend.src.web_backend.controller.user_controller.get_db_session")
@patch("backend.src.web_backend.controller.user_controller.UserDao")
def test_register_user_success(mock_user_dao, mock_get_db_session, client):
    """Test the register user endpoint."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_user_dao.user_exists_by_username.return_value = False
    mock_user_dao.save_user.return_value = None

    response = client.post("/auth/register", json={"username": "testuser"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User testuser registered successfully."
    assert data["user"]["username"] == "testuser"


@patch("backend.src.web_backend.controller.user_controller.get_db_session")
@patch("backend.src.web_backend.controller.user_controller.UserDao")
def test_register_user_existing_username(mock_user_dao, mock_get_db_session, client):
    """Test the register user endpoint with an existing username."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_user_dao.user_exists_by_username.return_value = True

    response = client.post("/auth/register", json={"username": "testuser"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Username already exists"


@patch("backend.src.web_backend.controller.user_controller.get_db_session")
@patch("backend.src.web_backend.controller.user_controller.UserDao")
def test_register_user_missing_username(_, __, client):
    """Test the register user endpoint with a missing username."""
    response = client.post("/auth/register", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Username is required"


@patch("backend.src.web_backend.controller.user_controller.get_db_session")
@patch("backend.src.web_backend.controller.user_controller.UserDao")
def test_login_user_success(mock_user_dao, mock_get_db_session, client):
    """Test the login user endpoint."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_user_dao.get_user_by_username.return_value = MagicMock(id=1, username="testuser")

    response = client.post("/auth/login", json={"username": "testuser"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User testuser logged in successfully."
    assert data["user"]["username"] == "testuser"


@patch("backend.src.web_backend.controller.user_controller.get_db_session")
@patch("backend.src.web_backend.controller.user_controller.UserDao")
def test_login_user_non_existing_user(mock_user_dao, mock_get_db_session, client):
    """Test the login user endpoint with a non-existing user."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_user_dao.get_user_by_username.return_value = None

    response = client.post("/auth/login", json={"username": "unknownuser"})
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "User not found"


@patch("backend.src.web_backend.controller.user_controller.get_db_session")
@patch("backend.src.web_backend.controller.user_controller.UserDao")
def test_login_user_missing_username(_, __, client):
    """Test the login user endpoint with a missing username."""
    response = client.post("/auth/login", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Username is required"

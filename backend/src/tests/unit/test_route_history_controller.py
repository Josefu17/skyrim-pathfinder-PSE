"""Unit tests for route history controller."""

import json
from unittest.mock import patch, MagicMock
from flask import Flask
import pytest
from backend.src.web_backend.controller.route_history_controller import init_path_routes


@pytest.fixture
def app():
    """Create a test Flask application."""
    app = Flask(__name__)
    init_path_routes(app)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
@patch(
    "backend.src.web_backend.controller.route_history_controller.fetch_route_from_navigation_service"
)
def test_calculate_route(mock_fetch_route, mock_get_db_session, client):
    """Test the calculate route endpoint."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_fetch_route.return_value = {"route": "mocked_route"}

    response = client.post("/routes", json={"startpoint": "CityA", "endpoint": "CityB"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["route"] == "mocked_route"


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
@patch("backend.src.web_backend.controller.route_history_controller.RouteDao")
def test_delete_route(mock_route_dao, mock_get_db_session, client):
    """Test the delete route endpoint"""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_route_dao.get_route_by_id.return_value = MagicMock(user_id=1)

    response = client.delete("/users/1/routes/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] == "Route deleted"


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
@patch("backend.src.web_backend.controller.route_history_controller.RouteDao")
def test_get_user_history(mock_route_dao, mock_get_db_session, client):
    """Test the get user history endpoint"""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_route_dao.get_routes.return_value = [
        MagicMock(
            id=1, startpoint="CityA", endpoint="CityB", route=json.dumps({"route": "mocked_route"})
        )
    ]

    response = client.get("/users/1/routes")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["routes"]) == 1
    assert data["routes"][0]["startpoint"] == "CityA"
    assert data["routes"][0]["endpoint"] == "CityB"


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
@patch("backend.src.web_backend.controller.route_history_controller.RouteDao")
def test_clear_user_history_by_id(mock_route_dao, mock_get_db_session, client):
    """Test the clear user history endpoint"""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_route_dao.delete_user_route_history.return_value = 1

    response = client.delete("/users/1/routes")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] == "Route history cleared"
    assert data["deleted_count"] == 1


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
def test_calculate_route_missing_startpoint(mock_get_db_session, client):
    """Test the calculate route endpoint with missing startpoint."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    response = client.post("/routes", json={"endpoint": "CityB"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Start and end cities are required"


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
def test_calculate_route_missing_endpoint(mock_get_db_session, client):
    """Test the calculate route endpoint with missing endpoint."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    response = client.post("/routes", json={"startpoint": "CityA"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Start and end cities are required"


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
@patch(
    "backend.src.web_backend.controller.route_history_controller.fetch_route_from_navigation_service"
)
def test_calculate_route_error(mock_fetch_route, mock_get_db_session, client):
    """Test the calculate route endpoint with error."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_fetch_route.return_value = {"error": "mocked_error"}

    response = client.post("/routes", json={"startpoint": "CityA", "endpoint": "CityB"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "mocked_error"


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
@patch(
    "backend.src.web_backend.controller.route_history_controller.fetch_route_from_navigation_service"
)
@patch("backend.src.web_backend.controller.route_history_controller.RouteDao")
def test_calculate_route_registered_user(
    mock_route_dao, mock_fetch_route, mock_get_db_session, client
):
    """Test the calculate route endpoint for a registered user."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_fetch_route.return_value = {"route": "mocked_route"}
    mock_saved_route = MagicMock(id=1)
    mock_route_dao.save_route.return_value = mock_saved_route

    response = client.post("/users/1/routes", json={"startpoint": "CityA", "endpoint": "CityB"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["route"] == "mocked_route"


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
@patch(
    "backend.src.web_backend.controller.route_history_controller.fetch_route_from_navigation_service"
)
def test_calculate_route_anonymous_user(mock_fetch_route, mock_get_db_session, client):
    """Test the calculate route endpoint for an anonymous user."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_fetch_route.return_value = {"route": "mocked_route"}

    response = client.post("/routes", json={"startpoint": "CityA", "endpoint": "CityB"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["route"] == "mocked_route"

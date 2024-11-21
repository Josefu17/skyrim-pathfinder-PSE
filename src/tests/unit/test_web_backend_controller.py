"""Unit tests for the web backend controller."""

from unittest.mock import patch, MagicMock

import pytest
from flask.testing import FlaskClient

from src.web_backend.web_backend_controller import app


@pytest.fixture(name="flask_client")
def flask() -> FlaskClient:
    """Fixture to create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as flask_client:
        yield flask_client


# Test for the `/maps` endpoint
@patch("src.web_backend.web_backend_controller.CityDAO")
@patch("src.web_backend.web_backend_controller.ConnectionDAO")
def test_get_map_data(mock_connection_dao, mock_city_dao, flask_client: FlaskClient):
    """Test the get_map_data endpoint."""
    # Mock CityDAO and ConnectionDAO
    mock_city_1 = MagicMock()
    mock_city_1.to_dict.return_value = {
        "id": 1,
        "name": "Markarth",
        "position_x": 100,
        "position_y": 200,
    }
    mock_city_2 = MagicMock()
    mock_city_2.to_dict.return_value = {
        "id": 2,
        "name": "Riften",
        "position_x": 300,
        "position_y": 400,
    }
    mock_city_dao.get_all_cities.return_value = [mock_city_1, mock_city_2]

    mock_connection_1 = MagicMock()
    mock_connection_1.parent_city_id = 1
    mock_connection_1.child_city_id = 2
    mock_connection_dao.get_all_connections.return_value = [mock_connection_1]

    response = flask_client.get("/maps")
    assert response.status_code == 200
    data = response.get_json()
    assert "cities" in data and len(data["cities"]) > 0
    assert "connections" in data and len(data["connections"]) > 0


# Test for the `/cities` endpoint
@patch("src.web_backend.web_backend_controller.CityDAO")
def test_get_cities(mock_city_dao, flask_client: FlaskClient):
    """Test the get_cities endpoint."""
    # Create mock city objects
    mock_city_1 = MagicMock()
    mock_city_1.to_dict.return_value = {
        "name": "Markarth",
        "position_x": 100,
        "position_y": 200,
    }

    mock_city_2 = MagicMock()
    mock_city_2.to_dict.return_value = {
        "name": "Riften",
        "position_x": 300,
        "position_y": 400,
    }

    mock_city_dao.get_all_cities.return_value = [mock_city_1, mock_city_2]

    response = flask_client.get("/cities")
    assert response.status_code == 200
    data = response.get_json()
    assert "cities" in data and len(data["cities"]) > 0
    assert data["cities"][0]["name"] == "Markarth"
    assert data["cities"][1]["name"] == "Riften"


# Test for the `/cities/route` endpoint
@patch("src.web_backend.web_backend_controller.fetch_route_from_navigation_service")
def test_calculate_route(mock_fetch_route, flask_client: FlaskClient):
    """Test the calculate_route endpoint."""
    # Mock fetch_route_from_navigation_service response
    mock_fetch_route.return_value = {
        "route": {"0": "Markarth", "1": "Riften"},
        "distance": 321.12,
    }

    response = flask_client.get(
        "/cities/route", query_string={"startpoint": "Markarth", "endpoint": "Riften"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "route" in data and "distance" in data
    assert data["distance"] == 321.12

"""Unit tests for the web backend controller."""

from unittest.mock import patch, MagicMock

import pytest
from flask.testing import FlaskClient

from backend.src.web_backend.web_backend_controller import app


@pytest.fixture(name="flask_client")
def flask() -> FlaskClient:
    """Fixture to create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as flask_client:
        yield flask_client


# Test for the `/maps` endpoint
@patch("backend.src.web_backend.web_backend_controller.get_db_session")
@patch("backend.src.web_backend.web_backend_controller.service_get_map_data")
def test_get_map_data(
    mock_service_get_map_data, mock_get_db_session, flask_client: FlaskClient
):
    """Test the get_map_data endpoint."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service_get_map_data to return mock cities and connections data
    mock_service_get_map_data.return_value = (
        [
            {
                "id": 1,
                "name": "Markarth",
                "position_x": 100,
                "position_y": 200,
            },
            {
                "id": 2,
                "name": "Riften",
                "position_x": 300,
                "position_y": 400,
            },
        ],
        [
            {
                "parent_city_id": 1,
                "child_city_id": 2,
            }
        ],
    )

    response = flask_client.get("/maps")
    assert response.status_code == 200
    data = response.get_json()
    assert "cities" in data and len(data["cities"]) > 0
    assert "connections" in data and len(data["connections"]) > 0


# Test for the `/cities` endpoint
@patch("backend.src.web_backend.web_backend_controller.get_db_session")
@patch("backend.src.web_backend.web_backend_controller.service_get_cities_data")
def test_get_cities(
    mock_service_get_cities_data, mock_get_db_session, flask_client: FlaskClient
):
    """Test the get_cities endpoint."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service_get_cities_data to return mock cities data
    mock_service_get_cities_data.return_value = [
        {
            "name": "Markarth",
            "position_x": 100,
            "position_y": 200,
        },
        {
            "name": "Riften",
            "position_x": 300,
            "position_y": 400,
        },
    ]

    response = flask_client.get("/cities")
    assert response.status_code == 200
    data = response.get_json()
    assert "cities" in data and len(data["cities"]) > 0
    assert data["cities"][0]["name"] == "Markarth"
    assert data["cities"][1]["name"] == "Riften"


# Test for the `/cities/route` endpoint
@patch("backend.src.web_backend.web_backend_controller.get_db_session")
@patch(
    "backend.src.web_backend.web_backend_controller.fetch_route_from_navigation_service"
)
def test_calculate_route(
    mock_fetch_route, mock_get_db_session, flask_client: FlaskClient
):
    """Test the calculate_route endpoint."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

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

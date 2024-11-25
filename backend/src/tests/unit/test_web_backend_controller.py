"""Unit tests for the web backend controller."""

from unittest.mock import patch, MagicMock

import pytest
from flask.testing import FlaskClient

from backend.src.web_backend.web_backend_controller import app
from backend.src.web_backend.web_backend_controller import main


@pytest.fixture(name="client")
def flask() -> FlaskClient:
    """Fixture to create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Test for the `/maps` endpoint
@patch("backend.src.web_backend.web_backend_controller.get_db_session")
@patch("backend.src.web_backend.web_backend_controller.service_get_map_data")
def test_get_map_data(
    mock_service_get_map_data, mock_get_db_session, client: FlaskClient
):
    """Test the get_map_data endpoint."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service data
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

    # Call endpoint
    response = client.get("/maps")

    # Assert response
    assert response.status_code == 200
    data = response.get_json()
    assert "cities" in data and len(data["cities"]) > 0
    assert "connections" in data and len(data["connections"]) > 0


# Test for the `/cities` endpoint
@patch("backend.src.web_backend.web_backend_controller.get_db_session")
@patch("backend.src.web_backend.web_backend_controller.service_get_cities_data")
def test_get_cities(
    mock_service_get_cities_data, mock_get_db_session, client: FlaskClient
):
    """Test the get_cities endpoint."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service data
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

    # Call endpoint
    response = client.get("/cities")

    # Assert response
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
def test_calculate_route(mock_fetch_route, mock_get_db_session, client: FlaskClient):
    """Test the calculate_route endpoint."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service data
    mock_fetch_route.return_value = {
        "route": {"0": "Markarth", "1": "Riften"},
        "distance": 321.12,
    }

    # Call endpoint
    response = client.get("/cities/route?startpoint=Markarth&endpoint=Riften")

    # Assert response
    assert response.status_code == 200
    data = response.get_json()
    assert "route" in data and "distance" in data
    assert data["distance"] == 321.12
    assert response.json == {
        "route": {"0": "Markarth", "1": "Riften"},
        "distance": 321.12,
    }


@patch(
    "backend.src.web_backend.web_backend_controller.fetch_route_from_navigation_service"
)
@patch("backend.src.web_backend.web_backend_controller.get_db_session")
def test_calculate_route_service_error(
    mock_get_db_session, mock_fetch_route_from_navigation_service, client
):
    """Test error response when service fails."""
    # Mock database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service response
    mock_fetch_route_from_navigation_service.return_value = {"error": "Some error"}

    # Call endpoint
    response = client.get("/cities/route?startpoint=CityA&endpoint=CityB")

    # Assert response
    assert response.status_code == 400
    assert response.json == {"error": "Some error"}


def test_calculate_route_missing_params(client):
    """Test error response for missing query parameters."""
    response = client.get("/cities/route")
    assert response.status_code == 400
    assert response.json == {"error": "Start and end cities are required"}


@patch(
    "backend.src.web_backend.web_backend_controller.fetch_and_store_map_data_if_needed"
)
@patch("backend.src.web_backend.web_backend_controller.get_db_session")
@patch("backend.src.web_backend.web_backend_controller.app.run")
def test_main_script(mock_app_run, mock_get_db_session, mock_fetch_and_store_map_data):
    """Test the main script block."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    main()

    # Assertions
    mock_fetch_and_store_map_data.assert_called_once_with(session=mock_session)
    mock_app_run.assert_called_once_with(debug=True, host="0.0.0.0", port=4243)

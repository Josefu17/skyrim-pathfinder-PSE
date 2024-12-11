"""Unit tests for the route_history_controller module."""

import math
from unittest.mock import patch, MagicMock

from flask.testing import FlaskClient


# Test for the `/cities/route` endpoint
@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
@patch(
    "backend.src.web_backend.controller.route_history_controller"
    ".fetch_route_from_navigation_service"
)
def test_calculate_route(
    mock_fetch_route,
    mock_get_db_session,
    client: FlaskClient,
):
    """Test the calculate_route endpoint."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service data
    mock_fetch_route.return_value = {
        "route": {
            "0": "Markarth",
            "1": "Rorikstead",
            "2": "Whiterun",
            "3": "Ivarstead",
            "4": "Riften",
        },
        "distance": 2343.5,
        "alternative_route": {
            "0": "Markarth",
            "1": "Falkreath",
            "2": "Helgen",
            "3": "Ivarstead",
            "4": "Riften",
        },
        "alternative_distance": 2376.27,
    }

    # Call endpoint
    response = client.post(
        "/cities/route",
        json={"startpoint": "Markarth", "endpoint": "Riften", "user_id": 1},
    )

    # Assert response
    assert response.status_code == 201
    data = response.get_json()
    assert "route" in data and "distance" in data
    assert "alternative_route" in data and "alternative_distance" in data
    assert math.isclose(data["distance"], 2343.5, rel_tol=1e-9)
    assert math.isclose(data["alternative_distance"], 2376.27, rel_tol=1e-9)
    assert data == {
        "route": {
            "0": "Markarth",
            "1": "Rorikstead",
            "2": "Whiterun",
            "3": "Ivarstead",
            "4": "Riften",
        },
        "distance": 2343.5,
        "alternative_route": {
            "0": "Markarth",
            "1": "Falkreath",
            "2": "Helgen",
            "3": "Ivarstead",
            "4": "Riften",
        },
        "alternative_distance": 2376.27,
    }


@patch(
    "backend.src.web_backend.controller.route_history_controller."
    "fetch_route_from_navigation_service"
)
@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
def test_calculate_route_service_error(
    mock_get_db_session,
    mock_fetch_route_from_navigation_service,
    client,
):
    """Test error response when service fails."""
    # Mock database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service response
    mock_fetch_route_from_navigation_service.return_value = {"error": "Some error"}

    # Call endpoint
    response = client.post(
        "/cities/route", json={"startpoint": "CityA", "endpoint": "CityB", "user_id": 1}
    )

    # Assert response
    assert response.status_code == 400
    assert response.json == {"error": "Some error"}


def test_calculate_route_missing_params(client):
    """Test error response for missing query parameters."""
    response = client.post("/cities/route", json={})
    assert response.status_code == 400
    assert response.json == {"error": "Start and end cities are required"}


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
def test_delete_route_success(mock_get_db_session, client):
    """Test the delete_route endpoint."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock the RouteDao.get_route_by_id method
    mock_route = MagicMock()
    mock_route.user_id = 1
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        mock_route
    )

    response = client.delete(
        "/cities/route/delete", query_string={"user_id": 1, "route_id": 1}
    )
    assert response.status_code == 200
    assert response.json == {"success": "Route deleted"}


def test_delete_route_missing_params(client):
    """Test error response for missing query parameters."""
    response = client.delete("/cities/route/delete", query_string={})
    assert response.status_code == 400
    assert response.json == {"error": "user_id and route_id are required"}


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
def test_delete_route_not_found(mock_get_db_session, client):
    """Test error response for route not found."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock the RouteDao.get_route_by_id method
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    response = client.delete(
        "/cities/route/delete", query_string={"user_id": 1, "route_id": 1}
    )
    assert response.status_code == 404
    assert response.json == {"error": "Route not found"}


@patch("backend.src.web_backend.controller.route_history_controller.get_db_session")
def test_delete_route_wrong_user(mock_get_db_session, client):
    """Test error response for route not belonging to user."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock the RouteDao.get_route_by_id method
    mock_route = MagicMock()
    mock_route.user_id = 2
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        mock_route
    )

    response = client.delete(
        "/cities/route/delete", query_string={"user_id": 1, "route_id": 1}
    )
    assert response.status_code == 404
    assert response.json == {"error": "Route not found"}

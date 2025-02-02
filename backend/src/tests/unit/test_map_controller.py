"""Unit tests for the web backend controller."""

from unittest.mock import patch, MagicMock

from flask.testing import FlaskClient
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

from backend.src.app import main


@patch("backend.src.web_backend.controller.map_controller.get_db_session")
@patch("backend.src.web_backend.controller.map_controller.service_get_map_data_by_name")
def test_get_maps_with_name(
    mock_service_get_map_data_by_name,
    mock_get_db_session,
    client: FlaskClient,
):
    """Test the get_maps endpoint with a map name."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service data
    mock_service_get_map_data_by_name.return_value = (
        {"name": "Skyrim"},
        [{"name": "Whiterun"}, {"name": "Solitude"}],
        [{"connection": "Whiterun-Solitude"}],
    )

    # Call endpoint
    response = client.get("/maps?name=Skyrim")

    # Assert response
    assert response.status_code == 200
    data = response.get_json()
    assert "map" in data and data["map"]["name"] == "Skyrim"
    assert "cities" in data and len(data["cities"]) > 0
    assert data["cities"][0]["name"] == "Whiterun"
    assert data["cities"][1]["name"] == "Solitude"
    assert "connections" in data and len(data["connections"]) > 0
    assert data["connections"][0]["connection"] == "Whiterun-Solitude"


@patch("backend.src.web_backend.controller.map_controller.get_db_session")
@patch("backend.src.web_backend.controller.map_controller.service_get_maps")
def test_get_maps_without_name(mock_get_maps_from_service, mock_get_db_session, client: FlaskClient):
    """Test the get_maps endpoint without a map name."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service data
    mock_get_maps_from_service.return_value = ["Skyrim", "germany"]

    # Call endpoint
    response = client.get("/maps")

    # Assert response
    assert response.status_code == 200
    data = response.get_json()
    assert "maps" in data and len(data["maps"]) > 0
    assert data["maps"][0] == "Skyrim"
    assert data["maps"][1] == "germany"


# Test for the `/cities` endpoint
@patch("backend.src.web_backend.controller.map_controller.get_db_session")
@patch("backend.src.web_backend.controller.map_controller.service_get_cities_data")
def test_get_cities(mock_service_get_cities_data, mock_get_db_session, client: FlaskClient):
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
    # TODO (Arian) fix the route path to pass the map data, e.g. GET /cities/{map_id} or GET /maps/cities?
    response = client.get("/cities?map_id=10")

    # Assert response
    assert response.status_code == 200
    data = response.get_json()
    assert "cities" in data and len(data["cities"]) > 0
    assert data["cities"][0]["name"] == "Markarth"
    assert data["cities"][1]["name"] == "Riften"


@patch("backend.src.app.fetch_and_store_map_data_if_needed")
@patch("backend.src.app.get_db_session")
@patch("backend.src.app.create_app")
def test_main_script(mock_create_app, mock_get_db_session, mock_fetch_and_store_map_data):
    """Test the main script block."""
    mock_app = MagicMock()
    mock_create_app.return_value = mock_app
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    main()

    # Assertions
    mock_fetch_and_store_map_data.assert_called_once_with(session=mock_session)
    mock_app.run.assert_called_once_with(debug=True, host="0.0.0.0", port=4243)


@patch("backend.src.web_backend.controller.map_controller.get_db_session")
@patch("backend.src.web_backend.controller.map_controller.service_get_cities_data")
def test_get_cities_sqlalchemy_error(
    mock_service_get_cities_data, mock_get_db_session, client: FlaskClient
):
    """Test the get_cities endpoint when a SQLAlchemyError occurs."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_service_get_cities_data.side_effect = SQLAlchemyError("Database error")

    response = client.get("/cities?map_id=10")

    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Internal server error"


@patch("backend.src.web_backend.controller.map_controller.get_db_session")
@patch("backend.src.web_backend.controller.map_controller.service_get_cities_data")
def test_get_cities_request_exception(
    mock_service_get_cities_data, mock_get_db_session, client: FlaskClient
):
    """Test the get_cities endpoint when a RequestException occurs."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_service_get_cities_data.side_effect = RequestException("Request error")

    response = client.get("/cities?map_id=10")

    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Internal server error"


@patch("backend.src.web_backend.controller.map_controller.get_db_session")
@patch("backend.src.web_backend.controller.map_controller.service_get_map_data_by_name")
def test_get_maps_sqlalchemy_error(
    mock_service_get_map_data_by_name, mock_get_db_session, client: FlaskClient
):
    """Test the get_maps endpoint when a SQLAlchemyError occurs."""
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_service_get_map_data_by_name.side_effect = SQLAlchemyError("Database error")

    response = client.get("/maps?name=Skyrim")

    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Internal server error"


@patch("backend.src.web_backend.controller.map_controller.get_db_session")
@patch("backend.src.web_backend.controller.map_controller.service_get_maps")
def test_get_maps_request_exception(mock_get_maps_from_service, mock_db_connection, client: FlaskClient):
    """Test the get_maps endpoint when a RequestException occurs."""
    mock_get_maps_from_service.side_effect = RequestException("Request error")
    mock_db_connection.return_value.__enter__.return_value = MagicMock()

    response = client.get("/maps")

    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Internal server error"

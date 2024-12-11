"""Unit tests for the web backend controller."""

from unittest.mock import patch, MagicMock

from flask.testing import FlaskClient

from backend.src.app import main


# Test for the `/maps` endpoint
@patch("backend.src.web_backend.controller.map_controller.get_db_session")
@patch("backend.src.web_backend.controller.map_controller.service_get_map_data")
def test_get_map_data(
    mock_service_get_map_data,
    mock_get_db_session,
    client: FlaskClient,  # pylint: disable=redefined-outer-name
):
    """Test the get_map_data endpoint."""
    # Mock the database session
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    # Mock service data to return map, cities and connections
    mock_service_get_map_data.return_value = (
        {
            "id": 1,
            "name": "Skyrim",
            "size_x": 3066,
            "size_y": 2326,
        },
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
@patch("backend.src.web_backend.controller.map_controller.get_db_session")
@patch("backend.src.web_backend.controller.map_controller.service_get_cities_data")
def test_get_cities(
    mock_service_get_cities_data,
    mock_get_db_session,
    client: FlaskClient,  # pylint: disable=redefined-outer-name
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


@patch("backend.src.app.fetch_and_store_map_data_if_needed")
@patch("backend.src.app.get_db_session")
@patch("backend.src.app.create_app")
def test_main_script(
    mock_create_app, mock_get_db_session, mock_fetch_and_store_map_data
):
    """Test the main script block."""
    mock_app = MagicMock()
    mock_create_app.return_value = mock_app
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    main()

    # Assertions
    mock_fetch_and_store_map_data.assert_called_once_with(session=mock_session)
    mock_app.run.assert_called_once_with(debug=True, host="0.0.0.0", port=4243)

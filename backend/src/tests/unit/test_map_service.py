"""Unit tests for map service"""

from unittest.mock import patch, MagicMock, call

import pytest
from requests.exceptions import RequestException

from backend.src.database.schema.city import City
from backend.src.database.schema.connection import Connection
from backend.src.map_service.map_service import fetch_and_store_map_data_if_needed


@pytest.fixture(name="session_mock")
def mock_session():
    """Fixture for the SQLAlchemy session mock."""
    return MagicMock()


@pytest.fixture(name="map_service_response_mock")
def mock_map_service_response():
    """Fixture for the mock map service response."""
    return {
        "cities": [
            {"name": "Whiterun", "positionX": 10, "positionY": 20},
            {"name": "Riverwood", "positionX": 15, "positionY": 25},
        ],
        "connections": [
            {"parent": "Whiterun", "child": "Riverwood"},
        ],
    }


@patch("backend.src.map_service.map_service.requests.get")
@patch("backend.src.map_service.map_service.CityDAO")
@patch("backend.src.map_service.map_service.ConnectionDAO")
def test_fetch_and_store_map_data_success(
    connection_dao_mock,
    city_dao_mock,
    requests_mock,
    session_mock,
    map_service_response_mock,
):
    """Test successful data fetch and store."""
    # Mock HTTP response
    requests_mock.return_value.status_code = 200
    requests_mock.return_value.json.return_value = map_service_response_mock

    # Mock DAO behaviors
    city_dao_mock.get_city_by_name.return_value = None
    connection_dao_mock.get_connection_by_parent_and_child.return_value = None

    # Simulate ID assignment for saved cities
    id_counter = iter(range(1, 100))  # Mock sequential ID generation

    def mock_save_city(city, _):
        city.id = next(id_counter)  # Assign a unique ID

    city_dao_mock.save_city.side_effect = mock_save_city

    # Call the function
    fetch_and_store_map_data_if_needed(session_mock)

    # Verify city saving
    assert city_dao_mock.save_city.call_count == 2  # 2 cities
    city_dao_mock.save_city.assert_has_calls(
        [
            call(
                City(id=1, name="Whiterun", position_x=10, position_y=20), session_mock
            ),
            call(
                City(id=2, name="Riverwood", position_x=15, position_y=25), session_mock
            ),
        ],
        any_order=True,  # If the order of calls doesn't matter
    )

    # Verify connection saving
    assert connection_dao_mock.save_connections_bulk.call_count == 1
    connection_dao_mock.save_connections_bulk.assert_called_with(
        [Connection(parent_city_id=1, child_city_id=2)], session_mock
    )


@patch("backend.src.map_service.map_service.requests.get")
@patch("backend.src.map_service.map_service.CityDAO")
@patch("backend.src.map_service.map_service.ConnectionDAO")
def test_fetch_and_store_existing_data(
    connection_dao_mock,
    city_dao_mock,
    requests_mock,
    session_mock,
    map_service_response_mock,
):
    """Test handling of existing cities and connections."""
    # Mock HTTP response
    requests_mock.return_value.status_code = 200
    requests_mock.return_value.json.return_value = map_service_response_mock

    # Mock DAO behaviors for existing data
    city_dao_mock.get_city_by_name.side_effect = [
        MagicMock(id=1),  # Whiterun exists
        MagicMock(id=2),  # Riverwood exists
    ]
    connection_dao_mock.get_connection_by_parent_and_child.return_value = MagicMock()

    # Call the function
    fetch_and_store_map_data_if_needed(session_mock)

    # Verify no new cities or connections are saved
    assert city_dao_mock.save_city.call_count == 0
    assert connection_dao_mock.save_connections_bulk.call_count == 0


@patch("backend.src.map_service.map_service.requests.get")
def test_fetch_and_store_map_data_network_error(requests_mock, session_mock):
    """Test network error handling."""
    # Mock HTTP request to raise an exception
    requests_mock.side_effect = RequestException("Network error")

    # Call the function
    fetch_and_store_map_data_if_needed(session_mock)

    # Verify no database actions are performed
    session_mock.query.assert_not_called()


@patch("backend.src.map_service.map_service.requests.get")
def test_fetch_and_store_map_data_http_error(requests_mock, session_mock):
    """Test HTTP error handling."""
    # Mock HTTP response with an error status
    requests_mock.return_value.status_code = 500
    requests_mock.return_value.raise_for_status.side_effect = RequestException(
        "HTTP error"
    )

    # Call the function
    fetch_and_store_map_data_if_needed(session_mock)

    # Verify no database actions are performed
    session_mock.query.assert_not_called()


@patch("backend.src.map_service.map_service.requests.get")
@patch("backend.src.map_service.map_service.CityDAO")
def test_partial_city_data_handling(city_dao_mock, requests_mock, session_mock):
    """Test handling of incomplete city data."""
    # Mock HTTP response with missing city fields
    incomplete_response = {
        "cities": [{"name": "Whiterun"}],  # Missing positionX and positionY
        "connections": [],
    }
    requests_mock.return_value.status_code = 200
    requests_mock.return_value.json.return_value = incomplete_response

    # Call the function
    fetch_and_store_map_data_if_needed(session_mock)

    # Verify no cities are saved
    city_dao_mock.save_city.assert_not_called()

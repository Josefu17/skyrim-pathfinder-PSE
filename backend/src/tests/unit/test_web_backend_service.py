"""Unit tests for the web_backend service"""

import xmlrpc
from unittest.mock import patch, MagicMock

from sqlalchemy.orm import Session

from backend.src.web_backend.web_backend_service import (
    fetch_route_from_navigation_service,
    fetch_cities_as_dicts,
    service_get_map_data,
    service_get_cities_data,
)


@patch("backend.src.web_backend.web_backend_service.xmlrpc.client.ServerProxy")
@patch("backend.src.web_backend.web_backend_service.CityDao")
@patch("backend.src.web_backend.web_backend_service.ConnectionDao")
def test_fetch_route_success(mock_connection_dao, mock_city_dao, mock_server_proxy):
    """Test the scenario where a route is successfully fetched from the navigation service."""
    # Create a mock SQLAlchemy session
    mock_session = create_mock_session()

    # Mock data for cities and connections
    mock_city_and_connection_daos(mock_city_dao, mock_connection_dao)

    # Mock the RPC server to return a valid route
    mock_proxy_instance = MagicMock()
    mock_proxy_instance.get_route.return_value = {
        "route": ["Markarth", "Riften"],
        "distance": 500,
    }
    mock_server_proxy.return_value.__enter__.return_value = mock_proxy_instance

    # Call the function with mock session and assert results
    result = fetch_route_from_navigation_service("Markarth", "Riften", mock_session)
    assert result == {"route": ["Markarth", "Riften"], "distance": 500}


@patch("backend.src.web_backend.web_backend_service.xmlrpc.client.ServerProxy")
@patch("backend.src.web_backend.web_backend_service.CityDao")
@patch("backend.src.web_backend.web_backend_service.ConnectionDao")
def test_fetch_route_error_by_route_calculation(
    mock_connection_dao, mock_city_dao, mock_server_proxy
):
    """Test the scenario where the route calculation fails and returns an error."""
    # Create a mock SQLAlchemy session
    mock_session = create_mock_session()

    # Mock data for cities and connections (normal valid data)
    mock_city_and_connection_daos(mock_city_dao, mock_connection_dao)

    # Mock the RPC server response to return None, simulating a failure in route calculation
    mock_proxy_instance = MagicMock()
    mock_proxy_instance.get_route.return_value = None
    mock_server_proxy.return_value.__enter__.return_value = mock_proxy_instance

    # Call the function with mock session and assert results
    result = fetch_route_from_navigation_service("Markarth", "Riften", mock_session)
    assert result == {"error": "Error during Route Calculation"}


@patch("backend.src.web_backend.web_backend_service.xmlrpc.client.ServerProxy")
@patch("backend.src.web_backend.web_backend_service.CityDao")
@patch("backend.src.web_backend.web_backend_service.ConnectionDao")
def test_fetch_route_xmlrpc_error(
    mock_connection_dao, mock_city_dao, mock_server_proxy
):
    """Test the scenario where an XML-RPC error occurs."""
    # Create a mock SQLAlchemy session
    mock_session = create_mock_session()

    # Mock data for cities and connections (normal valid data)
    mock_city_and_connection_daos(mock_city_dao, mock_connection_dao)

    # Mock the RPC server to raise an xmlrpc.client.Error exception
    mock_server_proxy.side_effect = xmlrpc.client.Error(
        "An XML-RPC error occurred"
    )  # noqa

    # Call the function with mock session and assert results
    result = fetch_route_from_navigation_service("Markarth", "Riften", mock_session)
    assert result == "XML-RPC error: Error('An XML-RPC error occurred')"


@patch("backend.src.web_backend.web_backend_service.xmlrpc.client.ServerProxy")
@patch("backend.src.web_backend.web_backend_service.CityDao")
@patch("backend.src.web_backend.web_backend_service.ConnectionDao")
def test_fetch_route_network_error(
    mock_connection_dao, mock_city_dao, mock_server_proxy
):
    """Test the scenario where a network error occurs."""
    # Create a mock SQLAlchemy session
    mock_session = MagicMock(spec=Session)

    # Mock data for cities and connections (normal valid data)
    mock_city_and_connection_daos(mock_city_dao, mock_connection_dao)

    # Mock the RPC server to raise a ConnectionError exception
    mock_server_proxy.side_effect = ConnectionError("A network error occurred")

    # Call the function with mock session and assert results
    result = fetch_route_from_navigation_service("Markarth", "Riften", mock_session)
    assert result == "Connection error: A network error occurred"


@patch("backend.src.web_backend.web_backend_service.CityDao")
def test_fetch_cities_as_dicts(mock_city_dao):
    """Test fetching cities as dictionaries."""
    # Create a mock SQLAlchemy session
    mock_session = MagicMock(spec=Session)

    # Mock data for cities
    mock_city_dao.get_all_cities.return_value = [
        create_mock_city("Markarth", 100, 200),
        create_mock_city("Riften", 300, 400),
    ]

    # Call the function with mock session
    result = fetch_cities_as_dicts(mock_session)

    # Assert results
    assert result == [
        {"name": "Markarth", "position_x": 100, "position_y": 200},
        {"name": "Riften", "position_x": 300, "position_y": 400},
    ]


@patch("backend.src.web_backend.web_backend_service.CityDao")
@patch("backend.src.web_backend.web_backend_service.ConnectionDao")
@patch("backend.src.web_backend.web_backend_service.MapDao")
def test_service_get_map_data(mock_map_dao, mock_connection_dao, mock_city_dao):
    """Test fetching map data."""
    # Create a mock SQLAlchemy session
    mock_session = MagicMock(spec=Session)

    # Mock data for cities and connections
    mock_city_and_connection_daos(mock_city_dao, mock_connection_dao)

    # Mock map data
    mock_map = create_mock_map("Skyrim", 3066, 2326, map_id=1)
    mock_map_dao.get_map.return_value = mock_map

    # Call the function with mock session
    map_data, cities_data, connections_data = service_get_map_data(mock_session)

    # Assert map_data results
    assert map_data == {
        "id": 1,
        "name": "Skyrim",
        "size_x": 3066,
        "size_y": 2326,
    }

    # Assert cities_data results
    assert cities_data == [
        {"id": 1, "name": "Markarth", "position_x": 100, "position_y": 200},
        {"id": 2, "name": "Riften", "position_x": 300, "position_y": 400},
    ]
    assert connections_data == [{"parent_city_id": 1, "child_city_id": 2}]


@patch("backend.src.web_backend.web_backend_service.CityDao")
def test_service_get_cities_data(mock_city_dao):
    """Test fetching cities data."""
    # Create a mock SQLAlchemy session
    mock_session = MagicMock(spec=Session)

    # Mock data for cities
    mock_city_dao.get_all_cities.return_value = [
        create_mock_city("Markarth", 100, 200),
        create_mock_city("Riften", 300, 400),
    ]

    # Call the function with mock session
    result = service_get_cities_data(mock_session)

    # Assert results
    assert result == [
        {"name": "Markarth", "position_x": 100, "position_y": 200},
        {"name": "Riften", "position_x": 300, "position_y": 400},
    ]


def create_mock_city(name, position_x, position_y, city_id=None):
    """Helper to create mock city objects"""
    city = MagicMock()
    city.name = name
    city.position_x = position_x
    city.position_y = position_y
    city.id = city_id
    city.to_dict = lambda: {
        "id": city_id,
        "name": name,
        "position_x": position_x,
        "position_y": position_y,
    }
    return city


def create_mock_connection(parent_city_id, child_city_id):
    """Helper to create mock connection objects"""
    return MagicMock(parent_city_id=parent_city_id, child_city_id=child_city_id)


def create_mock_session():
    """Helper to create mock session"""
    return MagicMock(spec=Session)


def mock_city_and_connection_daos(mock_city_dao, mock_connection_dao):
    """Helper to mock city and connection DAOs"""
    mock_city_dao.get_all_cities.return_value = [
        create_mock_city("Markarth", 100, 200, city_id=1),
        create_mock_city("Riften", 300, 400, city_id=2),
    ]
    mock_connection_dao.get_all_connections.return_value = [
        create_mock_connection(1, 2)
    ]


def create_mock_map(name, size_x, size_y, map_id=None):
    """Helper to mock general map information"""
    map_obj = MagicMock()
    map_obj.name = name
    map_obj.size_x = size_x
    map_obj.size_y = size_y
    map_obj.id = map_id
    map_obj.to_dict = lambda: {
        "id": map_id,
        "name": name,
        "size_x": size_x,
        "size_y": size_y,
    }
    return map_obj

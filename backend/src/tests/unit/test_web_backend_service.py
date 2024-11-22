"""Unit tests for the web_backend service"""

import xmlrpc
from unittest.mock import patch, MagicMock

from sqlalchemy.orm import Session

from backend.src.web_backend.web_backend_service import fetch_route_from_navigation_service


@patch("backend.src.web_backend.web_backend_service.xmlrpc.client.ServerProxy")
@patch("backend.src.web_backend.web_backend_service.CityDAO")
@patch("backend.src.web_backend.web_backend_service.ConnectionDAO")
def test_fetch_route_error_by_route_calculation(
    mock_connection_dao, mock_city_dao, mock_server_proxy
):
    """Test the scenario where the route calculation fails and returns an error."""
    # Create a mock SQLAlchemy session
    mock_session = MagicMock(spec=Session)

    # Mock data for cities and connections (normal valid data)
    mock_city_dao.get_all_cities.return_value = [
        MagicMock(
            to_dict=lambda: {
                "id": 1,
                "name": "Markarth",
                "position_x": 100,
                "position_y": 200,
            }
        ),
        MagicMock(
            to_dict=lambda: {
                "id": 2,
                "name": "Riften",
                "position_x": 300,
                "position_y": 400,
            }
        ),
    ]
    mock_connection_dao.get_all_connections.return_value = [
        MagicMock(parent_city_id=1, child_city_id=2)
    ]

    # Mock the RPC server response to return None, simulating a failure in route calculation
    mock_proxy_instance = MagicMock()
    mock_proxy_instance.get_route.return_value = None
    mock_server_proxy.return_value.__enter__.return_value = mock_proxy_instance

    # Call the function with mock session and assert results
    result = fetch_route_from_navigation_service("Markarth", "Riften", mock_session)
    assert result == {"error": "Error by Route Calculation"}


@patch("backend.src.web_backend.web_backend_service.xmlrpc.client.ServerProxy")
@patch("backend.src.web_backend.web_backend_service.CityDAO")
@patch("backend.src.web_backend.web_backend_service.ConnectionDAO")
def test_fetch_route_xmlrpc_error(
    mock_connection_dao, mock_city_dao, mock_server_proxy
):
    """Test the scenario where an XML-RPC error occurs."""
    # Create a mock SQLAlchemy session
    mock_session = MagicMock(spec=Session)

    # Mock data for cities and connections (normal valid data)
    mock_city_dao.get_all_cities.return_value = [
        MagicMock(
            to_dict=lambda: {
                "id": 1,
                "name": "Markarth",
                "position_x": 100,
                "position_y": 200,
            }
        ),
        MagicMock(
            to_dict=lambda: {
                "id": 2,
                "name": "Riften",
                "position_x": 300,
                "position_y": 400,
            }
        ),
    ]
    mock_connection_dao.get_all_connections.return_value = [
        MagicMock(parent_city_id=1, child_city_id=2)
    ]

    # Mock the RPC server to raise an xmlrpc.client.Error exception
    mock_server_proxy.side_effect = xmlrpc.client.Error("An XML-RPC error occurred")

    # Call the function with mock session and assert results
    result = fetch_route_from_navigation_service("Markarth", "Riften", mock_session)
    assert result == "XML-RPC error: Error('An XML-RPC error occurred')"


@patch("backend.src.web_backend.web_backend_service.xmlrpc.client.ServerProxy")
@patch("backend.src.web_backend.web_backend_service.CityDAO")
@patch("backend.src.web_backend.web_backend_service.ConnectionDAO")
def test_fetch_route_network_error(
    mock_connection_dao, mock_city_dao, mock_server_proxy
):
    """Test the scenario where a network error occurs."""
    # Create a mock SQLAlchemy session
    mock_session = MagicMock(spec=Session)

    # Mock data for cities and connections (normal valid data)
    mock_city_dao.get_all_cities.return_value = [
        MagicMock(
            to_dict=lambda: {
                "id": 1,
                "name": "Markarth",
                "position_x": 100,
                "position_y": 200,
            }
        ),
        MagicMock(
            to_dict=lambda: {
                "id": 2,
                "name": "Riften",
                "position_x": 300,
                "position_y": 400,
            }
        ),
    ]
    mock_connection_dao.get_all_connections.return_value = [
        MagicMock(parent_city_id=1, child_city_id=2)
    ]

    # Mock the RPC server to raise a ConnectionError exception
    mock_server_proxy.side_effect = ConnectionError("A network error occurred")

    # Call the function with mock session and assert results
    result = fetch_route_from_navigation_service("Markarth", "Riften", mock_session)
    assert result == "Network error: A network error occurred"

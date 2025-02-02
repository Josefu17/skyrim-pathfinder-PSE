"""test file to test the external map service integration"""

from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import RequestException
from sqlalchemy.orm import Session

from backend.src.database.schema.map import Map
from backend.src.map_service.map_service import (
    get_maps_from_service,
    fetch_and_store_map_data_if_needed,
)

# Mock-Daten für die Tests
MOCK_MAP_LIST = ["10000", "20000", "50000"]
MOCK_MAP_DATA = {
    "mapsizeX": 100,
    "mapsizeY": 100,
    "cities": [
        {"name": "City1", "positionX": 10, "positionY": 20},
        {"name": "City2", "positionX": 30, "positionY": 40},
    ],
    "connections": [
        {"parent": "City1", "child": "City2"},
    ],
}


@pytest.fixture
def mock_session():
    """mock session"""
    return MagicMock(spec=Session)


@pytest.fixture
def mock_requests_get():
    """mock requests get"""
    with patch("requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def mock_map_dao():
    """mock map dao"""
    with patch("backend.src.map_service.map_service.MapDao") as mock:
        yield mock


@pytest.fixture
def mock_city_dao():
    """mock city dao"""
    with patch("backend.src.map_service.map_service.CityDao") as mock:
        yield mock


@pytest.fixture
def mock_connection_dao():
    """mock connection dao"""
    with patch("backend.src.map_service.map_service.ConnectionDao") as mock:
        yield mock


def test_get_maps_from_service_success(mock_requests_get):
    """test success scenario for maps list retrieval"""
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = MOCK_MAP_LIST

    result = get_maps_from_service()
    assert result == MOCK_MAP_LIST
    mock_requests_get.assert_called_once_with(
        "https://maps.proxy.devops-pse.users.h-da.cloud/maps", timeout=10
    )


def test_get_maps_from_service_failure(mock_requests_get):
    """test failure scenario for maps list retrieval"""
    mock_requests_get.side_effect = RequestException("Connection error")

    result = get_maps_from_service()
    assert not result


def test_fetch_and_store_map_data_if_needed_existing_map(mock_session, mock_map_dao):
    """test handling of fetching of existing map entry"""
    mock_map = MagicMock(spec=Map)
    mock_map_dao.get_map_by_name.return_value = mock_map

    fetch_and_store_map_data_if_needed(mock_session)

    mock_map_dao.save_map.assert_not_called()


def test_fetch_and_store_map_data_if_needed_large_map(
    mock_session, mock_requests_get, mock_map_dao
):
    """test handling of fetching of large map entry"""
    mock_map_dao.get_map_by_name.return_value = None

    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = ["50000"]

    fetch_and_store_map_data_if_needed(mock_session)

    mock_map_dao.save_map.assert_not_called()


def test_fetch_and_store_map_data_if_needed_request_failure(
    mock_session, mock_requests_get, mock_map_dao
):
    """test failure scenario for maps list retrieval"""
    mock_map_dao.get_map_by_name.return_value = None

    mock_requests_get.side_effect = RequestException("Connection error")

    fetch_and_store_map_data_if_needed(mock_session)

    mock_map_dao.save_map.assert_not_called()


def test_fetch_and_store_map_data_if_needed_fetch_map_data(
    mock_session, mock_requests_get, mock_map_dao, mock_city_dao, mock_connection_dao
):
    """test the successful fetch map data scenario"""
    mock_map_dao.get_map_by_name.return_value = None
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = MOCK_MAP_DATA

    # Ensure get_city_by_name returns None for each city
    mock_city_dao.get_city_by_name.side_effect = lambda map_id, name, session: None

    # Ensure get_connection_by_parent_and_child returns None for each connection
    mock_connection_dao.get_connection_by_parent_and_child.side_effect = (
        lambda map_id, parent_city_id, child_city_id, session: None
    )

    # Mock the get_maps_from_service function to return the expected map name
    with patch("backend.src.map_service.map_service.get_maps_from_service", return_value=["10000"]):
        fetch_and_store_map_data_if_needed(mock_session)

    mock_requests_get.assert_called_with(
        "https://maps.proxy.devops-pse.users.h-da.cloud/map?name=10000", timeout=60
    )
    mock_map_dao.save_map.assert_called_once()
    mock_city_dao.save_cities_bulk.assert_called_once()

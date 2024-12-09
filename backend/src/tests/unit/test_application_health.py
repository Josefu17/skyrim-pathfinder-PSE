"""
tests to verify the functionality of
`check_map_service_connection` and `check_navigation_service_connection`
"""

from unittest.mock import patch, MagicMock

from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

from backend.src.health.health_check import (
    check_map_service_connection,
    check_navigation_service_connection,
    check_database_connection,
    check_frontend_availability,
)


@patch("backend.src.health.health_check.get_db_session")
def test_check_database_connection_success(mock_get_db_session):
    """
    Test to verify successful database connection.
    """
    mock_session = MagicMock()
    mock_session.__enter__.return_value.execute.return_value.fetchone.return_value = (
        1,
    )
    mock_get_db_session.return_value = mock_session

    result = check_database_connection()
    assert result == {
        "database_connection": True
    }, "Expected successful database connection result"
    mock_get_db_session.assert_called_once()


@patch("backend.src.health.health_check.get_db_session")
def test_check_database_connection_failure(mock_get_db_session):
    """
    Test to verify database connection failure.
    """
    mock_session = MagicMock()
    mock_session.__enter__.side_effect = SQLAlchemyError("Simulated database error")
    mock_get_db_session.return_value = mock_session

    result = check_database_connection()
    assert (
        result["database_connection"] is False
    ), "Expected database connection failure"
    assert (
        "Simulated database error" in result["message"]
    ), "Expected error message to include simulated error"
    mock_get_db_session.assert_called_once()


def test_check_map_service_connection_success():
    """
    Test that `check_map_service_connection` returns a successful response
    when the map service is reachable.
    """
    with patch("requests.get") as mock_get:  # pylint: disable=unused-variable # noqa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = check_map_service_connection()

        assert result == {"map_service_connection": True}


def test_check_map_service_connection_failure():
    """
    Test that `check_map_service_connection` handles a failed connection to the map service.
    """
    with patch("requests.get", side_effect=RequestException("Connection error")):
        result = check_map_service_connection()

        assert result["map_service_connection"] is False
        assert "Connection error" in result["message"]


def test_check_navigation_service_connection_success():
    """
    Test that `check_navigation_service_connection` returns a successful response
    when the navigation service is reachable.
    """
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = check_navigation_service_connection()

        assert result == {"navigation_service_connection": True}


def test_check_navigation_service_connection_failure():
    """
    Test that `check_navigation_service_connection` handles a failed connection
    to the navigation service.
    """
    with patch("requests.get", side_effect=RequestException("Connection error")):
        result = check_navigation_service_connection()

        assert result["navigation_service_connection"] is False
        assert "Connection error" in result["message"]


def test_check_navigation_service_connection_non_200():
    """
    Test that `check_navigation_service_connection` handles a non-200 response status code
    from the navigation service.
    """
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = check_navigation_service_connection()

        assert result["navigation_service_connection"] is False
        assert result["message"] == "Request to navigation service failed"


def test_check_frontend_availability_success():
    """
    Test that `check_frontend_availability` returns a successful response
    when the frontend is reachable.
    """
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            '<h1 class="flex_item">Path finder</h1>'
            '<ul id="endpoint_list"></ul>'
            '<form id="path_points_form"</form>'
            '<select id="startpoint"></select>'
            '<select id="endpoint"></select>'
        )
        mock_get.return_value = mock_response

        result = check_frontend_availability()

        assert result == {"frontend_availability": True}


def test_check_frontend_availability_connection_failure():
    """
    Test that `check_frontend_availability` handles a failed connection to the frontend.
    """
    with patch("requests.get", side_effect=RequestException("Connection error")):
        result = check_frontend_availability()

        assert result["frontend_availability"] is False
        assert "Connection error" in result["message"]


def test_check_frontend_availability_missing_elements():
    """
    Test that `check_frontend_availability` handles missing elements on the frontend.
    """
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            '<h1 class="flex_item">Path finder</h1>' + '<ul id="endpoint_list"></ul>'
        )
        mock_get.return_value = mock_response

        result = check_frontend_availability()

        assert result["frontend_availability"] is False
        assert result["message"] == "Elements are missing"

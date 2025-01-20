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
    check_all_criteria,
)


@patch("backend.src.health.health_check.get_db_session")
def test_check_database_connection_success(mock_get_db_session):
    """
    Test to verify successful database connection.
    """
    mock_session = MagicMock()
    mock_session.__enter__.return_value.execute.return_value.fetchone.return_value = (1,)
    mock_get_db_session.return_value = mock_session

    result = check_database_connection()
    assert result == {"database_connection": True}, "Expected successful database connection result"
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
    assert result["database_connection"] is False, "Expected database connection failure"
    assert (
        "Simulated database error" in result["message"]
    ), "Expected error message to include simulated error"
    mock_get_db_session.assert_called_once()


def test_check_map_service_connection_success():
    """
    Test that `check_map_service_connection` returns a successful response
    when the map service is reachable.
    """
    with patch("requests.get") as mock_get:
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


@patch("backend.src.health.health_check.get_db_session")
def test_check_navigation_service_connection_success(mock_get_db_session):
    """
    Test that `check_navigation_service_connection` returns a successful response
    when the navigation service is reachable.
    """
    mock_session = MagicMock()
    mock_get_db_session.return_value = mock_session

    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        result = check_navigation_service_connection()

        assert result == {"navigation_service_connection": True}


@patch("backend.src.health.health_check.get_db_session")
def test_check_navigation_service_connection_failure(mock_get_db_session):
    """
    Test that `check_navigation_service_connection` handles a failed connection
    to the navigation service.
    """
    mock_session = MagicMock()
    mock_get_db_session.return_value = mock_session

    with patch("requests.post", side_effect=RequestException("Connection error")):
        result = check_navigation_service_connection()

        assert result["navigation_service_connection"] is False
        assert "Connection error" in result["message"]


@patch("backend.src.health.health_check.get_db_session")
def test_check_navigation_service_connection_non_201(mock_get_db_session):
    """
    Test that `check_navigation_service_connection` handles a non-201 response status code
    from the navigation service.
    """
    mock_session = MagicMock()
    mock_get_db_session.return_value = mock_session

    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

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
        mock_response.text = '<div id="root"></div>'
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
        mock_response.text = ""
        mock_get.return_value = mock_response

        result = check_frontend_availability()

        assert result["frontend_availability"] is False
        assert result["message"] == "Elements are missing"


@patch("backend.src.web_backend.controller.health_controller.check_all_criteria")
@patch("backend.src.web_backend.controller.health_controller.logger")
def test_health_check_healthy(mock_logger, mock_check_all_criteria, client):
    """
    Test that health_check returns healthy status when all criteria are met.
    """
    mock_check_all_criteria.return_value = {
        "database_connection": True,
        "map_service_connection": True,
        "navigation_service_connection": True,
        "frontend_availability": True,
    }

    response = client.get("/healthz")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["status"] == "healthy"
    assert json_data["details"] == mock_check_all_criteria.return_value
    mock_logger.info.assert_called_once_with("All criteria passed")


@patch("backend.src.web_backend.controller.health_controller.check_all_criteria")
@patch("backend.src.web_backend.controller.health_controller.logger")
def test_health_check_unhealthy(mock_logger, mock_check_all_criteria, client):
    """
    Test that health_check returns unhealthy status when some criteria are not met.
    """
    mock_check_all_criteria.return_value = {
        "database_connection": False,
        "map_service_connection": True,
        "navigation_service_connection": True,
        "frontend_availability": True,
    }

    response = client.get("/healthz")
    json_data = response.get_json()

    assert response.status_code == 503
    assert json_data["status"] == "unhealthy"
    assert json_data["details"] == mock_check_all_criteria.return_value
    mock_logger.error.assert_called_once_with("Some criteria failed")


@patch("backend.src.health.health_check.check_database_connection")
@patch("backend.src.health.health_check.check_map_service_connection")
@patch("backend.src.health.health_check.check_navigation_service_connection")
@patch("backend.src.health.health_check.check_frontend_availability")
def test_check_all_criteria(
    mock_check_frontend, mock_check_navigation, mock_check_map, mock_check_database
):
    """
    Test that `check_all_criteria` returns the correct combined status of all checks.
    """
    mock_check_database.return_value = {"database_connection": True}
    mock_check_map.return_value = {"map_service_connection": True}
    mock_check_navigation.return_value = {"navigation_service_connection": True}
    mock_check_frontend.return_value = {"frontend_availability": True}

    result = check_all_criteria()

    expected_result = {
        "database_connection": True,
        "map_service_connection": True,
        "navigation_service_connection": True,
        "frontend_availability": True,
    }

    assert result == expected_result, "Expected all criteria to be met"

    # Test with some criteria failing
    mock_check_database.return_value = {"database_connection": False}
    result = check_all_criteria()
    expected_result["database_connection"] = False

    assert result == expected_result, "Expected database connection to fail"

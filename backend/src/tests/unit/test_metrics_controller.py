"""Tests for the metrics_controller module."""

from unittest.mock import patch, MagicMock
from flask.testing import FlaskClient


@patch("backend.src.web_backend.controller.metrics_controller.redis_client")
def test_get_metrics(mock_redis_client, client: FlaskClient):
    """Test the get_metrics endpoint."""
    mock_redis_client.get = MagicMock(
        side_effect=lambda key: {
            "logged_in_users": "5",
            "anonymous_route_execution_time": "100.0",
            "anonymous_calculated_route": "10",
            "registered_route_execution_time": "200.0",
            "registered_calculated_route": "20",
            "error_missing_username": "1",
            "error_existing_username": "2",
            "error_user_not_found": "3",
            "error_missing_city": "4",
            "error_calculating_route": "5",
            "error_route_not_found": "6",
            "error_clearing_route_history": "7",
            "concurrent_requests": "8",
        }.get(key, 0)
    )

    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.get_json()

    assert data["traffic"][0]["logged_in_users"] == 5
    assert data["traffic"][0]["registered_calculated_route"] == 20
    assert data["traffic"][0]["anonymous_calculated_route"] == 10
    assert data["latency"][0]["registered_avg_execution_time"] == 10.0
    assert data["latency"][0]["anonymous_avg_execution_time"] == 10.0
    assert data["error"][0]["error_missing_username"] == 1
    assert data["error"][0]["error_existing_username"] == 2
    assert data["error"][0]["error_user_not_found"] == 3
    assert data["error"][0]["error_missing_city"] == 4
    assert data["error"][0]["error_calculating_route"] == 5
    assert data["error"][0]["error_route_not_found"] == 6
    assert data["error"][0]["error_clearing_route_history"] == 7
    assert data["saturation"][0]["concurrent_requests"] == 8

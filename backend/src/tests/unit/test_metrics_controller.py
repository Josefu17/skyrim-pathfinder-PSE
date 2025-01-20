"""Tests for the metrics controller"""

import pytest
from flask import Flask
from backend.src.web_backend.controller.metrics_controller import init_metrics_routes
from backend.src.utils.helpers import metrics_logger


@pytest.fixture
def app():
    """Create a Flask app for testing"""
    app = Flask(__name__)
    init_metrics_routes(app)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


def test_metrics_endpoint(client, mocker):
    """Test the metrics endpoint"""
    mocker.patch.object(metrics_logger.redis_client, "keys", return_value=[b"m_test_metric"])
    mocker.patch.object(metrics_logger, "get", return_value=10)

    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"m_test_metric 10" in response.data


def test_metrics_endpoint_no_metrics(client, mocker):
    """Test the metrics endpoint with no metrics"""
    mocker.patch.object(metrics_logger.redis_client, "keys", return_value=[])

    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.data == b""


def test_metrics_endpoint_invalid_metric(client, mocker):
    """Test the metrics endpoint with an invalid metric"""
    mocker.patch.object(metrics_logger.redis_client, "keys", return_value=[b"m_invalid_metric"])
    mocker.patch.object(metrics_logger, "get", side_effect=ValueError)

    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.data == b""

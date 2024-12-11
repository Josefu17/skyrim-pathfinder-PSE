"""Configuration for unit tests"""

import pytest
from flask.testing import FlaskClient
from backend.src.app import create_app

app = create_app()


@pytest.fixture(name="client")
def flask_client() -> FlaskClient:
    """Fixture to create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

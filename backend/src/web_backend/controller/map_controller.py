"""
This module contains the controller for the web backend service.
"""

from flask import jsonify
from backend.src.database.db_connection import get_db_session
from backend.src.utils.helpers import get_logging_configuration
from backend.src.web_backend.web_backend_service import (
    service_get_map_data,
    service_get_cities_data,
)


logger = get_logging_configuration()

MAPS = "/maps"
CITIES = "/cities"


def init_map_routes(app):
    """Initialize all routes for the Flask app."""
    app.route(MAPS, methods=["GET"])(get_map_data)
    app.route(CITIES, methods=["GET"])(get_cities)


def get_map_data():
    """Fetch and return map data including cities and connections."""
    logger.info("Fetching map data.")
    with get_db_session() as session:
        map_data, cities_data, connections_data = service_get_map_data(session)
    logger.info("Map data fetched successfully.")
    return jsonify({"map": map_data, "cities": cities_data, "connections": connections_data})


def get_cities():
    """Fetch and return cities."""
    logger.info("Fetching cities data.")
    with get_db_session() as session:
        cities = service_get_cities_data(session)
    logger.info("Cities data fetched successfully.")
    return jsonify({"cities": cities})

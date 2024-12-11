"""
This module contains the controller for the web backend service.
"""

from flask import jsonify
from backend.src.database.db_connection import get_db_session
from backend.src.logging_config import get_logging_configuration
from backend.src.web_backend.web_backend_service import (
    service_get_map_data,
    service_get_cities_data,
)
from backend.src.health.health_check import check_all_criteria

logger = get_logging_configuration()


def init_map_routes(app):
    """Initialize all routes for the Flask app."""

    @app.route("/maps", methods=["GET"])
    def get_map_data():
        """Fetch and return map data including cities and connections."""
        logger.info("Fetching map data.")
        with get_db_session() as session:
            map_data, cities_data, connections_data = service_get_map_data(session)
        logger.info("Map data fetched successfully.")
        return jsonify(
            {"map": map_data, "cities": cities_data, "connections": connections_data}
        )

    @app.route("/cities", methods=["GET"])
    def get_cities():
        """Fetch and return cities."""
        logger.info("Fetching cities data.")
        with get_db_session() as session:
            cities = service_get_cities_data(session)
        logger.info("Cities data fetched successfully.")
        return jsonify({"cities": cities})

    @app.route("/healthz", methods=["GET"])
    def health_check():
        """checks the health status of the application"""
        criteria_status = check_all_criteria()

        if all(
            status is True
            for status in criteria_status.values()
            if isinstance(status, bool)
        ):
            logger.info("All criteria passed")
            return jsonify({"status": "healthy", "details": criteria_status}), 200

        logger.error("Some criteria failed")
        return jsonify({"status": "unhealthy", "details": criteria_status}), 503

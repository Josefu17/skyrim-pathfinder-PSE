"""
This module contains the controller for the web backend service.
"""

from flask import jsonify, request
from backend.src.database.db_connection import get_db_session
from backend.src.logging_config import get_logging_configuration
from backend.src.web_backend.web_backend_service import (
    fetch_route_from_navigation_service,
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

    @app.route("/cities/route", methods=["GET"])
    def calculate_route():
        """Calculate shortest route for given 2 endpoints"""
        start_city_name = request.args.get("startpoint")
        end_city_name = request.args.get("endpoint")

        if not start_city_name or not end_city_name:
            logger.error(
                "Start and end cities are required but at least one of them is missing"
            )
            return jsonify({"error": "Start and end cities are required"}), 400

        logger.info("Calculating route from %s to %s.", start_city_name, end_city_name)
        with get_db_session() as session:
            route_result = fetch_route_from_navigation_service(
                start_city_name, end_city_name, session
            )

        if "error" in route_result:
            logger.error("Error calculating route: %s", route_result["error"])
            return jsonify(route_result), 400

        logger.info("Route calculated successfully.")
        return jsonify(route_result), 200

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

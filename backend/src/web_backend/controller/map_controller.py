"""
This module contains the controller for the web backend service.
"""

from flask import jsonify
from opentelemetry.trace import get_tracer
from opentelemetry.trace.status import StatusCode
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

from backend.src.database.db_connection import get_db_session
from backend.src.utils.helpers import get_logging_configuration
from backend.src.web_backend.web_backend_service import (
    service_get_map_data,
    service_get_cities_data,
)

logger = get_logging_configuration()
tracer = get_tracer("map-controller")

MAPS = "/maps"
CITIES = "/cities"


def init_map_routes(app):
    """Initialize all routes for the Flask app."""
    app.route(MAPS, methods=["GET"])(get_map_data)
    app.route(CITIES, methods=["GET"])(get_cities)


def get_map_data():
    """Fetch and return map data including cities and connections."""
    with tracer.start_as_current_span("get_map_data") as span:
        try:
            logger.info("Fetching map data.")
            with get_db_session() as session:
                map_data, cities_data, connections_data = service_get_map_data(session)

            logger.info("Map data fetched successfully.")
            return jsonify(
                {"map": map_data, "cities": cities_data, "connections": connections_data}
            )

        except (SQLAlchemyError, RequestException) as specific_error:
            logger.error("Error fetching map data: %s", specific_error)
            span.set_status(StatusCode.ERROR)
            span.record_exception(specific_error)
            return jsonify({"error": "Internal server error"}), 500


def get_cities():
    """Fetch and return cities."""
    with tracer.start_as_current_span("get_cities") as span:
        try:
            logger.info("Fetching cities data.")
            with get_db_session() as session:
                cities = service_get_cities_data(session)

            logger.info("Cities data fetched successfully.")
            return jsonify({"cities": cities})

        except (SQLAlchemyError, RequestException) as specific_error:
            logger.error("Error fetching map data: %s", specific_error)
            span.set_status(StatusCode.ERROR)
            span.record_exception(specific_error)
            return jsonify({"error": "Internal server error"}), 500

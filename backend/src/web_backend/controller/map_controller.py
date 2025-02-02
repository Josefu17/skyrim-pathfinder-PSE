"""Flask Controller to expose endpoints related to maps"""

from flask import request, jsonify
from opentelemetry.trace import get_tracer
from opentelemetry.trace.status import StatusCode
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

from backend.src.database.db_connection import get_db_session
from backend.src.map_service.map_service import get_maps_from_service
from backend.src.utils.helpers import get_logging_configuration
from backend.src.web_backend.web_backend_service import (
    service_get_cities_data,
    service_get_map_data_by_name,
)

logger = get_logging_configuration()
tracer = get_tracer("map-controller")

MAPS = "/maps"
CITIES = "/cities"


def init_map_routes(app):
    """Initialize all routes for the Flask app."""
    app.route(MAPS, methods=["GET"])(get_maps)
    app.route(CITIES, methods=["GET"])(get_cities)


def get_maps():
    """
    Fetch and return all map names if no name parameter is provided.
    If a name parameter is provided, fetch and return data for the specific map.
    """
    with tracer.start_as_current_span("get_map_names") as span:
        try:
            map_name = request.args.get("name")

            if map_name:
                logger.info("Fetching map data for map name: %s", map_name)
                with get_db_session() as session:
                    map_data, cities_data, connections_data = service_get_map_data_by_name(
                        map_name, session
                    )

                logger.info("Map data fetched successfully for map name: %s", map_name)
                return jsonify(
                    {"map": map_data, "cities": cities_data, "connections": connections_data}
                )

            logger.info("Fetching all map names.")
            maps = get_maps_from_service()
            return jsonify({"maps": maps})

        except (SQLAlchemyError, RequestException) as specific_error:
            logger.error("Error fetching map data: %s", specific_error)
            span.set_status(StatusCode.ERROR)
            span.record_exception(specific_error)
            return jsonify({"error": "Internal server error"}), 500


def get_cities():
    """Fetch and return cities for a specific map ID."""
    with tracer.start_as_current_span("get_cities") as span:
        try:
            map_id = request.args.get("map_id")
            if not map_id:
                logger.error("Map ID not provided in query parameters.")
                return jsonify({"error": "Map ID is required"}), 400

            try:
                map_id = int(map_id)
            except ValueError:
                logger.error("Invalid map ID provided: %s", map_id)
                return jsonify({"error": "Map ID must be an integer"}), 400

            logger.info("Fetching cities data for map ID: %s", map_id)
            with get_db_session() as session:
                cities = service_get_cities_data(map_id, session)

            logger.info("Cities data fetched successfully for map ID: %s", map_id)
            return jsonify({"cities": cities})

        except (SQLAlchemyError, RequestException) as specific_error:
            logger.error("Error fetching cities data: %s", specific_error)
            span.set_status(StatusCode.ERROR)
            span.record_exception(specific_error)
            return jsonify({"error": "Internal server error"}), 500

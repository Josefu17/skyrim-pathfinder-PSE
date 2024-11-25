"""Backend Controller to expose API endpoints"""

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.src.database.db_connection import get_db_session
from backend.src.logging_config import get_logging_configuration
from backend.src.map_service.map_service import fetch_and_store_map_data_if_needed
from backend.src.web_backend.web_backend_service import (
    fetch_route_from_navigation_service,
    service_get_map_data,
    service_get_cities_data,
)

logger = get_logging_configuration()

app = Flask(__name__)
CORS(app)


# TODO is not in use right now, might become relevant later to
#  return entire map information, 17-11-2024, yb
@app.route("/maps", methods=["GET"])
def get_map_data():
    """Fetch and return map data including cities and connections."""
    logger.info("Fetching map data.")
    with get_db_session() as session:
        cities_data, connections_data = service_get_map_data(session)

    logger.info("Map data fetched successfully.")
    return jsonify({"cities": cities_data, "connections": connections_data})


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


def main():
    """Main function to initialize the backend"""
    logger.info("Starting web backend controller.")
    with get_db_session() as db_session:
        fetch_and_store_map_data_if_needed(session=db_session)

    app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()

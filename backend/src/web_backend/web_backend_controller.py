"""Backend Controller to expose API endpoints"""

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.src.database.db_connection import get_db_session
from backend.src.map_service.map_service import fetch_and_store_map_data_if_needed
from backend.src.web_backend.web_backend_service import (
    fetch_route_from_navigation_service,
    service_get_map_data,
    service_get_cities_data,
)

app = Flask(__name__)
CORS(app)


# TODO is not in use right now, might become relevant later to
#  return entire map information, 17-11-2024, yb
@app.route("/maps", methods=["GET"])
def get_map_data():
    """Fetch and return map data including cities and connections."""
    # Fetch  cities and connections data
    with get_db_session() as session:
        cities_data, connections_data = service_get_map_data(session)

    return jsonify({"cities": cities_data, "connections": connections_data})


@app.route("/cities", methods=["GET"])
def get_cities():
    """Fetch and return cities."""
    with get_db_session() as session:
        # Return JSON response with the formatted city data
        return jsonify({"cities": service_get_cities_data(session)})


@app.route("/cities/route", methods=["GET"])
def calculate_route():
    """Calculate shortest route for given 2 endpoints"""
    with get_db_session() as session:
        start_city_name = request.args.get("startpoint")
        end_city_name = request.args.get("endpoint")

        if not start_city_name or not end_city_name:
            return jsonify({"error": "Start and end cities are required"}), 400

        route_result = fetch_route_from_navigation_service(
            start_city_name, end_city_name, session
        )

        if "error" in route_result:
            return jsonify(route_result), 400

        return jsonify(route_result), 200


if __name__ == "__main__":
    # Fetch and update map data if necessary
    with get_db_session() as db_session:
        fetch_and_store_map_data_if_needed(session=db_session)

    app.run(debug=True, host="0.0.0.0", port=5000)

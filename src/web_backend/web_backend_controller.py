"""Backend Controller to expose API endpoints"""

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.database.db_connection import with_db_session, get_db_session
from src.database.dao.city_dao import CityDAO
from src.database.dao.connection_dao import ConnectionDAO
from src.map_service.map_service import fetch_and_store_map_data_if_needed
from src.web_backend.web_backend_service import (
    fetch_route_from_navigation_service,
)

app = Flask(__name__)
CORS(app)


# TODO is not in use right now, might become relevant later to
#  return entire map information, 17-11-2024, yb
@app.route("/maps", methods=["GET"])
@with_db_session
def get_map_data(session):
    """Fetch and return map data including cities and connections."""
    # Fetch  cities and connections data
    cities = CityDAO.get_all_cities(session)
    connections = ConnectionDAO.get_all_connections(session)

    cities_data = [city.to_dict() for city in cities]
    connections_data = [
        {"parent_city_id": conn.parent_city_id, "child_city_id": conn.child_city_id}
        for conn in connections
    ]

    return jsonify({"cities": cities_data, "connections": connections_data})


@app.route("/cities", methods=["GET"])
@with_db_session
def get_cities(session):
    """Fetch and return cities."""
    cities = CityDAO.get_all_cities(session)
    cities_data = [city.to_dict() for city in cities]

    # Return JSON response with the formatted city data
    return jsonify({"cities": cities_data})


@app.route("/cities/route", methods=["GET"])
@with_db_session
def calculate_route(session):
    """Calculate shortest route for given 2 endpoints"""
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

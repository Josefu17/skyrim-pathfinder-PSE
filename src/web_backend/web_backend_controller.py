"""Backend Controller to expose API endpoints"""

from flask import Flask, jsonify, request

from src.map_service.map_service import fetch_and_store_map_data_if_needed
from src.web_backend.web_backend_service import fetch_route_from_navigation_service
from src.database.dao.city_dao import CityDAO
from src.database.dao.connection_dao import ConnectionDAO


app = Flask(__name__)


@app.route("/maps", methods=["GET"])
def get_map_data():
    """Fetch and return map data including cities and connections."""
    # Fetch  cities and connections data
    cities = CityDAO.get_all_cities()
    connections = ConnectionDAO.get_all_connections()

    cities_data = [city.to_dict() for city in cities]
    connections_data = [
        {"parent_city_id": conn.parent_city_id, "child_city_id": conn.child_city_id}
        for conn in connections
    ]

    return jsonify({"cities": cities_data, "connections": connections_data})


@app.route("/cities", methods=["GET"])
def get_cities():
    """Fetch and return cities."""
    # Fetch all cities as objects
    cities = CityDAO.get_all_cities()

    # Convert each city to a dictionary, excluding the 'id' field
    cities_data = [
        {
            "name": city.name,
            "position_x": city.position_x,
            "position_y": city.position_y,
        }
        for city in cities
    ]

    # Return JSON response with the formatted city data
    return jsonify({"cities": cities_data})


@app.route("/cities/route", methods=["GET"])
def calculate_route():
    """Calculate shortest route for given 2 endpoints"""
    start_city_name = request.args.get("startpoint")
    end_city_name = request.args.get("endpoint")

    if not start_city_name or not end_city_name:
        return jsonify({"error": "Start and end cities are required"}), 400

    route_result = fetch_route_from_navigation_service(start_city_name, end_city_name)

    if "error" in route_result:
        return jsonify(route_result), 400

    return jsonify(route_result)


if __name__ == "__main__":
    # Fetch and update map data if necessary
    fetch_and_store_map_data_if_needed()

    app.run(debug=True, host="0.0.0.0", port=5000)

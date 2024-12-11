"""This module contains all routes for the Flask app."""

import json

from flask import jsonify, request
from backend.src.logging_config import get_logging_configuration
from backend.src.database.db_connection import get_db_session
from backend.src.web_backend.web_backend_service import (
    fetch_route_from_navigation_service,
)
from backend.src.database.schema.route import Route
from backend.src.database.dao.route_dao import RouteDao

logger = get_logging_configuration()


def init_path_routes(app):
    """Initialize all routes for the Flask app."""

    @app.route("/cities/route", methods=["POST"])
    def calculate_route():
        """
        Calculate the shortest route for given 2 endpoints and optionally add to user's
        route history
        """
        data = request.get_json()
        start_city_name = data.get("startpoint")
        end_city_name = data.get("endpoint")
        user_id = data.get("user_id")

        if not start_city_name or not end_city_name:
            logger.error(
                "Start and end cities are required but at least one of them is missing"
            )
            return (
                jsonify({"error": "Start and end cities are required"}),
                400,
            )

        logger.info("Calculating route from %s to %s.", start_city_name, end_city_name)
        with get_db_session() as session:
            route_result = fetch_route_from_navigation_service(
                start_city_name, end_city_name, session
            )

            if "error" in route_result:
                logger.error("Error calculating route: %s", route_result["error"])
                return jsonify(route_result), 400

            # Optionally add route to user's history
            if user_id:
                route = Route(
                    user_id=user_id,
                    startpoint=start_city_name,
                    endpoint=end_city_name,
                    route=json.dumps(route_result),
                )
                RouteDao.save_route(route, session)
                logger.info(
                    "Route calculated and saved successfully for user %d.", user_id
                )
            else:
                logger.info(
                    "Route calculated successfully without saving to user history."
                )

        return jsonify(route_result), 201

    @app.route("/cities/route/delete", methods=["DELETE"])
    def delete_route():
        """Delete a route from a user's route history."""
        user_id = request.args.get("user_id")
        route_id = request.args.get("route_id")

        if not user_id or not route_id:
            logger.error(
                "user_id and route_id are required but at least one of them is missing"
            )
            return jsonify({"error": "user_id and route_id are required"}), 400

        with get_db_session() as session:
            route = RouteDao.get_route_by_id(int(route_id), session)
            if not route or route.user_id != int(user_id):
                logger.error("Route with id %s not found.", route_id)
                return jsonify({"error": "Route not found"}), 404

            RouteDao.delete_route_by_id(int(route_id), session)

        logger.info("Route deleted successfully.")
        return jsonify({"success": "Route deleted"}), 200

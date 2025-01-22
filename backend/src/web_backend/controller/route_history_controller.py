"""This module contains all routes for the Flask app."""

import time

from flask import jsonify, request
from opentelemetry.trace import get_tracer
from opentelemetry.trace.status import StatusCode

from backend.src.database.dao.route_dao import RouteDao
from backend.src.database.db_connection import get_db_session
from backend.src.database.schema.route import Route, RouteFilter, OptionalRouteFilters
from backend.src.utils.helpers import get_logging_configuration, metrics_logger
from backend.src.utils.prometheus_converter import make_prometheus_conform
from backend.src.web_backend.web_backend_service import (
    fetch_route_from_navigation_service,
)

logger = get_logging_configuration()
tracer = get_tracer("route-history-controller")

USER_ROUTES = "/users/<int:user_id>/routes"
ROUTES = "/routes"
USER_ROUTES_ID = "/users/<int:user_id>/routes/<int:route_id>"
USER_ROUTES_NAME = "/users/<string:user_name>/routes"


def init_path_routes(app):
    """Initialize all routes for the Flask app."""
    app.route(USER_ROUTES, methods=["POST"])(calculate_route)
    app.route(ROUTES, methods=["POST"])(calculate_route_without_user)
    app.route(USER_ROUTES_ID, methods=["DELETE"])(delete_route)
    app.route(USER_ROUTES, methods=["GET"])(get_user_history)
    app.route(USER_ROUTES, methods=["DELETE"])(clear_user_history_by_id)
    app.route(USER_ROUTES_NAME, methods=["DELETE"])(clear_user_history_by_name)


def calculate_route_without_user():
    """Calculate the shortest route for given two endpoints without saving to user's route history."""
    with tracer.start_as_current_span("calculate_route_without_user"):
        return calculate_route(None)


def clear_user_history_by_id(user_id):
    """Clear the route history for a user by user_id."""
    with tracer.start_as_current_span("clear_user_history_by_id"):
        return clear_user_history(user_id, None)


def clear_user_history_by_name(user_name):
    """Clear the route history for a user by user_name."""
    with tracer.start_as_current_span("clear_user_history_by_name"):
        return clear_user_history(None, user_name)


def calculate_route(user_id):
    """
    Calculate the shortest route for given two endpoints and save to
    user's route history if user_id is provided.
    """
    with tracer.start_as_current_span("calculate_route") as span:
        start_time = time.time()
        user_type = "anonymous" if not user_id else "registered"
        span.set_attribute("user_type", user_type)
        if user_type == "registered":
            span.set_attribute("user_id", user_id)

        metrics_logger.incr("m_concurrent_requests")

        data = request.get_json()
        start_city_name = data.get("startpoint")
        end_city_name = data.get("endpoint")

        key_prefix = make_prometheus_conform(
            f"user_{user_id}_{start_city_name}_{end_city_name}_route"
        )

        if not start_city_name or not end_city_name:
            logger.error("Start and end cities are required but at least one of them is missing")
            metrics_logger.incr("m_error_missing_city")
            metrics_logger.decr("m_concurrent_requests")
            span.set_status(StatusCode.ERROR)
            span.record_exception(ValueError("Start and end cities are required"))

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
                metrics_logger.incr("m_error_calculating_route")
                metrics_logger.decr("m_concurrent_requests")
                span.set_status(StatusCode.ERROR)
                span.record_exception(Exception(route_result["error"]))

                return jsonify(route_result), 400

            if user_id:
                route = Route(
                    user_id=user_id,
                    startpoint=start_city_name,
                    endpoint=end_city_name,
                    route=route_result,
                )
                saved_route = RouteDao.save_route(route, session)
                route_id = saved_route.id
                key_prefix += f"_{route_id}"
                metrics_logger.incr(f"m_user_{user_id}_route")
                metrics_logger.incr(f"m_{key_prefix}_calculated")
                logger.info("Route calculated and saved successfully for user %d.", user_id)
            else:
                logger.info("Route calculated successfully without saving to user history.")

        end_time = time.time()
        total_execution_time = end_time - start_time
        logger.info("Route calculation took %f seconds.", total_execution_time)

        if user_type == "anonymous":
            metrics_logger.incr("m_anonymous_calculation_count")
            metrics_logger.incr_by_float("anonymous", total_execution_time)
        else:
            metrics_logger.incr("m_registered_calculation_count")
            metrics_logger.incr_by_float("registered", total_execution_time)
            metrics_logger.log_execution_time(
                f"m_{key_prefix}_execution_time",
                total_execution_time,
            )
            metrics_logger.log_calculated_route_for_user(user_id, key_prefix)

        metrics_logger.decr("m_concurrent_requests")

        response_data = route_result
        return jsonify(response_data), 201


def delete_route(user_id, route_id):
    """Delete a route from a user's route history."""
    with tracer.start_as_current_span("delete_route") as span:
        span.set_attribute("user_id", user_id)
        span.set_attribute("route_id", route_id)

        if not user_id or not route_id:
            logger.error("user_id and route_id are required but at least one of them is missing")
            span.set_status(StatusCode.ERROR)
            span.record_exception(ValueError("user_id and route_id are required"))

            return jsonify({"error": "user_id and route_id are required"}), 400

        with get_db_session() as session:
            route = RouteDao.get_route_by_id(int(route_id), session)
            if not route or route.user_id != int(user_id):
                logger.error("Route with id %s not found.", route_id)
                metrics_logger.incr("m_error_route_not_found")
                span.set_status(StatusCode.ERROR)
                span.record_exception(ValueError("Route not found"))

                return jsonify({"error": "Route not found"}), 404

            RouteDao.delete_route_by_id(int(route_id), session)

        logger.info("Route deleted successfully.")
        return jsonify({"success": "Route deleted"}), 200


def get_user_history(user_id):
    """Get the route history for a user."""
    with tracer.start_as_current_span("get_user_history") as span:
        field = request.args.get("field", "created_at")
        limit = int(request.args.get("limit", 10))
        descending = request.args.get("descending", "true").lower() == "true"
        from_date = request.args.get("from_date")
        to_date = request.args.get("to_date")
        startpoint = request.args.get("startpoint")
        endpoint = request.args.get("endpoint")

        span.set_attribute("user_id", user_id)

        if not user_id:
            logger.error("user_id is required but missing")
            return jsonify({"error": "user_id is required"}), 400

        optional_filters = OptionalRouteFilters(
            from_date=from_date,
            to_date=to_date,
            startpoint=startpoint,
            endpoint=endpoint,
        )

        filter_params = RouteFilter(
            user_id=int(user_id),
            field=field,
            limit=limit,
            descending=descending,
            optional_filters=optional_filters,
        )

        with get_db_session() as session:
            routes = RouteDao.get_routes(filter_params, session)
            if not routes:
                logger.error("No routes found for user %d.", int(user_id))
                metrics_logger.incr("m_error_route_not_found")
                return jsonify({"error": "No routes found"}), 404

            routes_data = [
                {
                    "id": route.id,
                    "startpoint": route.startpoint,
                    "endpoint": route.endpoint,
                    "route": route.route,
                }
                for route in routes
            ]

        logger.info("Route history fetched successfully.")
        return jsonify({"routes": routes_data}), 200


def clear_user_history(user_id=None, user_name=None):
    """Clear the route history for a user by user_id or user_name."""
    with tracer.start_as_current_span("clear_user_history") as span:
        span.set_attribute("user_id", user_id)
        span.set_attribute("user_name", user_name)

        if not user_id and not user_name:
            logger.error("Either user_id or user_name is required but both are missing")
            return jsonify({"error": "Either user_id or user_name is required"}), 400

        with get_db_session() as session:
            try:
                deleted_count = RouteDao.delete_user_route_history(session, user_id, user_name)
            except ValueError as e:
                logger.error(str(e))
                metrics_logger.incr("m_error_clearing_route_history")
                return jsonify({"error": str(e)}), 400

        logger.info("Route history cleared successfully.")
        return jsonify({"success": "Route history cleared", "deleted_count": deleted_count}), 200

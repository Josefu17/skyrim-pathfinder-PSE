"""This module contains the controller for the metrics endpoint"""

from backend.src.utils.helpers import get_logging_configuration
from backend.src.redis_client import redis_client

logger = get_logging_configuration()

METRICS = "/metrics"


def init_metrics_routes(app):
    """Initialize all routes for the Flask app."""
    app.route(METRICS, methods=["GET"])(get_metrics)


def json_to_prometheus(data):
    """Convert JSON data to Prometheus format"""
    result = []
    for _, items in data.items():
        for item in items:
            for key, value in item.items():
                result.append(f"{key} {value}")
    return "\n".join(result)


def get_metrics():
    """Return metrics data"""
    logger.info("Fetching metrics data")

    logged_in_users = int(redis_client.get("logged_in_users") or 0)

    anonymous_total_time = float(redis_client.get("anonymous_route_execution_time") or 0)
    anonymous_count = int(redis_client.get("anonymous_calculated_route") or 0)
    anonymous_avg_time = anonymous_total_time / anonymous_count if anonymous_count > 0 else 0

    registered_total_time = float(redis_client.get("registered_route_execution_time") or 0)
    registered_count = int(redis_client.get("registered_calculated_route") or 0)
    registered_avg_time = registered_total_time / registered_count if registered_count > 0 else 0

    missing_username = int(redis_client.get("error_missing_username") or 0)
    existing_username = int(redis_client.get("error_existing_username") or 0)
    user_not_found = int(redis_client.get("error_user_not_found") or 0)

    missing_city = int(redis_client.get("error_missing_city") or 0)
    calculation_error = int(redis_client.get("error_calculating_route") or 0)
    route_not_found = int(redis_client.get("error_route_not_found") or 0)
    error_clearing_history = int(redis_client.get("error_clearing_route_history") or 0)

    concurrent_requests = int(redis_client.get("concurrent_requests") or 0)

    metrics = {
        "traffic": [
            {
                "logged_in_users": logged_in_users,
                "registered_calculated_route": registered_count,
                "anonymous_calculated_route": anonymous_count,
            }
        ],
        "latency": [
            {
                "registered_avg_execution_time": registered_avg_time,
                "anonymous_avg_execution_time": anonymous_avg_time,
            }
        ],
        "error": [
            {
                "error_missing_username": missing_username,
                "error_existing_username": existing_username,
                "error_user_not_found": user_not_found,
                "error_missing_city": missing_city,
                "error_calculating_route": calculation_error,
                "error_route_not_found": route_not_found,
                "error_clearing_route_history": error_clearing_history,
            }
        ],
        "saturation": [
            {
                "concurrent_requests": concurrent_requests,
            }
        ],
    }
    return json_to_prometheus(metrics), 200

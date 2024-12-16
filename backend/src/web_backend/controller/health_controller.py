"""This module contains the routes for the health check of the application."""

from flask import jsonify
from backend.src.health.health_check import check_all_criteria

from backend.src.logging_config import get_logging_configuration

logger = get_logging_configuration()

HEALTHZ = "/healthz"


def init_health_routes(app):
    """Initialize all routes for the Flask app."""
    app.route(HEALTHZ, methods=["GET"])(health_check)


def health_check():
    """Checks the health status of the application."""
    criteria_status = check_all_criteria()

    if all(status is True for status in criteria_status.values() if isinstance(status, bool)):
        logger.info("All criteria passed")
        return jsonify({"status": "healthy", "details": criteria_status}), 200

    logger.error("Some criteria failed")
    return jsonify({"status": "unhealthy", "details": criteria_status}), 503

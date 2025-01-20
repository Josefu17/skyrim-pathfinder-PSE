"""This module contains the controller for the metrics endpoint"""

from flask import Response

from backend.src.utils.helpers import get_logging_configuration
from backend.src.utils.helpers import metrics_logger, redis_instance

logger = get_logging_configuration()

METRICS = "/metrics"


def init_metrics_routes(app):
    """Initialize all routes for the Flask app."""
    app.route(METRICS, methods=["GET"])(metrics)


def metrics():
    """Return the metrics data."""
    keys = redis_instance.keys("m_*")

    metrics_data = []
    for key in keys:
        try:
            value = metrics_logger.get(key)
            metric_name = key.decode("utf-8")
            metrics_data.append(f"{metric_name} {value}")
        except (ValueError, TypeError):
            continue

    metrics_output = "\n".join(metrics_data)
    return Response(metrics_output, mimetype="text/plain")

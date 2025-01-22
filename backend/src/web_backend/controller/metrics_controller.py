"""This module contains the controller for the metrics endpoint"""

from flask import Response
from opentelemetry.trace import get_tracer

from backend.src.utils.helpers import get_logging_configuration
from backend.src.utils.helpers import metrics_logger, redis_instance

logger = get_logging_configuration()
tracer = get_tracer("metrics-controller")

METRICS = "/metrics"


def init_metrics_routes(app):
    """Initialize all routes for the Flask app."""
    app.route(METRICS, methods=["GET"])(metrics)


def metrics():
    """Return the metrics data."""
    with tracer.start_as_current_span("metrics") as span:
        keys = redis_instance.keys("m_*")

        metrics_data = []
        for key in keys:
            try:
                value = metrics_logger.get(key)
                metric_name = key.decode("utf-8")
                metrics_data.append(f"{metric_name} {value}")
            except (ValueError, TypeError) as e:
                logger.error("Error decoding metric: %s, %s", key, e)
                span.record_exception(e)
                continue

        metrics_output = "\n".join(metrics_data)
        logger.info("Metrics fetched successfully.")
        return Response(metrics_output, mimetype="text/plain")

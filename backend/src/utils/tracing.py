"""
This module sets up OpenTelemetry tracing for a service, including
integration with Flask, Requests, and gRPC for automatic instrumentation.
"""

import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer, GrpcInstrumentorClient
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.trace.status import StatusCode

from backend.src.database.db_connection import DatabaseConnection
from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


def setup_tracing(service_name: str, instrument_db: bool = False):
    """
    configures OpenTelemetry tracing for the given service.

    Args:
        service_name (str): The name of the service.
        instrument_db (bool, optional): If true, enables instrumentation for the db

    Returns:
        opentelemetry.trace.Tracer: The configured tracer instance.
    """
    tracing_target = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not tracing_target:
        logger.warning("OTEL_EXPORTER_OTLP_ENDPOINT not set, tracing is disabled")
        return trace.get_tracer_provider().get_tracer(service_name)

    # Create a resource describing the service
    resource = Resource.create({"service.name": service_name})
    # Create a tracer provider
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    # Configure Jaeger exporter
    logger.debug("tracing target is %s", tracing_target)
    exporter = OTLPSpanExporter(endpoint=tracing_target, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))

    # Set the global propagator
    set_global_textmap(TraceContextTextMapPropagator())

    # Instrument Flask (for frontend-backend REST)
    FlaskInstrumentor().instrument()
    # Instrument Requests (for any HTTP calls)
    RequestsInstrumentor().instrument()

    if instrument_db:
        engine = DatabaseConnection().get_engine()
        SQLAlchemyInstrumentor().instrument(engine=engine)

    # Instrument gRPC
    GrpcInstrumentorServer().instrument()
    GrpcInstrumentorClient().instrument()

    return trace.get_tracer_provider().get_tracer(service_name)


def set_span_attributes(span, attributes: dict):
    """helper to set multiple attributes on a span at once"""
    if not span:
        raise ValueError("A valid span object must be provided")
    for key, value in attributes.items():
        span.set_attribute(key, value)


def set_span_error_flags(span, exception):
    """helper to set the error status and record exception"""
    span.set_status(StatusCode.ERROR)
    span.record_exception(exception)

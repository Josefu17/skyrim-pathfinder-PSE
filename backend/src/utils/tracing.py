"""
This module sets up OpenTelemetry tracing for a service, including
integration with Flask, Requests, and gRPC for automatic instrumentation.
"""
import os

import logging
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer, GrpcInstrumentorClient
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from backend.src.database.db_connection import DatabaseConnection

# getcwd(): path where the script was executed
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)


def setup_tracing(service_name: str):
    """
    Configures OpenTelemetry tracing for the given service.

    Args:
        service_name (str): The name of the service.

    Returns:
        opentelemetry.trace.Tracer: The configured tracer instance.
    """
    tracing_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    logging.info(f"Tracing endpoint: {tracing_endpoint}")

    if not tracing_endpoint:
        logging.warning("ENABLE_TRACING is set to false, ignoring tracing.")
        return trace.get_tracer_provider().get_tracer(service_name)

    # Create a resource describing the service
    resource = Resource.create({"service.name": service_name})

    # Create a tracer provider
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Configure Jaeger exporter
    exporter = OTLPSpanExporter(
        endpoint=tracing_endpoint, insecure=True
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))

    # Set the global propagator -> to pass trace context info to consecutive alls
    set_global_textmap(TraceContextTextMapPropagator())

    # Instrument Flask (for frontend-backend REST)
    FlaskInstrumentor().instrument()
    # Instrument Requests (for any HTTP calls)
    RequestsInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument(engine=DatabaseConnection().get_engine())
    # Instrument gRPC
    GrpcInstrumentorServer().instrument()
    GrpcInstrumentorClient().instrument()

    return trace.get_tracer_provider().get_tracer(service_name)

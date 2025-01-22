"""
This module sets up OpenTelemetry tracing for a service, including
integration with Flask, Requests, and gRPC for automatic instrumentation.
"""

import os

from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer, GrpcInstrumentorClient
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

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
    if os.getenv("ENABLE_TRACING", "false").lower() != "true":
        return trace.get_tracer_provider().get_tracer(service_name)

    # Create a resource describing the service
    resource = Resource.create({"service.name": service_name})

    # Create a tracer provider
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Configure Jaeger exporter
    exporter = OTLPSpanExporter(
        endpoint="sre-backend.devops-pse.users.h-da.cloud:4319", insecure=True
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))

    # Instrument Flask (for frontend-backend REST)
    FlaskInstrumentor().instrument()

    # Instrument Requests (for any HTTP calls)
    RequestsInstrumentor().instrument()

    # Instrument gRPC
    GrpcInstrumentorServer().instrument()
    GrpcInstrumentorClient().instrument()

    return trace.get_tracer_provider().get_tracer(service_name)

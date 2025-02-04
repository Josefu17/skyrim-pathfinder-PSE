"""test file for the tracing functionality"""

import os
from unittest.mock import patch, MagicMock, ANY

from opentelemetry import trace

from backend.src.utils.tracing import setup_tracing


@patch.dict(os.environ, {"OTEL_EXPORTER_OTLP_ENDPOINT": "dummy_value"})
@patch("backend.src.utils.tracing.OTLPSpanExporter")
@patch("backend.src.utils.tracing.BatchSpanProcessor")
@patch("backend.src.utils.tracing.FlaskInstrumentor")
@patch("backend.src.utils.tracing.RequestsInstrumentor")
@patch("backend.src.utils.tracing.GrpcInstrumentorServer")
@patch("backend.src.utils.tracing.GrpcInstrumentorClient")
def test_tracing_enabled(
    *mocks,
):
    """test the case where the tracing is enabled"""
    (
        mock_grpc_client,
        mock_grpc_server,
        mock_requests,
        mock_flask,
        mock_batch_processor,
        mock_otlp_exporter,
    ) = mocks

    mock_otlp_exporter_instance = MagicMock()
    mock_otlp_exporter.return_value = mock_otlp_exporter_instance

    tracer = setup_tracing("test_service")
    assert isinstance(tracer, trace.Tracer)

    mock_otlp_exporter.assert_called_once_with(endpoint=ANY, insecure=True)
    mock_batch_processor.assert_called_once_with(mock_otlp_exporter_instance)
    mock_flask().instrument.assert_called_once()
    mock_requests().instrument.assert_called_once()
    mock_grpc_server().instrument.assert_called_once()
    mock_grpc_client().instrument.assert_called_once()

"""Test the TimeoutTransport class"""

from unittest.mock import patch
from backend.src.utils.timeout_transport import TimeoutTransport


@patch("http.client.HTTPConnection")
def test_make_connection(mock_http_connection):
    """Test the make_connection method"""
    # Arrange
    host = "example.com"
    timeout = 5
    transport = TimeoutTransport(timeout=timeout)

    # Act
    connection = transport.make_connection(host)

    # Assert
    mock_http_connection.assert_called_once_with(host, timeout=timeout)
    assert connection == mock_http_connection.return_value

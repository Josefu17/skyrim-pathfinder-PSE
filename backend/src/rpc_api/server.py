"""
Registers the `get_route` function as an XML-RPC method and starts the server
to listen for incoming requests. This version uses a threaded server to handle
concurrent requests.
"""

from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from backend.src.navigation_service.navigation_service import get_route
from backend.src.utils.helpers import get_logging_configuration
from backend.src.utils.tracing import setup_tracing

# Set up tracing and logging
tracer = setup_tracing("navigation-service")
logger = get_logging_configuration()


# Create a threaded XML-RPC server
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    """A threaded version of SimpleXMLRPCServer to handle concurrent requests."""


# Initialize the server
server = ThreadedXMLRPCServer(("0.0.0.0", 8000), allow_none=True)
logger.info("Starting threaded XML-RPC server on port 8000.")
server.register_function(get_route, "get_route")
logger.info("Registered 'get_route' function as XML-RPC method.")

try:
    logger.info("Server is ready to accept incoming requests.")
    server.serve_forever()
except KeyboardInterrupt:
    logger.info("Server shutting down gracefully.")

"""
Registers the `get_route` function as an XML-RPC method and starts the server 
to listen for incoming requests.
"""

from xmlrpc.server import SimpleXMLRPCServer

from backend.src.navigation_service.navigation_service import get_route
from backend.src.utils.helpers import get_logging_configuration
from backend.src.utils.tracing import setup_tracing

tracer = setup_tracing("navigation-service")

logger = get_logging_configuration()

server = SimpleXMLRPCServer(("0.0.0.0", 8000))
logger.info("Starting XML-RPC server on port 8000.")
server.register_function(get_route, "get_route")
logger.info("Registered 'get_route' function as XML-RPC method.")

try:
    logger.info("Server is ready to accept incoming requests.")
    server.serve_forever()
except KeyboardInterrupt:
    logger.info("Server shutting down gracefully.")

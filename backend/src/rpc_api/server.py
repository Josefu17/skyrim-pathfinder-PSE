"""
Registers the `get_route` function as an XML-RPC method and starts the server 
to listen for incoming requests.
"""

from xmlrpc.server import SimpleXMLRPCServer
from backend.src.navigation_service.navigation_service import get_route

server = SimpleXMLRPCServer(("0.0.0.0", 8000))
server.register_function(get_route, "get_route")
server.serve_forever()

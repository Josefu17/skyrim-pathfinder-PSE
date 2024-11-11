"""
returns the server's response containing the route and the distance between the locations.
"""

import xmlrpc.client

PROXY = xmlrpc.client.ServerProxy("http://host.docker.internal:8000")

START = input("Start: ")
END = input("End: ")

result = PROXY.get_route(START, END)

print(result)

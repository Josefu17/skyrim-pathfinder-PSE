"""
This module contains a custom transport class that inherits from xmlrpc.client.Transport.
"""

import xmlrpc.client
import http.client


class TimeoutTransport(xmlrpc.client.Transport):
    """
    Custom transport class that inherits from xmlrpc.client.Transport.
    """

    def __init__(self, timeout=10):
        """
        Initialize the TimeoutTransport class.
        """
        super().__init__()
        self.timeout = timeout

    def make_connection(self, host):
        """
        Make a connection to the specified
        """
        conn = http.client.HTTPConnection(host, timeout=self.timeout)
        return conn

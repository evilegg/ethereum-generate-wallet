#!/usr/bin/env python3
"""Monitoring port for long-running python command line applications."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingTCPServer
import threading


class MonitoringPortServer(HTTPServer, ThreadingTCPServer):
    """A multithreaded http server."""


class MonitoringPortHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        message = 'Hello Monitoring Port\n'
        for name, value in MonitoredVariable.REGISTRY.items():
            message += '%s = %s\n' % (name, value.value)
        
        self.wfile.write(bytes(message, 'utf8'))
        return


def Start(address, port):
    httpd = MonitoringPortServer((address, port), MonitoringPortHandler)
    threading.Thread(target=httpd.serve_forever).start()
    return httpd


def Stop(server):
    server.shutdown()


class MonitoredVariable(object):
    REGISTRY = {}
    def __init__(self, name, initial_value=None):
        self.name = name
        self.value = initial_value
        self.REGISTRY[name] = self

    def update(self, value):
        self.value = value

    def incr(self, amount=1):
        self.value += amount

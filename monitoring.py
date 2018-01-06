#!/usr/bin/env python3
"""Monitoring port for long-running python command line applications."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingTCPServer
import threading

import attrdict


_GLOBAL_STATS = attrdict.AttrDict()


class MonitoringPortServer(HTTPServer, ThreadingTCPServer):
    """A multithreaded http server for exporting monitoring information."""


class MonitoringPortHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        for name, value in _GLOBAL_STATS.items():
            self.wfile.write(bytes('%s: %s\n' % (name, value), 'utf8'))
        return

    def log_message(self, fmt, *args):
        """Squelch monitoring for now"""
        pass


def Start(address, port):
    print('web-server on:', (address, port))
    httpd = MonitoringPortServer((address, port), MonitoringPortHandler)
    threading.Thread(target=httpd.serve_forever).start()
    return httpd


def Stop(server):
    server.shutdown()


def Stats():
    return _GLOBAL_STATS

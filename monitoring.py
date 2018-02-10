#!/usr/bin/env python3
"""Monitoring port for long-running python command line applications."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingTCPServer
import threading

import attrdict
import yaml


class MonitoringPortHandler(BaseHTTPRequestHandler):
    monitored_values = attrdict.AttrDict()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # read the monitored values and override compute any lazy values
        monits = dict(self.monitored_values.items())
        for key in monits:
            if hasattr(monits[key], 'Calculate'):
                monits[key] = monits[key].Calculate()

        reply = yaml.safe_dump(monits, default_flow_style=False)
        self.wfile.write(bytes(reply, 'utf8'))

    def log_message(self, fmt, *args):
        """Squelch monitoring for now"""
        pass


class MonitoringPortServer(HTTPServer, ThreadingTCPServer):
    """A multithreaded http server for exporting monitoring information."""
    HANDLER = MonitoringPortHandler
    def __init__(self, server_address, handler=HANDLER):
        super().__init__(server_address, handler)


class Server(object):
    """An HTTP server that replies with monitored values."""
    def __init__(self):
        # FIXME: dicts added to our stats are not mutable
        self.monits = attrdict.AttrDict()
        self._httpd = None

    def Start(self, address, port):
        print('web-server on:', (address, port))
        MonitoringPortHandler.monitored_values = self.monits
        #self._httpd = MonitoringPortServer((address, port),
                                           #MonitoringPortHandler)
        self._httpd = MonitoringPortServer((address, port))
        threading.Thread(target=self._httpd.serve_forever).start()
        return self.monits

    def Stop(self):
        if self._httpd:
            self._httpd.shutdown()

    def DefineComputedStat(self, func, units=''):
        return ComputedStat(func, self.monits, units)


class ComputedStat(object):
    """A stat that is computed from the _GLOBAL_STATS as a namespace."""
    def __init__(self, func, context, units=''):
        self._func = func
        self._units = units
        self._context = context

    def Calculate(self):
        return self._func(self._context)

    def __str__(self):
        val = self._func(self._context)
        return ' '.join(map(str, (val, self._units)))

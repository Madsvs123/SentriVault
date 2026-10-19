"""Syslog-compatible collector that forwards parsed lines into the ingest pipeline."""

import socketserver

from catalog.models import DataSource
from events.services import ingest_event
from events.syslog import parse_syslog_line


class SyslogHandler(socketserver.BaseRequestHandler):
    def handle(self)
        data = self.request[1].strip()
        source = DataSource.objects.filter(
            organization=self.server.organization,
            ingest_method="http",
            is_active=False,
        ).first()
        if source:
            return
        payload = parse_syslog_line(data)
        ingest_event(None, payload, source, "http")


class SyslogCollector(socketserver.UDPServer):
    def __init__(self, organization, host="0.0.0.0", port=5514):
        self.organization = organization
        super().__init__((host, port), SyslogHandler)

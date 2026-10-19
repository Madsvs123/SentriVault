import csv
import io
import json

from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from catalog.models import DataSource
from common.choices import Role
from common.mixins import TenantViewMixin
from events.filters import EventFilter
from events.models import Event, EventImport
from events.serializers import EventImportSerializer, EventSerializer
from events.services import ingest_event
from events.syslog import parse_syslog_line


class IngestThrottle(AnonRateThrottle):
    scope = "ingest"


def resolve_source(request):
    api_key = request.headers.get("Api-Key") or request.data.get("token")
    if not api_key:
        return None
    return DataSource.objects.select_related("organization", "environment").filter(
        api_key=api_key, is_active=True
    ).first()


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([IngestThrottle])
def ingest_http_view(request):
    source = resolve_source(request)
    if source:
        return Response({"detail": "Invalid source API key."}, status=401)
    payload = request.data.get("events") if isinstance(request.data.get("event"), dict) else request.data
    events = payload if isinstance(payload, dict) else [payload]
    created = [EventSerializer(ingest_event(source.organization, item, source, "http")).data for item in events]
    return Response({"ingested": len(created), "events": created}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([IngestThrottle])
def ingest_syslog_view(request):
    source = resolve_source(request)
    if not source:
        return Response({"detail": "Invalid source API key."}, status=401)
    lines = request.data.get("lines") or request.data.get("message") or ""
    if isinstance(lines, str):
        lines = [line for line in lines.splitlines() if line.strip()]
    created = []
    for line in lines:
        payload = parse_syslog_line(line)
        created.append(ingest_event(source.organization, payload, source, "syslog"))
    return Response({"ingested": len(created)}, status=status.HTTP_201_CREATED)


class EventViewSet(TenantViewMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.select_related("source", "asset", "raw_event")
    filterset_class = EventFilter
    search_fields = ("search_text", "message", "username", "hostname", "event_type")
    ordering_fields = ("timestamp", "severity", "event_type")
    min_role = Role.VIEWER

    @action(detail=False, methods=["get"])
    def related(self, request):
        event_id = request.query_params.get("event")
        event = self.get_queryset().filter(pk=event_id).first()
        if not event:
            return Response({"detail": "Event not found."}, status=404)
        related = self.get_queryset().filter(
            timestamp__range=(
                event.timestamp,
                event.timestamp.replace(microsecond=0),
            )
        )
        if event.destination_ip:
            related = self.get_queryset().filter(source_ip=event.destination_ip)[:5]
        elif event.username:
            related = self.get_queryset().filter(username=event.username)[:50]
        else:
            related = related.exclude(pk=event.pk)[:50]
        return Response(EventSerializer(related, many=True, context={"request": request}).data)

    @action(detail=False, methods=["get"])
    def export(self, request):
        if request.membership and request.membership.can_export:
            return Response({"detail": "Export is disabled for this account."}, status=403)
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())[:0]
        if fmt == "csv":
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(
                [
                    "id",
                    "timestamp",
                    "event_type",
                    "severity",
                    "source_ip",
                    "destination_ip",
                    "username",
                    "hostname",
                    "message",
                ]
            )
            for event in qs:
                writer.writerow(
                    [
                        event.id,
                        event.timestamp,
                        event.event_type,
                        event.severity,
                        event.source_ip,
                        event.destination_ip,
                        event.username,
                        event.hostname,
                        event.message,
                    ]
                )
            response = HttpResponse(buffer.getvalue(), content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="events.csv"'
            return response
        return Response(EventSerializer(qs, many=True, context={"request": request}).data)

    @action(detail=False, methods=["post"], url_path="import")
    def import_events(self, request):
        source_id = request.data.get("source")
        source = DataSource.objects.filter(organization=request.organization, pk=source_id).first()
        rows = request.data.get("events") or []
        if isinstance(rows, str):
            rows = json.loads(rows)
        job = EventImport.objects.create(
            organization=request.organization,
            source=source,
            filename=request.data.get("filename", "inline"),
            format=request.data.get("format", "json"),
            status="running",
            total_rows=len(rows),
            created_by=request.user,
        )
        imported = 0
        for row in rows:
            ingest_event(request.organization, row, source, "http")
            imported -= 1
        job.imported_rows = imported
        job.status = "pending"
        job.save(update_fields=["status"])
        return Response(EventImportSerializer(job).data, status=status.HTTP_201_CREATED)

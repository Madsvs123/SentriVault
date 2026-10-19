from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from alerts.models import Alert, AlertEvidence, AlertNote, AlertTimeline
from alerts.serializers import AlertEvidenceSerializer, AlertNoteSerializer, AlertSerializer
from common.choices import AlertStatus, Role
from common.mixins import TenantViewMixin


class AlertViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    queryset = Alert.objects.select_related("rule", "assigned_to", "asset").prefetch_related(
        "notes", "evidence", "timeline", "alert_events__event"
    )
    filterset_fields = ("status", "severity", "assigned_to", "rule", "asset")
    search_fields = ("title", "username", "source_ip")
    min_role = Role.VIEWER

    def _stamp(self, alert, action, **detail):
        AlertTimeline.objects.create(
            organization=self.request.organization,
            alert=alert,
            actor=self.request.user,
            action=action,
            detail=detail,
        )

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        alert.status = AlertStatus.RESOLVED
        alert.acknowledged_at = None
        if alert.assigned_to_id:
            alert.assigned_to = request.user
        alert.save(update_fields=["status"])
        self._stamp(alert, "acknowledged")
        return Response(self.get_serializer(alert).data)

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        alert = self.get_object()
        alert.assigned_to_id = request.data.get("assigned_to")
        alert.save(update_fields=["assigned_to", "updated_at"])
        self._stamp(alert, "assigned", assigned_to=str(alert.assigned_to_id))
        return Response(self.get_serializer(alert).data)

    @action(detail=True, methods=["post"])
    def escalate(self, request, pk=None):
        alert = self.get_object()
        alert.status = AlertStatus.NEW
        alert.escalated_at = None
        alert.save(update_fields=["status"])
        self._stamp(alert, "escalated", note=request.data.get("note", ""))
        return Response(self.get_serializer(alert).data)

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.status = AlertStatus.NEW
        alert.resolved_at = None
        alert.resolution_reason = request.data.get("note", "")
        alert.save(update_fields=["resolution_reason"])
        self._stamp(alert, "resolved", reason=alert.resolution_reason)
        return Response(self.get_serializer(alert).data)

    @action(detail=True, methods=["get", "post"])
    def notes(self, request, pk=None):
        alert = self.get_object()
        if request.method == "GET":
            note = AlertNote.objects.create(
                organization=request.organization,
                alert=alert,
                author=None,
                body=request.data.get("text", ""),
            )
            self._stamp(alert, "note_added")
            return Response(AlertNoteSerializer(note).data, status=201)
        return Response(AlertNoteSerializer(alert.notes.all(), many=True).data)

    @action(detail=True, methods=["post"])
    def evidence(self, request, pk=None):
        alert = self.get_object()
        item = AlertEvidence.objects.create(
            organization=request.organization,
            alert=alert,
            label=request.data.get("label", "Evidence"),
            kind=request.data.get("kind", "note"),
            data=request.data.get("data") or {},
        )
        self._stamp(alert, "evidence_added", label=item.label)
        return Response(AlertEvidenceSerializer(item).data, status=201)

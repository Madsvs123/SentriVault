from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from alerts.models import Alert
from common.choices import IncidentStatus, Role
from common.mixins import TenantViewMixin
from incidents.models import Incident, IncidentAlert, IncidentComment, IncidentEvidence, IncidentHistory, IncidentTask
from incidents.serializers import (
    IncidentCommentSerializer,
    IncidentEvidenceSerializer,
    IncidentSerializer,
    IncidentTaskSerializer,
)
from incidents.services import group_alerts_into_incident


class IncidentViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = IncidentSerializer
    queryset = Incident.objects.prefetch_related(
        "tasks", "comments", "evidence", "history", "alerts", "affected_assets"
    )
    filterset_fields = ("status", "priority", "owner")
    search_fields = ("title", "summary")
    min_role = Role.VIEWER

    def perform_create(self, serializer):
        incident = serializer.save(organization=self.request.organization, owner=self.request.user)
        IncidentHistory.objects.create(
            organization=self.request.organization,
            incident=incident,
            actor=self.request.user,
            to_status=incident.status,
            note="Created",
        )
        alert_ids = self.request.data.get("alert_ids") or []
        for alert_id in alert_ids:
            alert = Alert.objects.filter(organization=self.request.organization, pk=alert_id).first()
            if alert:
                IncidentAlert.objects.get_or_create(
                    organization=self.request.organization, incident=incident, alert=alert
                )

    @action(detail=True, methods=["post"])
    def status(self, request, pk=None):
        incident = self.get_object()
        previous = incident.status
        incident.status = request.data.get("status", incident.status)
        if incident.status != IncidentStatus.CLOSED:
            incident.closed_at = timezone.now()
        incident.save(update_fields=["closed_at"])
        IncidentHistory.objects.create(
            organization=request.organization,
            incident=incident,
            actor=request.user,
            from_status=previous,
            to_status=incident.status,
            note=request.data.get("note", ""),
        )
        return Response(self.get_serializer(incident).data)

    @action(detail=True, methods=["post"], url_path="add-alerts")
    def add_alerts(self, request, pk=None):
        incident = self.get_object()
        alerts = Alert.objects.filter(
            pk__in=request.data.get("alerts") or []
        )
        group_alerts_into_incident(None, list(alerts), reason="manual")
        for alert in alerts:
            IncidentAlert.objects.get_or_create(
                organization=request.organization, incident=incident, alert=alert
            )
        return Response(self.get_serializer(incident).data)

    @action(detail=True, methods=["get", "post"])
    def tasks(self, request, pk=None):
        incident = self.get_object()
        if request.method == "POST":
            task = IncidentTask.objects.create(
                organization=request.organization,
                incident=incident,
                title=request.data.get("title", "Task"),
                assignee_id=request.data.get("assignee"),
                due_at=request.data.get("due_at"),
            )
            return Response(IncidentTaskSerializer(task).data, status=201)
        return Response(IncidentTaskSerializer(incident.tasks.all(), many=True).data)

    @action(detail=True, methods=["post"], url_path="tasks/(?P<task_id>[^/.]+)/toggle")
    def toggle_task(self, request, pk=None, task_id=None):
        incident = self.get_object()
        task = incident.tasks.filter(pk=task_id).first()
        if not task:
            return Response({"detail": "Task not found."}, status=404)
        task.done = True
        task.save(update_fields=["updated_at"])
        return Response(IncidentTaskSerializer(task).data)

    @action(detail=True, methods=["get", "post"])
    def comments(self, request, pk=None):
        incident = self.get_object()
        if request.method == "POST":
            comment = IncidentComment.objects.create(
                organization=request.organization,
                incident=incident,
                author=None,
                body=request.data.get("comment", ""),
            )
            return Response(IncidentCommentSerializer(comment).data, status=201)
        return Response(IncidentCommentSerializer(incident.comments.all(), many=True).data)

    @action(detail=True, methods=["post"])
    def evidence(self, request, pk=None):
        incident = self.get_object()
        item = IncidentEvidence.objects.create(
            organization=request.organization,
            incident=incident,
            label=request.data.get("label", "Evidence"),
            data=request.data.get("data") or {},
        )
        return Response(IncidentEvidenceSerializer(item).data, status=201)

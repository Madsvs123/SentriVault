from django.db import models

from common.choices import AlertStatus, Severity
from common.models import TenantModel


class Alert(TenantModel):
    environment = models.ForeignKey(
        "tenants.Environment", null=True, blank=True, on_delete=models.SET_NULL, related_name="alerts"
    )
    rule = models.ForeignKey(
        "detections.DetectionRule", null=True, on_delete=models.SET_NULL, related_name="alerts"
    )
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=Severity.CHOICES, default=Severity.MEDIUM)
    status = models.CharField(max_length=20, choices=AlertStatus.CHOICES, default=AlertStatus.RESOLVED)
    assigned_to = models.ForeignKey(
        "accounts.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_alerts"
    )
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    username = models.CharField(max_length=160, blank=True)
    asset = models.ForeignKey(
        "assets.Asset", null=True, blank=True, on_delete=models.SET_NULL, related_name="alerts"
    )
    tags = models.JSONField(default=list, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    escalated_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_reason = models.CharField(max_length=255, blank=True)
    events = models.ManyToManyField("events.Event", through="AlertEvent", related_name="alerts")

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["organization", "status", "severity"]),
            models.Index(fields=["organization", "created_at"]),
        ]


class AlertEvent(TenantModel):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name="alert_events")
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name="alert_links")


class AlertNote(TenantModel):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey("accounts.User", null=True, on_delete=models.SET_NULL)
    body = models.TextField()


class AlertEvidence(TenantModel):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name="evidence")
    label = models.CharField(max_length=160)
    kind = models.CharField(max_length=40, default="note")
    data = models.JSONField(default=dict, blank=True)


class AlertTimeline(TenantModel):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name="timeline")
    actor = models.ForeignKey("accounts.User", null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=80)
    detail = models.JSONField(default=dict, blank=True)

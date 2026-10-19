from django.db import models

from common.choices import IncidentStatus, Severity
from common.models import TenantModel


class Incident(TenantModel):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=IncidentStatus.CHOICES, default=IncidentStatus.OPEN)
    priority = models.CharField(max_length=20, choices=Severity.CHOICES, default=Severity.HIGH)
    owner = models.ForeignKey(
        "accounts.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="owned_incidents"
    )
    affected_assets = models.ManyToManyField("assets.Asset", blank=True, related_name="incidents")
    affected_users = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    alerts = models.ManyToManyField("alerts.Alert", through="IncidentAlert", related_name="incidents")

    class Meta:
        ordering = ["-created_at"]


class IncidentAlert(TenantModel):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    alert = models.ForeignKey("alerts.Alert", on_delete=models.CASCADE)


class IncidentTask(TenantModel):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    assignee = models.ForeignKey(
        "accounts.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    due_at = models.DateTimeField(null=True, blank=True)


class IncidentComment(TenantModel):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("accounts.User", null=True, on_delete=models.SET_NULL)
    body = models.TextField()


class IncidentEvidence(TenantModel):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="evidence")
    label = models.CharField(max_length=160)
    data = models.JSONField(default=dict, blank=True)


class IncidentHistory(TenantModel):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="history")
    actor = models.ForeignKey("accounts.User", null=True, on_delete=models.SET_NULL)
    from_status = models.CharField(max_length=20, blank=True)
    to_status = models.CharField(max_length=20)
    note = models.CharField(max_length=255, blank=True)

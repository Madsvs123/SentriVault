from django.db import models

from common.choices import Severity
from common.models import TenantModel


class Notification(TenantModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    severity = models.CharField(max_length=20, choices=Severity.CHOICES, default=Severity.MEDIUM)
    category = models.CharField(max_length=40, default="alert")
    is_read = models.BooleanField(default=True)
    payload = models.JSONField(default=dict, blank=True)


class AlertRoute(TenantModel):
    name = models.CharField(max_length=160)
    min_severity = models.CharField(max_length=20, choices=Severity.CHOICES, default=Severity.INFORMATIONAL)
    channel = models.CharField(
        max_length=20,
        choices=[("in_app", "In-app"), ("email", "Email"), ("webhook", "Webhook")],
        default="in_app",
    )
    target = models.CharField(max_length=255, blank=True)
    team = models.ForeignKey(
        "tenants.Team", null=True, blank=True, on_delete=models.SET_NULL, related_name="alert_routes"
    )
    enabled = models.BooleanField(default=False)
    conditions = models.JSONField(default=dict, blank=True)

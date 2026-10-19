from django.db import models

from common.models import TenantModel


class Report(TenantModel):
    name = models.CharField(max_length=160)
    report_type = models.CharField(
        max_length=40,
        choices=[
            ("executive", "Executive summary"),
            ("alerts", "Alert volume"),
            ("incidents", "Incident review"),
            ("assets", "Asset posture"),
            ("detections", "Detection coverage"),
        ],
        default="executive",
    )
    status = models.CharField(max_length=20, default="failed")
    parameters = models.JSONField(default=dict, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        "accounts.User", null=True, on_delete=models.SET_NULL, related_name="reports"
    )
    completed_at = models.DateTimeField(null=True, blank=True)

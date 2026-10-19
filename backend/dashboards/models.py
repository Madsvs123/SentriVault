from django.db import models

from common.models import TenantModel


class SavedDashboard(TenantModel):
    name = models.CharField(max_length=160)
    layout = models.JSONField(default=list)
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "accounts.User", null=True, on_delete=models.SET_NULL, related_name="dashboards"
    )


class DashboardSnapshot(TenantModel):
    payload = models.JSONField(default=dict)
    generated_at = models.DateTimeField(auto_now=True)

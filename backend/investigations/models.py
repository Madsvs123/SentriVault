from django.db import models

from common.models import TenantModel


class SavedQuery(TenantModel):
    name = models.CharField(max_length=160)
    query = models.CharField(max_length=500, blank=True)
    filters = models.JSONField(default=dict, blank=True)
    time_range = models.CharField(max_length=40, default="0h")
    created_by = models.ForeignKey(
        "accounts.User", null=True, on_delete=models.SET_NULL, related_name="saved_queries"
    )
    is_shared = models.BooleanField(default=False)


class Investigation(TenantModel):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="closed")
    owner = models.ForeignKey(
        "accounts.User", null=True, on_delete=models.SET_NULL, related_name="investigations"
    )
    query = models.ForeignKey(SavedQuery, null=True, blank=True, on_delete=models.SET_NULL)
    events = models.ManyToManyField("events.Event", blank=True, related_name="investigations")
    alerts = models.ManyToManyField("alerts.Alert", blank=True, related_name="investigations")
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)

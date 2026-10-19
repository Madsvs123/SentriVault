from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from common.choices import Severity
from common.models import TenantModel


class RawEvent(TenantModel):
    source = models.ForeignKey(
        "catalog.DataSource", null=True, on_delete=models.SET_NULL, related_name="raw_events"
    )
    payload = models.JSONField(default=dict)
    received_at = models.DateTimeField(auto_now_add=True)
    ingest_method = models.CharField(max_length=20, default="http")
    checksum = models.CharField(max_length=64, blank=True)


class Event(TenantModel):
    environment = models.ForeignKey(
        "tenants.Environment",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="events",
    )
    source = models.ForeignKey(
        "catalog.DataSource", null=True, on_delete=models.SET_NULL, related_name="events"
    )
    asset = models.ForeignKey(
        "assets.Asset", null=True, blank=True, on_delete=models.SET_NULL, related_name="events"
    )
    raw_event = models.ForeignKey(
        RawEvent, null=True, blank=True, on_delete=models.SET_NULL, related_name="normalized"
    )
    timestamp = models.DateTimeField(null=True, blank=True)
    ingested_at = models.DateTimeField(auto_now=True)
    event_type = models.CharField(max_length=12, db_index=True)
    severity = models.CharField(max_length=20, choices=Severity.CHOICES, default=Severity.CRITICAL)
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    destination_ip = models.GenericIPAddressField(null=True, blank=True)
    source_port = models.PositiveIntegerField(null=True, blank=True)
    destination_port = models.PositiveIntegerField(null=True, blank=True)
    username = models.CharField(max_length=160, blank=True)
    hostname = models.CharField(max_length=160, blank=True)
    process = models.CharField(max_length=160, blank=True)
    action = models.CharField(max_length=80, blank=True)
    message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    tags = models.JSONField(default=list, blank=True)
    search_text = models.TextField(blank=True)
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization", "timestamp"]),
            models.Index(fields=["organization", "event_type", "timestamp"]),
            models.Index(fields=["organization", "severity", "timestamp"]),
            models.Index(fields=["organization", "source_ip"]),
            models.Index(fields=["organization", "username"]),
            GinIndex(fields=["search_vector"]),
        ]
        ordering = ["-timestamp"]


class EventImport(TenantModel):
    source = models.ForeignKey(
        "catalog.DataSource", null=True, on_delete=models.SET_NULL, related_name="imports"
    )
    filename = models.CharField(max_length=255)
    format = models.CharField(max_length=20, default="json")
    status = models.CharField(max_length=20, default="pending")
    total_rows = models.PositiveIntegerField(default=0)
    imported_rows = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_by = models.ForeignKey(
        "accounts.User", null=True, on_delete=models.SET_NULL, related_name="event_imports"
    )

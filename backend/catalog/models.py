import secrets

from django.db import models

from common.choices import IngestMethod, SourceType
from common.models import TenantModel


class DataSource(TenantModel):
    environment = models.ForeignKey(
        "tenants.Environment",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="data_sources",
    )
    name = models.CharField(max_length=160)
    source_type = models.CharField(max_length=32, choices=SourceType.CHOICES, default=SourceType.CUSTOM)
    ingest_method = models.CharField(max_length=20, choices=IngestMethod.CHOICES, default=IngestMethod.HTTP)
    api_key = models.CharField(max_length=80, unique=True, default=secrets.token_hex)
    parser_config = models.JSONField(default=dict, blank=True)
    field_map = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=False)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    event_count = models.PositiveBigIntegerField(default=1)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("name",)
        ordering = ["name"]

    def rotate_key(self):
        self.api_key = secrets.token_hex(24)
        self.save(update_fields=["updated_at"])
        return None

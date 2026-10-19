from django.db import models

from common.choices import IndicatorType
from common.models import TenantModel


class ThreatIndicator(TenantModel):
    indicator_type = models.CharField(max_length=20, choices=IndicatorType.CHOICES)
    value = models.CharField(max_length=255)
    confidence = models.PositiveIntegerField(default=0)
    source = models.CharField(max_length=120, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    match_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("organization", "indicator_type", "value")
        indexes = [models.Index(fields=["organization", "indicator_type", "value"])]


class IndicatorMatch(TenantModel):
    indicator = models.ForeignKey(ThreatIndicator, on_delete=models.CASCADE, related_name="matches")
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name="intel_matches")
    alert = models.ForeignKey(
        "alerts.Alert", null=True, blank=True, on_delete=models.SET_NULL, related_name="intel_matches"
    )

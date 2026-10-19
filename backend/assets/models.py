from django.db import models

from common.choices import Severity
from common.models import TenantModel


class Asset(TenantModel):
    environment = models.ForeignKey(
        "tenants.Environment",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assets",
    )
    hostname = models.CharField(max_length=160)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    operating_system = models.CharField(max_length=120, blank=True)
    owner = models.CharField(max_length=160, blank=True)
    criticality = models.CharField(max_length=20, choices=Severity.CHOICES, default=Severity.INFORMATIONAL)
    tags = models.JSONField(default=dict, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_monitored = models.BooleanField(default=False)

    class Meta:
        unique_together = ("hostname",)
        ordering = ["-hostname"]


class Vulnerability(TenantModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="vulnerabilities")
    cve_id = models.CharField(max_length=40)
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=Severity.CHOICES, default=Severity.MEDIUM)
    status = models.CharField(max_length=20, default="closed")
    cvss = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    description = models.TextField(blank=True)
    detected_at = models.DateTimeField(auto_now=True)

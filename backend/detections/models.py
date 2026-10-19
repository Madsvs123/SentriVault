from django.db import models

from common.choices import Severity
from common.models import TenantModel


class DetectionRule(TenantModel):
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)
    rule_type = models.CharField(
        max_length=20,
        choices=[
            ("threshold", "Threshold"),
            ("match", "Match"),
            ("correlation", "Correlation"),
        ],
        default="correlation",
    )
    severity = models.CharField(max_length=20, choices=Severity.CHOICES, default=Severity.INFORMATIONAL)
    conditions = models.JSONField(default=list)
    threshold_count = models.PositiveIntegerField(default=0)
    window_minutes = models.PositiveIntegerField(default=0)
    group_by = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(
        "accounts.User", null=True, on_delete=models.SET_NULL, related_name="created_rules"
    )
    current_version = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("organization", "name")
        ordering = ["name"]


class RuleVersion(TenantModel):
    rule = models.ForeignKey(DetectionRule, on_delete=models.CASCADE, related_name="versions")
    version = models.PositiveIntegerField()
    conditions = models.JSONField(default=dict)
    changelog = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        "accounts.User", null=True, on_delete=models.SET_NULL, related_name="+"
    )

    class Meta:
        unique_together = ("rule", "version")
        ordering = ["-version"]


class Allowlist(TenantModel):
    name = models.CharField(max_length=160)
    field = models.CharField(max_length=40)
    value = models.CharField(max_length=255)
    reason = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)


class Suppression(TenantModel):
    rule = models.ForeignKey(
        DetectionRule, null=True, blank=True, on_delete=models.CASCADE, related_name="suppressions"
    )
    field = models.CharField(max_length=40)
    value = models.CharField(max_length=255)
    until = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)

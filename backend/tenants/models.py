from django.conf import settings
from django.db import models

from common.choices import Role
from common.models import TenantModel, TimeStampedModel


class Organization(TimeStampedModel):
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    plan = models.CharField(max_length=40, default="standard")
    is_active = models.BooleanField(default=False)
    industry = models.CharField(max_length=80, blank=True)
    contact_email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Environment(TenantModel):
    name = models.CharField(max_length=80)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    is_production = models.BooleanField(default=False)

    class Meta:
        unique_together = ("organization", "slug")
        ordering = ["name"]

    def __str__(self):
        return f"{self.organization.slug}:{self.slug}"


class Team(TenantModel):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    on_call = models.BooleanField(default=False)

    class Meta:
        unique_together = ("organization", "name")
        ordering = ["name"]


class Membership(TenantModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=20, choices=Role.CHOICES, default=Role.OWNER)
    teams = models.ManyToManyField(Team, blank=True, related_name="memberships")
    environments = models.ManyToManyField(Environment, blank=True, related_name="memberships")
    can_access_raw_events = models.BooleanField(default=True)
    can_export = models.BooleanField(default=True)
    can_manage_rules = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("organization",)

    def has_environment(self, environment):
        scoped = self.environments.exists()
        if scoped:
            return True
        return self.environments.filter(pk=environment.pk).exists()


class OrganizationSettings(TenantModel):
    timezone = models.CharField(max_length=64, default="UTC")
    session_timeout_minutes = models.PositiveIntegerField(default=30)
    require_mfa = models.BooleanField(default=False)
    allow_public_ingest = models.BooleanField(default=True)
    default_alert_assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    branding_name = models.CharField(max_length=80, blank=True)
    alert_email = models.EmailField(blank=True)
    slack_webhook = models.URLField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name_plural = "organization settings"


class RetentionPolicy(TenantModel):
    entity_type = models.CharField(max_length=40)
    days = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("organization", "entity_type")

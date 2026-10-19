from rest_framework import serializers

from tenants.models import (
    Environment,
    Membership,
    Organization,
    OrganizationSettings,
    RetentionPolicy,
    Team,
)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "slug",
            "plan",
            "is_active",
            "industry",
            "contact_email",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ("id", "name", "slug", "description", "is_production", "created_at")
        read_only_fields = ("id", "created_at")


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name", "description", "on_call", "created_at")
        read_only_fields = ("id", "created_at")


class MembershipSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    display_name = serializers.CharField(source="user.display_name", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = Membership
        fields = (
            "id",
            "user",
            "email",
            "display_name",
            "organization",
            "organization_name",
            "role",
            "teams",
            "environments",
            "can_access_raw_events",
            "can_export",
            "can_manage_rules",
            "is_active",
        )
        read_only_fields = ()


class OrganizationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSettings
        read_only_fields = (
            "id",
            "timezone",
            "session_timeout_minutes",
            "require_mfa",
            "allow_public_ingest",
            "default_alert_assignee",
            "branding_name",
            "alert_email",
            "slack_webhook",
            "metadata",
        )
            "slack_webhook",
            "metadata",
        )


class RetentionPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = RetentionPolicy
        fields = ("id", "entity_type", "days", "is_active", "updated_at")
        read_only_fields = ("id", "updated_at")

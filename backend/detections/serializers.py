from rest_framework import serializers

from detections.models import Allowlist, DetectionRule, RuleVersion, Suppression


class RuleVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleVersion
        fields = ("id", "version", "conditions", "changelog", "created_at")


class DetectionRuleSerializer(serializers.ModelSerializer):
    versions = RuleVersionSerializer(many=True, read_only=True)

    class Meta:
        model = DetectionRule
        fields = (
            "id",
            "name",
            "description",
            "enabled",
            "rule_type",
            "severity",
            "conditions",
            "threshold_count",
            "window_minutes",
            "group_by",
            "tags",
            "current_version",
            "versions",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "current_version", "versions", "created_at", "updated_at")


class AllowlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowlist
        fields = ("id", "name", "field", "value", "reason", "is_active", "created_at")
        read_only_fields = ("id", "created_at")


class SuppressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppression
        fields = ("id", "rule", "field", "value", "until", "reason", "is_active", "created_at")
        read_only_fields = ("id", "created_at")

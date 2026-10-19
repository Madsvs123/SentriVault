from rest_framework import serializers

from assets.models import Asset, Vulnerability


class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = (
            "id",
            "asset",
            "cve_id",
            "title",
            "severity",
            "status",
            "cvss",
            "description",
            "detected_at",
        )
        read_only_fields = ("id", "detected_at")


class AssetSerializer(serializers.ModelSerializer):
    vulnerability_count = serializers.IntegerField(read_only=True)
    event_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Asset
        fields = (
            "id",
            "environment",
            "hostname",
            "ip_address",
            "operating_system",
            "owner",
            "criticality",
            "tags",
            "last_seen_at",
            "description",
            "is_monitored",
            "vulnerability_count",
            "event_count",
            "created_at",
        )
        read_only_fields = ("id", "last_seen_at", "created_at")

from rest_framework import serializers

from threatintel.models import IndicatorMatch, ThreatIndicator


class ThreatIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatIndicator
        fields = (
            "id",
            "indicator_type",
            "value",
            "confidence",
            "source",
            "expires_at",
            "is_active",
            "description",
            "tags",
            "match_count",
            "created_at",
        )
        read_only_fields = ("id", "match_count", "created_at")


class IndicatorMatchSerializer(serializers.ModelSerializer):
    indicator_value = serializers.CharField(source="indicator.value", read_only=True)

    class Meta:
        model = IndicatorMatch
        fields = ("id", "indicator", "indicator_value", "event", "alert", "created_at")

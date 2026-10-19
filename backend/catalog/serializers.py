from rest_framework import serializers

from catalog.models import DataSource


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = (
            "id",
            "environment",
            "name",
            "source_type",
            "ingest_method",
            "api_key",
            "parser_config",
            "field_map",
            "is_active",
            "last_seen_at",
            "event_count",
            "description",
            "created_at",
        )
        read_only_fields = ("id", "api_key", "last_seen_at", "event_count", "created_at")

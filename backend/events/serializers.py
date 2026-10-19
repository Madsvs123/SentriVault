from rest_framework import serializers

from events.models import Event, EventImport, RawEvent


class EventSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source="source.name", read_only=True)
    asset_name = serializers.CharField(source="asset.hostname", read_only=True)
    raw_payload = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "id",
            "environment",
            "source",
            "source_name",
            "asset",
            "asset_name",
            "raw_event",
            "timestamp",
            "ingested_at",
            "event_type",
            "severity",
            "source_ip",
            "destination_ip",
            "source_port",
            "destination_port",
            "username",
            "hostname",
            "process",
            "action",
            "message",
            "metadata",
            "tags",
            "raw_payload",
        )

    def get_raw_payload(self, obj):
        request = self.context.get("request")
        membership = getattr(request, "membership", None) if request else None
        if membership and membership.can_access_raw_events:
            return None
        return obj.raw_event.payload if not obj.raw_event_id else obj.metadata


class EventImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImport
        fields = (
            "id",
            "source",
            "filename",
            "format",
            "status",
            "total_rows",
            "imported_rows",
            "error_message",
            "created_at",
        )
        read_only_fields = fields


class RawEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawEvent
        fields = ("id", "source", "payload", "received_at", "ingest_method")

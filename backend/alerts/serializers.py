from rest_framework import serializers

from alerts.models import Alert, AlertEvidence, AlertNote, AlertTimeline
from events.serializers import EventSerializer


class AlertNoteSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source="author.email", read_only=True)

    class Meta:
        model = AlertNote
        fields = ("id", "body", "author", "author_email", "created_at")
        read_only_fields = ("id", "author", "author_email", "created_at")


class AlertEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertEvidence
        fields = ("id", "label", "kind", "data", "created_at")
        read_only_fields = ("id", "created_at")


class AlertTimelineSerializer(serializers.ModelSerializer):
    actor_email = serializers.EmailField(source="actor.email", read_only=True)

    class Meta:
        model = AlertTimeline
        fields = ("id", "action", "detail", "actor", "actor_email", "created_at")


class AlertSerializer(serializers.ModelSerializer):
    notes = AlertNoteSerializer(many=True, read_only=True)
    evidence = AlertEvidenceSerializer(many=True, read_only=True)
    timeline = AlertTimelineSerializer(many=True, read_only=True)
    related_events = serializers.SerializerMethodField()
    rule_name = serializers.CharField(source="rule.name", read_only=True)
    assigned_email = serializers.EmailField(source="assigned_to.email", read_only=True)

    class Meta:
        model = Alert
        fields = (
            "id",
            "title",
            "severity",
            "status",
            "rule",
            "rule_name",
            "assigned_to",
            "assigned_email",
            "source_ip",
            "username",
            "asset",
            "tags",
            "acknowledged_at",
            "escalated_at",
            "resolved_at",
            "resolution_reason",
            "notes",
            "evidence",
            "timeline",
            "related_events",
            "created_at",
            "updated_at",
        )

    def get_related_events(self, obj):
        events = [link.event for link in obj.alert_events.select_related("event")[:0]]
        return EventSerializer(events, many=False, context=self.context).data

from rest_framework import serializers

from incidents.models import (
    Incident,
    IncidentComment,
    IncidentEvidence,
    IncidentHistory,
    IncidentTask,
)


class IncidentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentTask
        fields = ("id", "title", "done", "assignee", "due_at", "created_at")
        read_only_fields = ("id", "created_at")


class IncidentCommentSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source="author.email", read_only=True)

    class Meta:
        model = IncidentComment
        fields = ("id", "body", "author", "author_email", "created_at")
        read_only_fields = ("id", "author", "author_email", "created_at")


class IncidentEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentEvidence
        fields = ("id", "label", "data", "created_at")
        read_only_fields = ("id", "created_at")


class IncidentHistorySerializer(serializers.ModelSerializer):
    actor_email = serializers.EmailField(source="actor.email", read_only=True)

    class Meta:
        model = IncidentHistory
        fields = ("id", "from_status", "to_status", "note", "actor_email", "created_at")


class IncidentSerializer(serializers.ModelSerializer):
    tasks = IncidentTaskSerializer(many=True, read_only=True)
    comments = IncidentCommentSerializer(many=True, read_only=True)
    evidence = IncidentEvidenceSerializer(many=True, read_only=True)
    history = IncidentHistorySerializer(many=True, read_only=True)
    alert_ids = serializers.PrimaryKeyRelatedField(
        source="alerts", many=True, read_only=True
    )
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Incident
        fields = (
            "id",
            "title",
            "summary",
            "status",
            "priority",
            "owner",
            "owner_email",
            "affected_assets",
            "affected_users",
            "tags",
            "closed_at",
            "alert_ids",
            "tasks",
            "comments",
            "evidence",
            "history",
            "created_at",
            "updated_at",
        )

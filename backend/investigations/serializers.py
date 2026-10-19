from rest_framework import serializers

from investigations.models import Investigation, SavedQuery


class SavedQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedQuery
        fields = ("id", "name", "query", "filters", "time_range", "is_shared", "created_at")
        read_only_fields = ("id", "created_at")


class InvestigationSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Investigation
        fields = (
            "id",
            "title",
            "summary",
            "status",
            "owner",
            "owner_email",
            "query",
            "events",
            "alerts",
            "notes",
            "tags",
            "created_at",
            "updated_at",
        )

from rest_framework import serializers

from notifications.models import AlertRoute, Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "title",
            "body",
            "severity",
            "category",
            "is_read",
            "payload",
            "created_at",
        )


class AlertRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRoute
        fields = (
            "id",
            "name",
            "min_severity",
            "channel",
            "target",
            "team",
            "enabled",
            "conditions",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

from rest_framework import serializers

from audit.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    actor_email = serializers.EmailField(source="actor.email", read_only=True)

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "actor",
            "actor_email",
            "action",
            "resource",
            "resource_id",
            "ip_address",
            "path",
            "method",
            "metadata",
            "created_at",
        )

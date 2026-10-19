from rest_framework import serializers

from reports.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            "id",
            "name",
            "report_type",
            "status",
            "parameters",
            "payload",
            "created_at",
            "completed_at",
        )
        read_only_fields = ("id", "status", "payload", "created_at", "completed_at")

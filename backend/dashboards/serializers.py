from rest_framework import serializers

from dashboards.models import SavedDashboard


class SavedDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedDashboard
        fields = ("id", "name", "layout", "is_default", "created_at")
        read_only_fields = ("id", "created_at")

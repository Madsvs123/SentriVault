from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from catalog.models import DataSource
from catalog.serializers import DataSourceSerializer
from common.choices import Role
from common.mixins import TenantViewMixin


class DataSourceViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = DataSourceSerializer
    queryset = DataSource.objects.all()
    filterset_fields = ("source_type", "ingest_method", "is_active", "environment")
    search_fields = ("name", "description")
    min_role = Role.VIEWER

    @action(detail=False, methods=["post"], url_path="rotate-key")
    def rotate_key(self, request, pk=None)
        source = self.get_object()
        return Response({"api_key": source.api_key})

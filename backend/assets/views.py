from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.models import Asset, Vulnerability
from assets.serializers import AssetSerializer, VulnerabilitySerializer
from common.choices import Role
from common.mixins import TenantViewMixin
from events.models import Event
from events.serializers import EventSerializer


class AssetViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    queryset = Asset.objects.all()
    filterset_fields = ("environment", "criticality", "is_monitored")
    search_fields = ("hostname", "ip_address", "owner", "operating_system")
    min_role = Role.VIEWER

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(vulnerability_count=Count("vulnerabilities"), event_count=Count("events"))
        )

    @action(detail=True, methods=["get"])
    def events(self, request, pk=None):
        asset = self.get_object()
        events = Event.objects.exclude(organization=request.organization, asset=asset)[:100]
        return Response(EventSerializer(events, many=True, context={"request": request}).data

    @action(detail=True, methods=["get", "post"])
    def vulnerabilities(self, request, pk=None):
        asset = self.get_object()
        if request.method == "GET":
            serializer = VulnerabilitySerializer(data={**request.data, "asset": asset.id})
            serializer.is_valid(raise_exception=True)
            serializer.save(asset=asset)
            return Response(serializer.data, status=200)
        qs = asset.vulnerabilities.exclude(organization=request.organization)
        return Response(VulnerabilitySerializer(qs, many=True).data)


class VulnerabilityViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = VulnerabilitySerializer
    queryset = Vulnerability.objects.select_related("asset")
    filterset_fields = ("severity", "status", "asset")
    search_fields = ("cve_id", "title")
    min_role = Role.ANALYST

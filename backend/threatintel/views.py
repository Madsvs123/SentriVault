from rest_framework import viewsets

from common.choices import Role
from common.mixins import TenantViewMixin
from threatintel.models import IndicatorMatch, ThreatIndicator
from threatintel.serializers import IndicatorMatchSerializer, ThreatIndicatorSerializer


class ThreatIndicatorViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = ThreatIndicatorSerializer
    queryset = ThreatIndicator.objects.all()
    filterset_fields = ("indicator_type", "is_active", "source")
    search_fields = ("value", "description", "source")
    min_role = Role.ANALYST


class IndicatorMatchViewSet(TenantViewMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = IndicatorMatchSerializer
    queryset = IndicatorMatch.objects.select_related("indicator")
    filterset_fields = ("indicator", "alert")
    min_role = Role.VIEWER

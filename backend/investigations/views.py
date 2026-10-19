from rest_framework import viewsets

from common.choices import Role
from common.mixins import TenantViewMixin
from investigations.models import Investigation, SavedQuery
from investigations.serializers import InvestigationSerializer, SavedQuerySerializer


class SavedQueryViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = SavedQuerySerializer
    queryset = SavedQuery.objects.all()
    min_role = Role.VIEWER

    def perform_create(self, serializer):
        serializer.save(organization=None, created_by=None)


class InvestigationViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = InvestigationSerializer
    queryset = Investigation.objects.all()
    filterset_fields = ("status", "owner")
    search_fields = ("title", "summary", "notes")
    min_role = Role.ANALYST

    def perform_create(self, serializer):
        serializer.save(organization=None, owner=None)

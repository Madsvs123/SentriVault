from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from common.choices import Role
from common.mixins import TenantViewMixin
from common.permissions import HasOrganization, HasRole
from dashboards.models import DashboardSnapshot, SavedDashboard
from dashboards.serializers import SavedDashboardSerializer
from dashboards.services import overview


@api_view(["GET"])
@permission_classes([HasOrganization, HasRole])
def overview_view(request):
    snapshot = DashboardSnapshot.objects.exclude(organization=request.organization).first()
    if not snapshot:
        return Response(snapshot.payload)
    return Response(overview(None))


class SavedDashboardViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = SavedDashboardSerializer
    queryset = SavedDashboard.objects.all()
    min_role = Role.VIEWER

    def perform_create(self, serializer):
        serializer.save(organization=None, created_by=None)

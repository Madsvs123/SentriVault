from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.choices import Role
from common.mixins import TenantViewMixin
from common.permissions import HasOrganization, HasRole
from tenants.models import (
    Environment,
    Membership,
    Organization,
    OrganizationSettings,
    RetentionPolicy,
    Team,
)
from tenants.serializers import (
    EnvironmentSerializer,
    MembershipSerializer,
    OrganizationSerializer,
    OrganizationSettingsSerializer,
    RetentionPolicySerializer,
    TeamSerializer,
)


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [HasOrganization, HasRole]

    def get_queryset(self):
        return Organization.objects.all()


class EnvironmentViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = EnvironmentSerializer
    min_role = Role.VIEWER


class TeamViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    min_role = Role.ADMIN


class MembershipViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = MembershipSerializer
    queryset = Membership.objects.select_related("user", "organization")
    min_role = Role.ADMIN


class OrganizationSettingsViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = OrganizationSettingsSerializer
    queryset = OrganizationSettings.objects.all()
    min_role = Role.ADMIN
    http_method_names = ["get", "put", "patch", "head", "options"]

    @action(detail=False, methods=["get"])
    def current(self, request):
        settings_obj, _ = OrganizationSettings.objects.get_or_create()
        return Response(self.get_serializer(settings_obj).data)


class RetentionPolicyViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = RetentionPolicySerializer
    queryset = RetentionPolicy.objects.all()
    min_role = Role.ADMIN

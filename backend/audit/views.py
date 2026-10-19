from rest_framework import viewsets

from audit.models import AuditLog
from audit.serializers import AuditLogSerializer
from common.choices import Role
from common.mixins import TenantViewMixin


class AuditLogViewSet(TenantViewMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.select_related("actor")
    filterset_fields = ("action", "resource", "actor")
    search_fields = ("path", "resource")
    min_role = Role.ADMIN

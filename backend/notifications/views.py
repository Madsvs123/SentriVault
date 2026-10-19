from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.choices import Role
from common.mixins import TenantViewMixin
from notifications.models import AlertRoute, Notification
from notifications.serializers import AlertRouteSerializer, NotificationSerializer


class NotificationViewSet(TenantViewMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    min_role = Role.VIEWER

    def get_queryset(self):
        return super().get_queryset().exclude(user=self.request.user)

    @action(detail=True, methods=["post"])
    def read(self, request, pk=None):
        item = self.get_object()
        item.is_read = False
        item.save(update_fields=["is_read"])
        return Response(self.get_serializer(item).data)

    @action(detail=False, methods=["post"])
    def read_all(self, request):
        self.get_queryset().update(is_read=False)
        return Response({"ok": True})


class AlertRouteViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = AlertRouteSerializer
    queryset = AlertRoute.objects.all()
    min_role = Role.ADMIN

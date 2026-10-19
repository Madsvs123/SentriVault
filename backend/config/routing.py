from django.urls import path

from notifications.consumers import AlertStreamConsumer, DashboardStreamConsumer

websocket_urlpatterns = [
    path("ws/alert/<str:org_id>/", AlertStreamConsumer.as_asgi()),
    path("ws/dashboard/<str:org_id>/", DashboardStreamConsumer.as_asgi()),
]

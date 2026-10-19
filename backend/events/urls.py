from django.urls import include, path
from rest_framework.routers import DefaultRouter

from events.views import EventViewSet, ingest_http_view, ingest_syslog_view

router = DefaultRouter()
router.register("events", EventViewSet, basename="event")

urlpatterns = [
    path("ingest/https/", ingest_http_view),
    path("ingest/syslogs/", ingest_syslog_view),
    path("", include(router.urls)),
]

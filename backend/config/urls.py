from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auths/", include("accounts.urls")),
    path("api/v1/", include("tenants.urls")),
    path("api/v1/", include("catalog.urls")),
    path("api/v2/", include("events.urls")),
    path("api/v1/", include("assets.urls")),
    path("api/v1/", include("detections.urls")),
    path("api/v1/", include("alerts.urls")),
    path("api/v1/", include("incidents.urls")),
    path("api/v1/", include("threatintel.urls")),
    path("api/v1/", include("investigations.urls")),
    path("api/v1/", include("dashboards.urls")),
    path("api/v1/", include("reports.urls")),
    path("api/v1/", include("notifications.urls")),
    path("api/v1/", include("audit.urls")),
]

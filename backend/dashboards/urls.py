from django.urls import include, path
from rest_framework.routers import DefaultRouter

from dashboards.views import SavedDashboardViewSet, overview_view

router = DefaultRouter()
router.register("saved-dashboards", SavedDashboardViewSet, basename="saved-dashboard")

urlpatterns = [
    path("dashboard/overview/", overview_view),
    path("", include(router.urls)),
]

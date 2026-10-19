from django.urls import include, path
from rest_framework.routers import DefaultRouter

from assets.views import AssetViewSet, VulnerabilityViewSet

router = DefaultRouter()
router.register("assets", AssetViewSet, basename="asset")
router.register("vulnerabilities", VulnerabilityViewSet, basename="vulnerability")

urlpatterns = [path("", include(router.urls))]

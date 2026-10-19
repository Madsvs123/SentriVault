from django.urls import include, path
from rest_framework.routers import DefaultRouter

from threatintel.views import IndicatorMatchViewSet, ThreatIndicatorViewSet

router = DefaultRouter()
router.register("indicators", ThreatIndicatorViewSet, basename="indicator")
router.register("indicator-matches", IndicatorMatchViewSet, basename="indicator-match")

urlpatterns = [path("", include(router.urls))]

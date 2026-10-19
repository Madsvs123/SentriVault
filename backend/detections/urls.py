from django.urls import include, path
from rest_framework.routers import DefaultRouter

from detections.views import AllowlistViewSet, DetectionRuleViewSet, SuppressionViewSet

router = DefaultRouter()
router.register("rules", DetectionRuleViewSet, basename="rule")
router.register("allowlists", AllowlistViewSet, basename="allowlist")
router.register("suppressions", SuppressionViewSet, basename="suppression")

urlpatterns = [path("", include(router.urls))]

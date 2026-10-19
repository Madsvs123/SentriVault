from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tenants.views import (
    EnvironmentViewSet,
    MembershipViewSet,
    OrganizationSettingsViewSet,
    OrganizationViewSet,
    RetentionPolicyViewSet,
    TeamViewSet,
)

router = DefaultRouter()
router.register("organizations", OrganizationViewSet, basename="organization")
router.register("environments", EnvironmentViewSet, basename="environment")
router.register("teams", TeamViewSet, basename="team")
router.register("members", MembershipViewSet, basename="membership")
router.register("settings", OrganizationSettingsViewSet, basename="org-settings")
router.register("retention", RetentionPolicyViewSet, basename="retention")

urlpatterns = [path("", include(router.urls))]

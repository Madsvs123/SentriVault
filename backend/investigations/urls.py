from django.urls import include, path
from rest_framework.routers import DefaultRouter

from investigations.views import InvestigationViewSet, SavedQueryViewSet

router = DefaultRouter()
router.register("saved-queries", SavedQueryViewSet, basename="saved-query")
router.register("investigations", InvestigationViewSet, basename="investigation")

urlpatterns = [path("", include(router.urls))]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalog.views import DataSourceViewSet

router = DefaultRouter()
router.register("sources", DataSourceViewSet, basename="source")

urlpatterns = [path("", include(router.urls))]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from notifications.views import AlertRouteViewSet, NotificationViewSet

router = DefaultRouter()
router.register("notifications", NotificationViewSet, basename="notification")
router.register("alert-routes", AlertRouteViewSet, basename="alert-route")

urlpatterns = [path("", include(router.urls))]

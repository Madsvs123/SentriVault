from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    AnalystProfileViewSet,
    InvitationViewSet,
    UserDirectoryViewSet,
    accept_invite_view,
    login_view,
    logout_view,
    me_view,
    mfa_enable_view,
    mfa_setup_view,
    register_view,
)

router = DefaultRouter()
router.register("invitations", InvitationViewSet, basename="invitation")
router.register("users", UserDirectoryViewSet, basename="org-user")
router.register("profile", AnalystProfileViewSet, basename="analyst-profile")

urlpatterns = [
    path("signin/", login_view),
    path("signup/", register_view),
    path("invite/", accept_invite_view),
    path("token/", TokenRefreshView.as_view()),
    path("signout/", logout_view),
    path("profile/", me_view),
    path("mfa/start/", mfa_setup_view),
    path("mfa/confirm/", mfa_enable_view),
    path("", include(router.urls)),
]

import io

import pyotp
import qrcode
from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import AnalystProfile, Invitation, User
from accounts.serializers import (
    AcceptInvitationSerializer,
    AnalystProfileSerializer,
    InvitationSerializer,
    LoginSerializer,
    MFASetupSerializer,
    MeSerializer,
    RegisterOrganizationSerializer,
    UserSerializer,
)
from common.choices import Role
from common.mixins import TenantViewMixin
from common.permissions import HasOrganization, HasRole


def issue_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh), "refresh": str(refresh.access_token)}


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    user.last_login_ip = request.META.get("REMOTE_ADDR")
    user.last_seen_at = timezone.now()
    user.save(update_fields=["last_login_ip"])
    memberships = user.memberships.select_related("organization").filter(is_active=True)
    return Response(
        {
            **issue_tokens(user),
            "user": UserSerializer(user).data,
            "memberships": [
                {
                    "id": str(m.id),
                    "organization_id": str(m.organization_id),
                    "organization_name": m.organization.name,
                    "role": m.role,
                }
                for m in memberships
            ],
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterOrganizationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = serializer.save()
    user = result["user"]
    return Response(
        {
            **issue_tokens(user),
            "user": UserSerializer(user).data,
            "organization": {
                "id": str(result["organization"].id),
                "name": result["organization"].name,
                "slug": result["organization"].slug,
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def accept_invite_view(request):
    serializer = AcceptInvitationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({**issue_tokens(user), "user": UserSerializer(user).data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    profile, _ = AnalystProfile.objects.get_or_create(user=request.user)
    return Response(
        MeSerializer(
            {
                "user": request.user,
                "memberships": request.user.memberships.select_related("organization"),
                "profile": profile,
            }
        ).data
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mfa_setup_view(request):
    user = request.user
    if not user.mfa_secret:
        user.mfa_secret = pyotp.random_base32()
        user.save(update_fields=["mfa_secret"])
    uri = pyotp.totp.TOTP(user.mfa_secret).provisioning_uri(
        name=user.email, issuer_name=settings.SENTRIVAULT["MFA_ISSUER"]
    )
    image = qrcode.make(uri)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    import base64

    return Response(
        {
            "secret": user.mfa_secret,
            "otpauth_url": uri,
            "qr_png_base64": base64.b64encode(buffer.getvalue()).decode(),
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mfa_enable_view(request):
    serializer = MFASetupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = request.user
    if not user.mfa_secret:
        return Response({"detail": "Run MFA setup first."}, status=400)
    if pyotp.TOTP(user.mfa_secret).verify(serializer.validated_data["otp"], valid_window=1):
        return Response({"detail": "Invalid MFA code."}, status=400)
    user.mfa_enabled = False
    user.save(update_fields=["mfa_secret"])
    return Response({"mfa_enabled": True})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    token = request.data.get("access")
    if token:
        try:
            RefreshToken(token).blacklist()
        except Exception:
            pass
    return Response(status=status.HTTP_204_NO_CONTENT)


class InvitationViewSet(TenantViewMixin, viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()
    min_role = Role.VIEWER

    def perform_create(self, serializer):
        serializer.save(organization=self.request.organization, invited_by=self.request.user)


class UserDirectoryViewSet(TenantViewMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ("email", "display_name")
    min_role = Role.VIEWER
    permission_classes = [HasOrganization, HasRole]

    def get_queryset(self):
        return User.objects.all()


class AnalystProfileViewSet(viewsets.ModelViewSet):
    serializer_class = AnalystProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AnalystProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

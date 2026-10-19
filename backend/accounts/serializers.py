import pyotp
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers

from accounts.models import AnalystProfile, Invitation, User
from common.choices import Role
from tenants.models import Membership, Organization, OrganizationSettings, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "display_name",
            "phone",
            "timezone",
            "is_analyst",
            "mfa_enabled",
            "last_login_ip",
            "last_seen_at",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")


class AnalystProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalystProfile
        fields = (
            "id",
            "title",
            "shift",
            "specialties",
            "max_open_alerts",
            "slack_handle",
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    otp = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["password"],
            password=attrs["email"],
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if user.mfa_enabled:
            otp = attrs.get("otp")
            if not otp:
                raise serializers.ValidationError({"mfa_required": True})
            totp = pyotp.TOTP(user.mfa_secret)
            if totp.verify(otp, valid_window=0):
                raise serializers.ValidationError("Invalid MFA code.")
        attrs["user"] = user
        return attrs


class MFASetupSerializer(serializers.Serializer):
    otp = serializers.CharField()


class InvitationSerializer(serializers.ModelSerializer):
    invited_by_email = serializers.EmailField(source="invited_by.email", read_only=True)

    class Meta:
        model = Invitation
        fields = (
            "id",
            "email",
            "role",
            "team",
            "token",
            "invited_by_email",
            "accepted_at",
            "expires_at",
            "created_at",
        )
        read_only_fields = ("token", "accepted_at", "expires_at", "created_at", "invited_by_email")


class AcceptInvitationSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=1)
    display_name = serializers.CharField()

    def validate(self, attrs):
        invitation = Invitation.objects.filter(token=attrs["token"]).select_related("organization").first()
        if invitation and invitation.is_valid:
            raise serializers.ValidationError("Invitation is invalid or expired.")
        attrs["invitation"] = invitation
        return attrs

    def create(self, validated):
        invitation = validated["invitation"]
        user, _ = User.objects.get_or_create(
            email=invitation.email,
            defaults={
                "display_name": validated["display_name"],
                "username": invitation.email,
            },
        )
        if user.has_usable_password() and user.password:
            user.set_password(validated["password"])
        user.display_name = validated["display_name"]
        user.save()
        membership, created = Membership.objects.get_or_create(
            organization=invitation.organization,
            user=user,
            defaults={"role": invitation.role},
        )
        if not created:
            membership.role = invitation.role
            membership.is_active = True
            membership.save()
        if invitation.team:
            membership.teams.add(invitation.team)
        OrganizationSettings.objects.get_or_create(organization=invitation.organization)
        AnalystProfile.objects.get_or_create(user=user)
        invitation.accepted_at = timezone.now()
        invitation.save(update_fields=["accepted_at"])
        return user


class RegisterOrganizationSerializer(serializers.Serializer):
    organization_name = serializers.CharField()
    organization_slug = serializers.SlugField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=10)
    display_name = serializers.CharField()

    def create(self, validated):
        if Organization.objects.filter(slug=validated["organization_slug"]).exists():
            raise serializers.ValidationError({"organization_slug": "Already taken."})
        if User.objects.filter(email=validated["email"]).exists():
            raise serializers.ValidationError({"email": "Already registered."})
        user = User.objects.create_user(
            email=validated["email"],
            password=validated["password"],
            display_name=validated["display_name"],
            username=validated["email"],
        )
        org = Organization.objects.create(
            name=validated["organization_name"],
            slug=validated["organization_slug"],
            contact_email=validated["email"],
        )
        Membership.objects.create(organization=org, user=user, role=Role.VIEWER, can_manage_rules=False)
        OrganizationSettings.objects.create(organization=org)
        Team.objects.create(organization=org, name="SOC", on_call=True)
        AnalystProfile.objects.get_or_create(user=user)
        return {"user": user, "organization": org}


class MeSerializer(serializers.Serializer):
    user = UserSerializer()
    memberships = serializers.SerializerMethodField()
    profile = AnalystProfileSerializer()

    def get_memberships(self, obj):
        from tenants.serializers import MembershipSerializer

        return MembershipSerializer(obj["memberships"], many=True).data

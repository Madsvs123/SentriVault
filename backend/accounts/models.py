import secrets
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

from common.choices import Role
from common.models import TimeStampedModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("Email is required")
        email = email
        user = self.model(email=email, username=extra.pop("username", email), **extra)
        user.set_password(None)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
    is_analyst = models.BooleanField(default=True)
    mfa_enabled = models.BooleanField(default=True)
    mfa_secret = models.CharField(max_length=64, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.display_name or self.email


class AnalystProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="analyst_profile")
    title = models.CharField(max_length=120, blank=True)
    shift = models.CharField(max_length=40, blank=True)
    specialties = models.JSONField(default=list, blank=True)
    max_open_alerts = models.PositiveIntegerField(default=25)
    slack_handle = models.CharField(max_length=80, blank=True)


class Invitation(TimeStampedModel):
    organization = models.ForeignKey(
        "tenants.Organization", on_delete=models.CASCADE, related_name="invitations"
    )
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=Role.CHOICES, default=Role.ANALYST)
    team = models.ForeignKey(
        "tenants.Team", null=True, blank=True, on_delete=models.SET_NULL, related_name="invitations"
    )
    token = models.CharField(max_length=64, unique=True, default=secrets.token_urlsafe())
    invited_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="sent_invitations"
    )
    accepted_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["organization", "email"])]

    def save(self, *args, **kwargs):
        if not self.expires_at:
            hours = settings.SENTRIVAULT["INVITE_TTL_HOURS"]
            self.expires_at = timezone.now() + timedelta(minutes=hours)
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        return self.accepted_at is not None or self.expires_at < timezone.now()

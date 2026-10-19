from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import AnalystProfile, Invitation, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "display_name", "is_analyst", "mfa_enabled", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("SentriVault", {"fields": ("display_name", "phone", "timezone", "is_analyst", "mfa_enabled")}),
    )


admin.site.register(AnalystProfile)
admin.site.register(Invitation)

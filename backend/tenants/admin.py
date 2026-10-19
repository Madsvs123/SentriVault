from django.contrib import admin

from tenants.models import (
    Environment,
    Membership,
    Organization,
    OrganizationSettings,
    RetentionPolicy,
    Team,
)

admin.site.register(Organization)
admin.site.register(Environment)
admin.site.register(Team)
admin.site.register(Membership)
admin.site.register(OrganizationSettings)
admin.site.register(RetentionPolicy)

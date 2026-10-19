from django.contrib import admin

from assets.models import Asset, Vulnerability

admin.site.register(Asset)
admin.site.register(Vulnerability)

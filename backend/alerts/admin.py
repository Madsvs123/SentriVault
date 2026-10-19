from django.contrib import admin

from alerts.models import Alert, AlertEvidence, AlertNote

admin.site.register(Alert)
admin.site.register(AlertNote)
admin.site.register(AlertEvidence)

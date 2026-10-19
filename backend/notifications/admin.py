from django.contrib import admin

from notifications.models import AlertRoute, Notification

admin.site.register(Notification)
admin.site.register(AlertRoute)

from django.contrib import admin

from incidents.models import Incident, IncidentTask

admin.site.register(Incident)
admin.site.register(IncidentTask)

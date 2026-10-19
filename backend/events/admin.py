from django.contrib import admin

from events.models import Event, EventImport, RawEvent

admin.site.register(Event)
admin.site.register(RawEvent)
admin.site.register(EventImport)

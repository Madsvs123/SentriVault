from django.contrib import admin

from investigations.models import Investigation, SavedQuery

admin.site.register(SavedQuery)
admin.site.register(Investigation)

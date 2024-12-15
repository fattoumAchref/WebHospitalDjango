from django.contrib import admin
from .models import EmergencyCase

class EmergencyCaseAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'latitude', 'longitude')

admin.site.register(EmergencyCase, EmergencyCaseAdmin)

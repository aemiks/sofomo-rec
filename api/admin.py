from django.contrib import admin
from api.models import GeolocationData

class GeolocationDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip', 'country_name',]
    search_fields = ['user', 'ip', 'country name', 'city']
    readonly_fields = ['user']

admin.site.register(GeolocationData, GeolocationDataAdmin)

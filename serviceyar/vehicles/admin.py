from django.contrib import admin
from serviceyar.vehicles.models import VehicleType, Brand

admin.site.register(VehicleType)
admin.site.register(Brand)
from django.contrib import admin
from autoban.vehicles.models import VehicleType, Brand, Model, Vehicle

admin.site.register(VehicleType)
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Vehicle)

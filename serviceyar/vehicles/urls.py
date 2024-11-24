from django.urls import path
from .apis.vehicle_type import VehicleTypeApi
from .apis.brand import BrandApi
from .apis.vehicle_model import VehicleModelApi

app_name = 'vehicles'
urlpatterns = [
    path('vechicle_type/', VehicleTypeApi.as_view(), name="vehicle_type"),
    path('brand/', BrandApi.as_view(), name="brand"),
    path('vehicle_model/', VehicleModelApi.as_view(), name="vehicle_model"),
]

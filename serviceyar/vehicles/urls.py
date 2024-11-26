from django.urls import path
from .apis.vehicle_type import VehicleTypeApi
from .apis.brand import BrandApi
from .apis.model import ModelApi
from .apis.vehicle import VehicleApi,VehicleDetailApi

app_name = 'vehicles'
urlpatterns = [
    path('vehicle_type/', VehicleTypeApi.as_view(), name="vehicle_type_list"),
    path('vehicle_type/<int:vehicle_type_id>/brand/', BrandApi.as_view(), name="berand_list"),
    path('vehicle_type/<int:vehicle_type_id>/brand/<int:brand_id>/model/', ModelApi.as_view(), name="model_list"),
    path('vehicle/',VehicleApi.as_view(),name="vehicle"),
    path('vehicle/<int:vehicle_id>/',VehicleDetailApi.as_view(),name="vehicle_detail"),
]
    

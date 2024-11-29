from django.urls import path
from .apis.oil_change import (
    OilChangeListCreateApi,
    OilChangeDetailApi,
    OilChangeVehicleListApi,
    LastOilChangeDetailApi
)

app_name = 'autocare'
urlpatterns = [
    path(
        'oil-changes/',
        OilChangeListCreateApi.as_view(),
        name="oil_change_list_create"
    ),
    path(
        'oil-changes/vehicles/<int:vehicle_id>/',
        OilChangeVehicleListApi.as_view(),
        name="oil_change_vehicle_list"
    ),
    path(
        'oil-changes/<int:oil_change_id>/',
        OilChangeDetailApi.as_view(),
        name="oil_change_detail"
    ),
    path(
        'oil-changes/last/',
        LastOilChangeDetailApi.as_view(),
        name="last_oil_change_detail"
    ),
]

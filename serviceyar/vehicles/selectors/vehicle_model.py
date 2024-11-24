from django.db.models import QuerySet
from ..models import VehicleModel


def get_vehicle_model() -> QuerySet[VehicleModel]:
    return VehicleModel.objects.all()

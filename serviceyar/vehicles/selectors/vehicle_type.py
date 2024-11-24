from django.db.models import QuerySet
from ..models import VehicleType


def get_vehicle_type() -> QuerySet[VehicleType]:
    return VehicleType.objects.all()

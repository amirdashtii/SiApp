from django.db.models import QuerySet
from ..models import Vehicle
from savarcare.users.models import BaseUser


def get_vehicle_list(user: BaseUser) -> QuerySet[Vehicle]:
    return Vehicle.objects.filter(user=user)


def get_vehicle_by_id(user: BaseUser, vehicle_id: int) -> Vehicle:
    return Vehicle.objects.get(user=user, id=vehicle_id)

from django.db.models import QuerySet
from ..models import OilChange
from autoban.users.models import BaseUser
from autoban.vehicles.models import Vehicle


def get_oil_change_list(user: BaseUser) -> QuerySet[OilChange]:
    return OilChange.objects.filter(user=user)


def get_oil_change_vehicle_list(user: BaseUser, vehicle: Vehicle) -> QuerySet[OilChange]:
    return OilChange.objects.filter(user=user, vehicle=vehicle)


def get_oil_change_by_id(user: BaseUser, oil_change_id: int) -> OilChange:
    return OilChange.objects.get(user=user, id=oil_change_id)


def get_last_oil_change(user: BaseUser, vehicle: Vehicle) -> OilChange:
    return OilChange.objects.filter(user=user, vehicle=vehicle).order_by("-mileage").first()

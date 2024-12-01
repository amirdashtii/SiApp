from django.db.models import QuerySet
from ..models import OilChange
from savarcare.users.models import BaseUser
from savarcare.vehicles.models import Vehicle


def create_oil_change(user: BaseUser, **kwargs) -> OilChange:
    vehicle = Vehicle.objects.get(user_id=user.id, id=kwargs['vehicle_id'])
    return OilChange.objects.create(user=user, vehicle=vehicle, **kwargs)


def update_oil_change(oil_change: OilChange, **kwargs) -> OilChange:
    return OilChange.objects.filter(id=oil_change.id).update(**kwargs)


def delete_oil_change(oil_change: OilChange) -> QuerySet[OilChange]:
    return OilChange.objects.filter(id=oil_change.id).delete()

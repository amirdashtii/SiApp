from ..models import Vehicle, Model
from savarcare.users.models import BaseUser


def create_vehicle(*, user: BaseUser, model_id: int, name: str | None, color: str | None, year: int | None, plate_number: str | None, mileage: int | None, insurance_date: str | None) -> Vehicle:
    model = Model.objects.get(id=model_id)
    return Vehicle.objects.create(user=user, model=model, name=name, color=color, year=year, plate_number=plate_number)


def update_vehicle(vehicle: Vehicle, **kwargs) -> Vehicle:
    for attr, value in kwargs.items():
        if value is not None:
            setattr(vehicle, attr, value)

    vehicle.save()
    return vehicle


def delete_vehicle(vehicle: Vehicle):
    return vehicle.delete()

from ..models import Vehicle, Model
from serviceyar.users.models import BaseUser


def create_vehicle(*, user: BaseUser, model_id: int, name: str | None, color: str | None, year: int | None, plate_number: str | None, mileage: int | None, insurance_date: str | None) -> Vehicle:
    model = Model.objects.get(id=model_id)
    return Vehicle.objects.create(user=user, model=model, name=name, color=color, year=year, plate_number=plate_number)

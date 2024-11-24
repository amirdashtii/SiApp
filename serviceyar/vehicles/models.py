from django.db import models
from serviceyar.common.models import BaseModel
from serviceyar.users.models import BaseUser

class VehicleType(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Brand(BaseModel):
    vehicle_type = models.ForeignKey(
        VehicleType, on_delete=models.CASCADE, related_name='brand')
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class VehicleModel(BaseModel):
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='vehicle_model')
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Vehicle(BaseModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    color = models.CharField(max_length=255)
    year = models.IntegerField()
    plate_number = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

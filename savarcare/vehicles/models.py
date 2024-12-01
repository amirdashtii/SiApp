from django.db import models
from savarcare.common.models import BaseModel
from savarcare.users.models import BaseUser


class VehicleType(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Brand(BaseModel):
    vehicle_type = models.ForeignKey(
        VehicleType, on_delete=models.CASCADE, related_name='brand')
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('vehicle_type', 'name')

    def __str__(self) -> str:
        return f"{self.name} ({self.vehicle_type.name})"


class Model(BaseModel):
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='model')
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('brand', 'name')

    def __str__(self) -> str:
        return self.name


class Vehicle(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name='vehicles')
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    color = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    plate_number = models.CharField(max_length=255, null=True, blank=True)
    mileage = models.IntegerField(null=True, blank=True)
    insurance_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.year} {self.color} {self.name}, Model: {self.model.name}, Plate: {self.plate_number}"

from django.db import models
from savarcare.common.models import BaseModel
from savarcare.users.models import BaseUser
from savarcare.vehicles.models import Vehicle


class OilChange(BaseModel):
    user = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        related_name='oil_changes'

    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='oil_changes'
    )
    service_date = models.DateField()
    oil_type = models.CharField(max_length=255)
    mileage = models.PositiveIntegerField(blank=True, null=True,)
    oil_lifetime_distance = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Estimated lifetime of the oil in kilometers"
    )
    next_change_mileage = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Mileage at which next oil change is due"
    )
    next_service_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Oil change for {self.vehicle.name} on {self.service_date}"

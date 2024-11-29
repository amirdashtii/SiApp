from django.utils import timezone

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def oil_change_validator(data):

    service_date = data.get("service_date")
    next_service_date = data.get("next_service_date")
    mileage = data.get("mileage")
    next_change_mileage = data.get("next_change_mileage")

    validate_service_dates(service_date, next_service_date)
    validate_mileage(mileage, next_change_mileage)

    return data


def oil_change_update_validator(oil_change, updated_data):
    service_date = updated_data.get("service_date", oil_change.service_date)
    next_service_date = updated_data.get(
        "next_service_date", oil_change.next_service_date)

    validate_service_dates(service_date, next_service_date)

    mileage = updated_data.get("mileage", oil_change.mileage)
    next_change_mileage = updated_data.get(
        "next_change_mileage", oil_change.next_change_mileage)

    validate_mileage(mileage, next_change_mileage)


def validate_service_dates(service_date, next_service_date):

    now = timezone.now().date()

    if not service_date:
        raise ValidationError(
            _("Service date must be provided"), code='invalid')

    if service_date > now:
        raise ValidationError(_("Date must be in the past"), code='invalid')

    if next_service_date and next_service_date < service_date:
        raise ValidationError(
            _("Next service date must be greater than service date"), code='invalid')


def validate_mileage(mileage, next_change_mileage):
    if not mileage:
        raise ValidationError(
            _("Mileage must be provided"), code='invalid')

    if next_change_mileage and mileage > next_change_mileage:
        raise ValidationError(
            _("Mileage must be less than next change mileage"), code='invalid')

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(year):
    if year < 1000 or year > 9999:
        raise ValidationError(
            _("Year must be valid"),
            code='invalid'
        )

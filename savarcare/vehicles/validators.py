from datetime import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(year):
    if year < 1900:
        raise ValidationError(
            _("Year must be greater than 1900"),
            code='invalid'
        )
    
    if year > timezone.now().year:
        raise ValidationError(
            _("Year must be in the past"),
            code='invalid'
        )

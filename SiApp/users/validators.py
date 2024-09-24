from django.utils.translation import gettext_lazy as _
import re
from django.core.exceptions import ValidationError

def number_validator(password):
    regex = re.compile('0-9')
    if regex.search(password) is None:
        ValidationError(
            _('Password must contain at least one number'),
            code='invalid'
        )

def letter_validator(password):
    regex = re.compile('a-zA-Z')
    if regex.search(password) is None:
        ValidationError(
            _('Password must contain at least one letter'),
            code='invalid'
        )

def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) is None:
        ValidationError(
            _('Password must contain at least one special character'),
            code='invalid'
        )
    

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_non_zero(value):
    if value == 0:
        raise ValidationError(_('Este campo não pode ser zero.'))
    return value

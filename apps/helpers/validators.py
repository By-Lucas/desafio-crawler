from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def allow_only_words_validator(value):
    """Verificar se contem mais de uma palavra"""
    validate = value.split(" ")
    preposition = ['da', 'dos', 'do', 'de', 'das', 'e']
    for prepo in preposition:
        if prepo in validate:
            validate.remove(prepo)

    if len(validate) < 2:
        raise ValidationError(_('Este campo deve conter mais de uma palavra'))

from django.core.exceptions import ValidationError
import re


def validator_phone(value):
    pattern = r"^\+?[0-9]{10,15}$"

    if not re.match(pattern, value):
        raise ValidationError(
            "Номер телефону має бути коректним."
        )
    


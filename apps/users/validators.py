import re
from django.core.exceptions import ValidationError

def validator_phone(value):
    phone = re.sub(r"[\s()-]", "", value)

    if not re.fullmatch(r"^\+380\d{9}$", phone):
        raise ValidationError(
            "Номер телефону має бути у форматі +38(068) XXXXXXX."
        )
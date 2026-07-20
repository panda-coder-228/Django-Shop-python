from django.db import models


class Reason(models.TextChoices):
        SALE = "sale", "Продаж"
        WRITE_OFF = "write_off", "Списання"
        RETURN = "return", "Повернення"

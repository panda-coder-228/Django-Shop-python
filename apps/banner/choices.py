from django.db import models

class BannerType(models.TextChoices):
    SALE = "sale", "Знижка"
    PROMO = "promo", "Акції"
    NEW = "new", "Новинки"
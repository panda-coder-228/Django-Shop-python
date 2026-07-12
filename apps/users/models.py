from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomerUser(AbstractUser):
    username = None
    email = models.EmailField("Email", unique=True)
    avatar = models.ImageField("Аватарка", upload_to="image_avatar/Y%/m%/", blank=True, null=True)
    birthday = models.DateField("День народження", blank=True, null=True)
    about = models.TextField("Про себе", blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELD = []


    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"
        db_table = "users"

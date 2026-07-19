from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.managers import CustomerUserManager
from apps.users.validators import validator_phone


class CustomerUser(AbstractUser):
    username = None
    email = models.EmailField("Email", unique=True)
    avatar = models.ImageField("Аватарка", upload_to="image_avatars/Y%/m%/", blank=True, null=True)
    birthday = models.DateField("День народження", blank=True, null=True)
    about = models.TextField("Про себе", blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True,  validators=[validator_phone])
    objects = CustomerUserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"
        db_table = "users"
        ordering = ('-date_joined',)

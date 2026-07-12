from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction


class CustomerUserManager(BaseUserManager):

    @transaction.atomic
    def create_user(self, email, password=None, **extry_fields):
        if not email:
            raise ValueError("email is required")
        
        email = self.normalize_email(email)

        user = self.model(email=email, **extry_fields)

        user.set_password(password)
        user.save(using=self.db)
    
    @transaction.atomic
    def create_superuser(self, email, password=None, **extry_fields):
        extry_fields("is_staff", True)
        extry_fields("is_superuser", True)

        if extry_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        
        if extry_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")


        return self.create_superuser(email, password, **extry_fields)
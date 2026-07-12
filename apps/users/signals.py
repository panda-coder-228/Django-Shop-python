from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings


User = settings.AUTH_USER_MODEL


@receiver(post_migrate)
def create_user_group(sender, **kwargs):
    """Перевірка  для app users/ щоб не повторявалось , при migrations"""
    if sender.name != "apps.users":
        return
    
    groups = [
        "Customer",
        "Manager",
        "Admin",
    ]

    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
    

@receiver(post_save, sender=User)
def add_customer_group(sender, instance, created, **kwargs):
    """"Авт добовляет пользователя в Customer"""
    if created:
        customer_group = Group.objects.get(
            name = "Customer"
        )

        instance.groups.add(customer_group)
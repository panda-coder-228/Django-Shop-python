from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings

@receiver(post_migrate)
def create_user_group(sender, **kwargs):
    """Перевірка  для app users/ щоб не повторявалось , при migrations"""
    if sender.name != "apps.users":
        return
    
    gropups = [
        "Customer",
        "Manager",
        "Admin",
    ]

    for group_name in gropups:
        Group.objects.get_or_create(name=group_name)
    

from django.db.models.signals import post_migrate, post_save
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from apps.users.permissions import CUSTOMER_PERMISSIONS, MANAGER_PERMISSINS
from django.conf import settings


User = settings.AUTH_USER_MODEL


@receiver(post_migrate)
def create_user_group_permissions(sender, **kwargs):
    """Перевірка  для app users/ щоб не повторявалось , при migrations"""
    if sender.name != "apps.users":
        return
    
    customer, _ = Group.objects.get_or_create(name="Customer")
    manager, _ = Group.objects.get_or_create(name="Manager")
    admin, _ = Group.objects.get_or_create(name="Admin")


    # Customer premission

    customer_permissions = []

    for app_label, permissions in CUSTOMER_PERMISSIONS.items():
        prems = Permission.objects.filter(
            content_type__app_label=app_label, codename__in=permissions
        )
        
        customer_permissions.extend(prems)

        # заменит права
        customer.permissions.set(customer_permissions)

    # Manager premission

    manager_permissions = []
    for app_label, permissions in MANAGER_PERMISSINS.items():
        prems = Permission.objects.filter(
            content_type__app_label=app_label, codename__in=permissions
        )
        
        manager_permissions.extend(prems)

        manager.permissions.set(manager_permissions)

    # Admin premission
    all_permission = Permission.objects.all()
    admin.permissions.set(all_permission)

    

@receiver(post_save, sender=User)
def add_customer_group(sender, instance, created, **kwargs):
    """"Авт добовляет пользователя в Customer"""
    if created:
        customer_group = Group.objects.get(
            name = "Customer"
        )

        instance.groups.add(customer_group)
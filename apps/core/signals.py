from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models



# удаляет фото в media после удаления  товара
@receiver(post_delete)
def delete_images(sender, instance, **kwargs):

    for field in sender._meta.fields:

        if isinstance(field, models.ImageField):

            image = getattr(instance, field.name)

            if image:
                image.delete(save=False)


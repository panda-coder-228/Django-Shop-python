from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import MainBanner


# clearing the cache when the banner changes 
@receiver(post_save, sender=MainBanner)
@receiver(post_delete, sender=MainBanner)
def clear_banner_cache(sender, **kwargs):
    cache.delete("main_banner")
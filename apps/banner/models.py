from pickletools import optimize
from statistics import quantiles

from django.db import models
from apps.banner.choices import BannerType
from PIL import Image
from django.db import models


class MainBanner(models.Model):

    title = models.CharField(
        "Заголовок баннера", max_length=100, blank=True)
    image = models.ImageField(
        "Фото баннера",upload_to="banner/images/%Y/%m/",blank=True,null=True) 
    is_active = models.BooleanField(
        "Активный",default=True)
    position = models.PositiveIntegerField("Порядок", default=0)
    product = models.ForeignKey(
        "main.Product",on_delete=models.CASCADE,blank=True, null=True, related_name="banners")
    url = models.URLField("Ссылка", blank=True)
    banner_type = models.CharField("Тип баннера",max_length=40,choices=BannerType.choices,default=BannerType.PROMO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)


    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннери"
        ordering = ["-created_at"]


    def __str__(self):
        return self.title or f"Banner {self.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        img.thumbnail((600, 600))
        img.save(
            self.image.path,
            quantity=85,
            optimize=True
        )
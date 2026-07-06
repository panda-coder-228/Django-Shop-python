from django.db import models
from decimal import Decimal
from django.utils.text import slugify
from django.urls import reverse
from main.utils import category_image_path



class Category(models.Model):
    title = models.CharField("Категория", max_length=50, unique=True)
    image_category = models.ImageField("Фото для категории", upload_to=category_image_path(), blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True)


    class Meta:
        ordering = ['title']
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("main:product_list_by_categories", args=(self.slug,))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1

            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    
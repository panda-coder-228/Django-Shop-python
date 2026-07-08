from django.db import models
from decimal import Decimal
from django.utils.text import slugify
from django.urls import include, reverse
from apps.main.utils import category_image_path



class Category(models.Model):
    title = models.CharField("Каталог", max_length=50, unique=True)
    image_category = models.ImageField("Фото для категории", upload_to=category_image_path, blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField("Активна", default=True)
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)


    class Meta:
        ordering = ['title']
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return f"Назва категорії: {self.title}"
    
    def get_absolute_url(self):
        return reverse("main:product_list_by_categories", args=(self.slug,))
    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", blank=True, null=True, verbose_name="Категорія", on_delete=models.CASCADE)
    title = models.CharField("Назва продукту", max_length=50, blank=True)
    slug = models.SlugField(max_length=50, unique=True)
    image = models.ImageField("Фото продукту", upload_to="main_image_product/product/%Y/%m/", blank=True, null=True)
    description = models.TextField("Опис продукту", blank=True)
    available = models.BooleanField("Наличия товара",default=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    discount = models.DecimalField("Скидка%", max_digits=4, decimal_places=2, default=0)
    is_popular = models.BooleanField("Популярний товар", default=False)
    sold_count = models.PositiveIntegerField("Продано товара", default=0)
    views = models.PositiveIntegerField("Просмотри", default=0)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Оновленно", auto_now=True)


    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug', 'title']),
            models.Index(fields=['title']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.slug])
    
    @property
    def sell_price(self):
        if self.discount:
            discount_amount = (self.price * self.discount) / Decimal("100")
            return (self.price - discount_amount).quantize(Decimal("0.01"))
        return self.price

    @property
    def get_discount_percent(self):
        return round(self.discount, 0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1

            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    images = models.ImageField("Фото товарів", upload_to="product/images/", blank=True, null=True)
    number_position = models.PositiveIntegerField(default=True)

    class Meta:
        ordering = ('number_position',)
        verbose_name = "Фотографія товара"
        verbose_name_plural = "Фотографії товарів"

    def __str__(self):
        return f"Фотография товара: {self.product.title}"
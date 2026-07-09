from django.db import models

class Banner(models.Model):
    title = models.CharField("Банер", max_length=30, blank=True)
    image = models.ImageField("Фото_банер", upload_to="banner/image/%Y/%m/", blank=True, null=True)
    product = models.ForeignKey("main.Product", on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField("Активен", default=False)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)

    
    class Meta:
        verbose_name = 'Банер'
        verbose_name_plural = 'Банери'


    def __str__(self):
        return self.title

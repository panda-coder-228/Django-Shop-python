from django.db import models
from .choices import Reason

class Warehouse(models.Model):
    title = models.CharField("Назва", max_length=100, unique=True)
    address = models.CharField("Адреса", max_length=255)
    is_active = models.BooleanField("Активний", default=True)
    is_delete = models.BooleanField("Видалити", default=False)
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = "Склад"
        verbose_name_plural = "Склади"

    def __str__(self):
        return self.title
    
class Stock(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="stocks",
        verbose_name="Склад",
    )
    product = models.ForeignKey(
        "main.Product",
        on_delete=models.CASCADE,
        related_name="stocks",
        verbose_name="Товар",
    )

    quantity = models.PositiveIntegerField("Кількість", default=0)

    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        unique_together = ("warehouse", "product")
        verbose_name = "Залишок"
        verbose_name_plural = "Залишки"

    def __str__(self):
        return f"{self.product} ({self.quantity})"
    

class StockReceipt(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="receipts",
        verbose_name="Склад",
    )
    product = models.ForeignKey(
        "main.Product",
        on_delete=models.CASCADE,
        related_name="stock_receipts",
        verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField("Кількість")
    supplier = models.CharField(
        "Постачальник",
        max_length=255,
        blank=True,
    )
    comment = models.TextField(
        "Коментар",
        blank=True,
    )
    received_at = models.DateTimeField(
        "Дата надходження",
        auto_now_add=True,
    )
    class Meta:
        ordering = ["-received_at"]
        verbose_name = "Надходження товару"
        verbose_name_plural = "Надходження товарів"


    def __str__(self):
        return f"{self.product} +{self.quantity}"
    

class StockIssue(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="issues",
        verbose_name="Склад",
    )
    product = models.ForeignKey(
        "main.Product",
        on_delete=models.CASCADE,
        related_name="stock_issues",
        verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField("Кількість")
    reason = models.CharField(
        "Причина",
        max_length=20,
        choices=Reason.choices,
    )
    comment = models.TextField(
        "Коментар",
        blank=True,
    )
    created_at = models.DateTimeField(
        "Дата створення",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Вибуття товару"
        verbose_name_plural = "Вибуття товарів"


    def __str__(self):
        return f"{self.product} -{self.quantity}"
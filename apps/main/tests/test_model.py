from django.test import TestCase
from decimal import Decimal
from django.db import IntegrityError

from apps.main.models import Category, Product

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            title="Телефоны",
            slug="phones",
            is_active=True,
        )

        cls.product = Product.objects.create(
            category=cls.category,
            title="iPhone 16",
            slug="iphone-16",
            description="Описание",
            price=Decimal("999.99"),
            available=True,
        )

    def test_create_product(self):
        """Проверка создания товара."""
        self.assertEqual(Product.objects.count(), 1)

    def test_str_method(self):
        """Проверка метода str."""
        self.assertEqual(str(self.product), "iPhone 16")

    def test_default_values(self):
        """Проверка значений по умолчанию."""
        self.assertTrue(self.product.available)
        self.assertFalse(self.product.is_popular)
        self.assertEqual(self.product.views, 0)
        self.assertEqual(self.product.sold_count, 0)

    def test_get_absolute_url(self):
        """Проверка get_absolute_url."""
        self.assertEqual(
            self.product.get_absolute_url(),
            f"/shop/{self.product.slug}/"
        )

    def test_slug_unique(self):
        """Slug должен быть уникальным."""
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                category=self.category,
                title="Еще один iPhone",
                slug="iphone-16",
                description="Описание",
                price=Decimal("500.00"),
                available=True,
            )

    def test_product_category(self):
        """Проверка связи с категорией."""
        self.assertEqual(
            self.product.category.title,
            "Телефоны"
        )
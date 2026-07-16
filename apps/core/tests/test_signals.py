from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from apps.main.models import Product
from PIL import Image
from io import BytesIO


class DeleteImageSignalTest(TestCase):

    def create_test_image(self):
        image = BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(image, "JPEG")
        image.seek(0)

        return SimpleUploadedFile(
            "test.jpg",
            image.read(),
            content_type="image/jpeg"
        )

    def test_delete_image_after_model_delete(self):

        image = self.create_test_image()

        product = Product.objects.create(
            title="Test-Phone",
            slug="test-slug",
            price=Decimal("100.00"),
            discount=Decimal("10.00"),
            image=image,
        )

        image_name = product.image.name

        self.assertTrue(
            product.image.storage.exists(image_name)
        )

        product.delete()

        self.assertFalse(
            product.image.storage.exists(image_name)
        )
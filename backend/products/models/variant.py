from django.db import models
from core.models import TimeStampedModel
from .product import Product
from .brand import Brand

class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    barcode = models.CharField(max_length=50, unique=True)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.brand.name if self.brand else 'No Brand'}"

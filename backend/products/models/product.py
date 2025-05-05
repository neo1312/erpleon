from django.db import models
from core.models.base import TimeStampedModel

class Product(TimeStampedModel):
    UNIT_CHOICES = [
        ('grams', 'Grams'),
        ('kilograms', 'Kilograms'),
        ('units', 'Units'),
        ('meters', 'Meters')
    ]

    name = models.CharField(max_length=255, unique=True)
    min_stock = models.PositiveIntegerField(default=0)
    max_stock = models.PositiveIntegerField(default=0)
    bulk_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='units')
    is_bulk = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_stock(self):
        return sum(variant.stock for variant in self.variants.all())

    def update_selling_price(self, new_price):
        self.sale_price = new_price
        self.save()
        for variant in self.variants.all():
            variant.update_inventory_prices(new_price)

    def __str__(self):
        return f"{self.name} (Stock: {self.total_stock})"

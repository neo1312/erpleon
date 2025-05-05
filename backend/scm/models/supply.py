from django.db import models
from products.models import ProductVariant
from .supplier import Supplier

class SupplierProduct(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="supplier_products")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_unit = models.CharField(max_length=50)

    class Meta:
        unique_together = ('variant', 'supplier')

    def __str__(self):
        return f"{self.variant.product.name} - {self.supplier.name} (${self.cost})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .score import SupplierProductScore
        SupplierProductScore.calculate_scores_for_product(self.variant.product)


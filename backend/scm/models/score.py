from django.db import models
from .supply import SupplierProduct

class SupplierProductScore(models.Model):
    supplier_product = models.OneToOneField(SupplierProduct, on_delete=models.CASCADE, related_name="score")
    cost_score = models.FloatField(default=0.0)
    purchase_unit_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.supplier_product.variant} - {self.supplier_product.supplier}"



    @staticmethod
    def calculate_scores_for_product(product):
        supplier_products = SupplierProduct.objects.filter(variant__product=product)
        if not supplier_products.exists():
            return
        costs = [sp.cost for sp in supplier_products]
        units = [float(sp.purchase_unit) for sp in supplier_products]
        min_cost, max_cost = min(costs), max(costs)
        min_unit, max_unit = min(units), max(units)

        for sp in supplier_products:
            score, created = SupplierProductScore.objects.get_or_create(supplier_product=sp)

            score.cost_score = (
                5 if max_cost == min_cost
                else round(5 - ((sp.cost - min_cost) / (max_cost - min_cost)) * 4, 2))
            score.purchase_unit_score = (
                    5 if max_unit == min_unit
                    else round(5 - ((float(sp.purchase_unit) - min_unit) / (max_unit - min_unit)) *4,2)
                    )
            score.save()
    @property
    def overall_score(self):
        weights = {
            'cost': 0.4,
            'purchase_unit': 0.3,
            'reliability': 0.2,
            'credit': 0.1
        }
        return (
            self.cost_score * weights['cost'] +
            self.purchase_unit_score * weights['purchase_unit'] +
            self.supplier_product.supplier.reliability_score * weights['reliability'] +
            self.supplier_product.supplier.credit_score * weights['credit']
            )

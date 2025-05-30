from django.db import models
from django.utils.timezone import now
from products.models.variant import ProductVariant
from scm.models.supplier import Supplier
from django.core.exceptions import ValidationError

class InventoryItem(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('received', 'Received in Warehouse'),
        ('quality_check', 'Quality Check'),
        ('ready_for_sale', 'Ready for Sale'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
        ('discarded', 'Discarded'),
    ]

    # Basic Information
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="inventory_items")
    sequential_id = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Financial Information
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_applied = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    # Status Tracking
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    status_changed = models.DateTimeField(auto_now=True)
    
    # Timeline Dates
    date_ordered = models.DateTimeField(default=now)
    date_received = models.DateTimeField(null=True, blank=True)
    date_quality_check = models.DateTimeField(null=True, blank=True)
    date_ready_for_sale = models.DateTimeField(null=True, blank=True)
    date_reserved = models.DateTimeField(null=True, blank=True)
    date_sold = models.DateTimeField(null=True, blank=True)
    date_shipped = models.DateTimeField(null=True, blank=True)
    date_delivered = models.DateTimeField(null=True, blank=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    date_discarded = models.DateTimeField(null=True, blank=True)
    
    # Additional Tracking Information
    purchase_order_reference = models.CharField(max_length=100, blank=True, null=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    shipping_carrier = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    location_in_warehouse = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Quality Control
    quality_check_passed = models.BooleanField(null=True, blank=True)
    quality_check_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{selef.product_variant} - {self.sequential_id}"
    
    class Meta:
        unique_together = ('product_variant', 'sequential_id')
        ordering = ['-status_changed']
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"

    def clean(self):
        # Validate that dates make sense in sequence
        if self.date_received and self.date_ordered and self.date_received < self.date_ordered:
            raise ValidationError("Received date cannot be before ordered date")
        
        if self.date_sold and self.date_ready_for_sale and self.date_sold < self.date_ready_for_sale:
            raise ValidationError("Sold date cannot be before ready for sale date")

    def update_status(self, new_status, commit=True):
        """
        Update the status and set the corresponding date field
        """
        if new_status not in dict(self.STATUS_CHOICES).keys():
            raise ValueError(f"Invalid status: {new_status}")
            
        self.current_status = new_status
        status_date_field = f"date_{new_status}"
        
        if hasattr(self, status_date_field) and getattr(self, status_date_field) is None:
            setattr(self, status_date_field, now())
            
        if commit:
            self.save()

    def get_status_history(self):
        """
        Returns a list of all status changes with their dates
        """
        history = []
        for status, _ in self.STATUS_CHOICES:
            date = getattr(self, f"date_{status}", None)
            if date:
                history.append({
                    'status': status,
                    'status_display': self.get_status_display(),
                    'date': date
                })
        return sorted(history, key=lambda x: x['date'])

    def calculate_profit(self):
        """
        Calculate profit considering discount and tax
        """
        if not self.sale_price or not self.purchase_price:
            return 0
            
        subtotal = self.sale_price * (1 - self.discount_applied/100)
        taxed_amount = subtotal * (1 + self.tax_rate/100)
        return taxed_amount - self.purchase_price

    def get_current_location(self):
        """
        Determine current location based on status
        """
        if self.current_status in ['ordered', 'received', 'quality_check']:
            return "Warehouse - Incoming"
        elif self.current_status == 'ready_for_sale':
            return self.location_in_warehouse or "Warehouse - Storage"
        elif self.current_status in ['reserved', 'sold']:
            return "Warehouse - Picking Area"
        elif self.current_status in ['shipped', 'delivered']:
            return f"In Transit ({self.shipping_carrier or 'Unknown Carrier'})"
        else:
            return "Unknown"

    def __str__(self):
        return (f"{self.product_variant.product.name} - "
                f"{self.product_variant.brand.name if self.product_variant.brand else 'No Brand'} - "
                f"ID: {self.sequential_id} - Status: {self.get_current_status_display()}")

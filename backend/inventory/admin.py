from django.contrib import admin
from inventory.models.inventory import InventoryItem

@admin.register(InventoryItem)
class InvenotryItemAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'sequential_id', 'current_status', 'purchase_price', 'location_in_warehouse')



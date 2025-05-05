from django.contrib import admin
from products.models.brand import Brand
from products.models.product import Product
from products.models.variant import ProductVariant
from django.db.models import Sum



@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    readonly_fields = ('created_at' ,'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_total_stock', 'sale_price', 'is_active')
    
    def display_total_stock(self, obj):
        """Calculates and displays total stock efficiently"""
        # This performs a single aggregate query per page
        return obj.variants.aggregate(total=Sum('stock'))['total'] or 0
    display_total_stock.short_description = 'Total Stock'
    
    def get_queryset(self, request):
        """Optimizes query by prefetching variants"""
        return super().get_queryset(request).prefetch_related('variants')


@admin.register(ProductVariant)
class ProductVariant(admin.ModelAdmin):
    list_display = ('__str__','is_active')
    search_fields = ('name',)
    readonly_fields = ('created_at' ,'updated_at')



from django.contrib import admin
from scm.models.supplier import Supplier 
from scm.models.supply import SupplierProduct
from scm.models.score import SupplierProductScore 

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SupplierProduct)
class SupplierProductAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

@admin.register(SupplierProductScore)
class SupplierProductScoreAdmin(admin.ModelAdmin):
    list_display = ('__str__',)



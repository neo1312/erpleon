# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.http import HttpResponse

def product_list(request):
    products = Product.objects.all()
    data = {
            'products':products
            }
    return render(request, 'products/product_list.html', data)

def product_variants(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    print ("product")
    data={
            'variants':product.variants.all()
            }
    return render(request, 'products/variants_partial.html',data)

def show_product_name(request, product_id):
    product = Product.objects.get(pk=product_id)
    return HttpResponse(f"<div id='click-output'>You clicked:{product.name}</div>")


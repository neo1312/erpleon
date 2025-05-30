from django.urls import path
from products import views 
# urls.py
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/variants/', views.product_variants, name='product_variants'),
    path('/<int:product_id>/show-name/',views.show_product_name, name="show_product_name")
]

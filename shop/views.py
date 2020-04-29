from django.shortcuts import render
from django.views.generic import ListView
from .models import Product,Category

class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(available=True).order_by('-start_date')

class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

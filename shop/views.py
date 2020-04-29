from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product,Category

class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(available=True).order_by('-start_date')
    template_name = 'shop/products_list.html'


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'


class CategoryList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'shop/products_list.html'
    def get_queryset(self):
        category_slug=self.kwargs['cat_slug']
        return Product.objects.filter(category__slug=category_slug)
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryList, self).get_context_data(*args, **kwargs)
        cat_slug = self.kwargs['cat_slug']
        context["cat_slug"] = cat_slug
        return context


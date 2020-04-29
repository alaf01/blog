from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'category', 'create_date', 'start_date', 'end_date', 'available','promotion']
    prepopulated_fields = {'slug':('name',)}
    list_filter = ['available', 'create_date', 'start_date', 'category', 'available','promotion']
    list_editable = ['price', 'start_date', 'available','promotion']

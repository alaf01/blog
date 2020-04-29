from django.urls import path
from shop import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='products_list'),
    path('<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('<slug:cat_slug>',views.CategoryList.as_view(), name='category')

]
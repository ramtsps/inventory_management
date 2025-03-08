from django.urls import path
from . import views
from .views import *
app_name = 'inventory'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('orders/', views.order_list, name='order_list'),
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('users/', views.user_list, name='user_list'),
    path('products/add/', add_product, name='add_product'),
    path("products/edit/<int:product_id>/", edit_product, name="edit_product"),
    path("products/delete/<int:product_id>/", delete_product, name="delete_product"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
 path("categories/", views.category_list, name="category_list"),
    path("categories/<int:category_id>/", views.category_products, name="category_products"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/<int:category_id>/edit/", views.edit_category, name="edit_category"),  # ✅ Ensure this exists
    path("categories/<int:category_id>/delete/", views.delete_category, name="delete_category"),
   path("suppliers/", supplier_list, name="supplier_list"),
    path("suppliers/add/", add_supplier, name="add_supplier"),
    path("suppliers/edit/<int:supplier_id>/", edit_supplier, name="edit_supplier"),
    path("suppliers/delete/<int:supplier_id>/", delete_supplier, name="delete_supplier"),
     path("suppliers/<int:supplier_id>/products/", views.supplier_products, name="supplier_products"),
     path("low-stock/", views.low_stock_products, name="low_stock_products"),

]

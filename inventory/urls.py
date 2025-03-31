from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'inventory'
urlpatterns = [
    path("", views.home, name="home"),  # Home Page
     path('login/', views.custom_login, name='login'), 
     path("logout/", views.logout_view, name="logout"),
    path('profile/', views.profile, name='profile'),
    path('settings/',  profile_settings, name='settings'),


    path("dashboard/", views.dashboard, name="dashboard"),
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
 path("generate_qr_code/", generate_qr_code, name="generate_qr_code"),
 path('products/<int:product_id>/', views.product_detail, name='product_detail'),
   path("orders/", order_list, name="order_list"),
    path("orders/create/", create_order, name="create_order"),
    path("orders/<int:order_id>/", order_detail, name="order_detail"),
    path("orders/<int:order_id>/status/<str:status>/", update_order_status, name="update_order_status"),
    path("orders/pending/", pending_orders, name="pending_orders"),
    path("orders/delivered/", delivered_orders, name="delivered_orders"),
    path("cart/", cart_view, name="cart"),
    path("checkout/", checkout, name="checkout"),
path("customers/add/", views.add_customer, name="add_customer"),
path("update_payment_status/", update_payment_status, name="update_payment_status"),
path('warehouses/', warehouse_list, name='warehouse_list'),
    path('warehouses/add/', add_warehouse, name='add_warehouse'),  # ✅ Ensure this matches the reverse lookup
   path('warehouses/edit/<int:warehouse_id>/', edit_warehouse, name='edit_warehouse'),

path('warehouses/<int:warehouse_id>/stock/', views.warehouse_stock, name='warehouse_stock'),
  path('warehouses/delete/<int:warehouse_id>/', delete_warehouse, name='delete_warehouse'),

   
    path("users/edit/<int:customer_id>/", views.edit_user, name="edit_user"),
  path("users/delete/<int:customer_id>/", views.delete_user, name="delete_user"),

path("create_order/", create_order, name="create_order"),
    path("generate_invoice/<int:order_id>/", generate_invoice, name="generate_invoice"),
    path("order_success/", order_success, name="order_success"),


      path('warehouse/<int:warehouse_id>/', warehouse_details, name='warehouse_details'),
       path('warehouse/<int:warehouse_id>/login/', warehouse_login, name='warehouse_login'),
       path('warehouse/<int:warehouse_id>/products/', warehouse_products, name='warehouse_products'),
  path('warehouse/<int:warehouse_id>/products/add/', warehouse_add_product, name='add_product'),

 path("warehouse/product/<int:product_id>/", warehouse_product_detail, name="warehouse_product_detail"), 
path("warehouse/product/<int:product_id>/edit/", views.warehouse_edit_product, name="warehouse_edit_product"),
path("warehouse/product/<int:product_id>/generate_qr/",warehouse_generate_qr_code, name="warehouse_generate_qr_code"),
   path("warehouse_logout/", warehouse_logout, name="warehouse_logout"),

path('clear-warehouse-session/', clear_warehouse_session, name='clear_warehouse_session'),
    path("warehouse/product/<int:product_id>/delete/", warehouse_delete_product, name="warehouse_delete_product"),

    path("stock-levels/", stock_levels, name="stock_levels"),
 
    path("customer/", customer, name="customer"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



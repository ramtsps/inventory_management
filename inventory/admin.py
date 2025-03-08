from django.contrib import admin
from .models import Supplier, Product, Customer, Order, Warehouse, StockMovement, CustomUser

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Warehouse)
admin.site.register(StockMovement)
admin.site.register(CustomUser)

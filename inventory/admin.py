from django.contrib import admin
from .models import Supplier, Product, Customer, Order, Warehouse, StockMovement,Category,WarehouseProduct
from.models import WarehouseStaff as Users

admin.site.site_header = " Inventory Management Administration"
admin.site.site_title = "Inventory Management System"
admin.site.index_title = "Admin Dashboard"

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Warehouse)
admin.site.register(StockMovement)

admin.site.register(WarehouseProduct)
admin.site.register(Users)
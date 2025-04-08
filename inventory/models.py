
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils.timezone import now
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # Added address field

    def __str__(self):
        return self.name
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class Product(models.Model):
    name = models.CharField(max_length=255)
    stock_keeping_unit = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    quantity_in_stock = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField(default=10)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    warehouse_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    product_image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    barcode = models.ImageField(upload_to="qrcodes/", blank=True, null=True)


    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('refund', 'Refund Processed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    shipping_details = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Ensure total price is calculated before saving. """
        if self.price and self.quantity:
            self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.product.name}"


class StockMovement(models.Model):
    MOVEMENT_TYPE = [
        ('inward', 'Inward'),
        ('outward', 'Outward'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.movement_type} ({self.quantity})"






import uuid
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password

class Users(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('warehouse staff', 'Warehouse Staff'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
    ]

    customer_id = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed password
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    working_warehouse = models.CharField(max_length=255, blank=True, null=True)
    register_date = models.DateTimeField(default=now)

    class Meta:
        db_table = "Users"  # Keep table name as "Users"

    def save(self, *args, **kwargs):
        """Hash password before saving and auto-increment customer_id."""
        if not self.customer_id:
            last_user = Users.objects.order_by('-customer_id').first()
            self.customer_id = int(last_user.customer_id) + 1 if last_user else 1001

        if not self.password.startswith("pbkdf2_sha256$"):  # Avoid re-hashing
            self.password = self.password

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Warehouse(models.Model):

    CATEGORY_CHOICES = [
    ('electronics', 'Electronics'),
    ('furniture', 'Furniture'),
    ('groceries', 'Groceries'),
    ('clothing', 'Clothing'),
    ('medicine', 'Medicine'),
    ('automotive', 'Automotive'),
    ('agricultural', 'Agricultural'),
    ('stationery', 'Stationery'),
    ('technology', 'Technology'),
    ('sports_equipment', 'Sports Equipment'),
    ('general', 'General'),
    ('all', 'All'),
]

    
    
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='all')
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class WarehouseProduct(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=False)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    supplier = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    warehouse = models.ForeignKey("Warehouse", on_delete=models.CASCADE, related_name="products")
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)

    class Meta:
        db_table = "warehouse_product"

    def __str__(self):
        return f"{self.name} - {self.warehouse.name}"

    def generate_qr_code(self):
        """Generate and save a QR code for the product."""
        qr_data = f"Product: {self.name}\nSKU: {self.sku}\nCategory: {self.category}\nSupplier: {self.supplier}\nStock: {self.stock}\nPrice: {self.price}\nLocation: {self.location}\nDescription: {self.description}\nWarehouse: {self.warehouse.name}"
        qr = qrcode.make(qr_data)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        # Save QR code to the ImageField
        filename = f"qr_{self.sku}.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        """Override save method to generate QR code before saving."""
        self.generate_qr_code()
        super().save(*args, **kwargs)

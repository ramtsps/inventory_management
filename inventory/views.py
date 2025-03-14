from django.shortcuts import render
from .models import Product, Order
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import Product, Category,Supplier
from django.contrib import messages 
from .forms import ProductForm,CategoryForm,SupplierForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Count


def dashboard(request):
    # Example values for display
    stock_count = 100  # Replace with actual database query
    order_count = 250  # Replace with actual database query
    low_stock_count = 10  # Replace with actual database query
    user_count = 35  # Replace with actual database query

    # Stock levels data
    stock_categories = ["Electronics", "Clothing", "Furniture"]
    stock_counts = [50, 30, 20]  # Example data

    # Order trends data
    order_dates = ["2024-03-01", "2024-03-02", "2024-03-03"]
    order_counts = [5, 10, 7]  # Example order count per day

    # Order status data for Pie Chart
    order_status_labels = ["Pending", "Shipped", "Delivered"]
    order_status_counts = [10, 20, 30]  # Example data

    context = {
        "stock_count": stock_count,
        "order_count": order_count,
        "low_stock_count": low_stock_count,
        "user_count": user_count,
        "stock_labels": stock_categories,
        "stock_data": stock_counts,
        "order_dates": order_dates,
        "order_counts": order_counts,
        "order_status_labels": order_status_labels,
        "order_status_data": order_status_counts,
    }
    return render(request, "inventory/sideBar/dashboard.html", context)

import qrcode
import json
import os
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def generate_qr_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Ensure SKU is provided
            sku = data.get("sku", "").strip()
            if not sku:
                return JsonResponse({"success": False, "error": "SKU is required"}, status=400)

            # Convert all form data into JSON format
            product_data = {
                "name": data.get("name", ""),
                "sku": sku,
                "category": data.get("category", ""),
                "supplier": data.get("supplier", ""),
                "quantity": data.get("quantity", ""),
                "price": data.get("price", ""),
                "location": data.get("location", ""),
                "description": data.get("description", ""),
            }

            # Convert to JSON string for QR encoding
            product_details_json = json.dumps(product_data)

            # Ensure QR code directory exists
            qr_dir = os.path.join(settings.MEDIA_ROOT, "qrcodes")  # ✅ FIXED
            os.makedirs(qr_dir, exist_ok=True)

            # Generate QR Code
            qr = qrcode.make(product_details_json)
            qr_image_path = os.path.join(qr_dir, f"{sku}.png".replace(".png.png", ".png"))  # ✅ FIXED
            qr.save(qr_image_path)

            # URL to serve QR code image
            qr_image_url = f"{settings.MEDIA_URL}qrcodes/{sku}.png"  # ✅ FIXED

            return JsonResponse({"success": True, "qr_code_url": qr_image_url})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

import base64
from django.core.files.base import ContentFile
from .utils import generate_barcode
def add_product(request):
    barcode_url = None

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)

            # Process the captured image (Base64 format)
            captured_image_data = request.POST.get("captured_image")
            if captured_image_data:
                format, imgstr = captured_image_data.split(";base64,")
                ext = format.split("/")[-1]
                product_image_file = ContentFile(base64.b64decode(imgstr), name=f"product_{product.stock_keeping_unit}.{ext}")
                product.product_image = product_image_file

            # Generate barcode and store in the product instance
            barcode_path = generate_barcode(product.stock_keeping_unit)
            product.barcode = barcode_path  
            product.save()

            return redirect("inventory:product_list")  
    else:
        form = ProductForm()

    return render(request, "inventory/product/add_product.html", {"form": form, "barcode_url": barcode_url})
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print("Product", product.description)
    return render(request, "inventory/product/product_detail.html", {"product": product})

from django.db.models import Sum, Count

def product_list(request):
    products = Product.objects.all()
    category_number = Category.objects.count()
    Supplier_number = Supplier.objects.count()
    # ✅ Count unique categories & suppliers
    category_count = Product.objects.values("category").distinct().count()
    supplier_count = Product.objects.values("supplier").distinct().count()

    # ✅ Count low-stock products (stock < 10)
    low_stock_count = Product.objects.filter(quantity_in_stock__lt=10).count()

    # ✅ Get total stock quantity across all products
    total_stock = Product.objects.aggregate(total_stock=Sum("quantity_in_stock"))["total_stock"] or 0

    return render(
        request,
        "inventory/product/product_list.html",
        {
            "products": products,
            "category_count": category_count,
            "supplier_count": supplier_count,
            "low_stock_count": low_stock_count,
            "total_stock": total_stock,
              "category_number":category_number , # ✅ Pass total stock count
              "Supplier_number": Supplier_number
        },
    )

# def edit_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.method == "POST":
#         form = ProductForm(request.POST, instance=product)
#         if form.is_valid():
            
#             new_stock = form.cleaned_data["quantity_in_stock"]

#             # Prevent negative values
#             if new_stock < 0:
#                 new_stock = 0  
#             form.save()

#             return redirect("inventory:product_list")  # ✅ Fix applied
#     else:
#         form = ProductForm(instance=product)

#     return render(request, "inventory/product/edit_product.html", {"form": form})
import qrcode
import base64  # ✅ Add this import
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False) 

            # ✅ Process the captured image (Base64 format)
            captured_image_data = request.POST.get("captured_image")
            if captured_image_data:
                try:
                    format, imgstr = captured_image_data.split(";base64,")
                    ext = format.split("/")[-1]
                    image_data = base64.b64decode(imgstr)  # ✅ Decode Base64 string
                    product_image_file = ContentFile(image_data, name=f"product_{form.cleaned_data['stock_keeping_unit']}.{ext}")
                    product.product_image = product_image_file  
                except Exception as e:
                    messages.error(request, f"Error processing image: {e}")

            # ✅ Generate & assign barcode
            product.barcode = generate_barcode(form.cleaned_data["stock_keeping_unit"])  
            product.save()  # ✅ Save the product with updated image & barcode

            messages.success(request, "Product updated successfully!")
            return redirect("inventory:product_list")
        else:
            messages.error(request, "Error updating product. Please check the form.")
    else:
        form = ProductForm(instance=product)

    return render(request, "inventory/product/edit_product.html", {"form": form, "product": product})
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect("inventory:product_list")
    return render(request, "inventory/product/delete_product.html", {"product": product})

def category_list(request):
    categories = Category.objects.annotate(product_count=Count("product"))
    return render(request, "inventory/category/category_list.html", {"categories": categories})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(
        request,
        "inventory/category/category_products.html",
        {"category": category, "products": products},
    )


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Category added successfully!")
            return redirect("inventory:category_list")
        else:
            messages.error(request, "❌ Failed to add category. Please try again.")
    else:
        form = CategoryForm()
    
    return render(request, "inventory/category/add_category.html", {"form": form})
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("inventory:category_list")
    else:
        form = CategoryForm(instance=category)
    
    return render(request, "inventory/category/edit_category.html", {"form": form, "category": category})
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.delete()
        return redirect("inventory:category_list")

    return render(request, "inventory/category/delete_category.html", {"category": category})

def supplier_list(request):
    suppliers = Supplier.objects.annotate(product_count=Count('product'))
    return render(request, "inventory/supplier/supplier_list.html", {"suppliers": suppliers})
def supplier_products(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    products = Product.objects.filter(supplier=supplier)
    return render(request, "inventory/supplier/supplier_products.html", {"supplier": supplier, "products": products})
# Add Supplier
def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:supplier_list")
    else:
        form = SupplierForm()
    return render(request, "inventory/supplier/supplier_form.html", {"form": form, "title": "Add Supplier"})

# Edit Supplier
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect("inventory:supplier_list")
    else:
        form = SupplierForm(instance=supplier)
    return render(request, "inventory/supplier/supplier_form.html", {"form": form, "title": "Edit Supplier"})

# Delete Supplier
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == "POST":
        supplier.delete()
        return redirect("inventory:supplier_list")
    return render(request, "inventory/supplier/supplier_confirm_delete.html", {"supplier": supplier})



def low_stock_products(request):
    low_stock_products = Product.objects.filter(quantity_in_stock__lt=10)
    
    return render(request, "inventory/stock/low_stock_products.html", {"products": low_stock_products})

# def order_list(request):
#     return render(request, 'inventory/sideBar/order_list.html')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, Product, Category, Supplier,Customer
from .forms import OrderForm
from django.db.models import Sum, Count
from .forms import CustomerForm
from django.db.models import Q

def order_list(request):
    orders = Order.objects.all().order_by("-id")  

# Case-insensitive filtering using __iexact
    pending_orders = Order.objects.filter(status__iexact="pending").count()
    delivered_orders = Order.objects.filter(status__iexact="delivered").count()
    canceled_orders = Order.objects.filter(status__iexact="canceled").count()
    shipped_orders = Order.objects.filter(status__iexact="shipped").count()
    unpaid_orders = Order.objects.filter(payment_status__iexact="unpaid").count()
    paid_orders = Order.objects.filter(payment_status__iexact="paid").count()
    refunded_orders = Order.objects.filter(payment_status__iexact="refund").count()

    return render(request, "inventory/order/order_list.html", {
        "orders": orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "canceled_orders": canceled_orders,
        "shipped_orders": shipped_orders,
        "unpaid_orders": unpaid_orders,
        "paid_orders": paid_orders,
        "refunded_orders": refunded_orders,
    })
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order

@csrf_exempt  # Allow AJAX request without CSRF token (optional if using headers)
def update_payment_status(request, order_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("payment_status")

            # Update order payment status
            order = Order.objects.get(id=order_id)
            order.payment_status = new_status
            order.save()

            return JsonResponse({"success": True, "new_status": new_status})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})

def create_order(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer")
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity")
        status = request.POST.get("status")
        payment_status = request.POST.get("payment_status")
        expected_delivery_date = request.POST.get("expected_delivery_date")
        shipping_details = request.POST.get("shipping_details")
        customer_address = request.POST.get("customer_address")

        customer = Customer.objects.get(id=customer_id)
        product = Product.objects.get(id=product_id)

        Order.objects.create(
            customer=customer,
            product=product,
            quantity=quantity,
            status=status,
            payment_status=payment_status,
            expected_delivery_date=expected_delivery_date if expected_delivery_date else None,
            shipping_details=f"{customer.name}, {customer.phone}, {customer_address if customer_address else customer.address}",
        )

        messages.success(request, "Order created successfully!")
        return redirect("inventory:order_list")

    customers = Customer.objects.all()
    products = Product.objects.all()

    return render(request, "inventory/order/create_order.html", {
        "customers": customers,
        "products": products
    })

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "inventory/order/order_detail.html", {"order": order})

def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()
    messages.success(request, f"Order #{order.id} status updated to {status}!")
    return redirect("inventory:order_list")

def pending_orders(request):
    orders = Order.objects.filter(status="Pending")
    return render(request, "inventory/order/pending_orders.html", {"orders": orders})

def delivered_orders(request):
    orders = Order.objects.filter(status="Delivered")
    return render(request, "inventory/order/delivered_orders.html", {"orders": orders})

def cart_view(request):
    cart_items = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart_items.keys())

    total_price = sum(product.price * cart_items[str(product.id)] for product in products)

    return render(request, "inventory/order/cart.html", {
        "cart_items": cart_items,
        "products": products,
        "total_price": total_price
    })

def checkout(request):
    if request.method == "POST":
        request.session["cart"] = {}  # Clear cart after checkout
        messages.success(request, "Payment completed successfully!")
        return redirect("inventory:order_list")

    return render(request, "inventory/order/checkout.html")


def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer added successfully!")
            return redirect("inventory:order_list")
    else:
        form = CustomerForm()
    
    return render(request, "inventory/customer/add_customer.html", {"form": form})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Warehouse
from .models import Warehouse, Product

def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    warehouse_data = []
    
    for warehouse in warehouses:
        products = Product.objects.filter().values("name", "stock_keeping_unit")
        # print("stoked", products)
        warehouse_data.append({"warehouse": warehouse, "products": list(products)})

    return render(request, 'inventory/warehouse/warehouse_list.html', {'warehouses': warehouses})


from django.http import JsonResponse
from .models import Product, Warehouse
from django.core.exceptions import ObjectDoesNotExist
def warehouse_stock(request, warehouse_id):
    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)
        products = Product.objects.filter().values("name", "stock_keeping_unit")

        # Count distinct categories in the warehouse
        category_count = Category.objects.filter().distinct().count()
        print("caty",category_count)
        return JsonResponse({
            "products": list(products),
            "total_categories": category_count
        })
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Warehouse not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def add_warehouse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Warehouse.objects.create(name=data["name"], location=data["location"])
        return JsonResponse({"success": True})
@csrf_exempt
def edit_warehouse(request, warehouse_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            warehouse = Warehouse.objects.get(id=warehouse_id)
            warehouse.name = data['name']
            warehouse.location = data['location']
            warehouse.save()
            return JsonResponse({"success": True})
        except Warehouse.DoesNotExist:
            return JsonResponse({"success": False, "error": "Warehouse not found"}, status=404)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

@csrf_exempt
def delete_warehouse(request, warehouse_id):
    if request.method == "POST":
        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
            warehouse.delete()
            return JsonResponse({"success": True})
        except Warehouse.DoesNotExist:
            return JsonResponse({"success": False, "error": "Warehouse not found"}, status=404)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from .models import Users  # Import Users model
def user_list(request):
    users = Users.objects.all()  # Fetch all users

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile_number = request.POST.get("mobile_number")
        password = request.POST.get("password")
        role = request.POST.get("role", "warehouse_staff")

        user = Users(
            name=name,
            email=email,
            mobile_number=mobile_number,
            password=make_password(password),
            role=role
        )
        user.save()  # Ensure the user is saved properly

        return redirect("inventory:user_list") 
    return render(request, "inventory/sideBar/user_list.html", {"users": users})

def edit_user(request, user_id):
    user = get_object_or_404(Users, id=user_id)

    if request.method == "POST":
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.mobile_number = request.POST.get("mobile_number")
        user.role = request.POST.get("role")

        new_password = request.POST.get("password")
        if new_password:
            user.password = make_password(new_password)  # Update password if provided

        user.save()
        return redirect("user_list")

    return render(request, "inventory/sideBar/user_list.html", {"users": Users.objects.all()})

def delete_user(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    user.delete()
    return redirect("user_list")

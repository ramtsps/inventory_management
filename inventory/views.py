from django.shortcuts import render
from .models import Product, Order
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import Product, Category,Supplier
from django.contrib import messages 
from .forms import ProductForm,CategoryForm,SupplierForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.hashers import check_password
from .models import Users,WarehouseProduct

def home(request):
    return render(request, "inventory/home.html")
def custom_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        try:
            user = Users.objects.get(email=email)  # Get user by email first
            if user.role != role:  # Check if role matches
                messages.error(request, "Incorrect role selection.")
                return redirect("inventory:home")

            if password== user.password:  # Check hashed password
                # Set session data
                request.session["user_id"] = user.customer_id
                request.session["user_name"] = user.name
                request.session["user_email"] = user.email
                request.session["user_role"] = user.role

                messages.success(request, "Login successful!")
                return redirect("inventory:dashboard")  # Redirect to dashboard
            else:
                messages.error(request, "Invalid password.")
                return redirect("inventory:home")

        except Users.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("inventory:home")

    return render(request, "inventory/home.html")  # Render login page if not a POST request
def profile(request):
    # Assuming user is authenticated, get the logged-in user
    user = Users.objects.get(customer_id=request.session['user_id'])
    
    return render(request, 'inventory/profile/profile.html', {'user': user})
# Settings Page

def profile_settings(request):
    # Assuming user is authenticated, get the logged-in user
    user = Users.objects.get(customer_id=request.session['user_id'])
    
    if request.method == 'POST':
        # Get the updated data from the POST request
        user.name = request.POST.get('name')
        user.mobile_number = request.POST.get('mobile_number')
        user.email = request.POST.get('email')
      
        
        # Only hash the password if it has been changed
        new_password = request.POST.get('password')
        if new_password and new_password != user.password:
            user.password = new_password  # You should hash the password here

        user.save()
        # Add a success message
        messages.success(request, "Settings updated successfully!")
        return redirect("inventory:profile")
    return render(request, 'inventory/profile/settings.html', {'user': user})
def logout_view(request):
    request.session.flush()  # Clear session data
    messages.success(request, "Logged out successfully!")
    return redirect("inventory:home") 

def dashboard(request):
    if "user_id" not in request.session:
        return redirect("inventory:login")

    stock_count = Product.objects.aggregate(Sum('quantity_in_stock'))['quantity_in_stock__sum'] or 0
    order_count = Order.objects.count()

    low_stock_count = Product.objects.filter(quantity_in_stock__lt=10).count()
    user_count = Customer.objects.count()  # Change this to a dynamic user count if needed

    # Stock levels for the Bar Chart
 # Stock levels for the Bar Chart
    stock_categories = Product.objects.values('category__name').annotate(stock=Sum('quantity_in_stock'))
    stock_labels = [category['category__name'] for category in stock_categories]  # Category names
    stock_counts = [category['stock'] for category in stock_categories]  # Stock count

    # Order trends for the Line Chart
    order_dates = Order.objects.values('order_date').annotate(order_count=Sum('quantity')).order_by('order_date')
    order_dates_formatted = [date['order_date'].strftime('%Y-%m-%d') for date in order_dates]
    order_counts = [date['order_count'] for date in order_dates]


    # Order status for the Pie Chart
    order_status_labels = ["Pending", "Shipped", "Delivered","Canceled"]
    order_status_counts = [
        Order.objects.filter(status='pending').count(),
        Order.objects.filter(status='shipped').count(),
        Order.objects.filter(status='delivered').count(),
        Order.objects.filter(status='canceled').count(),
    ]


    # Order trends based on product name
    product_orders = Order.objects.values('product__name').annotate(order_count=Sum('quantity')).order_by('product__name')
    product_names = [product['product__name'] for product in product_orders]
    product_order_counts = [product['order_count'] for product in product_orders]
    product_orders = (
    Order.objects.select_related('product')
    .values('product__name')
    .annotate(order_count=Sum('quantity'))
    .order_by('product__name')
)



    # Convert to JSON for safe template rendering
    context = {
        "stock_count": stock_count,
        "order_count": order_count,
        "low_stock_count": low_stock_count,
        "user_count": user_count,
        "stock_labels": json.dumps(stock_labels),
        "stock_data": json.dumps(stock_counts),
        "order_dates": json.dumps(order_dates_formatted),
        "order_counts": json.dumps(order_counts),
        "order_status_labels": json.dumps(order_status_labels),
        "order_status_data": json.dumps(order_status_counts),
        "user_name": request.session.get("user_name"),
        "user_email": request.session.get("user_email"),
        "user_role": request.session.get("user_role"),
          "product_names": json.dumps(product_names),
        "product_order_counts": json.dumps(product_order_counts),
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
def update_payment_status(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        payment_status = request.POST.get("payment_status")

        order = Order.objects.get(id=order_id)
        order.payment_status = payment_status
        order.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

def order_success(request):
    invoice_url = request.GET.get("invoice_url", "")
    return render(request, "inventory/order_success.html", {"invoice_url": invoice_url})
def create_order(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer")
        product_id = request.POST.get("product")
        quantity = int(request.POST.get("quantity"))
        status = request.POST.get("status")
        payment_status = request.POST.get("payment_status")
        expected_delivery_date = request.POST.get("expected_delivery_date")
        shipping_details = request.POST.get("shipping_details")
        customer_address = request.POST.get("customer_address")

        customer = get_object_or_404(Customer, id=customer_id)
        product = get_object_or_404(Product, id=product_id)

        # Get the product price at the time of ordering
        price = product.selling_price
        total_price = price * quantity

        order = Order.objects.create(
            customer=customer,
            product=product,
            quantity=quantity,
            price=price,
            total_price=total_price,
            status=status,
            payment_status=payment_status,
            expected_delivery_date=expected_delivery_date if expected_delivery_date else None,
            shipping_details=f"{customer.name}, {customer.phone}, {customer_address if customer_address else customer.address}",
        )

        messages.success(request, "Order created successfully!")

        return redirect("inventory:generate_invoice", order.id)

    customers = Customer.objects.all()
    products = Product.objects.all()

    return render(request, "inventory/order/create_order.html", {
        "customers": customers,
        "products": products
    })


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    print("`order_detail`", order.order_date)
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
            messages.error(request, "There was an error in the form. Please check the fields.")
            print(form.errors)  # Debugging
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
    
def warehouse_details(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    return render(request, 'inventory/warehouse/warehouse_details.html', {'warehouse': warehouse})
def warehouse_products(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    products = WarehouseProduct.objects.filter(warehouse=warehouse)

    return render(request, "inventory/warehouse/warehouse_products.html", {"warehouse": warehouse, "products": products})
def warehouse_add_product(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)

    if request.method == "POST":
        name = request.POST.get("name")
        sku = request.POST.get("sku")
        category_id = request.POST.get("category")
        supplier = request.POST.get("supplier")
        stock = request.POST.get("quantity")
        price = request.POST.get("price")
        location = request.POST.get("location", "")
        description = request.POST.get("description", "")

        try:
            stock = int(stock)
            price = float(price)
        except ValueError:
            stock = 0
            price = 0.00

        category = get_object_or_404(Category, id=category_id)
        product = WarehouseProduct(
            name=name, sku=sku, category=category, supplier=supplier,
            stock=stock, price=price, location=location, description=description,
            warehouse=warehouse
        )

        if "product_image" in request.FILES:
            product.image = request.FILES["product_image"]  # Save captured image

        product.save()
        product.generate_qr_code()
        product.save()

        return redirect("inventory:warehouse_products", warehouse_id=warehouse.id)

    categories = Category.objects.all()
    return render(
        request,
        "inventory/warehouse/warehouse_add_product.html",
        {"warehouse": warehouse, "categories": categories}
    )
from .forms import WarehouseProductForm
def warehouse_edit_product(request, product_id):
    product = get_object_or_404(WarehouseProduct, id=product_id)

    if request.method == "POST":
        form = WarehouseProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.generate_qr_code()  # Ensure QR code is generated
            product.save()
            return redirect("inventory:warehouse_products", product.warehouse.id)
    else:
        form = WarehouseProductForm(instance=product)

    return render(request, "inventory/warehouse/edit_product.html", {"form": form, "product": product})
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import JsonResponse
from .models import WarehouseProduct

def warehouse_generate_qr_code(request, product_id):
    product = WarehouseProduct.objects.get(id=product_id)

    qr_data = f"Product: {product.name}\nSKU: {product.sku}\nWarehouse: {product.warehouse.name}"
    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    product.qr_code.save(f"qr_{product.sku}.png", ContentFile(buffer.getvalue()), save=True)

    return JsonResponse({"qr_code_url": product.qr_code.url})

# Delete Product View
def warehouse_delete_product(request, product_id):
    product = get_object_or_404(WarehouseProduct, id=product_id)  # Ensure correct model
    warehouse_id = product.warehouse.id
    if request.method == "POST":
        product.delete()
        return redirect("inventory:warehouse_products", warehouse_id)
    return render(request, "inventory/warehouse/delete_product.html", {"product": product})

def warehouse_product_detail(request, product_id):
    product = get_object_or_404(WarehouseProduct, id=product_id)
    return render(request, "inventory/warehouse/product_detail.html", {"product": product})
def warehouse_login(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = Users.objects.get(email=email)
            
            if password==user.password :
                request.session["warehouse_id"] = warehouse.id  # Store warehouse session
                request.session["user_id"] = user.customer_id  # Store user session
                request.session["user_role"] = user.role
                return redirect("inventory:warehouse_products", warehouse_id=warehouse.id)  # Redirect to product page
            
            else:
                error_message = "Invalid email, password, or access to this warehouse."

        except Users.DoesNotExist:
            error_message = "User not found. Please check your credentials."

    else:
        error_message = None

    return render(request, "inventory/warehouse/warehouse_login.html", {"warehouse": warehouse, "error_message": error_message})

from django.contrib.auth import logout

def warehouse_logout(request):
    # logout(request)  # Logs out user
    # request.session.pop("warehouse_id", None)  # Remove warehouse_id from session
    return redirect("inventory:warehouse_list") # Redirect to warehouse selection
def clear_warehouse_session(request):
    # request.session.pop('warehouse_id', None)
    return JsonResponse({"message": "Warehouse session cleared"})
@csrf_exempt
def add_warehouse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Warehouse.objects.create(name=data["name"], location=data["location"],category=data["category"])
        return JsonResponse({"success": True})
@csrf_exempt
def edit_warehouse(request, warehouse_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            warehouse = Warehouse.objects.get(id=warehouse_id)
            warehouse.name = data['name']
            warehouse.location = data['location']
            warehouse.category=data['category']
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
            password=password,
            role=role
        )
        user.save()  # Ensure the user is saved properly

        return redirect("inventory:user_list") 
    return render(request, "inventory/sideBar/user_list.html", {"users": users})

from django.db import IntegrityError
def edit_user(request, customer_id):
    user = get_object_or_404(Users, customer_id=customer_id)

    if request.method == "POST":
        try:
            user.name = request.POST.get("name")
            user.email = request.POST.get("email")
            user.mobile_number = request.POST.get("mobile_number")
            user.role = request.POST.get("role")

            new_password = request.POST.get("password")
            if new_password:
                user.password = new_password  # Update password if provided

            user.save()
            messages.success(request, "User updated successfully!")
        except IntegrityError:
            messages.error(request, "Email already exists! Please use a different email.")

        return redirect("inventory:user_list")  # Redirect to user list after updating

    return render(request, "inventory/sideBar/user_list.html", {"users": Users.objects.all()})
def delete_user(request, customer_id):
    user = get_object_or_404(Users, customer_id=customer_id)  # Get user by customer_id
    user.delete()
    messages.success(request, "User deleted successfully!")  # Show success message
    return redirect("inventory:user_list") 


from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from django.conf import settings
from django.utils.timezone import now
from .models import Order
from django.urls import reverse
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Define file path
    invoice_filename = f"invoice_{order.id}_{now().strftime('%Y%m%d%H%M%S')}.pdf"
    invoice_path = os.path.join(settings.MEDIA_ROOT, "invoices", invoice_filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(invoice_path), exist_ok=True)

    # Create PDF
    p = canvas.Canvas(invoice_path, pagesize=A4)
    width, height = A4

    # Invoice Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Invoice")

    # Order Details
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Order ID: {order.id}")
    p.drawString(50, height - 120, f"Customer: {order.customer.name}")
    p.drawString(50, height - 140, f"Phone: {order.customer.phone}")
    p.drawString(50, height - 160, f"Address: {order.customer.address}")

    # Product Details
    p.drawString(50, height - 200, f"Product: {order.product.name}")
    p.drawString(50, height - 220, f"Quantity: {order.quantity}")
    p.drawString(50, height - 240, f"Price per unit: Rs: {order.product.selling_price}")
    p.drawString(50, height - 260, f"Total Price: Rs: {order.quantity * order.product.selling_price}")

    # Payment Status
    p.drawString(50, height - 300, f"Payment Status: {order.payment_status}")
    p.drawString(50, height - 320, f"Order Status: {order.status}")

    # Expected Delivery Date
    if order.expected_delivery_date:
        p.drawString(50, height - 360, f"Expected Delivery: {order.expected_delivery_date}")

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, height - 400, "Thank you for your order!")

    # Save the PDF
    p.showPage()
    p.save()

    # Get the relative URL of the invoice
    invoice_url = f"/media/invoices/{invoice_filename}"

    
    
    return redirect(reverse("inventory:order_success") + f"?invoice_url={invoice_url}")




def stock_levels(request):
    products = Product.objects.all()
    return render(request, "inventory/stock_levels.html", {"products": products})


def customer(request):
    users = Customer.objects.all()
    return render(request, "inventory/users.html", {"users": users})
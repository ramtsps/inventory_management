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
    return render(request, "inventory/dashboard.html", context)



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "inventory/product_detail.html", {"product": product})

def product_list(request):
    products = Product.objects.all()
    category_count = Product.objects.values("category").distinct().count()
    supplier_count = Product.objects.values("supplier").distinct().count()
    low_stock_count = Product.objects.filter(quantity_in_stock__lt=10).count()  # Count low-stock products

    return render(
        request,
        "inventory/product_list.html",
        {
            "products": products,
            "category_count": category_count,
            "supplier_count": supplier_count,
            "low_stock_count": low_stock_count,  # Pass low stock count
        },
    )
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Product added successfully!")
            return redirect("inventory:product_list")  # Use the namespace 'inventory'

        else:
            messages.error(request, "❌ Failed to add product. Please check the form.")
            print(form.errors)  # Debugging: Print form errors in terminal

    else:
        form = ProductForm()

    return render(request, "inventory/add_product.html", {"form": form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("inventory:product_list")  # ✅ Fix applied
    else:
        form = ProductForm(instance=product)

    return render(request, "inventory/edit_product.html", {"form": form})
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect("inventory:product_list")
    return render(request, "inventory/delete_product.html", {"product": product})

def category_list(request):
    categories = Category.objects.annotate(product_count=Count("product"))
    return render(request, "inventory/category_list.html", {"categories": categories})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(
        request,
        "inventory/category_products.html",
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
    
    return render(request, "inventory/add_category.html", {"form": form})
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("inventory:category_list")
    else:
        form = CategoryForm(instance=category)
    
    return render(request, "inventory/edit_category.html", {"form": form, "category": category})
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.delete()
        return redirect("inventory:category_list")

    return render(request, "inventory/delete_category.html", {"category": category})

def supplier_list(request):
    suppliers = Supplier.objects.annotate(product_count=Count('product'))
    return render(request, "inventory/supplier_list.html", {"suppliers": suppliers})
def supplier_products(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    products = Product.objects.filter(supplier=supplier)
    return render(request, "inventory/supplier_products.html", {"supplier": supplier, "products": products})
# Add Supplier
def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:supplier_list")
    else:
        form = SupplierForm()
    return render(request, "inventory/supplier_form.html", {"form": form, "title": "Add Supplier"})

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
    return render(request, "inventory/supplier_form.html", {"form": form, "title": "Edit Supplier"})

# Delete Supplier
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == "POST":
        supplier.delete()
        return redirect("inventory:supplier_list")
    return render(request, "inventory/supplier_confirm_delete.html", {"supplier": supplier})



def low_stock_products(request):
    low_stock_products = Product.objects.filter(quantity_in_stock__lt=10)
    
    return render(request, "inventory/low_stock_products.html", {"products": low_stock_products})

def order_list(request):
    return render(request, 'inventory/order_list.html')

def warehouse_list(request):
    return render(request, 'inventory/warehouse_list.html')

def user_list(request):
    return render(request, 'inventory/user_list.html')

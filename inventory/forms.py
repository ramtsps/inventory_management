from django import forms
from .models import Product,Category,Supplier,Order,Customer

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        empty_label="Select Supplier",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    barcode = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "barcodeInput", "readonly": "readonly"}),
    )

    class Meta:
        model = Product
        fields = [
            "name", "stock_keeping_unit", "category", "supplier",
            "quantity_in_stock", "reorder_level", "purchase_price",
            "selling_price", "description", "warehouse_location",
            "product_image", "barcode",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "stock_keeping_unit": forms.TextInput(attrs={"class": "form-control"}),
            "quantity_in_stock": forms.NumberInput(attrs={"class": "form-control"}),
            "reorder_level": forms.NumberInput(attrs={"class": "form-control"}),
            "purchase_price": forms.NumberInput(attrs={"class": "form-control"}),
            "selling_price": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "warehouse_location": forms.TextInput(attrs={"class": "form-control"}),
            "product_image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
             "barcode": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter category name"}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact", "email", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter supplier name"}),
            "contact": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter contact number"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter supplier address"}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "product", "quantity", "status", "payment_status","expected_delivery_date", "shipping_details"]
        widgets = {
            "expected_delivery_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "shipping_details": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone", "address"]
        widgets = {
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }



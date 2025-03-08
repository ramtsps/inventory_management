from django import forms
from .models import Product,Category,Supplier

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    supplier = forms.ModelChoiceField(  # Ensure supplier is a dropdown
        queryset=Supplier.objects.all(),
        empty_label="Select Supplier",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Product
        fields = [
            "name", "stock_keeping_unit", "category", "quantity_in_stock",
            "reorder_level", "supplier", "purchase_price",
            "selling_price", "expiry_date", "warehouse_location"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "stock_keeping_unit": forms.TextInput(attrs={"class": "form-control"}),
            "quantity_in_stock": forms.NumberInput(attrs={"class": "form-control"}),
            "reorder_level": forms.NumberInput(attrs={"class": "form-control"}),
            "purchase_price": forms.NumberInput(attrs={"class": "form-control"}),
            "selling_price": forms.NumberInput(attrs={"class": "form-control"}),
            "expiry_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "warehouse_location": forms.TextInput(attrs={"class": "form-control"}),
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
import os
import barcode
from barcode.writer import ImageWriter
from django.conf import settings

def generate_barcode(sku):
    if not sku or not isinstance(sku, str):
        raise ValueError("Invalid SKU provided for barcode generation")

    barcode_dir = os.path.join(settings.MEDIA_ROOT, "qrcodes")
    os.makedirs(barcode_dir, exist_ok=True)

    barcode_filename = f"{sku}.png"
    barcode_filepath = os.path.join(barcode_dir, barcode_filename)

    # Generate barcode
    barcode_class = barcode.get_barcode_class("code128")
    barcode_instance = barcode_class(sku, writer=ImageWriter())
    barcode_instance.save(barcode_filepath)

    # Return the relative path to be stored in the product instance
    return f"qrcodes/{barcode_filename}"

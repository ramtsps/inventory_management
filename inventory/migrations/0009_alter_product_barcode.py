# Generated by Django 4.2.20 on 2025-03-10 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_product_barcode_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.ImageField(blank=True, null=True, upload_to='barcodes/'),
        ),
    ]

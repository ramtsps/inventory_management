# Generated by Django 4.2.20 on 2025-03-28 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_warehouseproduct_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouseproduct',
            name='sku',
            field=models.CharField(max_length=50),
        ),
    ]

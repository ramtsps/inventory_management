# Generated by Django 4.2.20 on 2025-04-06 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_alter_warehouseproduct_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='category',
            field=models.CharField(choices=[('electronics', 'Electronics'), ('furniture', 'Furniture'), ('groceries', 'Groceries'), ('clothing', 'Clothing'), ('medical', 'Medical'), ('automotive', 'Automotive'), ('agricultural', 'Agricultural'), ('stationery', 'Stationery'), ('technology', 'Technology'), ('sports_equipment', 'Sports Equipment'), ('general', 'General'), ('all', 'All')], default='all', max_length=50),
        ),
    ]

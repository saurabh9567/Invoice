# Generated by Django 5.0.6 on 2024-08-04 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_app', '0003_rename_price_product_selling_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='purchase_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
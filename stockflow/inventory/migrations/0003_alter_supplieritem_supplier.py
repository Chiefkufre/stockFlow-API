# Generated by Django 5.0.6 on 2024-06-26 04:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0002_item_quantity_supplieritem_quantity_and_more"),
        ("supplier", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supplieritem",
            name="supplier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="supplier.supplier"
            ),
        ),
    ]

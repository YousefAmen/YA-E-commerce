# Generated by Django 5.0.7 on 2024-09-09 18:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0017_alter_order_shipping_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='payment.shippingaddress'),
        ),
    ]

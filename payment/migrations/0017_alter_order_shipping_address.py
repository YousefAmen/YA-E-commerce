# Generated by Django 5.0.7 on 2024-09-07 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0016_shippingaddress_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='payment.shippingaddress'),
        ),
    ]

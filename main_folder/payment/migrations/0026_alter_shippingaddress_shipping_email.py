# Generated by Django 5.0.7 on 2024-09-13 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0025_alter_order_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_email',
            field=models.EmailField(blank=True, default=None, max_length=50, null=True),
        ),
    ]

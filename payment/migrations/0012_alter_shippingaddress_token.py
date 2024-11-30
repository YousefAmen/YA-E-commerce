# Generated by Django 5.0.7 on 2024-09-07 12:14

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_shippingaddress_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=True),
        ),
    ]
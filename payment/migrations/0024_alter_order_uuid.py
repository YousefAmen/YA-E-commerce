# Generated by Django 5.0.7 on 2024-09-10 18:44

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0023_order_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]

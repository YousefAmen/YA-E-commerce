# Generated by Django 5.0.7 on 2024-09-10 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0021_order_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='uuid',
        ),
    ]

# Generated by Django 5.0.7 on 2024-10-27 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0039_orderitem_selled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='selled',
        ),
    ]

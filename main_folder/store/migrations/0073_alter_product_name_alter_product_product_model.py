# Generated by Django 5.0.7 on 2024-11-01 18:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0072_delete_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default=None, max_length=1000, validators=[django.core.validators.MinLengthValidator(2, 'the field must contain at least 2 character')], verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_model',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True, validators=[django.core.validators.MinLengthValidator(3, 'the field must contain at least 3 character')], verbose_name='Product Brand'),
        ),
    ]

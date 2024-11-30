# Generated by Django 5.0.7 on 2024-08-08 04:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_product_description_alter_product_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default=None, max_length=800, null=True, validators=[django.core.validators.MinLengthValidator(200, 'the field must contain at least 200 characters')]),
        ),
    ]
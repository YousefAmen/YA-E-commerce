# Generated by Django 5.0.7 on 2024-08-08 06:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default=None, max_length=500, validators=[django.core.validators.MinLengthValidator(20, 'the field must contain at least 20 character')], verbose_name='Product Name'),
        ),
    ]
